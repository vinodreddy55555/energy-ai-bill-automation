# ⚡ Energy AI Bill Automation

## 📌 Overview

This project automates the analysis of electricity bills using OCR (Optical Character Recognition) and generates a structured Excel report with solar energy insights.

The system allows users to upload a bill image, extracts key information, and fills a predefined Excel template for further analysis.

---

## 🚀 Features

* 📄 Upload electricity bill (JPG/PNG)
* 🔍 Extract data using OCR (Tesseract)
* 📊 Automatically fill Excel template
* ⚡ Generate solar capacity recommendations
* 🌐 Simple web interface using Flask

---

## 🛠️ Tech Stack

* **Python**
* **Flask**
* **Tesseract OCR**
* **OpenPyXL**
* **Pillow (Image Processing)**

---

## 📂 Project Structure

```
energy-ai-bill-automation/
│── app.py
│── process_bill.py
│── Energybae_Solar_NoAPI.xlsx
│── requirements.txt
└── templates/
    └── index.html
```

---

## ⚙️ Installation & Setup

### 1️⃣ Clone the repository

```
git clone https://github.com/your-username/energy-ai-bill-automation.git
cd energy-ai-bill-automation
```

### 2️⃣ Install dependencies

```
pip install -r requirements.txt
```

### 3️⃣ Install Tesseract OCR

Download and install from:
https://github.com/tesseract-ocr/tesseract

> Make sure to add Tesseract to your system PATH

---

## ▶️ Run the Application

```
python app.py
```

Open your browser:

```
http://127.0.0.1:5000/
```

---

## 📸 Workflow

1. Upload electricity bill image
2. OCR extracts bill details
3. Data is processed using Python
4. Excel report is generated and downloaded

---

## 📊 Output

* Processed Excel file (`result.xlsx`)
* Contains:

  * Consumer details
  * Units consumed
  * Bill amount
  * Solar system estimation

---

## 🎯 Use Case

* Automates manual bill analysis
* Helps in solar energy planning
* Useful for energy consultants & analysts

---

## ⚠️ Note

* Ensure Tesseract OCR is properly installed
* Works best with clear bill images

---
# ⚡ Energy AI Bill Automation

## 📌 Overview

This project automates the analysis of electricity bills using OCR (Optical Character Recognition) and generates a structured Excel report with solar energy insights.

The system allows users to upload a bill image, extracts key information, and fills a predefined Excel template for further analysis.

---

## 🚀 Features

* 📄 Upload electricity bill (JPG/PNG)
* 🔍 Extract data using OCR (Tesseract)
* 📊 Automatically fill Excel template
* ⚡ Generate solar capacity recommendations
* 🌐 Simple web interface using Flask

---

## 🛠️ Tech Stack

* **Python**
* **Flask**
* **Tesseract OCR**
* **OpenPyXL**
* **Pillow (Image Processing)**

---

## 📂 Project Structure

```
energy-ai-bill-automation/
│── app.py
│── process_bill.py
│── Energybae_Solar_NoAPI.xlsx
│── requirements.txt
└── templates/
    └── index.html
```

---

## ⚙️ Installation & Setup

### 1️⃣ Clone the repository

```
git clone https://github.com/your-username/energy-ai-bill-automation.git
cd energy-ai-bill-automation
```

### 2️⃣ Install dependencies

```
pip install -r requirements.txt
```

### 3️⃣ Install Tesseract OCR

Download and install from:
https://github.com/tesseract-ocr/tesseract

> Make sure to add Tesseract to your system PATH

---

## ▶️ Run the Application

```
python app.py
```

Open your browser:

```
http://127.0.0.1:5000/
```

---

## 📸 Workflow

1. Upload electricity bill image
2. OCR extracts bill details
3. Data is processed using Python
4. Excel report is generated and downloaded

---

## 📊 Output

* Processed Excel file (`result.xlsx`)
* Contains:

  * Consumer details
  * Units consumed
  * Bill amount
  * Solar system estimation

---

## 🎯 Use Case

* Automates manual bill analysis
* Helps in solar energy planning
* Useful for energy consultants & analysts

---

## ⚠️ Note

* Ensure Tesseract OCR is properly installed
* Works best with clear bill images

---

## 👨‍💻 Author

Vinod Reddy

---

## 📌 Future Improvements

* Support multiple bill uploads
* Add dashboard visualization
* Improve OCR accuracy with ML models


## 📌 Future Improvements

* Support multiple bill uploads
* Add dashboard visualization
* Improve OCR accuracy with ML models
