import pytesseract
from PIL import Image
import re
import os


# --- IMPORTANT CONFIGURATION ---
# On Windows, you might need to tell pytesseract where you installed the Tesseract engine.
# Uncomment the line below and set the correct path if you get a "TesseractNotFoundError".
# pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def extract_details_from_image(image_path: str) -> dict:
    """
    Uses Tesseract OCR to extract text from an image and then parses it
    to find key details from an Indian PAN or Aadhar card.

    Args:
        image_path: The full path to the image file.

    Returns:
        A dictionary containing the extracted details.
    """
    if not os.path.exists(image_path):
        return {"error": f"File not found at {image_path}"}

    try:
        # 1. Open the image file
        image = Image.open(image_path)

        # 2. Use Tesseract to extract all text from the image
        # Using lang='eng+hin' can help if there's Hindi text, e.g., on Aadhar cards.
        # You may need to install the Hindi language pack for Tesseract for this to work.
        full_text = pytesseract.image_to_string(image, lang='eng')

        # 3. Parse the extracted text to find specific details
        extracted_data = {"raw_text": full_text}

        # --- PAN Card Parsing Logic ---
        # A PAN number has a format of 5 letters, 4 numbers, 1 letter.
        pan_regex = r"[A-Z]{5}[0-9]{4}[A-Z]{1}"
        pan_match = re.search(pan_regex, full_text)
        if pan_match:
            extracted_data["doc_type"] = "PAN Card"
            extracted_data["pan_number"] = pan_match.group(0)
            # You would add more complex regex to find Name/Father's Name/DOB here

        # --- Aadhar Card Parsing Logic ---
        # An Aadhar number is 12 digits, often in XXXX XXXX XXXX format.
        aadhar_regex = r"\b\d{4}\s\d{4}\s\d{4}\b"
        aadhar_match = re.search(aadhar_regex, full_text)
        if aadhar_match:
            extracted_data["doc_type"] = "Aadhar Card"
            extracted_data["aadhar_number"] = aadhar_match.group(0)
            # Look for "DOB" or "Year of Birth"
            dob_match = re.search(r"(?:DOB|Birth|DoB|Binh)\s*[:\s]*\s*(\d{2}/\d{2}/\d{4})", full_text, re.IGNORECASE)
            if dob_match:
                extracted_data["date_of_birth"] = dob_match.group(1)

        if "doc_type" not in extracted_data:
            extracted_data["warning"] = "Could not confidently determine document type."

        return extracted_data

    except Exception as e:
        return {"error": f"An error occurred during OCR processing: {e}"}


# This block allows you to test the script directly from the command line
if __name__ == '__main__':
    # To test, create a folder named 'data' in your root directory and place a sample image there.
    # For example: smartloan360x/data/sample_pan.png

    # Create a dummy image path for testing
    # IMPORTANT: Change this to the actual path of a test image on your system
    # For example: test_image_path = os.path.join("..", "data", "sample_pan.png")
    test_image_path = "path/to/your/test_image.png"

    if os.path.exists(test_image_path):
        print(f"--- Processing image: {test_image_path} ---")
        details = extract_details_from_image(test_image_path)

        if "error" in details:
            print(f"Error: {details['error']}")
        else:
            print("Successfully extracted details:")
            for key, value in details.items():
                if key != "raw_text":
                    print(f"  - {key}: {value}")
            # print("\n--- Full Raw Text ---")
            # print(details['raw_text'])
    else:
        print(f"Test file not found: '{test_image_path}'.")
        print("Please update the 'test_image_path' variable in ocr_tool.py and place a sample image file there.")
