"""
Enhanced lab results manager - Display and manage lab results
Location: gui/components/enhanced_lab_results_manager.py
"""
import customtkinter as ctk
from tkinter import messagebox
from gui.styles import *
from core.lab_manager import lab_manager
from datetime import datetime
import os


class EnhancedLabResultsManager(ctk.CTkFrame):
    """Enhanced lab results display with filtering and search"""
    
    def __init__(self, parent, patient_data, is_doctor=False):
        super().__init__(parent, fg_color='transparent')
        
        self.patient_data = patient_data
        self.is_doctor = is_doctor
        self.all_results = []
        self.filtered_results = []
        
        self.create_ui()
        self.load_results()
    
    def create_ui(self):
        """Create lab results UI"""
        # Header
        header = ctk.CTkFrame(self, fg_color='transparent')
        header.pack(fill='x', padx=20, pady=(20, 10))
        
        title = ctk.CTkLabel(
            header,
            text="🔬 Laboratory Results",
            font=FONTS['heading'],
            text_color=COLORS['text_primary']
        )
        title.pack(side='left')
        
        # Add button (doctor only)
        if self.is_doctor:
            add_btn = ctk.CTkButton(
                header,
                text="+ Add Lab Result",
                command=self.add_lab_result,
                font=FONTS['body_bold'],
                height=40,
                fg_color=COLORS['secondary'],
                hover_color='#059669'
            )
            add_btn.pack(side='right')
        
        # Search and Filter Bar
        filter_frame = ctk.CTkFrame(self, fg_color=COLORS['bg_medium'], corner_radius=RADIUS['lg'])
        filter_frame.pack(fill='x', padx=20, pady=(0, 20))
        
        filter_content = ctk.CTkFrame(filter_frame, fg_color='transparent')
        filter_content.pack(fill='x', padx=20, pady=15)
        
        # Search
        search_frame = ctk.CTkFrame(filter_content, fg_color='transparent')
        search_frame.pack(side='left', fill='x', expand=True, padx=(0, 15))
        
        search_label = ctk.CTkLabel(
            search_frame,
            text="🔍 Search:",
            font=FONTS['body'],
            text_color=COLORS['text_secondary']
        )
        search_label.pack(side='left', padx=(0, 10))
        
        self.search_entry = ctk.CTkEntry(
            search_frame,
            placeholder_text="Search test name...",
            font=FONTS['body'],
            height=40
        )
        self.search_entry.pack(side='left', fill='x', expand=True)
        self.search_entry.bind('<KeyRelease>', lambda e: self.apply_filters())
        
        # Filter by category
        category_frame = ctk.CTkFrame(filter_content, fg_color='transparent')
        category_frame.pack(side='left')
        
        category_label = ctk.CTkLabel(
            category_frame,
            text="Category:",
            font=FONTS['body'],
            text_color=COLORS['text_secondary']
        )
        category_label.pack(side='left', padx=(0, 10))
        
        self.category_filter = ctk.CTkOptionMenu(
            category_frame,
            values=["All", "Blood Test", "Urine Test", "Imaging", "Biopsy", "Culture", "Other"],
            command=lambda x: self.apply_filters(),
            font=FONTS['body'],
            height=40,
            width=150
        )
        self.category_filter.pack(side='left')
        
        # Results container
        self.results_scroll = ctk.CTkScrollableFrame(
            self,
            fg_color='transparent'
        )
        self.results_scroll.pack(fill='both', expand=True, padx=20, pady=(0, 20))
    
    def load_results(self):
        """Load all lab results"""
        self.all_results = lab_manager.get_patient_results(
            self.patient_data.get('national_id')
        )
        self.apply_filters()
    
    def apply_filters(self):
        """Apply search and category filters"""
        search_text = self.search_entry.get().lower()
        category = self.category_filter.get()
        
        # Filter results
        self.filtered_results = []
        for result in self.all_results:
            # Category filter
            if category != "All" and result.get('category', 'Other') != category:
                continue
            
            # Search filter
            if search_text:
                test_name = result.get('test_name', '').lower()
                if search_text not in test_name:
                    continue
            
            self.filtered_results.append(result)
        
        self.display_results()
    
    def display_results(self):
        """Display filtered results"""
        # Clear existing
        for widget in self.results_scroll.winfo_children():
            widget.destroy()
        
        if not self.filtered_results:
            no_data = ctk.CTkLabel(
                self.results_scroll,
                text="No lab results found" if not self.all_results else "No results match your filters",
                font=FONTS['body'],
                text_color=COLORS['text_secondary']
            )
            no_data.pack(pady=50)
            return
        
        # Group by date
        results_by_date = {}
        for result in self.filtered_results:
            date = result.get('date', 'Unknown')
            if date not in results_by_date:
                results_by_date[date] = []
            results_by_date[date].append(result)
        
        # Display by date (newest first)
        sorted_dates = sorted(results_by_date.keys(), reverse=True)
        
        for date in sorted_dates:
            # Date header
            date_header = ctk.CTkFrame(
                self.results_scroll,
                fg_color='transparent'
            )
            date_header.pack(fill='x', pady=(10, 5))
            
            date_label = ctk.CTkLabel(
                date_header,
                text=f"📅 {date}",
                font=FONTS['body_bold'],
                text_color=COLORS['text_primary']
            )
            date_label.pack(anchor='w')
            
            # Results for this date
            for result in results_by_date[date]:
                self.create_result_card(result)
    
    def create_result_card(self, result):
        """Create card for single lab result"""
        card = ctk.CTkFrame(
            self.results_scroll,
            fg_color=COLORS['bg_medium'],
            corner_radius=RADIUS['lg']
        )
        card.pack(fill='x', pady=5)
        
        content = ctk.CTkFrame(card, fg_color='transparent')
        content.pack(fill='both', padx=20, pady=15)
        
        # Header row
        header_row = ctk.CTkFrame(content, fg_color='transparent')
        header_row.pack(fill='x', pady=(0, 10))
        
        # Test name and category badge
        left_frame = ctk.CTkFrame(header_row, fg_color='transparent')
        left_frame.pack(side='left', fill='x', expand=True)
        
        test_name = ctk.CTkLabel(
            left_frame,
            text=f"🔬 {result.get('test_name', 'Unknown Test')}",
            font=FONTS['subheading'],
            text_color=COLORS['text_primary']
        )
        test_name.pack(side='left')
        
        # Category badge
        category = result.get('category', 'Other')
        badge_color = self.get_category_color(category)
        
        category_badge = ctk.CTkFrame(
            left_frame,
            fg_color=badge_color,
            corner_radius=RADIUS['sm'],
            height=24
        )
        category_badge.pack(side='left', padx=(10, 0))
        
        category_label = ctk.CTkLabel(
            category_badge,
            text=category,
            font=FONTS['small_bold'],
            text_color='white'
        )
        category_label.pack(padx=10, pady=3)
        
        # Status badge
        status = result.get('status', 'Completed')
        status_color = COLORS['success'] if status == 'Completed' else COLORS['warning']
        
        status_badge = ctk.CTkFrame(
            header_row,
            fg_color=status_color,
            corner_radius=RADIUS['sm'],
            height=24
        )
        status_badge.pack(side='right')
        
        status_label = ctk.CTkLabel(
            status_badge,
            text=status,
            font=FONTS['small_bold'],
            text_color='white'
        )
        status_label.pack(padx=10, pady=3)
        
        # Details
        details_frame = ctk.CTkFrame(content, fg_color='transparent')
        details_frame.pack(fill='x', pady=(0, 10))
        
        # Lab and Doctor
        lab_info = f"🏥 {result.get('lab_name', 'N/A')} | 👨‍⚕️ {result.get('ordered_by', 'N/A')}"
        lab_label = ctk.CTkLabel(
            details_frame,
            text=lab_info,
            font=FONTS['small'],
            text_color=COLORS['text_secondary']
        )
        lab_label.pack(anchor='w')
        
        # Values section
        if result.get('values'):
            values_frame = ctk.CTkFrame(
                content,
                fg_color=COLORS['bg_light'],
                corner_radius=RADIUS['md']
            )
            values_frame.pack(fill='x', pady=(0, 10))
            
            values_content = ctk.CTkFrame(values_frame, fg_color='transparent')
            values_content.pack(fill='x', padx=15, pady=12)
            
            # Display each value
            for value_data in result['values'][:3]:  # Show first 3
                value_row = ctk.CTkFrame(values_content, fg_color='transparent')
                value_row.pack(fill='x', pady=2)
                
                # Parameter name
                param_label = ctk.CTkLabel(
                    value_row,
                    text=value_data.get('parameter', 'N/A'),
                    font=FONTS['small'],
                    text_color=COLORS['text_secondary']
                )
                param_label.pack(side='left')
                
                # Value with unit
                value_text = f"{value_data.get('value', 'N/A')} {value_data.get('unit', '')}"
                value_label = ctk.CTkLabel(
                    value_row,
                    text=value_text,
                    font=FONTS['small_bold'],
                    text_color=COLORS['text_primary']
                )
                value_label.pack(side='right')
                
                # Reference range
                if value_data.get('reference_range'):
                    ref_label = ctk.CTkLabel(
                        value_row,
                        text=f"(Ref: {value_data['reference_range']})",
                        font=FONTS['small'],
                        text_color=COLORS['text_secondary']
                    )
                    ref_label.pack(side='right', padx=(10, 5))
            
            # Show more indicator
            if len(result.get('values', [])) > 3:
                more_label = ctk.CTkLabel(
                    values_content,
                    text=f"+ {len(result['values']) - 3} more values",
                    font=FONTS['small'],
                    text_color=COLORS['info']
                )
                more_label.pack(pady=(5, 0))
        
        # Notes
        if result.get('notes'):
            notes_label = ctk.CTkLabel(
                content,
                text=f"📝 {result['notes']}",
                font=FONTS['small'],
                text_color=COLORS['text_secondary'],
                wraplength=600
            )
            notes_label.pack(anchor='w', pady=(0, 10))
        
        # Actions
        actions_frame = ctk.CTkFrame(content, fg_color='transparent')
        actions_frame.pack(fill='x')
        
        # View full button
        view_btn = ctk.CTkButton(
            actions_frame,
            text="📄 View Full Report",
            command=lambda r=result: self.view_full_report(r),
            font=FONTS['small_bold'],
            height=35,
            fg_color=COLORS['info'],
            hover_color='#0284c7'
        )
        view_btn.pack(side='left', padx=(0, 10))
        
        # Download PDF (if available)
        if result.get('file_path'):
            download_btn = ctk.CTkButton(
                actions_frame,
                text="💾 Download PDF",
                command=lambda r=result: self.download_pdf(r),
                font=FONTS['small_bold'],
                height=35,
                fg_color=COLORS['secondary'],
                hover_color='#059669'
            )
            download_btn.pack(side='left')
    
    def get_category_color(self, category):
        """Get color for category badge"""
        colors = {
            'Blood Test': '#EF4444',
            'Urine Test': '#F59E0B',
            'Imaging': '#3B82F6',
            'Biopsy': '#8B5CF6',
            'Culture': '#10B981',
            'Other': '#6B7280'
        }
        return colors.get(category, '#6B7280')
    
    def view_full_report(self, result):
        """View full lab report"""
        # Create detailed view dialog
        dialog = ctk.CTkToplevel(self)
        dialog.title(f"Lab Result: {result.get('test_name', 'N/A')}")
        dialog.geometry("700x800")
        
        # Center on parent
        dialog.transient(self.winfo_toplevel())
        dialog.grab_set()
        
        # Header
        header = ctk.CTkFrame(dialog, fg_color=COLORS['bg_medium'])
        header.pack(fill='x', padx=30, pady=(30, 0))
        
        title = ctk.CTkLabel(
            header,
            text=result.get('test_name', 'Lab Result'),
            font=FONTS['heading'],
            text_color=COLORS['text_primary']
        )
        title.pack(padx=20, pady=15)
        
        # Content
        scroll = ctk.CTkScrollableFrame(dialog, fg_color='transparent')
        scroll.pack(fill='both', expand=True, padx=30, pady=20)
        
        # Date
        date_label = ctk.CTkLabel(
            scroll,
            text=f"📅 Date: {result.get('date', 'N/A')}",
            font=FONTS['body_bold'],
            text_color=COLORS['text_primary']
        )
        date_label.pack(anchor='w', pady=(0, 10))
        
        # Lab and Doctor
        lab_label = ctk.CTkLabel(
            scroll,
            text=f"🏥 Laboratory: {result.get('lab_name', 'N/A')}",
            font=FONTS['body'],
            text_color=COLORS['text_secondary']
        )
        lab_label.pack(anchor='w', pady=3)
        
        doctor_label = ctk.CTkLabel(
            scroll,
            text=f"👨‍⚕️ Ordered by: {result.get('ordered_by', 'N/A')}",
            font=FONTS['body'],
            text_color=COLORS['text_secondary']
        )
        doctor_label.pack(anchor='w', pady=3)
        
        # All values
        if result.get('values'):
            values_title = ctk.CTkLabel(
                scroll,
                text="Test Values:",
                font=FONTS['subheading'],
                text_color=COLORS['text_primary']
            )
            values_title.pack(anchor='w', pady=(20, 10))
            
            for value_data in result['values']:
                value_card = ctk.CTkFrame(
                    scroll,
                    fg_color=COLORS['bg_medium'],
                    corner_radius=RADIUS['md']
                )
                value_card.pack(fill='x', pady=5)
                
                value_content = ctk.CTkFrame(value_card, fg_color='transparent')
                value_content.pack(fill='x', padx=15, pady=12)
                
                # Parameter
                param = ctk.CTkLabel(
                    value_content,
                    text=value_data.get('parameter', 'N/A'),
                    font=FONTS['body_bold'],
                    text_color=COLORS['text_primary']
                )
                param.pack(anchor='w')
                
                # Value and unit
                value_text = f"Value: {value_data.get('value', 'N/A')} {value_data.get('unit', '')}"
                value_label = ctk.CTkLabel(
                    value_content,
                    text=value_text,
                    font=FONTS['body'],
                    text_color=COLORS['text_primary']
                )
                value_label.pack(anchor='w', pady=(5, 0))
                
                # Reference range
                if value_data.get('reference_range'):
                    ref_label = ctk.CTkLabel(
                        value_content,
                        text=f"Reference Range: {value_data['reference_range']}",
                        font=FONTS['small'],
                        text_color=COLORS['text_secondary']
                    )
                    ref_label.pack(anchor='w', pady=(3, 0))
        
        # Notes
        if result.get('notes'):
            notes_title = ctk.CTkLabel(
                scroll,
                text="Notes:",
                font=FONTS['subheading'],
                text_color=COLORS['text_primary']
            )
            notes_title.pack(anchor='w', pady=(20, 10))
            
            notes_text = ctk.CTkLabel(
                scroll,
                text=result['notes'],
                font=FONTS['body'],
                text_color=COLORS['text_secondary'],
                wraplength=600,
                justify='left'
            )
            notes_text.pack(anchor='w')
        
        # Close button
        close_btn = ctk.CTkButton(
            dialog,
            text="Close",
            command=dialog.destroy,
            font=FONTS['body_bold'],
            height=50,
            fg_color=COLORS['danger'],
            hover_color='#dc2626'
        )
        close_btn.pack(fill='x', padx=30, pady=(0, 30))
    
    def download_pdf(self, result):
        """Download PDF report"""
        file_path = result.get('file_path')
        if file_path and os.path.exists(file_path):
            messagebox.showinfo("Download", f"PDF available at: {file_path}")
        else:
            messagebox.showwarning("Not Available", "PDF file not found")
    
    def add_lab_result(self):
        """Open dialog to add new lab result (doctor only)"""
        messagebox.showinfo("Add Lab Result", "Lab result entry dialog would open here")
        # This would open a comprehensive lab entry dialog