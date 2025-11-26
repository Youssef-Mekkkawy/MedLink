"""
Lab results tab component
"""
import customtkinter as ctk
from tkinter import messagebox, filedialog
from gui.styles import *
from gui.components.file_viewer import FileViewer
from core.lab_manager import lab_manager
from utils.date_utils import format_date, time_ago
import os
import shutil


class LabResultsTab(ctk.CTkFrame):
    """Lab results display and management"""
    
    def __init__(self, parent, patient_data, doctor_data=None, is_doctor=False):
        super().__init__(parent, fg_color='transparent')
        
        self.patient_data = patient_data
        self.doctor_data = doctor_data
        self.is_doctor = is_doctor
        
        self.create_ui()
        self.load_results()
    
    def create_ui(self):
        """Create lab results UI"""
        # Header
        header = ctk.CTkFrame(self, fg_color=COLORS['bg_medium'], height=80)
        header.pack(fill='x', pady=(0, 20))
        header.pack_propagate(False)
        
        header_content = ctk.CTkFrame(header, fg_color='transparent')
        header_content.pack(fill='both', expand=True, padx=20, pady=15)
        
        title_label = ctk.CTkLabel(
            header_content,
            text="🧪  Lab Results",
            font=FONTS['heading'],
            text_color=COLORS['text_primary']
        )
        title_label.pack(side='left')
        
        # Result count
        self.count_label = ctk.CTkLabel(
            header_content,
            text="",
            font=FONTS['body'],
            text_color=COLORS['text_secondary']
        )
        self.count_label.pack(side='left', padx=(20, 0))
        
        # Add button (only for doctors)
        if self.is_doctor:
            add_btn = ctk.CTkButton(
                header_content,
                text="➕ Add Lab Result",
                command=self.show_add_dialog,
                font=FONTS['body_bold'],
                height=45,
                fg_color=COLORS['secondary'],
                hover_color='#059669'
            )
            add_btn.pack(side='right')
        
        # Scrollable results container
        self.results_scroll = ctk.CTkScrollableFrame(
            self,
            fg_color='transparent'
        )
        self.results_scroll.pack(fill='both', expand=True)
    
    def load_results(self):
        """Load and display lab results"""
        # Clear existing
        for widget in self.results_scroll.winfo_children():
            widget.destroy()
        
        # Get results
        national_id = self.patient_data.get('national_id')
        results = lab_manager.get_patient_lab_results(national_id)
        
        # Update count
        self.count_label.configure(text=f"{len(results)} total results")
        
        if not results:
            self.show_empty_state()
            return
        
        # Display results
        for result in results:
            result_card = self.create_result_card(result)
            result_card.pack(fill='x', pady=10)
    
    def create_result_card(self, result):
        """Create lab result card"""
        card = ctk.CTkFrame(
            self.results_scroll,
            fg_color=COLORS['bg_medium'],
            corner_radius=RADIUS['lg'],
            border_width=2,
            border_color=COLORS['bg_hover']
        )
        
        content = ctk.CTkFrame(card, fg_color='transparent')
        content.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Header row
        header = ctk.CTkFrame(content, fg_color='transparent')
        header.pack(fill='x', pady=(0, 15))
        
        # Date
        date_str = result.get('date', 'N/A')
        date_label = ctk.CTkLabel(
            header,
            text=f"📅  {format_date(date_str)}",
            font=FONTS['body_bold'],
            text_color=COLORS['primary']
        )
        date_label.pack(side='left', padx=(0, 20))
        
        # Time ago
        time_ago_label = ctk.CTkLabel(
            header,
            text=time_ago(date_str),
            font=FONTS['small'],
            text_color=COLORS['text_muted']
        )
        time_ago_label.pack(side='left')
        
        # Status badge
        status = result.get('status', 'completed')
        status_colors = {
            'completed': COLORS['secondary'],
            'pending': COLORS['warning'],
            'cancelled': COLORS['danger']
        }
        
        status_badge = ctk.CTkLabel(
            header,
            text=status.title(),
            font=FONTS['small'],
            text_color='white',
            fg_color=status_colors.get(status, COLORS['primary']),
            corner_radius=RADIUS['sm'],
            padx=12,
            pady=6
        )
        status_badge.pack(side='right')
        
        # Lab info
        info_frame = ctk.CTkFrame(content, fg_color='transparent')
        info_frame.pack(fill='x', pady=(0, 15))
        
        lab_label = ctk.CTkLabel(
            info_frame,
            text=f"🏥  {result.get('lab_name', 'Unknown Lab')}",
            font=FONTS['body'],
            text_color=COLORS['text_primary']
        )
        lab_label.pack(side='left', padx=(0, 30))
        
        test_label = ctk.CTkLabel(
            info_frame,
            text=f"🧪  {result.get('test_type', 'N/A')}",
            font=FONTS['body'],
            text_color=COLORS['text_secondary']
        )
        test_label.pack(side='left')
        
        # Divider
        ctk.CTkFrame(
            content,
            height=1,
            fg_color=COLORS['bg_hover']
        ).pack(fill='x', pady=15)
        
        # Results
        results_data = result.get('results', {})
        if results_data:
            results_label = ctk.CTkLabel(
                content,
                text="Results:",
                font=FONTS['body_bold'],
                text_color=COLORS['text_primary']
            )
            results_label.pack(anchor='w', pady=(0, 10))
            
            results_frame = ctk.CTkFrame(
                content,
                fg_color=COLORS['bg_light'],
                corner_radius=RADIUS['md']
            )
            results_frame.pack(fill='x')
            
            results_content = ctk.CTkFrame(results_frame, fg_color='transparent')
            results_content.pack(fill='x', padx=15, pady=15)
            
            for key, value in results_data.items():
                result_row = ctk.CTkFrame(results_content, fg_color='transparent')
                result_row.pack(fill='x', pady=2)
                
                key_label = ctk.CTkLabel(
                    result_row,
                    text=f"{key}:",
                    font=FONTS['body'],
                    text_color=COLORS['text_secondary'],
                    width=200,
                    anchor='w'
                )
                key_label.pack(side='left')
                
                value_label = ctk.CTkLabel(
                    result_row,
                    text=str(value),
                    font=FONTS['body_bold'],
                    text_color=COLORS['text_primary'],
                    anchor='w'
                )
                value_label.pack(side='left')
        
        # Attachment
        attachment = result.get('attachment', '')
        if attachment:
            attach_btn = ctk.CTkButton(
                content,
                text="📄 View Report",
                command=lambda: self.view_attachment(attachment, result.get('test_type', 'Lab Result')),
                font=FONTS['body'],
                height=40,
                fg_color=COLORS['primary'],
                hover_color=COLORS['primary_hover']
            )
            attach_btn.pack(pady=(15, 0))
        
        return card
    
    def view_attachment(self, file_path, title):
        """View attached file"""
        if not os.path.exists(file_path):
            messagebox.showerror("Error", "File not found")
            return
        
        viewer = FileViewer(self, file_path, title)
    
    def show_add_dialog(self):
        """Show add lab result dialog"""
        dialog = AddLabResultDialog(
            self,
            self.patient_data,
            self.doctor_data,
            self.refresh
        )
        dialog.wait_window()
    
    def show_empty_state(self):
        """Show empty state"""
        empty_frame = ctk.CTkFrame(
            self.results_scroll,
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
            text="🧪",
            font=('Segoe UI', 64)
        )
        icon_label.pack()
        
        text_label = ctk.CTkLabel(
            empty_content,
            text="No Lab Results Yet",
            font=FONTS['heading'],
            text_color=COLORS['text_muted']
        )
        text_label.pack(pady=(10, 5))
        
        if self.is_doctor:
            hint_label = ctk.CTkLabel(
                empty_content,
                text="Click 'Add Lab Result' to add the first result",
                font=FONTS['body'],
                text_color=COLORS['text_muted']
            )
            hint_label.pack()
    
    def refresh(self):
        """Refresh results list"""
        self.load_results()


