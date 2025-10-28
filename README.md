# 🇪🇬 Egyptian National ID OCR & Text Extraction API

A **FastAPI-powered OCR (Optical Character Recognition)** service for **extracting and processing text data from Egyptian National ID cards**, enhanced with **Arabic spell correction**, **factory number recognition**, and **JWT key generation** utilities.

This project integrates computer vision and natural language processing tools — including **OpenCV**, **PyTesseract**, **EasyOCR**, and **PySpellChecker** — to automatically read and structure information from scanned ID cards.

---

## 🚀 Features

* 🔍 **OCR-based text extraction** from Egyptian national ID cards
* 🧠 **Arabic name normalization and spell correction** using PySpellChecker
* 🏙️ **City, birth date, and gender extraction** from the ID number
* 🧾 **Factory number recognition** via `read_factory_number()`
* ⚡ Built on **FastAPI** — modern, fast, asynchronous Python web framework
* 🖼️ **OpenCV + EasyOCR + PyTesseract** for image preprocessing and recognition

---

## 🧩 Tech Stack

| Layer                | Library                                                                                                             | Purpose                                     |
| -------------------- | ------------------------------------------------------------------------------------------------------------------- | ------------------------------------------- |
| **Framework**        | [FastAPI](https://fastapi.tiangolo.com/)                                                                            | Core REST API                               |
| **Server**           | [Uvicorn](https://www.uvicorn.org/)                                                                                 | ASGI web server                             |
| **Data Validation**  | [Pydantic](https://docs.pydantic.dev/)                                                                              | Request/response models                     |
| **OCR Engine**       | [PyTesseract](https://pypi.org/project/pytesseract/)                                                                | Tesseract OCR bindings                      |
| **Deep OCR**         | [EasyOCR](https://github.com/JaidedAI/EasyOCR)                                                                      | Multi-language OCR backend                  |
| **Image Processing** | [OpenCV](https://opencv.org/)                                                                                       | Preprocessing, cropping, and edge detection |
| **Text Correction**  | [PySpellChecker](https://pyspellchecker.readthedocs.io/en/latest/)                                                  | Arabic text spell correction                |
| **Computer Vision**  | [Ultralytics (YOLO)](https://github.com/ultralytics/ultralytics)                                                    | Object detection / region identification    |
| **Utilities**        | [NumPy](https://numpy.org/), [Pillow](https://pillow.readthedocs.io/), [Jinja2](https://jinja.palletsprojects.com/) | Image and template utilities                |

---

## 📂 Project Structure

```
project/
│
├── app.py                  # Main FastAPI application
├── utils.py                # OCR and ID extraction logic
├── requirements.txt
└── README.md
```

---

## ⚙️ Installation

### 1️⃣ Clone the repository

```bash
git clone https://github.com/<kendor74>/OCR.git
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

Example `requirements.txt`:

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

## 🚀 Running the API

### Development Mode

Run locally using **Uvicorn**:

```bash
uvicorn app:app --reload --host 0.0.0.0 --port 8080
```

### Access the API:

* **Base URL:** [http://127.0.0.1:8080](http://127.0.0.1:8080)
* **Interactive Docs (Swagger UI):** [http://127.0.0.1:8080/docs](http://127.0.0.1:8080/docs)
* **Alternative Docs (ReDoc):** [http://127.0.0.1:8080/redoc](http://127.0.0.1:8080/redoc)

---

## 📡 API Endpoints

### 🔹 `POST /process-id-path/`

Extracts textual information from an Egyptian National ID image.

**Request Example:**

```json
{
  "image_path": "C:/images/id_sample.jpg",
  "application_number": "APP-12345"
}
```

**Response Example:**

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

### 🔹 `POST /read-factory/`

Reads only the **factory number** from the ID image.

**Request Example:**

```json
{
  "image_path": "C:/images/id_sample.jpg",
  "application_number": "APP-67890"
}
```

---

## 🧠 How It Works

1. **Preprocessing** — The image is enhanced using OpenCV (thresholding, noise removal, contour detection).
2. **Text Detection** — EasyOCR/YOLO identifies text zones on the ID.
3. **Text Extraction** — PyTesseract reads the text content from cropped regions.
4. **Arabic Correction** — The PySpellChecker model corrects detected Arabic spelling errors.
5. **Data Structuring** — Extracted fields (name, ID, date, gender) are organized and returned as JSON.

---

## 🔐 Security Notes

* All OCR and text processing are done locally — **no external API calls**.
* JWT secret generation uses **Python’s `secrets` module**, which provides cryptographically secure random bytes ([Python Docs](https://docs.python.org/3/library/secrets.html)).

---

## 🧾 License

This project is licensed under the **MIT License** — see the [LICENSE](LICENSE) file for details.

---

## 🤝 Contributing

Contributions are welcome!

1. Fork the repository
2. Create a feature branch
3. Submit a pull request with clear details

---

## 📚 References

* [FastAPI Documentation](https://fastapi.tiangolo.com/)
* [OpenCV Documentation](https://docs.opencv.org/)
* [Tesseract OCR Docs](https://tesseract-ocr.github.io/)
* [EasyOCR GitHub](https://github.com/JaidedAI/EasyOCR)
* [PySpellChecker Docs](https://pyspellchecker.readthedocs.io/en/latest/)
* [Ultralytics YOLO Docs](https://docs.ultralytics.com/)

---
