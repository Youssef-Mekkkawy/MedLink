"""
Visit card component - Display individual visit
"""
import customtkinter as ctk
from gui.styles import *
from utils.date_utils import format_date, format_datetime, time_ago


class VisitCard(ctk.CTkFrame):
    """Display single visit record as a card"""
    
    def __init__(self, parent, visit_data, on_edit=None, on_delete=None):
        super().__init__(
            parent,
            fg_color=COLORS['bg_medium'],
            corner_radius=RADIUS['lg'],
            border_width=2,
            border_color=COLORS['bg_hover']
        )
        
        self.visit_data = visit_data
        self.on_edit = on_edit
        self.on_delete = on_delete
        
        self.create_ui()
    
    def create_ui(self):
        """Create visit card UI"""
        # Main content
        content = ctk.CTkFrame(self, fg_color='transparent')
        content.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Header row
        header = ctk.CTkFrame(content, fg_color='transparent')
        header.pack(fill='x', pady=(0, 15))
        
        # Left side - Date and time
        left_header = ctk.CTkFrame(header, fg_color='transparent')
        left_header.pack(side='left', fill='x', expand=True)
        
        # Date with icon
        date_str = self.visit_data.get('date', 'N/A')
        time_str = self.visit_data.get('time', '')
        
        if time_str:
            datetime_text = format_datetime(date_str, time_str)
        else:
            datetime_text = format_date(date_str)
        
        date_label = ctk.CTkLabel(
            left_header,
            text=f"📅  {datetime_text}",
            font=FONTS['body_bold'],
            text_color=COLORS['primary'],
            anchor='w'
        )
        date_label.pack(side='left', padx=(0, 20))
        
        # Time ago
        time_ago_label = ctk.CTkLabel(
            left_header,
            text=time_ago(date_str),
            font=FONTS['small'],
            text_color=COLORS['text_muted'],
            anchor='w'
        )
        time_ago_label.pack(side='left')
        
        # Right side - Visit type badge
        visit_type = self.visit_data.get('visit_type', 'Consultation')
        type_colors = {
            'Emergency': COLORS['danger'],
            'Consultation': COLORS['primary'],
            'Follow-up': COLORS['secondary'],
            'Routine': COLORS['info']
        }
        
        badge_color = type_colors.get(visit_type, COLORS['primary'])
        
        type_badge = ctk.CTkLabel(
            header,
            text=visit_type,
            font=FONTS['small'],
            text_color='white',
            fg_color=badge_color,
            corner_radius=RADIUS['sm'],
            padx=12,
            pady=6
        )
        type_badge.pack(side='right')
        
        # Doctor and hospital info
        info_frame = ctk.CTkFrame(content, fg_color='transparent')
        info_frame.pack(fill='x', pady=(0, 15))
        
        doctor_label = ctk.CTkLabel(
            info_frame,
            text=f"👨‍⚕️  {self.visit_data.get('doctor_name', 'Unknown Doctor')}",
            font=FONTS['body'],
            text_color=COLORS['text_primary'],
            anchor='w'
        )
        doctor_label.pack(side='left', padx=(0, 30))
        
        hospital_label = ctk.CTkLabel(
            info_frame,
            text=f"🏥  {self.visit_data.get('hospital', 'N/A')}",
            font=FONTS['small'],
            text_color=COLORS['text_secondary'],
            anchor='w'
        )
        hospital_label.pack(side='left', padx=(0, 30))
        
        department_label = ctk.CTkLabel(
            info_frame,
            text=f"🏢  {self.visit_data.get('department', 'N/A')}",
            font=FONTS['small'],
            text_color=COLORS['text_secondary'],
            anchor='w'
        )
        department_label.pack(side='left')
        
        # Divider
        ctk.CTkFrame(
            content,
            height=1,
            fg_color=COLORS['bg_hover']
        ).pack(fill='x', pady=15)
        
        # Chief complaint
        complaint = self.visit_data.get('chief_complaint', '')
        if complaint:
            complaint_label = ctk.CTkLabel(
                content,
                text=f"Chief Complaint:",
                font=FONTS['body_bold'],
                text_color=COLORS['text_primary'],
                anchor='w'
            )
            complaint_label.pack(anchor='w', pady=(0, 5))
            
            complaint_text = ctk.CTkLabel(
                content,
                text=complaint,
                font=FONTS['body'],
                text_color=COLORS['text_secondary'],
                anchor='w',
                wraplength=800,
                justify='left'
            )
            complaint_text.pack(anchor='w', pady=(0, 15))
        
        # Diagnosis
        diagnosis = self.visit_data.get('diagnosis', '')
        if diagnosis:
            diagnosis_label = ctk.CTkLabel(
                content,
                text=f"Diagnosis:",
                font=FONTS['body_bold'],
                text_color=COLORS['text_primary'],
                anchor='w'
            )
            diagnosis_label.pack(anchor='w', pady=(0, 5))
            
            diagnosis_text = ctk.CTkLabel(
                content,
                text=diagnosis,
                font=FONTS['body'],
                text_color=COLORS['text_secondary'],
                anchor='w',
                wraplength=800,
                justify='left'
            )
            diagnosis_text.pack(anchor='w', pady=(0, 15))
        
        # Treatment plan
        treatment = self.visit_data.get('treatment_plan', '')
        if treatment:
            treatment_label = ctk.CTkLabel(
                content,
                text=f"Treatment Plan:",
                font=FONTS['body_bold'],
                text_color=COLORS['text_primary'],
                anchor='w'
            )
            treatment_label.pack(anchor='w', pady=(0, 5))
            
            treatment_text = ctk.CTkLabel(
                content,
                text=treatment,
                font=FONTS['body'],
                text_color=COLORS['text_secondary'],
                anchor='w',
                wraplength=800,
                justify='left'
            )
            treatment_text.pack(anchor='w', pady=(0, 15))
        
        # Prescriptions
        prescriptions = self.visit_data.get('prescriptions', [])
        if prescriptions:
            rx_label = ctk.CTkLabel(
                content,
                text=f"💊  Prescriptions:",
                font=FONTS['body_bold'],
                text_color=COLORS['text_primary'],
                anchor='w'
            )
            rx_label.pack(anchor='w', pady=(0, 8))
            
            rx_frame = ctk.CTkFrame(
                content,
                fg_color=COLORS['bg_light'],
                corner_radius=RADIUS['md']
            )
            rx_frame.pack(fill='x', pady=(0, 15))
            
            rx_content = ctk.CTkFrame(rx_frame, fg_color='transparent')
            rx_content.pack(fill='x', padx=15, pady=15)
            
            for i, med in enumerate(prescriptions, 1):
                med_text = f"{i}. {med.get('medication', 'N/A')}"
                dosage = med.get('dosage', '')
                freq = med.get('frequency', '')
                
                if dosage:
                    med_text += f" - {dosage}"
                if freq:
                    med_text += f", {freq}"
                
                med_label = ctk.CTkLabel(
                    rx_content,
                    text=med_text,
                    font=FONTS['body'],
                    text_color=COLORS['text_secondary'],
                    anchor='w'
                )
                med_label.pack(anchor='w', pady=2)
        
        # Vital signs (if present)
        vitals = self.visit_data.get('vital_signs', {})
        if vitals:
            vitals_label = ctk.CTkLabel(
                content,
                text=f"📊  Vital Signs:",
                font=FONTS['body_bold'],
                text_color=COLORS['text_primary'],
                anchor='w'
            )
            vitals_label.pack(anchor='w', pady=(0, 8))
            
            vitals_frame = ctk.CTkFrame(content, fg_color='transparent')
            vitals_frame.pack(fill='x')
            
            vitals_text = " | ".join([f"{k}: {v}" for k, v in vitals.items()])
            vitals_display = ctk.CTkLabel(
                vitals_frame,
                text=vitals_text,
                font=FONTS['small'],
                text_color=COLORS['text_secondary'],
                anchor='w'
            )
            vitals_display.pack(anchor='w')
        
        # Notes (if present)
        notes = self.visit_data.get('notes', '')
        if notes:
            notes_label = ctk.CTkLabel(
                content,
                text=f"📝  Notes:",
                font=FONTS['body_bold'],
                text_color=COLORS['text_primary'],
                anchor='w'
            )
            notes_label.pack(anchor='w', pady=(15, 5))
            
            notes_text = ctk.CTkLabel(
                content,
                text=notes,
                font=FONTS['small'],
                text_color=COLORS['text_muted'],
                anchor='w',
                wraplength=800,
                justify='left'
            )
            notes_text.pack(anchor='w')