"""
QR code generation for patient identification
"""
import qrcode
from PIL import Image
import io


def generate_qr_code(data: str, size: int = 200) -> Image.Image:
    """
    Generate QR code image
    
    Args:
        data: Data to encode in QR code
        size: Size of QR code image in pixels
    
    Returns:
        PIL Image object
    """
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)
    
    img = qr.make_image(fill_color="black", back_color="white")
    
    # Resize to requested size
    img = img.resize((size, size), Image.Resampling.LANCZOS)
    
    return img


def generate_patient_qr(national_id: str) -> Image.Image:
    """
    Generate QR code for patient National ID
    
    Args:
        national_id: Patient's National ID
    
    Returns:
        PIL Image with QR code
    """
    # Format: MEDLINK:ID:national_id
    data = f"MEDLINK:ID:{national_id}"
    return generate_qr_code(data, size=150)


def qr_to_bytes(qr_image: Image.Image) -> bytes:
    """
    Convert QR code image to bytes
    
    Args:
        qr_image: PIL Image
    
    Returns:
        Image bytes
    """
    img_byte_arr = io.BytesIO()
    qr_image.save(img_byte_arr, format='PNG')
    img_byte_arr.seek(0)
    return img_byte_arr.getvalue()