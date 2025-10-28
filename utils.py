import os
import cv2
import pytesseract
import numpy as np
from ultralytics import YOLO
import re
from PIL import Image
import json
import easyocr
# ----------------------------------------------------------------------
# 1. Configure Tesseract Path (IMPORTANT for Windows)
# ----------------------------------------------------------------------
pytesseract.pytesseract.tesseract_cmd = r"C:\Users\mohamed.abdallateaf\AppData\Local\Programs\Tesseract-OCR\tesseract.exe"

# ----------------------------------------------------------------------
# 2. Tesseract Configurations (Arabic + English)
# ----------------------------------------------------------------------
tess_config_ar = "--psm 6 --oem 3 -l ara"
tess_config_en = "--psm 6 --oem 3 -l eng"

# ----------------------------------------------------------------------
# 3. Paths for Saving Data
# ----------------------------------------------------------------------
BASE_DIR = r"D:/egyption id"
IMAGES_DIR = os.path.join(BASE_DIR, "images")
ANNOTATIONS_DIR = os.path.join(BASE_DIR, "annotations")
LABELS_DIR = os.path.join(BASE_DIR, "labels")

os.makedirs(IMAGES_DIR, exist_ok=True)
os.makedirs(ANNOTATIONS_DIR, exist_ok=True)
os.makedirs(LABELS_DIR, exist_ok=True)

