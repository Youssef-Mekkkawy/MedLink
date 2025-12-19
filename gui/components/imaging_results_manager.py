"""
Imaging Results Manager - FIXED VERSION (Color fix)
Location: gui/components/imaging_results_manager.py
"""

import customtkinter as ctk
from gui.styles import *
from core.imaging_manager import imaging_manager
from datetime import datetime
from typing import Optional


class ImagingResultsManager(ctk.CTkFrame):
    """Imaging results display"""
    
    def __init__(self, parent, patient_data, is_doctor=False):
        super().__init__(parent, fg_color='transparent')
        
        # DATABASE FIX: Convert and assign
        from gui.components.db_converter import convert_to_dict
        self.patient_data = convert_to_dict(patient_data)
        
        # Extract patient ID
        self.patient_id = self.patient_data.get('national_id')
        self.is_doctor = is_doctor
        
        self.create_ui()
        self.load_imaging_results()
    
    def create_ui(self):
        """Create UI"""
        # Main scrollable container
        self.scroll_frame = ctk.CTkScrollableFrame(
            self,
            fg_color='transparent'
        )
        self.scroll_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Header
        header = ctk.CTkFrame(self.scroll_frame, fg_color='transparent')
        header.pack(fill='x', pady=(0, 20))
        
        title = ctk.CTkLabel(
            header,
            text="📸 Imaging Results",
            font=FONTS['heading'],
            text_color=COLORS['text_primary']
        )
        title.pack(side='left')
        
        # Add button (if doctor)
        if self.is_doctor:
            add_btn = ctk.CTkButton(
                header,
                text="+ Add Result",
                command=self.add_imaging_result,
                font=FONTS['small_bold'],
                height=35,
                width=120,
                fg_color=COLORS['primary'],
                hover_color=COLORS['primary_hover']  # ✅ FIXED: Use primary_hover instead of primary_dark
            )
            add_btn.pack(side='right')
        
        # Results container
        self.results_frame = ctk.CTkFrame(
            self.scroll_frame,
            fg_color='transparent'
        )
        self.results_frame.pack(fill='both', expand=True)
    
    def load_imaging_results(self):
        """Load and display imaging results"""
        # Clear existing
        for widget in self.results_frame.winfo_children():
            widget.destroy()
        
        # Get results
        if not self.patient_id:
            self.show_no_results("Patient ID not found")
            return
        
        results = imaging_manager.get_patient_imaging_results(self.patient_id)
        
        if not results:
            self.show_no_results("No imaging results found")
            return
        
        # Display results
        for result in results:
            self.create_result_card(result)
    
    def create_result_card(self, result: dict):
        """Create card for single imaging result"""
        card = ctk.CTkFrame(
            self.results_frame,
            fg_color=COLORS['bg_medium'],
            corner_radius=RADIUS['lg']
        )
        card.pack(fill='x', pady=5)
        
        content = ctk.CTkFrame(card, fg_color='transparent')
        content.pack(fill='x', padx=15, pady=12)
        
        # Imaging type and date
        header_frame = ctk.CTkFrame(content, fg_color='transparent')
        header_frame.pack(fill='x')
        
        imaging_type = ctk.CTkLabel(
            header_frame,
            text=f"📸 {result.get('imaging_type', 'Unknown')} - {result.get('body_part', 'N/A')}",
            font=FONTS['body_bold'],
            text_color=COLORS['text_primary']
        )
        imaging_type.pack(side='left')
        
        date_label = ctk.CTkLabel(
            header_frame,
            text=f"📅 {result.get('imaging_date', 'N/A')}",
            font=FONTS['small'],
            text_color=COLORS['text_secondary']
        )
        date_label.pack(side='right')
        
        # Findings
        if result.get('findings'):
            findings_label = ctk.CTkLabel(
                content,
                text=f"Findings: {result['findings']}",
                font=FONTS['body'],
                text_color=COLORS['text_primary'],
                wraplength=600
            )
            findings_label.pack(anchor='w', pady=(8, 0))
        
        # Impression
        if result.get('impression'):
            impression_label = ctk.CTkLabel(
                content,
                text=f"Impression: {result['impression']}",
                font=FONTS['body'],
                text_color=COLORS['text_primary'],
                wraplength=600
            )
            impression_label.pack(anchor='w', pady=(5, 0))
        
        # Radiologist
        if result.get('radiologist_name'):
            radiologist_label = ctk.CTkLabel(
                content,
                text=f"👨‍⚕️ {result['radiologist_name']}",
                font=FONTS['small'],
                text_color=COLORS['text_secondary']
            )
            radiologist_label.pack(anchor='w', pady=(3, 0))
        
        # Facility
        if result.get('facility_name'):
            facility_label = ctk.CTkLabel(
                content,
                text=f"🏥 {result['facility_name']}",
                font=FONTS['small'],
                text_color=COLORS['text_secondary']
            )
            facility_label.pack(anchor='w', pady=(3, 0))
    
    def show_no_results(self, message: str):
        """Show no results message"""
        no_data = ctk.CTkLabel(
            self.results_frame,
            text=message,
            font=FONTS['body'],
            text_color=COLORS['text_secondary']
        )
        no_data.pack(pady=40)
    
    def add_imaging_result(self):
        """Open dialog to add imaging result"""
        from tkinter import messagebox
        messagebox.showinfo(
            "Add Imaging Result",
            "Add Imaging Result dialog coming soon!\n\n"
            "This will allow doctors to add new imaging results."
        )


# IMPORTANT: Alias for backwards compatibility
class EnhancedImagingResultsManager(ImagingResultsManager):
    """Alias for backwards compatibility with doctor_dashboard.py"""
    pass