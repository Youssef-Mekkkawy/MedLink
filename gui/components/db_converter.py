"""
Universal Database Compatibility Converter
Works with ANY GUI component - NO DESIGN CHANGES!

Location: gui/components/db_converter.py
"""


def convert_to_dict(obj):
    """
    Universal converter: SQLAlchemy object → Python dict
    Works with Patient, Doctor, Visit, or any model
    
    Returns dict if input is dict, converts if SQLAlchemy object
    """
    # Already a dict? Return as-is
    if isinstance(obj, dict):
        return obj
    
    # Try to_dict() method first
    if hasattr(obj, 'to_dict') and callable(getattr(obj, 'to_dict')):
        try:
            return obj.to_dict()
        except:
            pass
    
    # Manual conversion for SQLAlchemy models
    result = {}
    
    # Basic attributes
    basic_attrs = [
        'national_id', 'full_name', 'age', 'gender', 'blood_type', 
        'phone', 'email', 'address', 'date_of_birth',
        'user_id', 'username', 'role', 'specialization', 'license_number',
        'hospital', 'department'
    ]
    
    for attr in basic_attrs:
        if hasattr(obj, attr):
            value = getattr(obj, attr, None)
            # Handle Enums
            if hasattr(value, 'value'):
                result[attr] = value.value
            # Handle dates
            elif hasattr(value, 'isoformat'):
                result[attr] = value.isoformat()
            else:
                result[attr] = value
    
    # Relationships - Allergies
    if hasattr(obj, 'allergies'):
        try:
            result['allergies'] = [
                a.allergen_name for a in obj.allergies
            ] if obj.allergies else []
        except:
            result['allergies'] = []
    
    # Relationships - Chronic Diseases
    if hasattr(obj, 'chronic_diseases'):
        try:
            result['chronic_diseases'] = [
                cd.disease_name for cd in obj.chronic_diseases
            ] if obj.chronic_diseases else []
        except:
            result['chronic_diseases'] = []
    
    # Relationships - Current Medications
    if hasattr(obj, 'current_medications'):
        try:
            result['current_medications'] = [
                {
                    'name': m.medication_name,
                    'dosage': m.dosage,
                    'frequency': m.frequency
                }
                for m in obj.current_medications
                if hasattr(m, 'is_active') and m.is_active
            ] if obj.current_medications else []
        except:
            result['current_medications'] = []
    
    return result


def safe_get(obj, key, default=None):
    """Safely get value from dict or object"""
    if isinstance(obj, dict):
        return obj.get(key, default)
    return getattr(obj, key, default)