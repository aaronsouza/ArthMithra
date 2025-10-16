# tools/pdf_generator.py
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
import qrcode


def generate_sanction_letter(customer_name, loan_amount, interest_rate, file_path="sanction_letter.pdf"):
    """Generates a PDF sanction letter with a QR code."""
    c = canvas.Canvas(file_path, pagesize=letter)
    width, height = letter

    c.drawString(72, height - 72, "Loan Sanction Letter")
    c.drawString(72, height - 100, f"Dear {customer_name},")
    c.drawString(72, height - 120, f"Your loan of INR {loan_amount} has been approved at {interest_rate}%.")

    # Generate and add QR code
    qr_data = f"Customer: {customer_name}, Amount: {loan_amount}"
    qr_img = qrcode.make(qr_data)
    qr_img_path = "loan_qr.png"
    qr_img.save(qr_img_path)
    c.drawImage(qr_img_path, width - 150, height - 150, width=100, height=100)

    c.save()
    return file_path