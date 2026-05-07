"""
Energybae — app.py
Flask web server: upload bill → OCR → fill Excel → download
"""

from flask import Flask, render_template, request, send_file, jsonify
import os, subprocess, sys
from pathlib import Path

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
TEMPLATE      = "Energybae_Solar_NoAPI.xlsx"
OUTPUT_FILE   = os.path.join(UPLOAD_FOLDER, "result.xlsx")

os.makedirs(UPLOAD_FOLDER, exist_ok=True)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/process", methods=["POST"])
def process():
    # 1. Check file was uploaded
    if "file" not in request.files or not request.files["file"].filename:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files["file"]
    filepath = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(filepath)

    # 2. Run OCR + Excel fill script with a 90-second timeout
    try:
        result = subprocess.run(
            [sys.executable, "process_bill.py", filepath,
             "--template", TEMPLATE,
             "--output",   OUTPUT_FILE],
            capture_output=True,
            text=True,
            timeout=90
        )
    except subprocess.TimeoutExpired:
        return jsonify({"error": "Processing timed out. Try a smaller/clearer image."}), 500

    if result.returncode != 0:
        return jsonify({"error": result.stderr or "Processing failed"}), 500

    # 3. Send the filled Excel back
    if not os.path.exists(OUTPUT_FILE):
        return jsonify({"error": "Output file not created"}), 500

    return send_file(
        os.path.abspath(OUTPUT_FILE),
        as_attachment=True,
        download_name="Energybae_Solar_Analysis.xlsx"
    )


if __name__ == "__main__":
    app.run(debug=True, port=5000)
