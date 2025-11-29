"""
Emergency directives manager - Patient self-service for emergency settings
Location: gui/components/emergency_directives_manager.py
"""
import customtkinter as ctk
from tkinter import messagebox
from gui.styles import *
from core.data_manager import data_manager
from utils.date_utils import get_current_date, is_valid_date


class EmergencyDirectivesManager(ctk.CTkFrame):
    """Patient interface for managing emergency directives"""
    
    def __init__(self, parent, patient_data):
        super().__init__(parent, fg_color='transparent')
        
        self.patient_data = patient_data
        self.emergency_directives = patient_data.get('emergency_directives', {})
        
        self.create_ui()
        self.load_current_settings()
    
    def create_ui(self):
        """Create emergency directives UI"""
        # Header
        header = ctk.CTkFrame(self, fg_color='transparent')
        header.pack(fill='x', padx=20, pady=(20, 10))
        
        title = ctk.CTkLabel(
            header,
            text="🚨 Emergency Directives",
            font=FONTS['heading'],
            text_color=COLORS['text_primary']
        )
        title.pack(anchor='w')
        
        subtitle = ctk.CTkLabel(
            header,
            text="Manage your end-of-life care preferences and emergency instructions",
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
        
        # DNR Section
        self.create_dnr_section(scroll_frame)
        
        # Organ Donor Section
        self.create_organ_donor_section(scroll_frame)
        
        # Power of Attorney Section
        self.create_power_of_attorney_section(scroll_frame)
        
        # Religious Preferences Section
        self.create_religious_preferences_section(scroll_frame)
        
        # Advanced Directives Section
        self.create_advanced_directives_section(scroll_frame)
        
        # Save Button
        save_frame = ctk.CTkFrame(self, fg_color='transparent')
        save_frame.pack(fill='x', padx=20, pady=20)
        
        save_btn = ctk.CTkButton(
            save_frame,
            text="💾 Save Emergency Directives",
            command=self.save_directives,
            font=FONTS['body_bold'],
            height=50,
            fg_color=COLORS['secondary'],
            hover_color='#059669'
        )
        save_btn.pack(fill='x')
    
    def create_dnr_section(self, parent):
        """Create DNR section"""
        card = self.create_section_card(parent, "🚫 Do Not Resuscitate (DNR)")
        
        content = ctk.CTkFrame(card, fg_color='transparent')
        content.pack(fill='x', padx=20, pady=(0, 15))
        
        # Info box
        info_box = ctk.CTkFrame(
            content,
            fg_color=COLORS['bg_light'],
            corner_radius=RADIUS['md']
        )
        info_box.pack(fill='x', pady=(0, 15))
        
        info_label = ctk.CTkLabel(
            info_box,
            text="ℹ️ A DNR order tells medical staff not to perform CPR if your heart stops or you stop breathing.",
            font=FONTS['small'],
            text_color=COLORS['text_secondary'],
            wraplength=600,
            justify='left'
        )
        info_label.pack(padx=15, pady=12)
        
        # DNR Checkbox
        self.dnr_checkbox = ctk.CTkCheckBox(
            content,
            text="I have a Do Not Resuscitate (DNR) order",
            font=FONTS['body'],
            onvalue=True,
            offvalue=False,
            command=self.toggle_dnr_date
        )
        self.dnr_checkbox.pack(anchor='w', pady=(0, 10))
        
        # DNR Date
        date_label = ctk.CTkLabel(
            content,
            text="📅 DNR Order Date:",
            font=FONTS['body'],
            text_color=COLORS['text_secondary']
        )
        date_label.pack(anchor='w', pady=(0, 5))
        
        self.dnr_date_entry = ctk.CTkEntry(
            content,
            placeholder_text="YYYY-MM-DD",
            font=FONTS['body'],
            height=40
        )
        self.dnr_date_entry.pack(fill='x')
    
    def create_organ_donor_section(self, parent):
        """Create organ donor section"""
        card = self.create_section_card(parent, "❤️ Organ Donation")
        
        content = ctk.CTkFrame(card, fg_color='transparent')
        content.pack(fill='x', padx=20, pady=(0, 15))
        
        # Info box
        info_box = ctk.CTkFrame(
            content,
            fg_color=COLORS['bg_light'],
            corner_radius=RADIUS['md']
        )
        info_box.pack(fill='x', pady=(0, 15))
        
        info_label = ctk.CTkLabel(
            info_box,
            text="ℹ️ Organ donation can save lives. Your decision helps medical teams respect your wishes.",
            font=FONTS['small'],
            text_color=COLORS['text_secondary'],
            wraplength=600,
            justify='left'
        )
        info_label.pack(padx=15, pady=12)
        
        # Organ Donor Checkbox
        self.organ_donor_checkbox = ctk.CTkCheckBox(
            content,
            text="I wish to be an organ donor",
            font=FONTS['body'],
            onvalue=True,
            offvalue=False,
            command=self.toggle_organ_donor_fields
        )
        self.organ_donor_checkbox.pack(anchor='w', pady=(0, 10))
        
        # Donor Card Number
        card_label = ctk.CTkLabel(
            content,
            text="🆔 Organ Donor Card Number (if applicable):",
            font=FONTS['body'],
            text_color=COLORS['text_secondary']
        )
        card_label.pack(anchor='w', pady=(0, 5))
        
        self.donor_card_entry = ctk.CTkEntry(
            content,
            placeholder_text="Enter card number",
            font=FONTS['body'],
            height=40
        )
        self.donor_card_entry.pack(fill='x', pady=(0, 10))
        
        # Blood Transfusion Consent
        self.blood_transfusion_checkbox = ctk.CTkCheckBox(
            content,
            text="I consent to blood transfusions",
            font=FONTS['body'],
            onvalue=True,
            offvalue=False
        )
        self.blood_transfusion_checkbox.pack(anchor='w', pady=(0, 10))
        
        # Tissue Donation
        self.tissue_donation_checkbox = ctk.CTkCheckBox(
            content,
            text="I consent to tissue donation for research",
            font=FONTS['body'],
            onvalue=True,
            offvalue=False
        )
        self.tissue_donation_checkbox.pack(anchor='w')
    
    def create_power_of_attorney_section(self, parent):
        """Create power of attorney section"""
        card = self.create_section_card(parent, "⚖️ Power of Attorney for Healthcare")
        
        content = ctk.CTkFrame(card, fg_color='transparent')
        content.pack(fill='x', padx=20, pady=(0, 15))
        
        # Info box
        info_box = ctk.CTkFrame(
            content,
            fg_color=COLORS['bg_light'],
            corner_radius=RADIUS['md']
        )
        info_box.pack(fill='x', pady=(0, 15))
        
        info_label = ctk.CTkLabel(
            info_box,
            text="ℹ️ Designate someone to make healthcare decisions on your behalf if you're unable to do so.",
            font=FONTS['small'],
            text_color=COLORS['text_secondary'],
            wraplength=600,
            justify='left'
        )
        info_label.pack(padx=15, pady=12)
        
        # Has POA Checkbox
        self.has_poa_checkbox = ctk.CTkCheckBox(
            content,
            text="I have designated a Power of Attorney for healthcare",
            font=FONTS['body'],
            onvalue=True,
            offvalue=False,
            command=self.toggle_poa_fields
        )
        self.has_poa_checkbox.pack(anchor='w', pady=(0, 15))
        
        # POA Fields
        self.poa_frame = ctk.CTkFrame(content, fg_color='transparent')
        self.poa_frame.pack(fill='x')
        
        # Name
        name_label = ctk.CTkLabel(
            self.poa_frame,
            text="👤 Full Name:",
            font=FONTS['body'],
            text_color=COLORS['text_secondary']
        )
        name_label.pack(anchor='w', pady=(0, 5))
        
        self.poa_name_entry = ctk.CTkEntry(
            self.poa_frame,
            placeholder_text="Enter full name",
            font=FONTS['body'],
            height=40
        )
        self.poa_name_entry.pack(fill='x', pady=(0, 10))
        
        # Relation
        relation_label = ctk.CTkLabel(
            self.poa_frame,
            text="👥 Relationship:",
            font=FONTS['body'],
            text_color=COLORS['text_secondary']
        )
        relation_label.pack(anchor='w', pady=(0, 5))
        
        self.poa_relation_entry = ctk.CTkEntry(
            self.poa_frame,
            placeholder_text="e.g., Spouse, Parent, Sibling",
            font=FONTS['body'],
            height=40
        )
        self.poa_relation_entry.pack(fill='x', pady=(0, 10))
        
        # Phone
        phone_label = ctk.CTkLabel(
            self.poa_frame,
            text="📱 Phone Number:",
            font=FONTS['body'],
            text_color=COLORS['text_secondary']
        )
        phone_label.pack(anchor='w', pady=(0, 5))
        
        self.poa_phone_entry = ctk.CTkEntry(
            self.poa_frame,
            placeholder_text="+20 XXX XXX XXXX",
            font=FONTS['body'],
            height=40
        )
        self.poa_phone_entry.pack(fill='x', pady=(0, 10))
        
        # Document Date
        doc_date_label = ctk.CTkLabel(
            self.poa_frame,
            text="📅 Document Date:",
            font=FONTS['body'],
            text_color=COLORS['text_secondary']
        )
        doc_date_label.pack(anchor='w', pady=(0, 5))
        
        self.poa_date_entry = ctk.CTkEntry(
            self.poa_frame,
            placeholder_text="YYYY-MM-DD",
            font=FONTS['body'],
            height=40
        )
        self.poa_date_entry.pack(fill='x')
    
    def create_religious_preferences_section(self, parent):
        """Create religious preferences section"""
        card = self.create_section_card(parent, "🕌 Religious Preferences")
        
        content = ctk.CTkFrame(card, fg_color='transparent')
        content.pack(fill='x', padx=20, pady=(0, 15))
        
        # Religion
        religion_label = ctk.CTkLabel(
            content,
            text="Religion:",
            font=FONTS['body'],
            text_color=COLORS['text_secondary']
        )
        religion_label.pack(anchor='w', pady=(0, 5))
        
        self.religion_entry = ctk.CTkOptionMenu(
            content,
            values=["Islam", "Christianity", "Judaism", "Buddhism", "Hinduism", "Other", "None"],
            font=FONTS['body'],
            height=40
        )
        self.religion_entry.pack(fill='x', pady=(0, 15))
        
        # Special Considerations
        considerations_label = ctk.CTkLabel(
            content,
            text="Special Religious Considerations:",
            font=FONTS['body'],
            text_color=COLORS['text_secondary']
        )
        considerations_label.pack(anchor='w', pady=(0, 5))
        
        self.religious_considerations_entry = ctk.CTkTextbox(
            content,
            font=FONTS['body'],
            height=80,
            wrap='word'
        )
        self.religious_considerations_entry.pack(fill='x')
        
        placeholder_text = "e.g., Halal food only, No blood products, Prayer times, Religious items"
        self.religious_considerations_entry.insert("1.0", placeholder_text)
        self.religious_considerations_entry.bind("<FocusIn>", lambda e: self.clear_placeholder(self.religious_considerations_entry, placeholder_text))
    
    def create_advanced_directives_section(self, parent):
        """Create advanced directives section"""
        card = self.create_section_card(parent, "📄 Living Will & Advanced Directives")
        
        content = ctk.CTkFrame(card, fg_color='transparent')
        content.pack(fill='x', padx=20, pady=(0, 15))
        
        # Living Will Checkbox
        self.living_will_checkbox = ctk.CTkCheckBox(
            content,
            text="I have a living will or advanced directive on file",
            font=FONTS['body'],
            onvalue=True,
            offvalue=False
        )
        self.living_will_checkbox.pack(anchor='w', pady=(0, 15))
        
        # Additional Instructions
        instructions_label = ctk.CTkLabel(
            content,
            text="Additional End-of-Life Care Instructions:",
            font=FONTS['body'],
            text_color=COLORS['text_secondary']
        )
        instructions_label.pack(anchor='w', pady=(0, 5))
        
        self.additional_instructions_entry = ctk.CTkTextbox(
            content,
            font=FONTS['body'],
            height=100,
            wrap='word'
        )
        self.additional_instructions_entry.pack(fill='x')
    
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
    
    def toggle_dnr_date(self):
        """Enable/disable DNR date field"""
        state = 'normal' if self.dnr_checkbox.get() else 'disabled'
        self.dnr_date_entry.configure(state=state)
    
    def toggle_organ_donor_fields(self):
        """Enable/disable organ donor fields"""
        state = 'normal' if self.organ_donor_checkbox.get() else 'disabled'
        self.donor_card_entry.configure(state=state)
    
    def toggle_poa_fields(self):
        """Enable/disable POA fields"""
        state = 'normal' if self.has_poa_checkbox.get() else 'disabled'
        
        for widget in self.poa_frame.winfo_children():
            if isinstance(widget, ctk.CTkEntry):
                widget.configure(state=state)
    
    def clear_placeholder(self, textbox, placeholder):
        """Clear placeholder text on focus"""
        if textbox.get("1.0", "end-1c") == placeholder:
            textbox.delete("1.0", "end")
    
    def load_current_settings(self):
        """Load current emergency directives settings"""
        # DNR
        if self.emergency_directives.get('dnr_status'):
            self.dnr_checkbox.select()
            if self.emergency_directives.get('dnr_date'):
                self.dnr_date_entry.insert(0, self.emergency_directives['dnr_date'])
        
        self.toggle_dnr_date()
        
        # Organ Donor
        if self.emergency_directives.get('organ_donor'):
            self.organ_donor_checkbox.select()
            if self.emergency_directives.get('organ_donor_card_number'):
                self.donor_card_entry.insert(0, self.emergency_directives['organ_donor_card_number'])
        
        self.toggle_organ_donor_fields()
        
        # Blood Transfusion
        if self.emergency_directives.get('blood_transfusion_consent'):
            self.blood_transfusion_checkbox.select()
        
        # Tissue Donation
        if self.emergency_directives.get('tissue_donation'):
            self.tissue_donation_checkbox.select()
        
        # Power of Attorney
        poa = self.emergency_directives.get('power_of_attorney', {})
        if poa.get('has_poa'):
            self.has_poa_checkbox.select()
            if poa.get('name'):
                self.poa_name_entry.insert(0, poa['name'])
            if poa.get('relation'):
                self.poa_relation_entry.insert(0, poa['relation'])
            if poa.get('phone'):
                self.poa_phone_entry.insert(0, poa['phone'])
            if poa.get('document_date'):
                self.poa_date_entry.insert(0, poa['document_date'])
        
        self.toggle_poa_fields()
        
        # Religious Preferences
        religious = self.emergency_directives.get('religious_preferences', {})
        if religious.get('religion'):
            self.religion_entry.set(religious['religion'])
        if religious.get('special_considerations'):
            self.religious_considerations_entry.delete("1.0", "end")
            self.religious_considerations_entry.insert("1.0", religious['special_considerations'])
        
        # Living Will
        if self.emergency_directives.get('living_will'):
            self.living_will_checkbox.select()
    
    def save_directives(self):
        """Save emergency directives"""
        try:
            # Build directives data
            directives = {}
            
            # DNR
            directives['dnr_status'] = self.dnr_checkbox.get()
            if directives['dnr_status']:
                dnr_date = self.dnr_date_entry.get().strip()
                if dnr_date and not is_valid_date(dnr_date):
                    messagebox.showerror("Invalid Date", "DNR date must be in YYYY-MM-DD format")
                    return
                directives['dnr_date'] = dnr_date if dnr_date else None
            
            # Organ Donor
            directives['organ_donor'] = self.organ_donor_checkbox.get()
            if directives['organ_donor']:
                directives['organ_donor_card_number'] = self.donor_card_entry.get().strip() or None
            
            directives['blood_transfusion_consent'] = self.blood_transfusion_checkbox.get()
            directives['tissue_donation'] = self.tissue_donation_checkbox.get()
            
            # Power of Attorney
            poa_data = {
                'has_poa': self.has_poa_checkbox.get()
            }
            
            if poa_data['has_poa']:
                poa_data['name'] = self.poa_name_entry.get().strip() or None
                poa_data['relation'] = self.poa_relation_entry.get().strip() or None
                poa_data['phone'] = self.poa_phone_entry.get().strip() or None
                
                poa_date = self.poa_date_entry.get().strip()
                if poa_date and not is_valid_date(poa_date):
                    messagebox.showerror("Invalid Date", "POA document date must be in YYYY-MM-DD format")
                    return
                poa_data['document_date'] = poa_date if poa_date else None
            
            directives['power_of_attorney'] = poa_data
            
            # Religious Preferences
            religious_considerations = self.religious_considerations_entry.get("1.0", "end-1c").strip()
            placeholder = "e.g., Halal food only, No blood products, Prayer times, Religious items"
            if religious_considerations == placeholder:
                religious_considerations = None
            
            directives['religious_preferences'] = {
                'religion': self.religion_entry.get(),
                'special_considerations': religious_considerations
            }
            
            # Living Will
            directives['living_will'] = self.living_will_checkbox.get()
            
            # Update patient data
            self.patient_data['emergency_directives'] = directives
            
            # Save to database
            success = data_manager.update_item(
                'patients',
                'patients',
                self.patient_data.get('national_id'),
                'national_id',
                self.patient_data
            )
            
            if success:
                messagebox.showinfo("Success", "Emergency directives saved successfully!")
            else:
                messagebox.showerror("Error", "Failed to save emergency directives")
        
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save directives: {str(e)}")