"""
Energybae — process_bill.py
Reads an MSEDCL electricity bill image/PDF using Tesseract OCR
and fills the Solar Load Excel template.
"""

import re, argparse, shutil
from datetime import datetime
from pathlib import Path
from collections import Counter

import pytesseract
from PIL import Image, ImageEnhance
import openpyxl
from openpyxl.styles import Font

# ── Constants ──────────────────────────────────────────────────────────────────
PANEL_WATT    = 600   # Watt per solar panel
FIXED_CHARGE  = 130   # Default fixed charge if not found in bill

# Excel row for each billing month (matches the template)
MONTH_TO_ROW = {
    "2025-02": 9,  "2025-03": 10, "2025-04": 11, "2025-05": 12,
    "2025-06": 13, "2025-07": 14, "2025-08": 15, "2025-09": 16,
    "2025-10": 17, "2025-11": 18, "2025-12": 19,
    "2026-01": 20, "2026-02": 21,
}


# ── Step 1: Run OCR on the bill image ─────────────────────────────────────────
def run_ocr(path: str) -> str:
    img = Image.open(path)
    w, h = img.size

    # Only upscale if image is small (avoids slowness on large photos)
    if w < 1500:
        img = img.resize((w * 2, h * 2), Image.LANCZOS)

    img = img.convert("L")
    img = ImageEnhance.Contrast(img).enhance(2.0)
    img = ImageEnhance.Sharpness(img).enhance(2.0)

    text = pytesseract.image_to_string(img, lang="eng", config="--psm 6")
    return text


# ── Step 2: Parse key fields from OCR text ────────────────────────────────────
def parse_consumer_name(text):
    patterns = [
        r"(SHRI\s+[A-Z][A-Z\s]{8,45})",
        r"(SMT\.?\s+[A-Z][A-Z\s]{8,40})",
        r"(RANJANA\s+[A-Z][A-Z\s]{5,40})",
        r"([A-Z]{3,}\s+[A-Z]{3,}\s+KHOBRAGADE)",
    ]
    for pat in patterns:
        m = re.search(pat, text)
        if m:
            name = re.sub(r"\s+", " ", m.group(1)).strip()
            name = re.split(r"[a-z\|:;$]", name)[0].strip()
            if 8 < len(name) < 65:
                return name
    return "Unknown"


def parse_consumer_no(text):
    candidates = re.findall(r"\b(\d{9,12})\b", text)
    for c in candidates:
        if c.startswith("43") and len(c) == 12:
            return c
    m = re.search(r"MSEDCL\d{2}(\d{12})", text)
    if m:
        return m.group(1)
    for c in candidates:
        if len(c) == 12:
            return c
    return "Unknown"


def parse_sanctioned_load(text):
    m = re.search(r"(\d+\.\d+)\s*KW", text, re.I)
    if m:
        return m.group(1) + " KW"
    return "Unknown"


def parse_connection_type(text):
    m = re.search(r"(?:9[O0]|QO)/LT[I1]\s*Res\s*\d-Phase", text, re.I)
    if m:
        ct = m.group(0)
        ct = ct.replace("QO", "90").replace("9O", "90")
        ct = re.sub(r"LT[I1]", "LT I", ct)
        return re.sub(r"\s+", " ", ct).strip()
    return "90/LT I Res 1-Phase"


def parse_billing_month(text):
    m = re.search(r"MONTH\s+OF[^\n]{0,50}(\d{4})", text, re.I)
    if m:
        year = m.group(1)
        dates = re.findall(r"\b\d{2}[/-](\d{2})[/-]" + year + r"\b", text[:1000])
        if dates:
            return f"{year}-{dates[0]}"
        return f"{year}-01"
    m2 = re.search(r"\b\d{2}[/-](\d{2})[/-](20\d{2})\b", text)
    if m2:
        return f"{m2.group(2)}-{m2.group(1)}"
    return datetime.now().strftime("%Y-%m")


