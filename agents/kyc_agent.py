# tools/ocr_tool.py
import pytesseract
from PIL import Image

# IMPORTANT: You must point pytesseract to your Tesseract installation path
# pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe' # Example for Windows

def extract_text_from_image(image_path: str) -> str:
    """Uses OCR to extract text from an image file."""
    try:
        image = Image.open(image_path)
        text = pytesseract.image_to_string(image)
        # You would add logic here to parse the text for PAN/Aadhar numbers, names, etc.
        return text
    except Exception as e:
        return f"Error processing image: {e}"

# agents/kyc_agent.py
from tools.ocr_tool import extract_text_from_image

def verify_documents(image_path: str):
    """Orchestrates the KYC process."""
    extracted_text = extract_text_from_image(image_path)
    # Dummy parsing logic
    if "INCOME TAX" in extracted_text.upper():
        return {"doc_type": "PAN", "details": {"pan_number": "ABCDE1234F", "pan_name": "ROHIT SHARMA"}}
    else:
        return {"doc_type": "Unknown", "details": {}}