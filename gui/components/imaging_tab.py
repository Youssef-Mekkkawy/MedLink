"""
Imaging results tab component
"""
import customtkinter as ctk
from tkinter import messagebox, filedialog
from gui.styles import *
from gui.components.file_viewer import FileViewer
from core.imaging_manager import imaging_manager
from utils.date_utils import format_date, time_ago
import os
import shutil


class ImagingTab(ctk.CTkFrame):
    """Imaging results display and management"""
    
    def __init__(self, parent, patient_data, doctor_data=None, is_doctor=False):
        super().__init__(parent, fg_color='transparent')
        
        self.patient_data = patient_data
        self.doctor_data = doctor_data
        self.is_doctor = is_doctor
        
        self.create_ui()
        self.load_results()
    
    def create_ui(self):
        """Create imaging results UI"""
        # Header
        header = ctk.CTkFrame(self, fg_color=COLORS['bg_medium'], height=80)
        header.pack(fill='x', pady=(0, 20))
        header.pack_propagate(False)
        
        header_content = ctk.CTkFrame(header, fg_color='transparent')
        header_content.pack(fill='both', expand=True, padx=20, pady=15)
        
        title_label = ctk.CTkLabel(
            header_content,
            text="📷  Imaging Results",
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
                text="➕ Add Imaging Result",
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
        """Load and display imaging results"""
        # Clear existing
        for widget in self.results_scroll.winfo_children():
            widget.destroy()
        
        # Get results
        national_id = self.patient_data.get('national_id')
        results = imaging_manager.get_patient_imaging_results(national_id)
        
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
        """Create imaging result card"""
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
        
        # Type badge
        imaging_type = result.get('imaging_type', 'X-Ray')
        type_colors = {
            'X-Ray': COLORS['info'],
            'CT': COLORS['primary'],
            'MRI': COLORS['accent_purple'],
            'Ultrasound': COLORS['secondary']
        }
        
        type_badge = ctk.CTkLabel(
            header,
            text=imaging_type,
            font=FONTS['small'],
            text_color='white',
            fg_color=type_colors.get(imaging_type, COLORS['primary']),
            corner_radius=RADIUS['sm'],
            padx=12,
            pady=6
        )
        type_badge.pack(side='right')
        
        # Center info
        info_frame = ctk.CTkFrame(content, fg_color='transparent')
        info_frame.pack(fill='x', pady=(0, 15))
        
        center_label = ctk.CTkLabel(
            info_frame,
            text=f"🏥  {result.get('imaging_center', 'Unknown Center')}",
            font=FONTS['body'],
            text_color=COLORS['text_primary']
        )
        center_label.pack(side='left', padx=(0, 30))
        
        body_part = result.get('body_part', 'N/A')
        part_label = ctk.CTkLabel(
            info_frame,
            text=f"📍  {body_part}",
            font=FONTS['body'],
            text_color=COLORS['text_secondary']
        )
        part_label.pack(side='left')
        
        # Divider
        ctk.CTkFrame(
            content,
            height=1,
            fg_color=COLORS['bg_hover']
        ).pack(fill='x', pady=15)
        
        # Findings
        findings = result.get('findings', '')
        if findings:
            findings_label = ctk.CTkLabel(
                content,
                text="Findings:",
                font=FONTS['body_bold'],
                text_color=COLORS['text_primary']
            )
            findings_label.pack(anchor='w', pady=(0, 5))
            
            findings_text = ctk.CTkLabel(
                content,
                text=findings,
                font=FONTS['body'],
                text_color=COLORS['text_secondary'],
                anchor='w',
                wraplength=800,
                justify='left'
            )
            findings_text.pack(anchor='w', pady=(0, 15))
        
        # Radiologist
        radiologist = result.get('radiologist', '')
        if radiologist:
            rad_label = ctk.CTkLabel(
                content,
                text=f"👨‍⚕️  Radiologist: {radiologist}",
                font=FONTS['small'],
                text_color=COLORS['text_muted']
            )
            rad_label.pack(anchor='w', pady=(0, 15))
        
        # Images
        images = result.get('images', [])
        if images:
            images_frame = ctk.CTkFrame(content, fg_color='transparent')
            images_frame.pack(fill='x')
            
            for i, image_path in enumerate(images[:3], 1):  # Show first 3
                img_btn = ctk.CTkButton(
                    images_frame,
                    text=f"🖼️  View Image {i}",
                    command=lambda p=image_path: self.view_image(p, body_part),
                    font=FONTS['body'],
                    height=40,
                    fg_color=COLORS['primary'],
                    hover_color=COLORS['primary_hover']
                )
                img_btn.pack(side='left', padx=(0, 10))
        
        return card
    
    def view_image(self, file_path, title):
        """View imaging file"""
        if not os.path.exists(file_path):
            messagebox.showerror("Error", "File not found")
            return
        
        viewer = FileViewer(self, file_path, f"{title} - Imaging")
    
    def show_add_dialog(self):
        """Show add imaging result dialog"""
        dialog = AddImagingResultDialog(
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
            text="📷",
            font=('Segoe UI', 64)
        )
        icon_label.pack()
        
        text_label = ctk.CTkLabel(
            empty_content,
            text="No Imaging Results Yet",
            font=FONTS['heading'],
            text_color=COLORS['text_muted']
        )
        text_label.pack(pady=(10, 5))
        
        if self.is_doctor:
            hint_label = ctk.CTkLabel(
                empty_content,
                text="Click 'Add Imaging Result' to add the first result",
                font=FONTS['body'],
                text_color=COLORS['text_muted']
            )
            hint_label.pack()
    
    def refresh(self):
        """Refresh results list"""
        self.load_results()


class AddImagingResultDialog(ctk.CTkToplevel):
    """Dialog for adding imaging result"""
    
    def __init__(self, parent, patient_data, doctor_data, on_success):
        super().__init__(parent)
        
        self.patient_data = patient_data
        self.doctor_data = doctor_data
        self.on_success = on_success
        self.image_paths = []
        
        # Configure window
        self.title("Add Imaging Result")
        self.geometry("600x750")
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
        
        main_frame = ctk.CTkFrame(self, fg_color=COLORS['bg_dark'])
        main_frame.pack(fill='both', expand=True, padx=30, pady=30)
        
        # Header
        header = ctk.CTkFrame(main_frame, fg_color='transparent')
        header.pack(fill='x', pady=(0, 20))
        
        title_label = ctk.CTkLabel(
            header,
            text="📷  Add Imaging Result",
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
        
        # Imaging Center
        center_label = ctk.CTkLabel(
            form_content,
            text="🏥  Imaging Center *",
            font=FONTS['body_bold'],
            text_color=COLORS['text_primary']
        )
        center_label.pack(anchor='w', pady=(0, 5))
        
        self.center_entry = ctk.CTkOptionMenu(
            form_content,
            values=[
                "Scan Center",
                "Cairo Scan",
                "Radiology Plus",
                "Modern Imaging",
                "Al Borg Scan",
                "Other"
            ],
            font=FONTS['body'],
            height=40
        )
        self.center_entry.pack(fill='x', pady=(0, 15))
        
        # Imaging Type
        type_label = ctk.CTkLabel(
            form_content,
            text="📷  Imaging Type *",
            font=FONTS['body_bold'],
            text_color=COLORS['text_primary']
        )
        type_label.pack(anchor='w', pady=(0, 5))
        
        self.type_entry = ctk.CTkOptionMenu(
            form_content,
            values=["X-Ray", "CT", "MRI", "Ultrasound", "Mammogram", "PET Scan"],
            font=FONTS['body'],
            height=40
        )
        self.type_entry.pack(fill='x', pady=(0, 15))
        
        # Body Part
        part_label = ctk.CTkLabel(
            form_content,
            text="📍  Body Part *",
            font=FONTS['body_bold'],
            text_color=COLORS['text_primary']
        )
        part_label.pack(anchor='w', pady=(0, 5))
        
        self.part_entry = ctk.CTkEntry(
            form_content,
            placeholder_text="e.g., Chest, Abdomen, Head",
            font=FONTS['body'],
            height=40
        )
        self.part_entry.pack(fill='x', pady=(0, 15))
        
        # Findings
        findings_label = ctk.CTkLabel(
            form_content,
            text="📝  Findings *",
            font=FONTS['body_bold'],
            text_color=COLORS['text_primary']
        )
        findings_label.pack(anchor='w', pady=(0, 5))
        
        self.findings_entry = ctk.CTkTextbox(
            form_content,
            font=FONTS['body'],
            height=100,
            wrap='word'
        )
        self.findings_entry.pack(fill='x', pady=(0, 15))
        
        # Radiologist
        rad_label = ctk.CTkLabel(
            form_content,
            text="👨‍⚕️  Radiologist Name",
            font=FONTS['body_bold'],
            text_color=COLORS['text_primary']
        )
        rad_label.pack(anchor='w', pady=(0, 5))
        
        self.rad_entry = ctk.CTkEntry(
            form_content,
            placeholder_text="Enter radiologist name",
            font=FONTS['body'],
            height=40
        )
        self.rad_entry.pack(fill='x', pady=(0, 15))
        
        # Attach Images
        attach_frame = ctk.CTkFrame(form_content, fg_color='transparent')
        attach_frame.pack(fill='x', pady=(0, 15))
        
        attach_label = ctk.CTkLabel(
            attach_frame,
            text="🖼️  Attach Images",
            font=FONTS['body_bold'],
            text_color=COLORS['text_primary']
        )
        attach_label.pack(anchor='w', pady=(0, 10))
        
        self.attach_btn = ctk.CTkButton(
            attach_frame,
            text="📁 Choose Images",
            command=self.choose_images,
            font=FONTS['body'],
            height=40,
            fg_color=COLORS['bg_light'],
            hover_color=COLORS['bg_hover']
        )
        self.attach_btn.pack(fill='x')
        
        self.files_label = ctk.CTkLabel(
            attach_frame,
            text="No files selected",
            font=FONTS['small'],
            text_color=COLORS['text_muted']
        )
        self.files_label.pack(anchor='w', pady=(5, 0))
        
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
    
    def choose_images(self):
        """Choose images to attach"""
        file_paths = filedialog.askopenfilenames(
            title="Select Imaging Files",
            filetypes=[
                ("Image Files", "*.png;*.jpg;*.jpeg;*.bmp;*.gif"),
                ("All Files", "*.*")
            ]
        )
        
        if file_paths:
            self.image_paths = list(file_paths)
            count = len(self.image_paths)
            self.files_label.configure(text=f"Selected: {count} file{'s' if count > 1 else ''}")
            self.attach_btn.configure(text=f"✓ {count} File{'s' if count > 1 else ''} Selected", fg_color=COLORS['secondary'])
    
    def handle_save(self):
        """Save imaging result"""
        from utils.date_utils import is_valid_date
        from config.settings import ATTACHMENTS_DIR
        
        # Get form data
        date = self.date_entry.get().strip()
        center = self.center_entry.get()
        imaging_type = self.type_entry.get()
        body_part = self.part_entry.get().strip()
        findings = self.findings_entry.get("1.0", "end-1c").strip()
        radiologist = self.rad_entry.get().strip()
        
        # Validate
        if not all([date, center, imaging_type, body_part, findings]):
            messagebox.showerror("Validation Error", "Please fill all required fields (*)")
            return
        
        if not is_valid_date(date):
            messagebox.showerror("Invalid Date", "Please enter date in YYYY-MM-DD format")
            return
        
        # Handle attachments
        image_paths_saved = []
        if self.image_paths:
            try:
                xrays_dir = ATTACHMENTS_DIR / "xrays"
                xrays_dir.mkdir(exist_ok=True)
                
                for i, image_path in enumerate(self.image_paths, 1):
                    ext = os.path.splitext(image_path)[1]
                    filename = f"{body_part.replace(' ', '_')}_{date}_{i}{ext}"
                    dest_path = xrays_dir / filename
                    
                    shutil.copy2(image_path, dest_path)
                    image_paths_saved.append(str(dest_path))
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save images: {str(e)}")
                return
        
        # Create result data
        result_data = {
            'patient_national_id': self.patient_data.get('national_id'),
            'date': date,
            'imaging_center': center,
            'imaging_type': imaging_type,
            'body_part': body_part,
            'findings': findings,
            'radiologist': radiologist,
            'images': image_paths_saved,
            'ordered_by': self.doctor_data.get('user_id') if self.doctor_data else None
        }
        
        # Save
        success, message = imaging_manager.add_imaging_result(result_data)
        
        if success:
            messagebox.showinfo("Success", "Imaging result added successfully!")
            self.on_success()
            self.destroy()
        else:
            messagebox.showerror("Error", f"Failed to save result: {message}")