"""
Medical timeline - Chronological view of all medical events
Location: gui/components/medical_timeline.py
"""
import customtkinter as ctk
from gui.styles import *
from core.surgery_manager import surgery_manager
from core.hospitalization_manager import hospitalization_manager
from datetime import datetime


class MedicalTimeline(ctk.CTkFrame):
    """Timeline view of all medical events"""
    
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
        self.create_ui()
    
    def create_ui(self):
        """Create timeline UI"""
        # Scrollable timeline
        self.timeline_scroll = ctk.CTkScrollableFrame(
            self,
            fg_color='transparent'
        )
        self.timeline_scroll.pack(fill='both', expand=True)
        
        self.load_timeline()
    
    def load_timeline(self):
        """Load and display all medical events in chronological order"""
        # Clear existing
        for widget in self.timeline_scroll.winfo_children():
            widget.destroy()
        
        # Collect all events
        events = []
        national_id = self.patient_data.get('national_id')
        
        # Add surgeries
        surgeries = surgery_manager.get_patient_surgeries(national_id)
        for surgery in surgeries:
            events.append({
                'type': 'surgery',
                'date': surgery.get('date', ''),
                'data': surgery
            })
        
        # Add hospitalizations
        hospitalizations = hospitalization_manager.get_patient_hospitalizations(national_id)
        for hosp in hospitalizations:
            events.append({
                'type': 'hospitalization',
                'date': hosp.get('admission_date', ''),
                'data': hosp
            })
        
        # Sort by date (newest first)
        events.sort(key=lambda x: x['date'], reverse=True)
        
        if not events:
            no_data = ctk.CTkLabel(
                self.timeline_scroll,
                text="No medical events recorded",
                font=FONTS['body'],
                text_color=COLORS['text_secondary']
            )
            no_data.pack(pady=50)
            return
        
        # Display events
        for event in events:
            if event['type'] == 'surgery':
                self.create_surgery_event(event['data'])
            elif event['type'] == 'hospitalization':
                self.create_hospitalization_event(event['data'])
    
    def create_surgery_event(self, surgery):
        """Create timeline event for surgery"""
        # Event container
        event_frame = ctk.CTkFrame(
            self.timeline_scroll,
            fg_color='transparent'
        )
        event_frame.pack(fill='x', pady=10)
        
        # Timeline dot and line
        timeline_col = ctk.CTkFrame(event_frame, fg_color='transparent', width=40)
        timeline_col.pack(side='left', fill='y', padx=(0, 15))
        timeline_col.pack_propagate(False)
        
        # Dot
        dot = ctk.CTkFrame(
            timeline_col,
            width=16,
            height=16,
            fg_color=COLORS['secondary'],
            corner_radius=RADIUS['full']
        )
        dot.pack(pady=(5, 0))
        
        # Line
        line = ctk.CTkFrame(
            timeline_col,
            width=2,
            fg_color=COLORS['bg_light']
        )
        line.pack(fill='y', expand=True, pady=(5, 0))
        
        # Event card
        card = ctk.CTkFrame(
            event_frame,
            fg_color=COLORS['bg_medium'],
            corner_radius=RADIUS['md']
        )
        card.pack(side='left', fill='both', expand=True)
        
        content = ctk.CTkFrame(card, fg_color='transparent')
        content.pack(fill='both', padx=15, pady=12)
        
        # Date badge
        date_badge = ctk.CTkFrame(
            content,
            fg_color=COLORS['secondary'],
            corner_radius=RADIUS['sm']
        )
        date_badge.pack(anchor='w', pady=(0, 8))
        
        date_label = ctk.CTkLabel(
            date_badge,
            text=f"🏥 {surgery.get('date', 'N/A')}",
            font=FONTS['small_bold'],
            text_color='white'
        )
        date_label.pack(padx=10, pady=4)
        
        # Surgery title
        title = ctk.CTkLabel(
            content,
            text=f"Surgery: {surgery.get('procedure', 'Unknown')}",
            font=FONTS['body_bold'],
            text_color=COLORS['text_primary']
        )
        title.pack(anchor='w')
        
        # Details
        details = f"🏥 {surgery.get('hospital', 'N/A')} • 👨‍⚕️ {surgery.get('surgeon', 'N/A')}"
        details_label = ctk.CTkLabel(
            content,
            text=details,
            font=FONTS['small'],
            text_color=COLORS['text_secondary']
        )
        details_label.pack(anchor='w', pady=(5, 0))
        
        # Complications if any
        if surgery.get('complications') and surgery['complications'] != 'None':
            comp_label = ctk.CTkLabel(
                content,
                text=f"⚠️ Complications: {surgery['complications']}",
                font=FONTS['small'],
                text_color=COLORS['warning']
            )
            comp_label.pack(anchor='w', pady=(5, 0))
        
        # Recovery
        if surgery.get('recovery_time'):
            recovery_label = ctk.CTkLabel(
                content,
                text=f"⏱️ Recovery: {surgery['recovery_time']}",
                font=FONTS['small'],
                text_color=COLORS['text_secondary']
            )
            recovery_label.pack(anchor='w', pady=(3, 0))
    
    def create_hospitalization_event(self, hosp):
        """Create timeline event for hospitalization"""
        # Event container
        event_frame = ctk.CTkFrame(
            self.timeline_scroll,
            fg_color='transparent'
        )
        event_frame.pack(fill='x', pady=10)
        
        # Timeline dot and line
        timeline_col = ctk.CTkFrame(event_frame, fg_color='transparent', width=40)
        timeline_col.pack(side='left', fill='y', padx=(0, 15))
        timeline_col.pack_propagate(False)
        
        # Dot
        dot = ctk.CTkFrame(
            timeline_col,
            width=16,
            height=16,
            fg_color=COLORS['danger'],
            corner_radius=RADIUS['full']
        )
        dot.pack(pady=(5, 0))
        
        # Line
        line = ctk.CTkFrame(
            timeline_col,
            width=2,
            fg_color=COLORS['bg_light']
        )
        line.pack(fill='y', expand=True, pady=(5, 0))
        
        # Event card
        card = ctk.CTkFrame(
            event_frame,
            fg_color=COLORS['bg_medium'],
            corner_radius=RADIUS['md']
        )
        card.pack(side='left', fill='both', expand=True)
        
        content = ctk.CTkFrame(card, fg_color='transparent')
        content.pack(fill='both', padx=15, pady=12)
        
        # Calculate length of stay
        los = hospitalization_manager.calculate_length_of_stay(hosp)
        los_text = f" ({los} days)" if los else ""
        
        # Date badge
        date_badge = ctk.CTkFrame(
            content,
            fg_color=COLORS['danger'],
            corner_radius=RADIUS['sm']
        )
        date_badge.pack(anchor='w', pady=(0, 8))
        
        date_text = f"🏥 {hosp.get('admission_date', 'N/A')} → {hosp.get('discharge_date', 'N/A')}{los_text}"
        date_label = ctk.CTkLabel(
            date_badge,
            text=date_text,
            font=FONTS['small_bold'],
            text_color='white'
        )
        date_label.pack(padx=10, pady=4)
        
        # Hospitalization title
        title = ctk.CTkLabel(
            content,
            text=f"Hospitalization: {hosp.get('reason', 'Unknown')}",
            font=FONTS['body_bold'],
            text_color=COLORS['text_primary']
        )
        title.pack(anchor='w')
        
        # Hospital and department
        location = f"🏥 {hosp.get('hospital', 'N/A')}"
        if hosp.get('department'):
            location += f" - {hosp['department']}"
        
        location_label = ctk.CTkLabel(
            content,
            text=location,
            font=FONTS['small'],
            text_color=COLORS['text_secondary']
        )
        location_label.pack(anchor='w', pady=(5, 0))
        
        # Diagnosis
        if hosp.get('diagnosis'):
            diag_label = ctk.CTkLabel(
                content,
                text=f"🔬 {hosp['diagnosis']}",
                font=FONTS['small'],
                text_color=COLORS['text_secondary'],
                wraplength=600
            )
            diag_label.pack(anchor='w', pady=(3, 0))
        
        # Outcome
        outcome = hosp.get('outcome', 'Unknown')
        outcome_color = COLORS['success'] if outcome == 'Recovered' else COLORS['text_secondary']
        
        outcome_label = ctk.CTkLabel(
            content,
            text=f"📊 Outcome: {outcome}",
            font=FONTS['small'],
            text_color=outcome_color
        )
        outcome_label.pack(anchor='w', pady=(3, 0))
    
    def refresh(self):
        """Refresh timeline"""
        self.load_timeline()