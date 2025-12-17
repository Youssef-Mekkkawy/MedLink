"""
Lifestyle manager - Patient self-reporting for lifestyle factors
Location: gui/components/lifestyle_manager.py
"""
import customtkinter as ctk
from tkinter import messagebox
from gui.styles import *
from core.data_manager import data_manager


class LifestyleManager(ctk.CTkFrame):
    """Patient interface for managing lifestyle information"""
    
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
        self.lifestyle = patient_data.get('lifestyle', {})
        
        self.create_ui()
        self.load_current_settings()
    
    def create_ui(self):
        """Create lifestyle manager UI"""
        # Header
        header = ctk.CTkFrame(self, fg_color='transparent')
        header.pack(fill='x', padx=20, pady=(20, 10))
        
        title = ctk.CTkLabel(
            header,
            text="🏃 Lifestyle & Health Habits",
            font=FONTS['heading'],
            text_color=COLORS['text_primary']
        )
        title.pack(anchor='w')
        
        subtitle = ctk.CTkLabel(
            header,
            text="Track your daily habits and lifestyle factors that affect your health",
            font=FONTS['body'],
            text_color=COLORS['text_secondary']
        )
        subtitle.pack(anchor='w', pady=(5, 0))
        
        # Scrollable content
        scroll_frame = ctk.CTkScrollableFrame(
            self,
            fg_color='transparent'
        )
        scroll_frame.pack(fill='both', expand=True, padx=20, pady=10)
        
        # Smoking Section
        self.create_smoking_section(scroll_frame)
        
        # Alcohol Section
        self.create_alcohol_section(scroll_frame)
        
        # Exercise Section
        self.create_exercise_section(scroll_frame)
        
        # Diet Section
        self.create_diet_section(scroll_frame)
        
        # Occupation Section
        self.create_occupation_section(scroll_frame)
        
        # Sleep Section
        self.create_sleep_section(scroll_frame)
        
        # Stress Section
        self.create_stress_section(scroll_frame)
        
        # Save Button
        save_frame = ctk.CTkFrame(self, fg_color='transparent')
        save_frame.pack(fill='x', padx=20, pady=20)
        
        save_btn = ctk.CTkButton(
            save_frame,
            text="💾 Save Lifestyle Information",
            command=self.save_lifestyle,
            font=FONTS['body_bold'],
            height=50,
            fg_color=COLORS['secondary'],
            hover_color='#059669'
        )
        save_btn.pack(fill='x')
    
    def create_smoking_section(self, parent):
        """Create smoking section"""
        card = self.create_section_card(parent, "🚬 Smoking")
        
        content = ctk.CTkFrame(card, fg_color='transparent')
        content.pack(fill='x', padx=20, pady=(0, 15))
        
        # Smoking Status
        status_label = ctk.CTkLabel(
            content,
            text="Smoking Status:",
            font=FONTS['body'],
            text_color=COLORS['text_secondary']
        )
        status_label.pack(anchor='w', pady=(0, 5))
        
        self.smoking_status = ctk.CTkOptionMenu(
            content,
            values=["Never", "Former", "Current", "Occasional"],
            font=FONTS['body'],
            height=40
        )
        self.smoking_status.pack(fill='x')
    
    def create_alcohol_section(self, parent):
        """Create alcohol section"""
        card = self.create_section_card(parent, "🍷 Alcohol Consumption")
        
        content = ctk.CTkFrame(card, fg_color='transparent')
        content.pack(fill='x', padx=20, pady=(0, 15))
        
        # Alcohol Consumption
        consumption_label = ctk.CTkLabel(
            content,
            text="Alcohol Consumption:",
            font=FONTS['body'],
            text_color=COLORS['text_secondary']
        )
        consumption_label.pack(anchor='w', pady=(0, 5))
        
        self.alcohol_consumption = ctk.CTkOptionMenu(
            content,
            values=["None", "Occasional", "Moderate", "Heavy"],
            font=FONTS['body'],
            height=40
        )
        self.alcohol_consumption.pack(fill='x')
    
    def create_exercise_section(self, parent):
        """Create exercise section"""
        card = self.create_section_card(parent, "🏃 Physical Activity")
        
        content = ctk.CTkFrame(card, fg_color='transparent')
        content.pack(fill='x', padx=20, pady=(0, 15))
        
        # Exercise Frequency
        freq_label = ctk.CTkLabel(
            content,
            text="Exercise Frequency:",
            font=FONTS['body'],
            text_color=COLORS['text_secondary']
        )
        freq_label.pack(anchor='w', pady=(0, 5))
        
        self.exercise_frequency = ctk.CTkOptionMenu(
            content,
            values=["Sedentary", "1-2 times/week", "3-4 times/week", "5+ times/week", "Daily"],
            font=FONTS['body'],
            height=40
        )
        self.exercise_frequency.pack(fill='x', pady=(0, 15))
        
        # Exercise Type
        type_label = ctk.CTkLabel(
            content,
            text="Primary Exercise Type:",
            font=FONTS['body'],
            text_color=COLORS['text_secondary']
        )
        type_label.pack(anchor='w', pady=(0, 5))
        
        self.exercise_type = ctk.CTkEntry(
            content,
            placeholder_text="e.g., Walking, Gym, Swimming, Yoga",
            font=FONTS['body'],
            height=40
        )
        self.exercise_type.pack(fill='x')
    
    def create_diet_section(self, parent):
        """Create diet section"""
        card = self.create_section_card(parent, "🥗 Diet & Nutrition")
        
        content = ctk.CTkFrame(card, fg_color='transparent')
        content.pack(fill='x', padx=20, pady=(0, 15))
        
        # Diet Type
        type_label = ctk.CTkLabel(
            content,
            text="Diet Type:",
            font=FONTS['body'],
            text_color=COLORS['text_secondary']
        )
        type_label.pack(anchor='w', pady=(0, 5))
        
        self.diet_type = ctk.CTkOptionMenu(
            content,
            values=[
                "Regular",
                "Vegetarian",
                "Vegan",
                "Halal",
                "Kosher",
                "Low-carb",
                "Mediterranean",
                "Diabetic",
                "Other"
            ],
            font=FONTS['body'],
            height=40
        )
        self.diet_type.pack(fill='x', pady=(0, 15))
        
        # Dietary Restrictions
        restrictions_label = ctk.CTkLabel(
            content,
            text="Dietary Restrictions (comma-separated):",
            font=FONTS['body'],
            text_color=COLORS['text_secondary']
        )
        restrictions_label.pack(anchor='w', pady=(0, 5))
        
        self.dietary_restrictions = ctk.CTkEntry(
            content,
            placeholder_text="e.g., Gluten-free, Lactose-free, No pork",
            font=FONTS['body'],
            height=40
        )
        self.dietary_restrictions.pack(fill='x')
    
    def create_occupation_section(self, parent):
        """Create occupation section"""
        card = self.create_section_card(parent, "💼 Occupation")
        
        content = ctk.CTkFrame(card, fg_color='transparent')
        content.pack(fill='x', padx=20, pady=(0, 15))
        
        # Occupation
        occupation_label = ctk.CTkLabel(
            content,
            text="Current Occupation:",
            font=FONTS['body'],
            text_color=COLORS['text_secondary']
        )
        occupation_label.pack(anchor='w', pady=(0, 5))
        
        self.occupation = ctk.CTkEntry(
            content,
            placeholder_text="e.g., Software Engineer, Teacher, Retired",
            font=FONTS['body'],
            height=40
        )
        self.occupation.pack(fill='x', pady=(0, 15))
        
        # Occupation Hazards
        hazards_label = ctk.CTkLabel(
            content,
            text="Occupational Hazards (comma-separated):",
            font=FONTS['body'],
            text_color=COLORS['text_secondary']
        )
        hazards_label.pack(anchor='w', pady=(0, 5))
        
        self.occupation_hazards = ctk.CTkEntry(
            content,
            placeholder_text="e.g., Heavy lifting, Chemical exposure, Repetitive motion",
            font=FONTS['body'],
            height=40
        )
        self.occupation_hazards.pack(fill='x')
    
    def create_sleep_section(self, parent):
        """Create sleep section"""
        card = self.create_section_card(parent, "😴 Sleep")
        
        content = ctk.CTkFrame(card, fg_color='transparent')
        content.pack(fill='x', padx=20, pady=(0, 15))
        
        # Sleep Hours
        sleep_label = ctk.CTkLabel(
            content,
            text="Average Hours of Sleep per Night:",
            font=FONTS['body'],
            text_color=COLORS['text_secondary']
        )
        sleep_label.pack(anchor='w', pady=(0, 5))
        
        # Sleep slider
        slider_frame = ctk.CTkFrame(content, fg_color='transparent')
        slider_frame.pack(fill='x')
        
        self.sleep_hours = ctk.CTkSlider(
            slider_frame,
            from_=0,
            to=24,
            number_of_steps=24,
            command=self.update_sleep_label
        )
        self.sleep_hours.pack(side='left', fill='x', expand=True, padx=(0, 15))
        self.sleep_hours.set(7)
        
        self.sleep_label = ctk.CTkLabel(
            slider_frame,
            text="7 hours",
            font=FONTS['body_bold'],
            text_color=COLORS['text_primary'],
            width=80
        )
        self.sleep_label.pack(side='right')
    
    def create_stress_section(self, parent):
        """Create stress section"""
        card = self.create_section_card(parent, "😰 Stress Level")
        
        content = ctk.CTkFrame(card, fg_color='transparent')
        content.pack(fill='x', padx=20, pady=(0, 15))
        
        # Stress Level
        stress_label = ctk.CTkLabel(
            content,
            text="Overall Stress Level:",
            font=FONTS['body'],
            text_color=COLORS['text_secondary']
        )
        stress_label.pack(anchor='w', pady=(0, 5))
        
        self.stress_level = ctk.CTkOptionMenu(
            content,
            values=["Low", "Moderate", "Moderate to High", "High", "Very High"],
            font=FONTS['body'],
            height=40
        )
        self.stress_level.pack(fill='x')
    
    def create_section_card(self, parent, title):
        """Create section card with title"""
        card = ctk.CTkFrame(
            parent,
            fg_color=COLORS['bg_medium'],
            corner_radius=RADIUS['lg']
        )
        card.pack(fill='x', pady=(0, 15))
        
        title_label = ctk.CTkLabel(
            card,
            text=title,
            font=FONTS['subheading'],
            text_color=COLORS['text_primary']
        )
        title_label.pack(anchor='w', padx=20, pady=(15, 10))
        
        return card
    
    def update_sleep_label(self, value):
        """Update sleep hours label"""
        hours = int(value)
        self.sleep_label.configure(text=f"{hours} hour{'s' if hours != 1 else ''}")
    
    def load_current_settings(self):
        """Load current lifestyle settings"""
        # Smoking
        if self.lifestyle.get('smoking_status'):
            self.smoking_status.set(self.lifestyle['smoking_status'])
        
        # Alcohol
        if self.lifestyle.get('alcohol_consumption'):
            self.alcohol_consumption.set(self.lifestyle['alcohol_consumption'])
        
        # Exercise
        if self.lifestyle.get('exercise_frequency'):
            self.exercise_frequency.set(self.lifestyle['exercise_frequency'])
        if self.lifestyle.get('exercise_type'):
            self.exercise_type.insert(0, self.lifestyle['exercise_type'])
        
        # Diet
        if self.lifestyle.get('diet_type'):
            self.diet_type.set(self.lifestyle['diet_type'])
        if self.lifestyle.get('dietary_restrictions'):
            self.dietary_restrictions.insert(0, ', '.join(self.lifestyle['dietary_restrictions']))
        
        # Occupation
        if self.lifestyle.get('occupation'):
            self.occupation.insert(0, self.lifestyle['occupation'])
        if self.lifestyle.get('occupation_hazards'):
            self.occupation_hazards.insert(0, ', '.join(self.lifestyle['occupation_hazards']))
        
        # Sleep
        if self.lifestyle.get('sleep_hours') is not None:
            self.sleep_hours.set(self.lifestyle['sleep_hours'])
            self.update_sleep_label(self.lifestyle['sleep_hours'])
        
        # Stress
        if self.lifestyle.get('stress_level'):
            self.stress_level.set(self.lifestyle['stress_level'])
    
    def save_lifestyle(self):
        """Save lifestyle information"""
        try:
            # Build lifestyle data
            lifestyle_data = {}
            
            # Smoking
            lifestyle_data['smoking_status'] = self.smoking_status.get()
            
            # Alcohol
            lifestyle_data['alcohol_consumption'] = self.alcohol_consumption.get()
            
            # Exercise
            lifestyle_data['exercise_frequency'] = self.exercise_frequency.get()
            exercise_type = self.exercise_type.get().strip()
            lifestyle_data['exercise_type'] = exercise_type if exercise_type else None
            
            # Diet
            lifestyle_data['diet_type'] = self.diet_type.get()
            
            restrictions_text = self.dietary_restrictions.get().strip()
            if restrictions_text:
                lifestyle_data['dietary_restrictions'] = [r.strip() for r in restrictions_text.split(',') if r.strip()]
            else:
                lifestyle_data['dietary_restrictions'] = []
            
            # Occupation
            occupation = self.occupation.get().strip()
            lifestyle_data['occupation'] = occupation if occupation else None
            
            hazards_text = self.occupation_hazards.get().strip()
            if hazards_text:
                lifestyle_data['occupation_hazards'] = [h.strip() for h in hazards_text.split(',') if h.strip()]
            else:
                lifestyle_data['occupation_hazards'] = []
            
            # Sleep
            lifestyle_data['sleep_hours'] = int(self.sleep_hours.get())
            
            # Stress
            lifestyle_data['stress_level'] = self.stress_level.get()
            
            # Update patient data
            self.patient_data['lifestyle'] = lifestyle_data
            
            # Save to database
            success = data_manager.update_item(
                'patients',
                'patients',
                self.patient_data.get('national_id'),
                'national_id',
                self.patient_data
            )
            
            if success:
                messagebox.showinfo("Success", "Lifestyle information saved successfully!")
            else:
                messagebox.showerror("Error", "Failed to save lifestyle information")
        
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save lifestyle: {str(e)}")