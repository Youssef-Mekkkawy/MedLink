"""
Add visit dialog
"""
import customtkinter as ctk
from tkinter import messagebox
from gui.styles import *
from core.visit_manager import visit_manager
from utils.date_utils import get_current_date, get_current_time, is_valid_date


class AddVisitDialog(ctk.CTkToplevel):
    """Dialog for adding new visit"""
    
    def __init__(self, parent, patient_data, doctor_data, on_success):
        super().__init__(parent)
        
        self.patient_data = patient_data
        self.doctor_data = doctor_data
        self.on_success = on_success
        
        # Configure window
        self.title("Add New Visit")
        self.geometry("700x800")
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
        """Create add visit form"""
        # Main container
        main_frame = ctk.CTkFrame(self, fg_color=COLORS['bg_dark'])
        main_frame.pack(fill='both', expand=True, padx=30, pady=30)
        
        # Header
        header = ctk.CTkFrame(main_frame, fg_color='transparent')
        header.pack(fill='x', pady=(0, 20))
        
        title_label = ctk.CTkLabel(
            header,
            text="📋  New Visit Record",
            font=FONTS['heading'],
            text_color=COLORS['text_primary']
        )
        title_label.pack(anchor='w')
        
        patient_label = ctk.CTkLabel(
            header,
            text=f"Patient: {self.patient_data.get('full_name', 'N/A')}",
            font=FONTS['body'],
            text_color=COLORS['text_secondary']
        )
        patient_label.pack(anchor='w', pady=(5, 0))
        
        # Scrollable form
        form_scroll = ctk.CTkScrollableFrame(
            main_frame,
            fg_color=COLORS['bg_medium'],
            corner_radius=RADIUS['lg']
        )
        form_scroll.pack(fill='both', expand=True)
        
        form_content = ctk.CTkFrame(form_scroll, fg_color='transparent')
        form_content.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Date and Time
        datetime_frame = ctk.CTkFrame(form_content, fg_color='transparent')
        datetime_frame.pack(fill='x', pady=(0, 15))
        
        # Date
        date_container = ctk.CTkFrame(datetime_frame, fg_color='transparent')
        date_container.pack(side='left', fill='x', expand=True, padx=(0, 10))
        
        date_label = ctk.CTkLabel(
            date_container,
            text="📅  Date *",
            font=FONTS['body_bold'],
            text_color=COLORS['text_primary']
        )
        date_label.pack(anchor='w', pady=(0, 5))
        
        self.date_entry = ctk.CTkEntry(
            date_container,
            placeholder_text="YYYY-MM-DD",
            font=FONTS['body'],
            height=40
        )
        self.date_entry.pack(fill='x')
        self.date_entry.insert(0, get_current_date())
        
        # Time
        time_container = ctk.CTkFrame(datetime_frame, fg_color='transparent')
        time_container.pack(side='left', fill='x', expand=True, padx=(10, 0))
        
        time_label = ctk.CTkLabel(
            time_container,
            text="🕐  Time *",
            font=FONTS['body_bold'],
            text_color=COLORS['text_primary']
        )
        time_label.pack(anchor='w', pady=(0, 5))
        
        self.time_entry = ctk.CTkEntry(
            time_container,
            placeholder_text="HH:MM",
            font=FONTS['body'],
            height=40
        )
        self.time_entry.pack(fill='x')
        self.time_entry.insert(0, get_current_time())
        
        # Visit Type
        type_label = ctk.CTkLabel(
            form_content,
            text="🏥  Visit Type *",
            font=FONTS['body_bold'],
            text_color=COLORS['text_primary']
        )
        type_label.pack(anchor='w', pady=(0, 5))
        
        self.visit_type = ctk.CTkOptionMenu(
            form_content,
            values=["Consultation", "Follow-up", "Emergency", "Routine"],
            font=FONTS['body'],
            height=40
        )
        self.visit_type.pack(fill='x', pady=(0, 15))
        
        # Department
        dept_label = ctk.CTkLabel(
            form_content,
            text="🏢  Department",
            font=FONTS['body_bold'],
            text_color=COLORS['text_primary']
        )
        dept_label.pack(anchor='w', pady=(0, 5))
        
        self.dept_entry = ctk.CTkEntry(
            form_content,
            placeholder_text="Enter department",
            font=FONTS['body'],
            height=40
        )
        self.dept_entry.pack(fill='x', pady=(0, 15))
        self.dept_entry.insert(0, self.doctor_data.get('specialization', ''))
        
        # Chief Complaint
        complaint_label = ctk.CTkLabel(
            form_content,
            text="🗣️  Chief Complaint *",
            font=FONTS['body_bold'],
            text_color=COLORS['text_primary']
        )
        complaint_label.pack(anchor='w', pady=(0, 5))
        
        self.complaint_entry = ctk.CTkTextbox(
            form_content,
            font=FONTS['body'],
            height=80,
            wrap='word'
        )
        self.complaint_entry.pack(fill='x', pady=(0, 15))
        
        # Diagnosis
        diagnosis_label = ctk.CTkLabel(
            form_content,
            text="🔬  Diagnosis *",
            font=FONTS['body_bold'],
            text_color=COLORS['text_primary']
        )
        diagnosis_label.pack(anchor='w', pady=(0, 5))
        
        self.diagnosis_entry = ctk.CTkTextbox(
            form_content,
            font=FONTS['body'],
            height=80,
            wrap='word'
        )
        self.diagnosis_entry.pack(fill='x', pady=(0, 15))
        
        # Treatment Plan
        treatment_label = ctk.CTkLabel(
            form_content,
            text="💊  Treatment Plan *",
            font=FONTS['body_bold'],
            text_color=COLORS['text_primary']
        )
        treatment_label.pack(anchor='w', pady=(0, 5))
        
        self.treatment_entry = ctk.CTkTextbox(
            form_content,
            font=FONTS['body'],
            height=100,
            wrap='word'
        )
        self.treatment_entry.pack(fill='x', pady=(0, 15))
        
        # Notes
        notes_label = ctk.CTkLabel(
            form_content,
            text="📝  Additional Notes",
            font=FONTS['body_bold'],
            text_color=COLORS['text_primary']
        )
        notes_label.pack(anchor='w', pady=(0, 5))
        
        self.notes_entry = ctk.CTkTextbox(
            form_content,
            font=FONTS['body'],
            height=80,
            wrap='word'
        )
        self.notes_entry.pack(fill='x', pady=(0, 15))
        
        # Buttons
        btn_frame = ctk.CTkFrame(main_frame, fg_color='transparent')
        btn_frame.pack(fill='x', pady=(20, 0))
        
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
            text="Save Visit",
            command=self.handle_save,
            font=FONTS['body_bold'],
            height=50,
            fg_color=COLORS['secondary'],
            hover_color='#059669'
        )
        save_btn.pack(side='right', fill='x', expand=True, padx=(10, 0))
    
    def handle_save(self):
        """Save new visit"""
        # Get form data
        date = self.date_entry.get().strip()
        time = self.time_entry.get().strip()
        visit_type = self.visit_type.get()
        department = self.dept_entry.get().strip()
        complaint = self.complaint_entry.get("1.0", "end-1c").strip()
        diagnosis = self.diagnosis_entry.get("1.0", "end-1c").strip()
        treatment = self.treatment_entry.get("1.0", "end-1c").strip()
        notes = self.notes_entry.get("1.0", "end-1c").strip()
        
        # Validate
        if not all([date, time, complaint, diagnosis, treatment]):
            messagebox.showerror("Validation Error", "Please fill all required fields (*)")
            return
        
        if not is_valid_date(date):
            messagebox.showerror("Invalid Date", "Please enter date in YYYY-MM-DD format")
            return
        
        # Create visit data
        visit_data = {
            'patient_national_id': self.patient_data.get('national_id'),
            'date': date,
            'time': time,
            'doctor_id': self.doctor_data.get('user_id'),
            'doctor_name': self.doctor_data.get('full_name'),
            'hospital': self.doctor_data.get('hospital', 'N/A'),
            'department': department or self.doctor_data.get('specialization', 'N/A'),
            'visit_type': visit_type,
            'chief_complaint': complaint,
            'diagnosis': diagnosis,
            'treatment_plan': treatment,
            'notes': notes,
            'prescriptions': [],  # Can be extended later
            'attachments': []
        }
        
        # Save visit
        success, message = visit_manager.add_visit(visit_data)
        
        if success:
            messagebox.showinfo("Success", "Visit added successfully!")
            self.on_success()
            self.destroy()
        else:
            messagebox.showerror("Error", f"Failed to save visit: {message}")