class AddLabResultDialog(ctk.CTkToplevel):
    """Dialog for adding lab result"""
    
    def __init__(self, parent, patient_data, doctor_data, on_success):
        super().__init__(parent)
        
        self.patient_data = patient_data
        self.doctor_data = doctor_data
        self.on_success = on_success
        self.attachment_path = None
        
        # Configure window
        self.title("Add Lab Result")
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
        """Create add result form"""
        from utils.date_utils import get_current_date
        from config.settings import ATTACHMENTS_DIR
        
        main_frame = ctk.CTkFrame(self, fg_color=COLORS['bg_dark'])
        main_frame.pack(fill='both', expand=True, padx=30, pady=30)
        
        # Header
        header = ctk.CTkFrame(main_frame, fg_color='transparent')
        header.pack(fill='x', pady=(0, 20))
        
        title_label = ctk.CTkLabel(
            header,
            text="🧪  Add Lab Result",
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
        
        # Date
        date_label = ctk.CTkLabel(
            form_content,
            text="📅  Date *",
            font=FONTS['body_bold'],
            text_color=COLORS['text_primary']
        )
        date_label.pack(anchor='w', pady=(0, 5))
        
        self.date_entry = ctk.CTkEntry(
            form_content,
            placeholder_text="YYYY-MM-DD",
            font=FONTS['body'],
            height=40
        )
        self.date_entry.pack(fill='x', pady=(0, 15))
        self.date_entry.insert(0, get_current_date())
        
        # Lab Name
        lab_label = ctk.CTkLabel(
            form_content,
            text="🏥  Lab Name *",
            font=FONTS['body_bold'],
            text_color=COLORS['text_primary']
        )
        lab_label.pack(anchor='w', pady=(0, 5))
        
        self.lab_entry = ctk.CTkOptionMenu(
            form_content,
            values=[
                "Al Borg Medical Laboratories",
                "Bio Lab",
                "Alpha Lab",
                "Cairo Lab",
                "El Mokhtabar",
                "Other"
            ],
            font=FONTS['body'],
            height=40
        )
        self.lab_entry.pack(fill='x', pady=(0, 15))
        
        # Test Type
        test_label = ctk.CTkLabel(
            form_content,
            text="🧪  Test Type *",
            font=FONTS['body_bold'],
            text_color=COLORS['text_primary']
        )
        test_label.pack(anchor='w', pady=(0, 5))
        
        self.test_entry = ctk.CTkEntry(
            form_content,
            placeholder_text="e.g., Complete Blood Count (CBC)",
            font=FONTS['body'],
            height=40
        )
        self.test_entry.pack(fill='x', pady=(0, 15))
        
        # Status
        status_label = ctk.CTkLabel(
            form_content,
            text="📊  Status",
            font=FONTS['body_bold'],
            text_color=COLORS['text_primary']
        )
        status_label.pack(anchor='w', pady=(0, 5))
        
        self.status_menu = ctk.CTkOptionMenu(
            form_content,
            values=["completed", "pending"],
            font=FONTS['body'],
            height=40
        )
        self.status_menu.pack(fill='x', pady=(0, 15))
        
        # Notes
        notes_label = ctk.CTkLabel(
            form_content,
            text="📝  Notes / Results Summary",
            font=FONTS['body_bold'],
            text_color=COLORS['text_primary']
        )
        notes_label.pack(anchor='w', pady=(0, 5))
        
        self.notes_entry = ctk.CTkTextbox(
            form_content,
            font=FONTS['body'],
            height=100,
            wrap='word'
        )
        self.notes_entry.pack(fill='x', pady=(0, 15))
        
        # Attachment
        attach_frame = ctk.CTkFrame(form_content, fg_color='transparent')
        attach_frame.pack(fill='x', pady=(0, 15))
        
        attach_label = ctk.CTkLabel(
            attach_frame,
            text="📎  Attach Report (PDF/Image)",
            font=FONTS['body_bold'],
            text_color=COLORS['text_primary']
        )
        attach_label.pack(anchor='w', pady=(0, 10))
        
        self.attach_btn = ctk.CTkButton(
            attach_frame,
            text="📁 Choose File",
            command=self.choose_file,
            font=FONTS['body'],
            height=40,
            fg_color=COLORS['bg_light'],
            hover_color=COLORS['bg_hover']
        )
        self.attach_btn.pack(fill='x')
        
        self.file_label = ctk.CTkLabel(
            attach_frame,
            text="No file selected",
            font=FONTS['small'],
            text_color=COLORS['text_muted']
        )
        self.file_label.pack(anchor='w', pady=(5, 0))
        
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
            text="Save Result",
            command=self.handle_save,
            font=FONTS['body_bold'],
            height=50,
            fg_color=COLORS['secondary'],
            hover_color='#059669'
        )
        save_btn.pack(side='right', fill='x', expand=True, padx=(10, 0))
    
    def choose_file(self):
        """Choose file to attach"""
        file_path = filedialog.askopenfilename(
            title="Select Lab Report",
            filetypes=[
                ("All Files", "*.*"),
                ("PDF Files", "*.pdf"),
                ("Image Files", "*.png;*.jpg;*.jpeg")
            ]
        )
        
        if file_path:
            self.attachment_path = file_path
            filename = os.path.basename(file_path)
            self.file_label.configure(text=f"Selected: {filename}")
            self.attach_btn.configure(text="✓ File Selected", fg_color=COLORS['secondary'])
    
    def handle_save(self):
        """Save lab result"""
        from utils.date_utils import is_valid_date
        from config.settings import ATTACHMENTS_DIR
        
        # Get form data
        date = self.date_entry.get().strip()
        lab_name = self.lab_entry.get()
        test_type = self.test_entry.get().strip()
        status = self.status_menu.get()
        notes = self.notes_entry.get("1.0", "end-1c").strip()
        
        # Validate
        if not all([date, lab_name, test_type]):
            messagebox.showerror("Validation Error", "Please fill all required fields (*)")
            return
        
        if not is_valid_date(date):
            messagebox.showerror("Invalid Date", "Please enter date in YYYY-MM-DD format")
            return
        
        # Handle attachment
        attachment_relative = ""
        if self.attachment_path:
            try:
                # Copy file to attachments folder
                lab_results_dir = ATTACHMENTS_DIR / "lab_results"
                lab_results_dir.mkdir(exist_ok=True)
                
                filename = f"{test_type.replace(' ', '_')}_{date}{os.path.splitext(self.attachment_path)[1]}"
                dest_path = lab_results_dir / filename
                
                shutil.copy2(self.attachment_path, dest_path)
                attachment_relative = str(dest_path)
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save attachment: {str(e)}")
                return
        
        # Create result data
        result_data = {
            'patient_national_id': self.patient_data.get('national_id'),
            'date': date,
            'lab_name': lab_name,
            'test_type': test_type,
            'status': status,
            'results': {},  # Can be extended to parse notes
            'notes': notes,
            'attachment': attachment_relative,
            'ordered_by': self.doctor_data.get('user_id') if self.doctor_data else None
        }
        
        # Save
        success, message = lab_manager.add_lab_result(result_data)
        
        if success:
            messagebox.showinfo("Success", "Lab result added successfully!")
            self.on_success()
            self.destroy()
        else:
            messagebox.showerror("Error", f"Failed to save result: {message}")