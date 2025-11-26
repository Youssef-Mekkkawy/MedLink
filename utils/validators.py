"""
Input validation utilities
"""
import re
from datetime import datetime


def validate_national_id(national_id: str) -> tuple[bool, str]:
    """
    Validate Egyptian National ID (14 digits)
    Format: XYYMMDDCCCCCCG
    - X: Century (2 for 1900s, 3 for 2000s)
    - YYMMDD: Birth date
    - CCCCCC: Governorate code and sequence
    - G: Gender (odd=male, even=female)
    """
    # Remove any spaces or dashes
    national_id = national_id.replace(' ', '').replace('-', '')

    # Check if 14 digits
    if not re.match(r'^\d{14}$', national_id):
        return False, "National ID must be exactly 14 digits"

    # Check century digit (must be 2 or 3)
    century = int(national_id[0])
    if century not in [2, 3]:
        return False, "Invalid century digit (must be 2 or 3)"

    # Extract and validate birth date
    try:
        year = int(national_id[1:3])
        month = int(national_id[3:5])
        day = int(national_id[5:7])

        # Add century
        full_year = 1900 + year if century == 2 else 2000 + year

        # Validate date
        birth_date = datetime(full_year, month, day)

        # Check if date is not in future
        if birth_date > datetime.now():
            return False, "Birth date cannot be in the future"

    except ValueError:
        return False, "Invalid birth date in National ID"

    return True, "Valid"


def validate_phone(phone: str) -> tuple[bool, str]:
    """Validate Egyptian phone number"""
    phone = phone.replace(' ', '').replace('-', '')

    # Egyptian mobile: 11 digits starting with 01
    if re.match(r'^01[0-9]{9}$', phone):
        return True, "Valid"

    return False, "Phone must be 11 digits starting with 01"


def validate_email(email: str) -> tuple[bool, str]:
    """Validate email address"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if re.match(pattern, email):
        return True, "Valid"
    return False, "Invalid email format"


def validate_password(password: str) -> tuple[bool, str]:
    """Validate password strength"""
    if len(password) < 6:
        return False, "Password must be at least 6 characters"
    return True, "Valid"
