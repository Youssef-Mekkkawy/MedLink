"""
Link external accounts dialog
"""
import customtkinter as ctk
from tkinter import messagebox
from gui.styles import *
from core.patient_manager import patient_manager


class LinkAccountsDialog(ctk.CTkToplevel):
    """Dialog for linking external lab/imaging accounts"""
    
    def __init__(self, parent, patient_data, on_success):
        super().__init__(parent)
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
        self.on_success = on_success
        
        # Configure window
        self.title("Link External Accounts")
        self.geometry("600x700")
        self.resizable(False, False)
        
        # Center on parent
        self.transient(parent)
        self.grab_set()
        
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = parent.winfo_x() + (parent.winfo_width() // 2) - (width // 2)
        y = parent.winfo_y() + (parent.winfo_height() // 2) - (height // 2)
        self.geometry(f'{width}x{height}+{x}+{y}')
        
        self.create_ui()
    
    def create_ui(self):
        """Create link accounts UI"""
        main_frame = ctk.CTkFrame(self, fg_color=COLORS['bg_dark'])
        main_frame.pack(fill='both', expand=True, padx=30, pady=30)
        
        # Header
        header = ctk.CTkFrame(main_frame, fg_color='transparent')
        header.pack(fill='x', pady=(0, 20))
        
        icon_label = ctk.CTkLabel(
            header,
            text="🔗",
            font=('Segoe UI', 48)
        )
        icon_label.pack()
        
        title_label = ctk.CTkLabel(
            header,
            text="Link External Accounts",
            font=FONTS['heading'],
            text_color=COLORS['text_primary']
        )
        title_label.pack(pady=(10, 0))
        
        subtitle_label = ctk.CTkLabel(
            header,
            text="Connect your accounts from labs and imaging centers",
            font=FONTS['body'],
            text_color=COLORS['text_secondary']
        )
        subtitle_label.pack(pady=(5, 0))
        
        # Form card
        form_card = ctk.CTkFrame(
            main_frame,
            fg_color=COLORS['bg_medium'],
            corner_radius=RADIUS['lg']
        )
        form_card.pack(fill='both', expand=True, pady=20)
        
        form_content = ctk.CTkFrame(form_card, fg_color='transparent')
        form_content.pack(fill='both', expand=True, padx=25, pady=25)
        
        # Current links
        current_links = self.patient_data.get('external_links', {})
        
        # Lab Account Section
        lab_label = ctk.CTkLabel(
            form_content,
            text="🧪  Laboratory Account",
            font=FONTS['subheading'],
            text_color=COLORS['text_primary']
        )
        lab_label.pack(anchor='w', pady=(0, 15))
        
        # Lab provider selection
        lab_provider_label = ctk.CTkLabel(
            form_content,
            text="Select Lab Provider",
            font=FONTS['body_bold'],
            text_color=COLORS['text_primary']
        )
        lab_provider_label.pack(anchor='w', pady=(0, 5))
        
        self.lab_provider = ctk.CTkOptionMenu(
            form_content,
            values=[
                "Al Borg Medical Laboratories",
                "Bio Lab",
                "Alpha Lab",
                "Cairo Lab",
                "El Mokhtabar"
            ],
            font=FONTS['body'],
            height=40
        )
        self.lab_provider.pack(fill='x', pady=(0, 15))
        
        # Lab account ID
        lab_id_label = ctk.CTkLabel(
            form_content,
            text="Lab Account ID",
            font=FONTS['body_bold'],
            text_color=COLORS['text_primary']
        )
        lab_id_label.pack(anchor='w', pady=(0, 5))
        
        self.lab_id_entry = ctk.CTkEntry(
            form_content,
            placeholder_text="Enter your lab account ID",
            font=FONTS['body'],
            height=40
        )
        self.lab_id_entry.pack(fill='x', pady=(0, 25))
        
        # Pre-fill if exists
        if current_links.get('lab_account'):
            self.lab_id_entry.insert(0, current_links.get('lab_account'))
        
        # Divider
        ctk.CTkFrame(
            form_content,
            height=1,
            fg_color=COLORS['bg_hover']
        ).pack(fill='x', pady=20)
        
        # Imaging Account Section
        imaging_label = ctk.CTkLabel(
            form_content,
            text="📷  Imaging Center Account",
            font=FONTS['subheading'],
            text_color=COLORS['text_primary']
        )
        imaging_label.pack(anchor='w', pady=(0, 15))
        
        # Imaging provider selection
        imaging_provider_label = ctk.CTkLabel(
            form_content,
            text="Select Imaging Center",
            font=FONTS['body_bold'],
            text_color=COLORS['text_primary']
        )
        imaging_provider_label.pack(anchor='w', pady=(0, 5))
        
        self.imaging_provider = ctk.CTkOptionMenu(
            form_content,
            values=[
                "Scan Center",
                "Cairo Scan",
                "Radiology Plus",
                "Modern Imaging",
                "Al Borg Scan"
            ],
            font=FONTS['body'],
            height=40
        )
        self.imaging_provider.pack(fill='x', pady=(0, 15))
        
        # Imaging account ID
        imaging_id_label = ctk.CTkLabel(
            form_content,
            text="Imaging Account ID",
            font=FONTS['body_bold'],
            text_color=COLORS['text_primary']
        )
        imaging_id_label.pack(anchor='w', pady=(0, 5))
        
        self.imaging_id_entry = ctk.CTkEntry(
            form_content,
            placeholder_text="Enter your imaging account ID",
            font=FONTS['body'],
            height=40
        )
        self.imaging_id_entry.pack(fill='x')
        
        # Pre-fill if exists
        if current_links.get('imaging_account'):
            self.imaging_id_entry.insert(0, current_links.get('imaging_account'))
        
        # Info note
        info_frame = ctk.CTkFrame(
            main_frame,
            fg_color=COLORS['info'],
            corner_radius=RADIUS['md']
        )
        info_frame.pack(fill='x', pady=(0, 20))
        
        info_content = ctk.CTkFrame(info_frame, fg_color='transparent')
        info_content.pack(fill='x', padx=15, pady=15)
        
        info_label = ctk.CTkLabel(
            info_content,
            text="ℹ️  Your results will be automatically synced from these accounts",
            font=FONTS['small'],
            text_color='white',
            anchor='w'
        )
        info_label.pack(anchor='w')
        
        # Buttons
        btn_frame = ctk.CTkFrame(main_frame, fg_color='transparent')
        btn_frame.pack(fill='x')
        
        cancel_btn = ctk.CTkButton(
            btn_frame,
            text="Cancel",
            command=self.destroy,
            font=FONTS['body_bold'],
            height=50,
            fg_color='transparent',
            hover_color=COLORS['bg_light'],
            border_width=2,
            border_color=COLORS['danger'],
            text_color=COLORS['danger']
        )
        cancel_btn.pack(side='left', fill='x', expand=True, padx=(0, 10))
        
        save_btn = ctk.CTkButton(
            btn_frame,
            text="Link Accounts",
            command=self.handle_link,
            font=FONTS['body_bold'],
            height=50,
            fg_color=COLORS['secondary'],
            hover_color='#059669'
        )
        save_btn.pack(side='right', fill='x', expand=True, padx=(10, 0))
    
    def handle_link(self):
        """Handle linking accounts"""
        try:
            lab_id = self.lab_id_entry.get().strip()
            imaging_id = self.imaging_id_entry.get().strip()
            
            if not lab_id and not imaging_id:
                messagebox.showwarning("Input Required", "Please enter at least one account ID")
                return
            
            # Update patient data
            updated_data = self.patient_data.copy()
            
            if 'external_links' not in updated_data:
                updated_data['external_links'] = {}
            
            if lab_id:
                updated_data['external_links']['lab_account'] = lab_id
                updated_data['external_links']['lab_provider'] = self.lab_provider.get()
            
            if imaging_id:
                updated_data['external_links']['imaging_account'] = imaging_id
                updated_data['external_links']['imaging_provider'] = self.imaging_provider.get()
            
            # Save to database
            success = patient_manager.update_patient(
                self.patient_data.get('national_id'),
                updated_data
            )
            
            if success:
                messagebox.showinfo("Success", "Accounts linked successfully!")
                self.on_success()
                self.destroy()
            else:
                messagebox.showerror("Error", "Failed to link accounts")
        
        except Exception as e:
            messagebox.showerror("Error", f"Failed to link accounts: {str(e)}")