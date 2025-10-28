from fastapi import FastAPI, Request, Body, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from kiwisolver import strength
from pydantic import BaseModel
from spellchecker import SpellChecker
import uvicorn
import os
from utils import detect_and_process_id_card, read_factory_number
from JwtKey import generate_jwt_secret
# from utils2 import read_factory_number
# from transformers import AutoTokenizer, AutoModelForMaskedLM
# import torch

# ---------------------------------------------------
# Initialize FastAPI
# ---------------------------------------------------
app = FastAPI(title="Arabic Spell Checker", version="1.1")

# ---------------------------------------------------
# Setup templates
# ---------------------------------------------------
templates = Jinja2Templates(directory="templates")

# ---------------------------------------------------
# Load AraBERT Model & Tokenizer
# ---------------------------------------------------
# tokenizer = AutoTokenizer.from_pretrained("aubmindlab/bert-base-arabertv2")
# model = AutoModelForMaskedLM.from_pretrained("aubmindlab/bert-base-arabertv2")
# model.eval()

# ---------------------------------------------------
# Pydantic Request Model
# ---------------------------------------------------
class SpellRequest(BaseModel):
    text: str

# ---------------------------------------------------
# Home Route
# ---------------------------------------------------
@app.get("/")
def home():
    return {"message": "Welcome to the Egyptian ID OCR + Arabic Spell Checker API 🚀"}

# ---------------------------------------------------
# Egyptian ID OCR Endpoint
# ---------------------------------------------------
@app.post("/process-id-path/")
async def process_id_card_path(
    image_path: str = Body(..., embed=True),
    application_number: str = Body(..., embed=True)
):
    if not os.path.exists(image_path):
        raise HTTPException(status_code=400, detail="File path does not exist")

    try:
        firstName, secName, fullName, nationalId, address, serial, birth, city, gender = detect_and_process_id_card(
            image_path, application_number
        )

        # --- Process Second Name (max 4 parts) ---
        secName_parts = secName.split()
        if len(secName_parts) > 4:
            secName = " ".join(secName_parts[:4])

        # --- Process Full Name (exactly 5 parts if possible) ---
        fullName_parts = fullName.split()
        if len(fullName_parts) > 5:
            fullName = " ".join(fullName_parts[:5])

        return {
            "First Name": firstName,
            "Second Name": secName,
            "Full Name": fullName,
            "National Id": nationalId,
            "Address": address,
            "Factory Number": serial,
            "Birth Date": birth,
            "City": city,
            "Gender": gender
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing ID card: {str(e)}")


@app.post("/read-factory/")
async def process_id_card_path(
    image_path: str = Body(..., embed=True),
    application_number: str = Body(..., embed=True)
):
    try:
        serial_number = read_factory_number(image_path)

        return {
            "application_number": application_number,
            "factory_number": serial_number,
            "status": "success"
        }
    except Exception as e:
        return {
            "application_number": application_number,
            "factory_number": None,
            "status": "error",
            "message": str(e)
        }

@app.get("/generate-jwt/")
async def generate_jwt_endpoint():
    try:
        result = generate_jwt_secret()
        print(result)
        return JSONResponse(content=result)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")


if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=9000, reload=True)
