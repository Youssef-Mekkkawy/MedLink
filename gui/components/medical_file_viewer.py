"""
Medical file viewer - View PDFs and medical images
Location: gui/components/medical_file_viewer.py
"""
import customtkinter as ctk
from tkinter import messagebox
from gui.styles import *
from PIL import Image, ImageTk
import os


class MedicalFileViewer(ctk.CTkToplevel):
    """Universal viewer for medical files (PDF, images)"""
    
    def __init__(self, parent, file_path, title="Medical File"):
        super().__init__(parent)
        
        self.file_path = file_path
        self.file_title = title
        
        # Configure window
        self.title(title)
        self.geometry("900x800")
        
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
        self.load_file()
    
    def create_ui(self):
        """Create file viewer UI"""
        # Header
        header = ctk.CTkFrame(self, fg_color=COLORS['bg_medium'])
        header.pack(fill='x', padx=30, pady=(30, 0))
        
        header_content = ctk.CTkFrame(header, fg_color='transparent')
        header_content.pack(fill='x', padx=20, pady=15)
        
        # Title
        title_label = ctk.CTkLabel(
            header_content,
            text=self.file_title,
            font=FONTS['heading'],
            text_color=COLORS['text_primary']
        )
        title_label.pack(side='left')
        
        # File type badge
        file_ext = os.path.splitext(self.file_path)[1].upper()[1:]
        
        type_badge = ctk.CTkFrame(
            header_content,
            fg_color=COLORS['info'],
            corner_radius=RADIUS['sm']
        )
        type_badge.pack(side='right')
        
        type_label = ctk.CTkLabel(
            type_badge,
            text=file_ext,
            font=FONTS['body_bold'],
            text_color='white'
        )
        type_label.pack(padx=15, pady=5)
        
        # Toolbar
        toolbar = ctk.CTkFrame(self, fg_color='transparent')
        toolbar.pack(fill='x', padx=30, pady=15)
        
        # File info
        file_name = os.path.basename(self.file_path)
        file_info = ctk.CTkLabel(
            toolbar,
            text=f"📄 {file_name}",
            font=FONTS['body'],
            text_color=COLORS['text_secondary']
        )
        file_info.pack(side='left')
        
        # Actions
        actions_frame = ctk.CTkFrame(toolbar, fg_color='transparent')
        actions_frame.pack(side='right')
        
        # Download button
        download_btn = ctk.CTkButton(
            actions_frame,
            text="💾 Download",
            command=self.download_file,
            font=FONTS['small_bold'],
            height=35,
            width=120,
            fg_color=COLORS['secondary'],
            hover_color='#059669'
        )
        download_btn.pack(side='left', padx=(0, 10))
        
        # Print button
        print_btn = ctk.CTkButton(
            actions_frame,
            text="🖨️ Print",
            command=self.print_file,
            font=FONTS['small_bold'],
            height=35,
            width=100,
            fg_color=COLORS['info'],
            hover_color='#0284c7'
        )
        print_btn.pack(side='left')
        
        # Content area
        self.content_frame = ctk.CTkScrollableFrame(
            self,
            fg_color=COLORS['bg_dark']
        )
        self.content_frame.pack(fill='both', expand=True, padx=30, pady=(0, 20))
        
        # Close button
        close_btn = ctk.CTkButton(
            self,
            text="Close",
            command=self.destroy,
            font=FONTS['body_bold'],
            height=50,
            fg_color=COLORS['danger'],
            hover_color='#dc2626'
        )
        close_btn.pack(fill='x', padx=30, pady=(0, 30))
    
    def load_file(self):
        """Load and display file"""
        if not os.path.exists(self.file_path):
            error_label = ctk.CTkLabel(
                self.content_frame,
                text="❌ File not found",
                font=FONTS['heading'],
                text_color=COLORS['danger']
            )
            error_label.pack(pady=100)
            return
        
        # Get file extension
        _, ext = os.path.splitext(self.file_path)
        ext = ext.lower()
        
        if ext == '.pdf':
            self.display_pdf()
        elif ext in ['.png', '.jpg', '.jpeg', '.gif', '.bmp']:
            self.display_image()
        else:
            self.display_unsupported()
    
    def display_pdf(self):
        """Display PDF file"""
        # PDF viewer
        pdf_info = ctk.CTkFrame(
            self.content_frame,
            fg_color=COLORS['bg_medium'],
            corner_radius=RADIUS['lg']
        )
        pdf_info.pack(fill='both', expand=True, pady=20)
        
        icon_label = ctk.CTkLabel(
            pdf_info,
            text="📄",
            font=('Segoe UI', 100)
        )
        icon_label.pack(pady=(50, 20))
        
        title_label = ctk.CTkLabel(
            pdf_info,
            text="PDF Document",
            font=FONTS['heading'],
            text_color=COLORS['text_primary']
        )
        title_label.pack()
        
        info_label = ctk.CTkLabel(
            pdf_info,
            text=f"File: {os.path.basename(self.file_path)}",
            font=FONTS['body'],
            text_color=COLORS['text_secondary']
        )
        info_label.pack(pady=(10, 0))
        
        # Instructions
        instructions = ctk.CTkLabel(
            pdf_info,
            text="Click 'Download' to save and open with your PDF reader",
            font=FONTS['small'],
            text_color=COLORS['text_secondary']
        )
        instructions.pack(pady=(20, 50))
    
    def display_image(self):
        """Display image file"""
        try:
            # Load image
            image = Image.open(self.file_path)
            
            # Calculate size to fit viewer
            max_width = 800
            max_height = 600
            
            # Get original dimensions
            orig_width, orig_height = image.size
            
            # Calculate scaling
            scale = min(max_width / orig_width, max_height / orig_height, 1.0)
            
            new_width = int(orig_width * scale)
            new_height = int(orig_height * scale)
            
            # Resize image
            image = image.resize((new_width, new_height), Image.Resampling.LANCZOS)
            
            # Convert to PhotoImage
            photo = ImageTk.PhotoImage(image)
            
            # Display image
            image_label = ctk.CTkLabel(
                self.content_frame,
                image=photo,
                text=""
            )
            image_label.image = photo  # Keep reference
            image_label.pack(pady=20)
            
            # Image info
            info_text = f"Original size: {orig_width}x{orig_height} pixels"
            if scale < 1.0:
                info_text += f" (scaled to {int(scale*100)}%)"
            
            info_label = ctk.CTkLabel(
                self.content_frame,
                text=info_text,
                font=FONTS['small'],
                text_color=COLORS['text_secondary']
            )
            info_label.pack(pady=(10, 20))
            
        except Exception as e:
            error_label = ctk.CTkLabel(
                self.content_frame,
                text=f"❌ Error loading image: {str(e)}",
                font=FONTS['body'],
                text_color=COLORS['danger']
            )
            error_label.pack(pady=100)
    
    def display_unsupported(self):
        """Display unsupported file type message"""
        unsupported_frame = ctk.CTkFrame(
            self.content_frame,
            fg_color=COLORS['bg_medium'],
            corner_radius=RADIUS['lg']
        )
        unsupported_frame.pack(fill='both', expand=True, pady=20)
        
        icon_label = ctk.CTkLabel(
            unsupported_frame,
            text="❓",
            font=('Segoe UI', 100)
        )
        icon_label.pack(pady=(50, 20))
        
        title_label = ctk.CTkLabel(
            unsupported_frame,
            text="Unsupported File Type",
            font=FONTS['heading'],
            text_color=COLORS['text_primary']
        )
        title_label.pack()
        
        ext = os.path.splitext(self.file_path)[1]
        info_label = ctk.CTkLabel(
            unsupported_frame,
            text=f"Cannot preview {ext} files in this viewer",
            font=FONTS['body'],
            text_color=COLORS['text_secondary']
        )
        info_label.pack(pady=(10, 0))
        
        # Supported formats
        supported_label = ctk.CTkLabel(
            unsupported_frame,
            text="Supported formats: PDF, PNG, JPG, JPEG, GIF, BMP",
            font=FONTS['small'],
            text_color=COLORS['text_secondary']
        )
        supported_label.pack(pady=(20, 50))
    
    def download_file(self):
        """Download/save file"""
        messagebox.showinfo(
            "Download",
            f"File location:\n{self.file_path}\n\nYou can copy this file to your desired location."
        )
    
    def print_file(self):
        """Print file"""
        messagebox.showinfo(
            "Print",
            "Print functionality would open the system print dialog here."
        )


def open_medical_file(parent, file_path, title="Medical File"):
    """Helper function to open medical file viewer"""
    if not os.path.exists(file_path):
        messagebox.showerror("File Not Found", f"File not found: {file_path}")
        return None
    
    viewer = MedicalFileViewer(parent, file_path, title)
    return viewer