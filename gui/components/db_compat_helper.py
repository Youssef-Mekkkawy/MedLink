"""
DATABASE COMPATIBILITY HELPER - Universal Fix
Add this to ANY GUI component that has database issues

Location: gui/components/db_compat_helper.py
"""


class DatabaseCompatibilityMixin:
    """
    Mixin class to add database compatibility to any GUI component
    
    Usage:
        class MyComponent(ctk.CTkFrame, DatabaseCompatibilityMixin):
            def __init__(self, parent, patient_data):
                ctk.CTkFrame.__init__(self, parent)
                self.patient_data = self.convert_to_dict(patient_data)
    """
    
    def convert_to_dict(self, obj):
        """Convert SQLAlchemy object to dictionary"""
        if isinstance(obj, dict):
            return obj
        
        if hasattr(obj, 'to_dict'):
            try:
                return obj.to_dict()
            except:
                pass
        
        # Manual conversion for SQLAlchemy objects
        result = {}
        
        # Get basic attributes
        if hasattr(obj, '__table__'):
            # It's a SQLAlchemy model
            for column in obj.__table__.columns:
                value = getattr(obj, column.name)
                
                # Handle enums
                if hasattr(value, 'value'):
                    result[column.name] = value.value
                # Handle dates
                elif hasattr(value, 'isoformat'):
                    result[column.name] = value.isoformat()
                else:
                    result[column.name] = value
        else:
            # Generic object
            for key in dir(obj):
                if not key.startswith('_') and not callable(getattr(obj, key, None)):
                    try:
                        value = getattr(obj, key)
                        if hasattr(value, 'value'):
                            result[key] = value.value
                        elif hasattr(value, 'isoformat'):
                            result[key] = value.isoformat()
                        else:
                            result[key] = value
                    except:
                        pass
        
        # Handle common relationships
        if hasattr(obj, 'allergies'):
            try:
                result['allergies'] = [a.allergen_name for a in obj.allergies]
            except:
                result['allergies'] = []
        
        if hasattr(obj, 'chronic_diseases'):
            try:
                result['chronic_diseases'] = [cd.disease_name for cd in obj.chronic_diseases]
            except:
                result['chronic_diseases'] = []
        
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
                ]
            except:
                result['current_medications'] = []
        
        if hasattr(obj, 'surgeries'):
            try:
                result['surgeries'] = [
                    {
                        'procedure': s.procedure_name,
                        'date': s.surgery_date.isoformat() if hasattr(s.surgery_date, 'isoformat') else str(s.surgery_date),
                        'hospital': s.hospital,
                        'surgeon': s.surgeon_name
                    }
                    for s in obj.surgeries
                ]
            except:
                result['surgeries'] = []
        
        if hasattr(obj, 'hospitalizations'):
            try:
                result['hospitalizations'] = [
                    {
                        'reason': h.admission_reason,
                        'admission_date': h.admission_date.isoformat() if hasattr(h.admission_date, 'isoformat') else str(h.admission_date),
                        'discharge_date': h.discharge_date.isoformat() if h.discharge_date and hasattr(h.discharge_date, 'isoformat') else str(h.discharge_date) if h.discharge_date else None,
                        'hospital': h.hospital
                    }
                    for h in obj.hospitalizations
                ]
            except:
                result['hospitalizations'] = []
        
        if hasattr(obj, 'vaccinations'):
            try:
                result['vaccinations'] = [
                    {
                        'vaccine_name': v.vaccine_name,
                        'date_administered': v.date_administered.isoformat() if hasattr(v.date_administered, 'isoformat') else str(v.date_administered),
                        'dose_number': v.dose_number
                    }
                    for v in obj.vaccinations
                ]
            except:
                result['vaccinations'] = []
        
        return result
    
    def safe_get(self, obj, key, default=None):
        """Safely get value from dict or object"""
        if isinstance(obj, dict):
            return obj.get(key, default)
        return getattr(obj, key, default)
    
    def extract_medication_name(self, med):
        """Extract medication name from various formats"""
        if isinstance(med, dict):
            return med.get('name', med.get('medication_name', 'Unknown'))
        return str(med)
    
    def format_medications(self, medications):
        """Format medications list for display"""
        if not medications:
            return []
        
        result = []
        for med in medications:
            if isinstance(med, dict):
                name = med.get('name', med.get('medication_name', 'Unknown'))
                dosage = med.get('dosage', '')
                frequency = med.get('frequency', '')
                result.append({
                    'name': name,
                    'dosage': dosage,
                    'frequency': frequency,
                    'display': f"{name} - {dosage} {frequency}".strip()
                })
            else:
                result.append({
                    'name': str(med),
                    'dosage': '',
                    'frequency': '',
                    'display': str(med)
                })
        
        return result


# Quick fix snippet to add to any component
QUICK_FIX = """
# Add this at the top of your __init__ method:
if hasattr(patient_data, '__dict__') and not isinstance(patient_data, dict):
    from gui.components.db_compat_helper import DatabaseCompatibilityMixin
    helper = DatabaseCompatibilityMixin()
    self.patient_data = helper.convert_to_dict(patient_data)
else:
    self.patient_data = patient_data
"""