def parse_units(text):
    m = re.findall(r"(\d{4,6})\s+(\d{4,6})\s+1[.,]00\s+(\d{1,4})\b", text)
    if m:
        return int(m[0][2])
    m2 = re.findall(r"\d{4,6}\s+\d{4,6}\s+[\d.,]+\s+(\d{1,4})\s+\d+\s+\1\b", text)
    if m2:
        return int(m2[0])
    m3 = re.findall(r"\b(\d{1,4})\s+0\s+\1\b", text)
    if m3:
        return int(m3[0])
    return 0


def parse_bill_amount(text):
    amounts = re.findall(r"Rs[.\s]*(\d{3,6}(?:[.,]\d{2})?)", text, re.I)
    vals = []
    for a in amounts:
        try:
            vals.append(float(a.replace(",", "")))
        except ValueError:
            pass
    plausible = [v for v in vals if 200 <= v <= 50000]
    if plausible:
        return Counter(plausible).most_common(1)[0][0]
    m = re.search(r":\s*(\d{3,6})\.00", text)
    if m:
        return float(m.group(1))
    return 0.0


def parse_fixed_charges(text):
    m = re.search(r"(?:Fixed|Demand)[^0-9]{0,25}(\d{2,5}(?:\.\d{2})?)", text, re.I)
    if m:
        try:
            v = float(m.group(1))
            if 50 <= v <= 5000:
                return v
        except ValueError:
            pass
    return FIXED_CHARGE


# ── Step 3: Bundle all parsed fields ──────────────────────────────────────────
def extract_bill(image_path: str) -> dict:
    print(f"Running OCR on: {Path(image_path).name}")
    text = run_ocr(image_path)

    data = {
        "consumer_name":   parse_consumer_name(text),
        "consumer_no":     parse_consumer_no(text),
        "sanctioned_load": parse_sanctioned_load(text),
        "connection_type": parse_connection_type(text),
        "billing_month":   parse_billing_month(text),
        "units_consumed":  parse_units(text),
        "bill_amount":     parse_bill_amount(text),
        "fixed_charges":   parse_fixed_charges(text),
    }

    print(f"Done: {data['consumer_name']} | {data['billing_month']} | {data['units_consumed']} units | Rs.{data['bill_amount']}")
    return data


# ── Step 4: Fill the Excel template ───────────────────────────────────────────
def fill_excel(template_path: str, bill: dict, output_path: str):
    shutil.copy(template_path, output_path)
    wb = openpyxl.load_workbook(output_path)
    ws = wb.active

    # Fill Consumer 1 info (column D)
    ws["D1"] = bill["consumer_name"]
    ws["D2"] = bill["consumer_no"]
    ws["D3"] = bill["fixed_charges"]
    ws["D4"] = bill["sanctioned_load"]
    ws["D5"] = bill["connection_type"]

    # Fill units and bill amount in the correct month row
    row = MONTH_TO_ROW.get(bill["billing_month"])
    if row:
        ws[f"D{row}"] = bill["units_consumed"]
        ws[f"E{row}"] = bill["bill_amount"]
        ws[f"F{row}"] = f"=(E{row}-$D$3)/D{row}"
    else:
        print(f"Warning: billing month {bill['billing_month']} not found in template rows.")

    # Timestamp note
    ws["B32"] = f"Extracted by OCR on {datetime.now().strftime('%d-%b-%Y %H:%M')} | Bill: {bill['billing_month']}"
    ws["B32"].font = Font(italic=True, size=9, color="808080")

    wb.save(output_path)
    print(f"Excel saved: {output_path}")


# ── Main ───────────────────────────────────────────────────────────────────────
def main():
    parser = argparse.ArgumentParser(description="Energybae Bill to Excel")
    parser.add_argument("bill", help="Path to bill image (JPG/PNG)")
    parser.add_argument("--template", default="Energybae_Solar_NoAPI.xlsx")
    parser.add_argument("--output",   default="result.xlsx")
    args = parser.parse_args()

    bill = extract_bill(args.bill)
    fill_excel(args.template, bill, args.output)

    print("\n===== SUMMARY =====")
    for k, v in bill.items():
        print(f"  {k}: {v}")
    print("===================")


if __name__ == "__main__":
    main()
