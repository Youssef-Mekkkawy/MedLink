"""
Localization support for future multi-language
Currently English only, but structured for easy expansion
"""

STRINGS = {
    'en': {
        # Login screen
        'app_title': 'MedLink - Medical Records System',
        'login_title': 'Login',
        'username': 'Username',
        'password': 'Password',
        'role': 'Role',
        'doctor': 'Doctor',
        'patient': 'Patient',
        'login_button': 'Login',
        'register_patient': 'Register New Patient',
        'login_error': 'Invalid username or password',

        # Common
        'save': 'Save',
        'cancel': 'Cancel',
        'delete': 'Delete',
        'edit': 'Edit',
        'search': 'Search',
        'logout': 'Logout',
        'loading': 'Loading...',

        # Dashboard
        'welcome': 'Welcome',
        'search_patient': 'Search Patient by National ID',
        'patient_profile': 'Patient Profile',
        'medical_history': 'Medical History',
        'lab_results': 'Lab Results',
        'imaging_results': 'Imaging Results',
        'emergency_card': 'Emergency Card',

        # Patient info
        'national_id': 'National ID',
        'full_name': 'Full Name',
        'date_of_birth': 'Date of Birth',
        'age': 'Age',
        'gender': 'Gender',
        'blood_type': 'Blood Type',
        'phone': 'Phone',
        'emergency_contact': 'Emergency Contact',

        # Medical
        'chronic_diseases': 'Chronic Diseases',
        'allergies': 'Allergies',
        'current_medications': 'Current Medications',
        'visit_date': 'Visit Date',
        'doctor': 'Doctor',
        'diagnosis': 'Diagnosis',
        'treatment': 'Treatment',
    },
    # Future: add 'ar' for Arabic
}

# Current language
CURRENT_LANG = 'en'


def get_string(key: str) -> str:
    """Get localized string by key"""
    return STRINGS.get(CURRENT_LANG, {}).get(key, key)


def set_language(lang: str):
    """Change application language"""
    global CURRENT_LANG
    if lang in STRINGS:
        CURRENT_LANG = lang
