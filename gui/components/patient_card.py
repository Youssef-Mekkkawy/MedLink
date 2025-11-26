"""
Patient profile card component
"""
import customtkinter as ctk
from gui.styles import *


class PatientCard(ctk.CTkFrame):
    """Display patient information card"""
    
    def __init__(self, parent, patient_data):
        super().__init__(
            parent,
            fg_color=COLORS['bg_medium'],
            corner_radius=RADIUS['lg']
        )
        
        self.patient_data = patient_data
        self.create_ui()
    
    def create_ui(self):
        """Create patient card UI"""
        if not self.patient_data:
            self.show_empty_state()
            return
        
        # Main content
        content = ctk.CTkFrame(self, fg_color='transparent')
        content.pack(fill='both', expand=True, padx=30, pady=30)
        
        # Header section
        header = ctk.CTkFrame(content, fg_color='transparent')
        header.pack(fill='x', pady=(0, 20))
        
        # Patient icon and name
        left_header = ctk.CTkFrame(header, fg_color='transparent')
        left_header.pack(side='left', fill='x', expand=True)
        
        icon_label = ctk.CTkLabel(
            left_header,
            text="👤",
            font=('Segoe UI', 48)
        )
        icon_label.pack(side='left', padx=(0, 15))
        
        name_frame = ctk.CTkFrame(left_header, fg_color='transparent')
        name_frame.pack(side='left', fill='x', expand=True)
        
        name_label = ctk.CTkLabel(
            name_frame,
            text=self.patient_data.get('full_name', 'N/A'),
            font=('Segoe UI', 24, 'bold'),
            text_color=COLORS['text_primary'],
            anchor='w'
        )
        name_label.pack(anchor='w')
        
        id_label = ctk.CTkLabel(
            name_frame,
            text=f"ID: {self.patient_data.get('national_id', 'N/A')}",
            font=FONTS['body'],
            text_color=COLORS['text_secondary'],
            anchor='w'
        )
        id_label.pack(anchor='w')
        
        # Emergency button
        emergency_btn = ctk.CTkButton(
            header,
            text="🚨 Emergency Info",
            font=FONTS['body_bold'],
            fg_color=COLORS['danger'],
            hover_color='#dc2626',
            height=40,
            width=160
        )
        emergency_btn.pack(side='right')
        
        # Divider
        ctk.CTkFrame(
            content,
            height=1,
            fg_color=COLORS['bg_hover']
        ).pack(fill='x', pady=20)
        
        # Info grid
        info_grid = ctk.CTkFrame(content, fg_color='transparent')
        info_grid.pack(fill='x', pady=(0, 20))
        
        # Row 1
        row1 = ctk.CTkFrame(info_grid, fg_color='transparent')
        row1.pack(fill='x', pady=(0, 15))
        
        self.create_info_item(row1, "🎂 Age", f"{self.patient_data.get('age', 'N/A')} years", side='left')
        self.create_info_item(row1, "⚧ Gender", self.patient_data.get('gender', 'N/A'), side='left')
        self.create_info_item(row1, "🩸 Blood Type", self.patient_data.get('blood_type', 'N/A'), side='left')
        
        # Row 2
        row2 = ctk.CTkFrame(info_grid, fg_color='transparent')
        row2.pack(fill='x', pady=(0, 15))
        
        self.create_info_item(row2, "📞 Phone", self.patient_data.get('phone', 'N/A'), side='left')
        self.create_info_item(row2, "📧 Email", self.patient_data.get('email', 'N/A'), side='left')
        
        # Medical alerts section
        alerts_frame = ctk.CTkFrame(
            content,
            fg_color=COLORS['bg_light'],
            corner_radius=RADIUS['md']
        )
        alerts_frame.pack(fill='x', pady=(10, 0))
        
        alerts_content = ctk.CTkFrame(alerts_frame, fg_color='transparent')
        alerts_content.pack(fill='x', padx=20, pady=20)
        
        # Allergies
        allergies = self.patient_data.get('allergies', [])
        if allergies:
            allergy_label = ctk.CTkLabel(
                alerts_content,
                text="⚠️  Allergies: " + ", ".join(allergies),
                font=FONTS['body_bold'],
                text_color=COLORS['warning'],
                anchor='w'
            )
            allergy_label.pack(fill='x', pady=(0, 10))
        
        # Chronic diseases
        chronic = self.patient_data.get('chronic_diseases', [])
        if chronic:
            chronic_label = ctk.CTkLabel(
                alerts_content,
                text="🏥  Chronic Conditions: " + ", ".join(chronic),
                font=FONTS['body'],
                text_color=COLORS['info'],
                anchor='w'
            )
            chronic_label.pack(fill='x')
        
        # Current medications
        meds = self.patient_data.get('current_medications', [])
        if meds:
            meds_frame = ctk.CTkFrame(alerts_content, fg_color='transparent')
            meds_frame.pack(fill='x', pady=(10, 0))
            
            meds_title = ctk.CTkLabel(
                meds_frame,
                text="💊  Current Medications:",
                font=FONTS['body_bold'],
                text_color=COLORS['text_primary'],
                anchor='w'
            )
            meds_title.pack(fill='x', pady=(0, 5))
            
            for med in meds[:3]:  # Show first 3
                med_label = ctk.CTkLabel(
                    meds_frame,
                    text=f"   • {med.get('name', 'N/A')} - {med.get('dosage', '')} {med.get('frequency', '')}",
                    font=FONTS['small'],
                    text_color=COLORS['text_secondary'],
                    anchor='w'
                )
                med_label.pack(fill='x', pady=2)
    
    def create_info_item(self, parent, label, value, side='left'):
        """Create info label-value pair"""
        container = ctk.CTkFrame(parent, fg_color='transparent')
        container.pack(side=side, padx=(0, 30))
        
        label_widget = ctk.CTkLabel(
            container,
            text=label,
            font=FONTS['small'],
            text_color=COLORS['text_muted'],
            anchor='w'
        )
        label_widget.pack(anchor='w')
        
        value_widget = ctk.CTkLabel(
            container,
            text=value,
            font=FONTS['body_bold'],
            text_color=COLORS['text_primary'],
            anchor='w'
        )
        value_widget.pack(anchor='w')
    
    def show_empty_state(self):
        """Show empty state when no patient selected"""
        content = ctk.CTkFrame(self, fg_color='transparent')
        content.pack(fill='both', expand=True)
        
        empty_label = ctk.CTkLabel(
            content,
            text="👤",
            font=('Segoe UI', 64)
        )
        empty_label.place(relx=0.5, rely=0.4, anchor='center')
        
        text_label = ctk.CTkLabel(
            content,
            text="No patient selected",
            font=FONTS['heading'],
            text_color=COLORS['text_muted']
        )
        text_label.place(relx=0.5, rely=0.55, anchor='center')
        
        hint_label = ctk.CTkLabel(
            content,
            text="Search for a patient to view their profile",
            font=FONTS['body'],
            text_color=COLORS['text_muted']
        )
        hint_label.place(relx=0.5, rely=0.62, anchor='center')