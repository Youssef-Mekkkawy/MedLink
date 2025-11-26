"""
File viewer component - Display PDFs and images
"""
import customtkinter as ctk
from tkinter import messagebox
from PIL import Image
import os
from gui.styles import *


class FileViewer(ctk.CTkToplevel):
    """Simple file viewer for PDFs and images"""
    
    def __init__(self, parent, file_path, title="File Viewer"):
        super().__init__(parent)
        
        self.file_path = file_path
        self.file_title = title
        
        # Configure window
        self.title(title)
        self.geometry("900x700")
        
        # Center on parent
        self.transient(parent)
        
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = parent.winfo_x() + (parent.winfo_width() // 2) - (width // 2)
        y = parent.winfo_y() + (parent.winfo_height() // 2) - (height // 2)
        self.geometry(f'{width}x{height}+{x}+{y}')
        
        self.create_ui()
    
    def create_ui(self):
        """Create viewer UI"""
        # Header
        header = ctk.CTkFrame(self, fg_color=COLORS['bg_medium'], height=60)
        header.pack(fill='x')
        header.pack_propagate(False)
        
        header_content = ctk.CTkFrame(header, fg_color='transparent')
        header_content.pack(fill='both', expand=True, padx=20, pady=10)
        
        title_label = ctk.CTkLabel(
            header_content,
            text=self.file_title,
            font=FONTS['heading'],
            text_color=COLORS['text_primary']
        )
        title_label.pack(side='left')
        
        open_btn = ctk.CTkButton(
            header_content,
            text="📂 Open in System Viewer",
            command=self.open_external,
            font=FONTS['body'],
            height=40,
            fg_color=COLORS['primary'],
            hover_color=COLORS['primary_hover']
        )
        open_btn.pack(side='right')
        
        # Content area
        content = ctk.CTkFrame(self, fg_color=COLORS['bg_dark'])
        content.pack(fill='both', expand=True)
        
        # Check file type and display
        if not os.path.exists(self.file_path):
            self.show_error(content, "File not found")
        elif self.file_path.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp')):
            self.show_image(content)
        elif self.file_path.lower().endswith('.pdf'):
            self.show_pdf_info(content)
        else:
            self.show_unsupported(content)
    
    def show_image(self, parent):
        """Display image file"""
        try:
            # Load and display image
            img = Image.open(self.file_path)
            
            # Calculate scaling to fit window
            max_width = 850
            max_height = 600
            
            img_width, img_height = img.size
            scale = min(max_width / img_width, max_height / img_height, 1.0)
            
            new_width = int(img_width * scale)
            new_height = int(img_height * scale)
            
            img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
            
            # Convert to CTkImage
            ctk_image = ctk.CTkImage(light_image=img, dark_image=img, size=(new_width, new_height))
            
            # Display in scrollable frame
            scroll_frame = ctk.CTkScrollableFrame(parent, fg_color='transparent')
            scroll_frame.pack(fill='both', expand=True, padx=20, pady=20)
            
            image_label = ctk.CTkLabel(
                scroll_frame,
                image=ctk_image,
                text=""
            )
            image_label.pack(expand=True)
            
        except Exception as e:
            self.show_error(parent, f"Failed to load image: {str(e)}")
    
    def show_pdf_info(self, parent):
        """Show PDF information (actual PDF rendering requires additional libraries)"""
        info_frame = ctk.CTkFrame(
            parent,
            fg_color=COLORS['bg_medium'],
            corner_radius=RADIUS['lg']
        )
        info_frame.place(relx=0.5, rely=0.5, anchor='center', relwidth=0.8, relheight=0.6)
        
        content = ctk.CTkFrame(info_frame, fg_color='transparent')
        content.place(relx=0.5, rely=0.5, anchor='center')
        
        icon_label = ctk.CTkLabel(
            content,
            text="📄",
            font=('Segoe UI', 64)
        )
        icon_label.pack()
        
        title_label = ctk.CTkLabel(
            content,
            text="PDF Document",
            font=FONTS['heading'],
            text_color=COLORS['text_primary']
        )
        title_label.pack(pady=(10, 5))
        
        filename_label = ctk.CTkLabel(
            content,
            text=os.path.basename(self.file_path),
            font=FONTS['body'],
            text_color=COLORS['text_secondary']
        )
        filename_label.pack(pady=(0, 20))
        
        info_label = ctk.CTkLabel(
            content,
            text="Click 'Open in System Viewer' to view the PDF\nin your default PDF reader",
            font=FONTS['body'],
            text_color=COLORS['text_muted'],
            justify='center'
        )
        info_label.pack()
        
        open_btn = ctk.CTkButton(
            content,
            text="📂 Open PDF",
            command=self.open_external,
            font=FONTS['body_bold'],
            height=50,
            fg_color=COLORS['primary'],
            hover_color=COLORS['primary_hover']
        )
        open_btn.pack(pady=(30, 0))
    
    def show_unsupported(self, parent):
        """Show unsupported file type message"""
        self.show_error(parent, "Unsupported file type")
    
    def show_error(self, parent, message):
        """Show error message"""
        error_frame = ctk.CTkFrame(parent, fg_color='transparent')
        error_frame.place(relx=0.5, rely=0.5, anchor='center')
        
        icon_label = ctk.CTkLabel(
            error_frame,
            text="❌",
            font=('Segoe UI', 64)
        )
        icon_label.pack()
        
        error_label = ctk.CTkLabel(
            error_frame,
            text=message,
            font=FONTS['heading'],
            text_color=COLORS['danger']
        )
        error_label.pack(pady=20)
    
    def open_external(self):
        """Open file in system default viewer"""
        try:
            import platform
            import subprocess
            
            if platform.system() == 'Windows':
                os.startfile(self.file_path)
            elif platform.system() == 'Darwin':  # macOS
                subprocess.call(['open', self.file_path])
            else:  # Linux
                subprocess.call(['xdg-open', self.file_path])
        except Exception as e:
            messagebox.showerror("Error", f"Failed to open file: {str(e)}")