# ----------------------------------------------------------------------
# 4. Preprocess Image for Better OCR Results
# ----------------------------------------------------------------------
def preprocess_image(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = cv2.bilateralFilter(gray, 11, 17, 17)  # Reduce noise
    _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    return thresh

# ----------------------------------------------------------------------
# 5. Extract Text Using Tesseract (Arabic / English)
# ----------------------------------------------------------------------
def extract_text_tesseract(image, bbox, lang='ara'):
    x1, y1, x2, y2 = bbox
    cropped = image[y1:y2, x1:x2]
    preprocessed = preprocess_image(cropped)

    try:
        if lang == 'ara':
            text = pytesseract.image_to_string(preprocessed, config=tess_config_ar)
        else:
            text = pytesseract.image_to_string(preprocessed, config=tess_config_en)
    except pytesseract.pytesseract.TesseractNotFoundError:
        raise RuntimeError("⚠️ Tesseract not found! Please check the path configuration.")

    return text.strip()

# ----------------------------------------------------------------------
# 6. Detect National ID Digits Using YOLO
# ----------------------------------------------------------------------
def detect_national_id(cropped_image):
    model = YOLO('detect_id.pt')
    results = model(cropped_image)
    detected_info = []

    for result in results:
        for box in result.boxes:
            cls = int(box.cls)
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            detected_info.append((cls, x1))

            # Draw rectangle for debugging
            cv2.rectangle(cropped_image, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(cropped_image, str(cls), (x1, y1 - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.9, (36, 255, 12), 2)

    detected_info.sort(key=lambda x: x[1])
    id_number = ''.join([str(cls) for cls, _ in detected_info])

    return id_number

# ----------------------------------------------------------------------
# 7. Decode Egyptian National ID
# ----------------------------------------------------------------------
def decode_egyptian_id(id_number):
    governorates = {
        '01': 'Cairo', '02': 'Alexandria', '03': 'Port Said', '04': 'Suez',
        '11': 'Damietta', '12': 'Dakahlia', '13': 'Ash Sharqia', '14': 'Kaliobeya',
        '15': 'Kafr El-Sheikh', '16': 'Gharbia', '17': 'Monoufia', '18': 'El Beheira',
        '19': 'Ismailia', '21': 'Giza', '22': 'Beni Suef', '23': 'Fayoum',
        '24': 'El Menia', '25': 'Assiut', '26': 'Sohag', '27': 'Qena',
        '28': 'Aswan', '29': 'Luxor', '31': 'Red Sea', '32': 'New Valley',
        '33': 'Matrouh', '34': 'North Sinai', '35': 'South Sinai', '88': 'Foreign'
    }

    century_digit = int(id_number[0])
    year = int(id_number[1:3])
    month = int(id_number[3:5])
    day = int(id_number[5:7])
    governorate_code = id_number[7:9]
    gender_code = int(id_number[12:13])

    if century_digit == 2:
        full_year = 1900 + year
    elif century_digit == 3:
        full_year = 2000 + year
    else:
        raise ValueError("Invalid century digit")

    gender = "Male" if gender_code % 2 != 0 else "Female"
    governorate = governorates.get(governorate_code, "Unknown")
    birth_date = f"{full_year:04d}-{month:02d}-{day:02d}"

    return {
        'Birth Date': birth_date,
        'Governorate': governorate,
        'Gender': gender
    }

# ----------------------------------------------------------------------
# 8. Process the Cropped ID Image
# ----------------------------------------------------------------------

def process_image(cropped_image, image_name):
    model = YOLO('detect_odjects.pt')
    results = model(cropped_image)

    first_name, second_name, merged_name, nid, address, serial = '', '', '', '', '', ''
    labels_data = []

    for result in results:
        for box in result.boxes:
            bbox = [int(coord) for coord in box.xyxy[0].tolist()]
            class_id = int(box.cls[0].item())
            class_name = result.names[class_id]
            confidence = float(box.conf[0].item())

            if class_name == 'firstName':
                first_name = extract_text_tesseract(cropped_image, bbox, lang='ara')

            elif class_name == 'lastName':
                second_name = extract_text_tesseract(cropped_image, bbox, lang='ara')

            elif class_name == 'serial':
                # --- Crop the serial region ---
                x1, y1, x2, y2 = bbox
                cropped_serial = cropped_image[y1:y2, x1:x2]

                # Save to temp path
                temp_path = os.path.join(LABELS_DIR, f"temp_serial_{image_name}")
                cv2.imwrite(temp_path, cropped_serial)

                # Use utils.read_factory_number to extract
                serial, variant_used = read_factory_number(temp_path)

                # Remove temp file after reading
                if os.path.exists(temp_path):
                    os.remove(temp_path)

                print(f"[INFO] Serial extracted: {serial} (variant {variant_used})")

            elif class_name == 'address':
                address = extract_text_tesseract(cropped_image, bbox, lang='ara')

            elif class_name == 'nid':
                nid = detect_national_id(cropped_image)

            # Save bounding box data
            labels_data.append({
                "class": class_name,
                "confidence": round(confidence, 3),
                "bbox": {
                    "x1": bbox[0],
                    "y1": bbox[1],
                    "x2": bbox[2],
                    "y2": bbox[3]
                }
            })

            # Draw bounding boxes for annotated image
            x1, y1, x2, y2 = bbox
            cv2.rectangle(cropped_image, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(cropped_image, class_name, (x1, y1 - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

    # Save annotated image
    annotated_path = os.path.join(ANNOTATIONS_DIR, f"annotated_{image_name}")
    cv2.imwrite(annotated_path, cropped_image)

    # Save labels JSON
    json_path = os.path.join(LABELS_DIR, f"{os.path.splitext(image_name)[0]}.json")
    with open(json_path, "w", encoding="utf-8") as json_file:
        json.dump(labels_data, json_file, indent=4, ensure_ascii=False)

    merged_name = f"{first_name} {second_name}"
    decoded_info = decode_egyptian_id(nid)

    return (
        first_name,
        second_name,
        merged_name,
        nid,
        address,
        serial,
        decoded_info["Birth Date"],
        decoded_info["Governorate"],
        decoded_info["Gender"]
    )

# ----------------------------------------------------------------------
# 9. Detect ID Card First, Then Crop & Process + Save
# ----------------------------------------------------------------------
# def detect_and_process_id_card(image_path):
#     id_card_model = YOLO('detect_id_card.pt')
#     id_card_results = id_card_model(image_path)
#     image = cv2.imread(image_path)
#     image_name = os.path.basename(image_path)

#     cropped_image = None
#     for result in id_card_results:
#         for box in result.boxes:
#             x1, y1, x2, y2 = map(int, box.xyxy[0])
#             cropped_image = image[y1:y2, x1:x2]

#     if cropped_image is None:
#         raise ValueError("⚠️ ID card not detected!")

#     # Save cropped image in images folder
#     cropped_path = os.path.join(IMAGES_DIR, image_name)
#     cv2.imwrite(cropped_path, cropped_image)

#     return process_image(cropped_image, image_name)

reader = easyocr.Reader(['en'])

def preprocess_variants(img):
    """Generate different preprocessed versions of the image."""
    variants = []

    # 1. Original
    variants.append(img)

    # 2. Grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    variants.append(gray)

    # 3. OTSU threshold
    _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    variants.append(thresh)

    # 4. Inverted
    variants.append(cv2.bitwise_not(thresh))

    # 5. Resized (scale up for better OCR)
    resized = cv2.resize(gray, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)
    variants.append(resized)

    return variants

def read_factory_number(image_path: str):
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"Image not found: {image_path}")

    img = cv2.imread(image_path)
    preprocessed_images = preprocess_variants(img)

    for i, processed in enumerate(preprocessed_images, start=1):
        results = reader.readtext(processed, detail=0)

        for text in results:
            text = text.strip().replace(" ", "").replace("\n", "")
            text = text.replace("O", "0").replace("o", "0")  # Fix OCR mistakes

            match = re.search(r'[A-Z]{2}\d{7}', text)
            if match:
                return match.group(0), i

    return None, None



def detect_and_process_id_card(image_path, application_number):
    # ---- 1. Load and convert image to JPG ----
    image = Image.open(image_path).convert("RGB")  # Force RGB (handles PNG, etc.)
    image_name = f"{application_number}.jpg"       # Use application number for naming
    jpg_path = os.path.join(IMAGES_DIR, image_name)
    image.save(jpg_path, "JPEG")                   # Save as JPG

    # ---- 2. Run YOLO on the JPG image ----
    id_card_model = YOLO('detect_id_card.pt')
    id_card_results = id_card_model(jpg_path)

    image_cv = cv2.imread(jpg_path)
    cropped_image = None

    for result in id_card_results:
        for box in result.boxes:
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            cropped_image = image_cv[y1:y2, x1:x2]

    if cropped_image is None:
        raise ValueError("⚠️ ID card not detected!")

    # ---- 3. Save cropped image with application number ----
    cropped_path = os.path.join(IMAGES_DIR, image_name)
    cv2.imwrite(cropped_path, cropped_image)

    # ---- 4. Process image ----
    return process_image(cropped_image, image_name)
