# 🏦 Egyptian National ID OCR API for Insurance Systems

A **FastAPI-based OCR (Optical Character Recognition)** service developed to help **insurance companies** automate the extraction and processing of **Egyptian National ID card data**.
This system leverages state-of-the-art **computer vision** and **natural language processing** tools to identify, read, and structure ID card information for accurate policy creation and client verification.

---

## 💼 Use Case

Insurance companies often require quick and accurate data entry from customer-provided ID cards.
This API automates that process by:

* Reading ID card images
* Extracting critical data (Name, National ID, Birth Date, Gender, Address, Factory Number)
* Optionally correcting Arabic text
* Returning a structured JSON ready for backend integration into policy management systems

---

## 🚀 Features

* 🔍 **Automatic ID text extraction** (OCR-based)
* 🧠 **Arabic name normalization & spell correction**
* 🏙️ **City, birth date, and gender parsing** from National ID
* 🏭 **Factory number detection** via OpenCV & OCR
* ⚡ **High-speed performance** using asynchronous FastAPI
* 📦 **Ready for integration** with insurance onboarding or policy systems

---

## 🧩 Tech Stack

| Layer                | Library                                                                                                             | Purpose                                  |
| -------------------- | ------------------------------------------------------------------------------------------------------------------- | ---------------------------------------- |
| **Framework**        | [FastAPI](https://fastapi.tiangolo.com/)                                                                            | REST API framework                       |
| **Server**           | [Uvicorn](https://www.uvicorn.org/)                                                                                 | ASGI server                              |
| **Validation**       | [Pydantic](https://docs.pydantic.dev/)                                                                              | Request/response data models             |
| **OCR Engine**       | [PyTesseract](https://pypi.org/project/pytesseract/)                                                                | Tesseract OCR engine                     |
| **Deep OCR**         | [EasyOCR](https://github.com/JaidedAI/EasyOCR)                                                                      | Multi-language text extraction           |
| **Computer Vision**  | [OpenCV](https://opencv.org/)                                                                                       | Image preprocessing and segmentation     |
| **Spell Correction** | [PySpellChecker](https://pyspellchecker.readthedocs.io/en/latest/)                                                  | Arabic text correction                   |
| **YOLO (Optional)**  | [Ultralytics](https://github.com/ultralytics/ultralytics)                                                           | Object detection (ID field localization) |
| **Utilities**        | [NumPy](https://numpy.org/), [Pillow](https://pillow.readthedocs.io/), [Jinja2](https://jinja.palletsprojects.com/) | Image manipulation & templating          |

---

## 📁 Project Structure

```
insurance-id-ocr/
│
├── app.py                  # Main FastAPI application
├── utils.py                # Core OCR & ID extraction functions
├── requirements.txt
└── README.md
```

---

## ⚙️ Installation

### 1️⃣ Clone the repository

```bash
git clone https://github.com/kendor74/OCR.git
cd OCR
```

### 2️⃣ Create a virtual environment

```bash
python -m venv venv
source venv/bin/activate      # On Linux/Mac
venv\Scripts\activate         # On Windows
```

### 3️⃣ Install dependencies

```bash
pip install -r requirements.txt
```

#### Example `requirements.txt`

```
fastapi
uvicorn
pydantic
opencv-python
pytesseract
numpy
ultralytics
pillow
easyocr
jinja2
pyspellchecker
```

---

## 🧠 How It Works

1. **Image Input** — Receive an ID image via API or file path
2. **Preprocessing** — OpenCV enhances image clarity and contrast
3. **Text Detection** — EasyOCR & PyTesseract identify text zones
4. **Arabic Correction** — PySpellChecker normalizes and corrects text
5. **Data Parsing** — Extracted text is analyzed for:

   * Full Name
   * National ID Number
   * Address
   * Factory Number
   * Birth Date
   * City
   * Gender
6. **JSON Response** — Clean structured output ready for policy creation

---

## 🚀 Running the Server

Run with Uvicorn (development mode):

```bash
uvicorn app:app --reload --host 0.0.0.0 --port 8080
```

### Access:

* **Swagger UI:** [http://127.0.0.1:8080/docs](http://127.0.0.1:8080/docs)
* **ReDoc UI:** [http://127.0.0.1:8080/redoc](http://127.0.0.1:8080/redoc)

---

## 📡 API Endpoints

### 🔹 `/process-id-path/` — Extract ID Card Data

**Method:** `POST`

**Request:**

```json
{
  "image_path": "C:/images/id_sample.jpg",
  "application_number": "APP-12345"
}
```

**Response Example (Arabic values):**

```json
{
  "First Name": "أحمد",
  "Second Name": "محمد علي",
  "Full Name": "أحمد محمد علي حسن",
  "National Id": "29803211501234",
  "Address": "القاهرة، مصر",
  "Factory Number": "F1234567",
  "Birth Date": "1998-03-21",
  "City": "القاهرة",
  "Gender": "ذكر"
}
```

---

### 🔹 `/read-factory/` — Extract Only Factory Number

**Method:** `POST`

**Request:**

```json
{
  "image_path": "C:/images/id_sample.jpg",
  "application_number": "APP-56789"
}
```

**Response:**

```json
{
  "application_number": "APP-56789",
  "factory_number": "F1234567",
  "status": "success"
}
```

---

---

## 🧱 Integration Example (Insurance Backend)

The API can be integrated into your insurance system for:

* **Customer onboarding**
* **Policy verification**
* **Automated data entry** from scanned ID cards
* **Document management** or **KYC** verification modules

You can call the `/process-id-path/` endpoint from .NET, Java, or Node.js using a simple HTTP request.

---

## 🔐 Security

* **Local-only processing:** No external OCR APIs — all processing runs securely on your own infrastructure.
* **Supports HTTPS and reverse proxy deployment** via Nginx or Traefik for production.

---

## 🧾 License

This project is licensed under the **MIT License** — you are free to use and adapt it for internal or commercial insurance systems.

---

## 🤝 Contributing

Contributions, suggestions, and feature improvements are welcome.

1. Fork the repo
2. Create a feature branch
3. Submit a pull request

---

## 📚 References

* [FastAPI Documentation](https://fastapi.tiangolo.com/)
* [OpenCV Documentation](https://docs.opencv.org/)
* [Tesseract OCR Docs](https://tesseract-ocr.github.io/)
* [EasyOCR GitHub](https://github.com/JaidedAI/EasyOCR)
* [PySpellChecker Docs](https://pyspellchecker.readthedocs.io/en/latest/)
* [Ultralytics YOLO Docs](https://docs.ultralytics.com/)

---

