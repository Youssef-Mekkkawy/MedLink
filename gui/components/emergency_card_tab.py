"""
Emergency Card Tab - WORKING VERSION
Location: gui/components/emergency_card_tab.py

REPLACE YOUR ENTIRE emergency_card_tab.py WITH THIS FILE!
"""
import customtkinter as ctk
from gui.components.emergency_card_content import EmergencyCardContent


class EmergencyCardTab(ctk.CTkFrame):
    """Emergency card tab - uses shared EmergencyCardContent"""
    
    def __init__(self, parent, patient_data):
        super().__init__(parent, fg_color='transparent')
        # DATABASE FIX: Convert SQLAlchemy objects to dict
        if hasattr(patient_data, '__dict__') and not isinstance(patient_data, dict):
            if hasattr(patient_data, 'to_dict'):
                self.patient_data = patient_data.to_dict()
            else:
                # Manual conversion
                self.patient_data = {}
                for attr in ['national_id', 'full_name', 'age', 'gender', 'blood_type', 'phone', 'email']:
                    value = getattr(patient_data, attr, None)
                    if hasattr(value, 'value'):  # Enum
                        self.patient_data[attr] = value.value
                    else:
                        self.patient_data[attr] = value
                
                # Handle relationships
                if hasattr(patient_data, 'allergies'):
                    self.patient_data['allergies'] = [a.allergen_name for a in patient_data.allergies]
                if hasattr(patient_data, 'chronic_diseases'):
                    self.patient_data['chronic_diseases'] = [cd.disease_name for cd in patient_data.chronic_diseases]
                if hasattr(patient_data, 'current_medications'):
                    self.patient_data['current_medications'] = [
                        {'name': m.medication_name, 'dosage': m.dosage, 'frequency': m.frequency}
                        for m in patient_data.current_medications if hasattr(m, 'is_active') and m.is_active
                    ]
        else:
            self.patient_data = patient_data

        
        self.patient_data = patient_data
        
        # Create emergency card content without Close button
        self.content = EmergencyCardContent(
            self, 
            patient_data, 
            show_close_button=False  # Tab doesn't need Close button
        )
        self.content.pack(fill='both', expand=True)