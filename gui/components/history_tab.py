"""
Medical history tab component
"""
import customtkinter as ctk
from tkinter import messagebox
from gui.styles import *
from gui.components.visit_card import VisitCard
from core.visit_manager import visit_manager


class HistoryTab(ctk.CTkFrame):
    """Medical history timeline view"""
    
    def __init__(self, parent, patient_data, doctor_data, on_add_visit):
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
        self.doctor_data = doctor_data
        self.on_add_visit = on_add_visit
        
        self.create_ui()
        self.load_visits()
    
    def create_ui(self):
        """Create history tab UI"""
        # Header with actions
        header = ctk.CTkFrame(self, fg_color=COLORS['bg_medium'], height=80)
        header.pack(fill='x', pady=(0, 20))
        header.pack_propagate(False)
        
        header_content = ctk.CTkFrame(header, fg_color='transparent')
        header_content.pack(fill='both', expand=True, padx=20, pady=15)
        
        # Title
        title_label = ctk.CTkLabel(
            header_content,
            text="📋  Medical History",
            font=FONTS['heading'],
            text_color=COLORS['text_primary']
        )
        title_label.pack(side='left')
        
        # Add visit button
        add_btn = ctk.CTkButton(
            header_content,
            text="➕  Add New Visit",
            command=self.on_add_visit,
            font=FONTS['body_bold'],
            height=45,
            fg_color=COLORS['secondary'],
            hover_color='#059669'
        )
        add_btn.pack(side='right')
        
        # Scrollable visits container
        self.visits_scroll = ctk.CTkScrollableFrame(
            self,
            fg_color='transparent'
        )
        self.visits_scroll.pack(fill='both', expand=True)
    
    def load_visits(self):
        """Load and display visit history"""
        # Clear existing
        for widget in self.visits_scroll.winfo_children():
            widget.destroy()
        
        # Get visits
        national_id = self.patient_data.get('national_id')
        visits = visit_manager.get_patient_visits(national_id)
        
        if not visits:
            # Show empty state
            self.show_empty_state()
            return
        
        # Display visits
        for visit in visits:
            visit_card = VisitCard(self.visits_scroll, visit)
            visit_card.pack(fill='x', pady=10)
    
    def show_empty_state(self):
        """Show empty state when no visits"""
        empty_frame = ctk.CTkFrame(
            self.visits_scroll,
            fg_color=COLORS['bg_medium'],
            corner_radius=RADIUS['lg'],
            height=300
        )
        empty_frame.pack(fill='both', expand=True, pady=50)
        empty_frame.pack_propagate(False)
        
        empty_content = ctk.CTkFrame(empty_frame, fg_color='transparent')
        empty_content.place(relx=0.5, rely=0.5, anchor='center')
        
        icon_label = ctk.CTkLabel(
            empty_content,
            text="📋",
            font=('Segoe UI', 64)
        )
        icon_label.pack()
        
        text_label = ctk.CTkLabel(
            empty_content,
            text="No Medical History Yet",
            font=FONTS['heading'],
            text_color=COLORS['text_muted']
        )
        text_label.pack(pady=(10, 5))
        
        hint_label = ctk.CTkLabel(
            empty_content,
            text="Click 'Add New Visit' to record the first visit",
            font=FONTS['body'],
            text_color=COLORS['text_muted']
        )
        hint_label.pack()
    
    def refresh(self):
        """Refresh visit list"""
        self.load_visits()