"""
Patient Card Component - FIXED FOR DATABASE
Displays patient information in a card format
Location: gui/components/patient_card.py
"""
import customtkinter as ctk
from gui.styles import *


class PatientCard(ctk.CTkFrame):
    def __init__(self, parent, patient_data, on_emergency=None):
        """
        Initialize patient card
        
        Args:
            parent: Parent widget
            patient_data: Patient object from database OR dictionary
            on_emergency: Optional callback function for emergency button
        """
        super().__init__(parent, fg_color=COLORS['bg_medium'], corner_radius=RADIUS['lg'])
        
        # Convert SQLAlchemy object to dict if needed
        if hasattr(patient_data, '__dict__') and not isinstance(patient_data, dict):
            self.patient_data = self._convert_to_dict(patient_data)
        else:
            self.patient_data = patient_data
            
        self.on_emergency = on_emergency
        
        self.create_ui()
    
    def _convert_to_dict(self, patient_obj):
        """Convert SQLAlchemy Patient object to dictionary"""
        try:
            # Try to use to_dict if available
            if hasattr(patient_obj, 'to_dict'):
                return patient_obj.to_dict()
            
            # Manual conversion
            data = {
                'national_id': patient_obj.national_id,
                'full_name': patient_obj.full_name,
                'age': patient_obj.age,
                'gender': patient_obj.gender.value if hasattr(patient_obj.gender, 'value') else str(patient_obj.gender),
                'blood_type': patient_obj.blood_type.value if hasattr(patient_obj.blood_type, 'value') else str(patient_obj.blood_type),
                'phone': patient_obj.phone or 'N/A',
                'allergies': [],
                'chronic_diseases': [],
                'current_medications': []
            }
            
            # Get allergies from relationship
            if hasattr(patient_obj, 'allergies'):
                data['allergies'] = [a.allergen_name for a in patient_obj.allergies]
            
            # Get chronic diseases from relationship
            if hasattr(patient_obj, 'chronic_diseases'):
                data['chronic_diseases'] = [cd.disease_name for cd in patient_obj.chronic_diseases]
            
            # Get current medications from relationship
            if hasattr(patient_obj, 'current_medications'):
                data['current_medications'] = [
                    {
                        'name': m.medication_name,
                        'dosage': m.dosage,
                        'frequency': m.frequency
                    }
                    for m in patient_obj.current_medications
                    if hasattr(m, 'is_active') and m.is_active
                ]
            
            return data
        except Exception as e:
            print(f"Error converting patient to dict: {e}")
            return patient_obj if isinstance(patient_obj, dict) else {}
    
    def create_ui(self):
        """Create the patient card UI"""
        # Main container with padding
        container = ctk.CTkFrame(self, fg_color='transparent')
        container.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Header section
        self.create_header(container)
        
        # Basic info section
        self.create_basic_info(container)
        
        # Medical summary section
        self.create_medical_summary(container)
    
    def create_header(self, parent):
        """Create patient header with photo and name"""
        header = ctk.CTkFrame(parent, fg_color='transparent')
        header.pack(fill='x', pady=(0, 15))
        
        # Photo placeholder
        photo_frame = ctk.CTkFrame(
            header,
            width=80,
            height=80,
            fg_color=COLORS['primary'],
            corner_radius=40
        )
        photo_frame.pack(side='left', padx=(0, 15))
        photo_frame.pack_propagate(False)
        
        # Initials in photo
        initials = self.get_initials(self.patient_data.get('full_name', 'N/A'))
        initials_label = ctk.CTkLabel(
            photo_frame,
            text=initials,
            font=('Segoe UI', 28, 'bold'),
            text_color='white'
        )
        initials_label.place(relx=0.5, rely=0.5, anchor='center')
        
        # Name and ID
        info_frame = ctk.CTkFrame(header, fg_color='transparent')
        info_frame.pack(side='left', fill='both', expand=True)
        
        # Patient name
        name_label = ctk.CTkLabel(
            info_frame,
            text=self.patient_data.get('full_name', 'Unknown Patient'),
            font=FONTS['heading'],
            text_color=COLORS['text_primary'],
            anchor='w'
        )
        name_label.pack(anchor='w')
        
        # National ID
        id_label = ctk.CTkLabel(
            info_frame,
            text=f"📋 ID: {self.patient_data.get('national_id', 'N/A')}",
            font=FONTS['body'],
            text_color=COLORS['text_secondary'],
            anchor='w'
        )
        id_label.pack(anchor='w', pady=(2, 0))
    
    def create_basic_info(self, parent):
        """Create basic patient information grid"""
        info_frame = ctk.CTkFrame(parent, fg_color=COLORS['bg_light'], corner_radius=RADIUS['md'])
        info_frame.pack(fill='x', pady=(0, 15))
        
        # Info grid
        grid = ctk.CTkFrame(info_frame, fg_color='transparent')
        grid.pack(fill='x', padx=15, pady=15)
        
        # Configure grid
        grid.grid_columnconfigure((0, 1, 2, 3), weight=1)
        
        # Info items
        info_items = [
            ("🩸 Blood Type", self.patient_data.get('blood_type', 'N/A')),
            ("🎂 Age", f"{self.patient_data.get('age', 'N/A')} years"),
            ("⚧ Gender", self.patient_data.get('gender', 'N/A')),
            ("📞 Phone", self.patient_data.get('phone', 'N/A'))
        ]
        
        for i, (label, value) in enumerate(info_items):
            self.create_info_item(grid, label, value, i // 2, i % 2 * 2)
    
    def create_info_item(self, parent, label, value, row, col):
        """Create a single info item"""
        # Label
        label_widget = ctk.CTkLabel(
            parent,
            text=label,
            font=FONTS['small'],
            text_color=COLORS['text_secondary'],
            anchor='w'
        )
        label_widget.grid(row=row, column=col, sticky='w', padx=(0, 10), pady=5)
        
        # Value
        value_widget = ctk.CTkLabel(
            parent,
            text=str(value),
            font=FONTS['body_bold'],
            text_color=COLORS['text_primary'],
            anchor='w'
        )
        value_widget.grid(row=row, column=col+1, sticky='w', pady=5)
    
    def create_medical_summary(self, parent):
        """Create medical summary section"""
        content = ctk.CTkFrame(parent, fg_color='transparent')
        content.pack(fill='x')
        
        # Allergies
        allergies = self.patient_data.get('allergies', [])
        if allergies:
            allergy_frame = ctk.CTkFrame(content, fg_color=COLORS['danger'], corner_radius=RADIUS['md'])
            allergy_frame.pack(fill='x', pady=(0, 8))
            
            allergy_text = "⚠️  ALLERGIES: " + ", ".join(allergies[:3])
            if len(allergies) > 3:
                allergy_text += f" (+{len(allergies)-3} more)"
            
            allergy_label = ctk.CTkLabel(
                allergy_frame,
                text=allergy_text,
                font=FONTS['body_bold'],
                text_color='white'
            )
            allergy_label.pack(padx=15, pady=10)
        
        # Chronic diseases
        chronic = self.patient_data.get('chronic_diseases', [])
        if chronic:
            chronic_text = "🥼 Chronic: " + ", ".join(chronic[:3])
            if len(chronic) > 3:
                chronic_text += f" (+{len(chronic)-3} more)"
            
            chronic_label = ctk.CTkLabel(
                content,
                text=chronic_text,
                font=FONTS['body'],
                text_color=COLORS['text_secondary'],
                anchor='w'
            )
            chronic_label.pack(anchor='w', pady=2)
        
        # Current medications - Handle both dict and string formats
        medications = self.patient_data.get('current_medications', [])
        if medications:
            # Extract medication names
            if medications and isinstance(medications[0], dict):
                med_names = [med.get('name', med.get('medication_name', 'Unknown')) for med in medications[:3]]
            else:
                med_names = [str(med) for med in medications[:3]]
            
            med_text = "💊 Medications: " + ", ".join(med_names)
            if len(medications) > 3:
                med_text += f" (+{len(medications)-3} more)"
            
            med_label = ctk.CTkLabel(
                content,
                text=med_text,
                font=FONTS['body'],
                text_color=COLORS['text_secondary'],
                anchor='w'
            )
            med_label.pack(anchor='w', pady=2)
    
    def get_initials(self, full_name):
        """Get initials from full name"""
        try:
            if not full_name or full_name == 'N/A':
                return "?"
            
            parts = full_name.split()
            if len(parts) >= 2:
                return (parts[0][0] + parts[1][0]).upper()
            elif len(parts) == 1:
                return parts[0][0].upper()
            else:
                return "?"
        except:
            return "?"


# For backwards compatibility
class EnhancedPatientCard(PatientCard):
    """Alias for backwards compatibility"""
    pass