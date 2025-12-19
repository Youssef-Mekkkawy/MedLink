"""
Enhanced Lab Results Manager Component - FIXED VERSION
Manages laboratory test results display and interaction
Location: gui/components/lab_results_manager.py
"""
import customtkinter as ctk
from gui.styles import *
from core.lab_manager import lab_manager
from datetime import datetime


class EnhancedLabResultsManager(ctk.CTkFrame):
    def __init__(self, parent, patient_data, is_doctor=False, on_add=None, on_view=None):
        """
        Initialize lab results manager
        
        Args:
            parent: Parent widget
            patient_data: Patient dict or object (NOT just ID!)
            is_doctor: Whether viewing as doctor (shows Add button)
            on_add: Optional callback for adding new results
            on_view: Optional callback for viewing detailed results
        """
        super().__init__(parent, fg_color='transparent')
        
        # DATABASE FIX: Convert and assign
        from gui.components.db_converter import convert_to_dict
        self.patient_data = convert_to_dict(patient_data)
        
        # Extract patient ID
        self.patient_id = self.patient_data.get('national_id')
        self.is_doctor = is_doctor
        self.on_add = on_add
        self.on_view = on_view
        self.all_results = []
        
        self.create_ui()
        self.load_results()
    
    def create_ui(self):
        """Create the lab results UI"""
        # Header with title and add button
        header = ctk.CTkFrame(self, fg_color='transparent')
        header.pack(fill='x', pady=(0, 15))
        
        # Title
        title = ctk.CTkLabel(
            header,
            text="🧪 Laboratory Results",
            font=FONTS['heading'],
            text_color=COLORS['text_primary']
        )
        title.pack(side='left')
        
        # Add button (if doctor or callback provided)
        if self.is_doctor or self.on_add:
            add_btn = ctk.CTkButton(
                header,
                text="➕ Add Result",
                command=self.on_add if self.on_add else self.show_add_dialog,
                font=FONTS['body_bold'],
                fg_color=COLORS['primary'],
                hover_color=COLORS['primary_hover'],
                height=35,
                width=120,
                corner_radius=RADIUS['md']
            )
            add_btn.pack(side='right')
        
        # Search and filter bar
        self.create_filter_bar()
        
        # Results container
        self.results_container = ctk.CTkScrollableFrame(
            self,
            fg_color='transparent',
            height=400
        )
        self.results_container.pack(fill='both', expand=True)
    
    def create_filter_bar(self):
        """Create search and filter controls"""
        filter_frame = ctk.CTkFrame(self, fg_color=COLORS['bg_light'], corner_radius=RADIUS['md'])
        filter_frame.pack(fill='x', pady=(0, 15))
        
        filter_content = ctk.CTkFrame(filter_frame, fg_color='transparent')
        filter_content.pack(fill='x', padx=15, pady=12)
        
        # Search box
        self.search_var = ctk.StringVar()
        search_entry = ctk.CTkEntry(
            filter_content,
            placeholder_text="🔍 Search by test name...",
            textvariable=self.search_var,
            fg_color=COLORS['bg_medium'],
            border_color=COLORS['secondary'],
            height=35,
            width=250,
            corner_radius=RADIUS['md']
        )
        search_entry.pack(side='left', padx=(0, 10))
        search_entry.bind('<KeyRelease>', lambda e: self.filter_results())
        
        # Filter by category
        self.category_var = ctk.StringVar(value="All Categories")
        category_menu = ctk.CTkOptionMenu(
            filter_content,
            variable=self.category_var,
            values=["All Categories", "Blood Test", "Urine Test", "Imaging", "Other"],
            command=lambda x: self.filter_results(),
            fg_color=COLORS['bg_medium'],
            button_color=COLORS['primary'],
            height=35,
            width=150,
            corner_radius=RADIUS['md']
        )
        category_menu.pack(side='left', padx=(0, 10))
        
        # Sort options
        self.sort_var = ctk.StringVar(value="Newest First")
        sort_menu = ctk.CTkOptionMenu(
            filter_content,
            variable=self.sort_var,
            values=["Newest First", "Oldest First", "Test Name A-Z"],
            command=lambda x: self.filter_results(),
            fg_color=COLORS['bg_medium'],
            button_color=COLORS['primary'],
            height=35,
            width=150,
            corner_radius=RADIUS['md']
        )
        sort_menu.pack(side='left')
    
    def load_results(self):
        """Load lab results for patient"""
        try:
            self.all_results = lab_manager.get_patient_lab_results(self.patient_id)
            self.filter_results()
        except Exception as e:
            print(f"Error loading lab results: {e}")
            self.show_no_results("Error loading results")
    
    def filter_results(self):
        """Filter and sort results based on current filters"""
        # Clear current results
        for widget in self.results_container.winfo_children():
            widget.destroy()
        
        if not self.all_results:
            self.show_no_results("No lab results found")
            return
        
        # Apply filters
        filtered = self.all_results.copy()
        
        # Search filter
        search_term = self.search_var.get().lower()
        if search_term:
            filtered = [r for r in filtered if search_term in r.get('test_name', '').lower()]
        
        # Category filter
        category = self.category_var.get()
        if category != "All Categories":
            filtered = [r for r in filtered if r.get('test_category', '') == category]
        
        # Sort
        sort_option = self.sort_var.get()
        if sort_option == "Newest First":
            filtered.sort(key=lambda x: x.get('test_date', ''), reverse=True)
        elif sort_option == "Oldest First":
            filtered.sort(key=lambda x: x.get('test_date', ''))
        elif sort_option == "Test Name A-Z":
            filtered.sort(key=lambda x: x.get('test_name', ''))
        
        # Display filtered results
        if filtered:
            for result in filtered:
                self.create_result_card(result)
        else:
            self.show_no_results("No results match your filters")
    
    def create_result_card(self, result):
        """Create a card for a single lab result"""
        card = ctk.CTkFrame(
            self.results_container,
            fg_color=COLORS['bg_medium'],
            corner_radius=RADIUS['md'],
            border_width=1,
            border_color=COLORS['secondary']
        )
        card.pack(fill='x', pady=(0, 10))
        
        content = ctk.CTkFrame(card, fg_color='transparent')
        content.pack(fill='both', expand=True, padx=15, pady=15)
        
        # Header row
        header_row = ctk.CTkFrame(content, fg_color='transparent')
        header_row.pack(fill='x')
        
        # Test icon and name
        name_frame = ctk.CTkFrame(header_row, fg_color='transparent')
        name_frame.pack(side='left', fill='x', expand=True)
        
        test_name = ctk.CTkLabel(
            name_frame,
            text=f"🧪 {result.get('test_name', 'Unknown Test')}",
            font=FONTS['subheading'],
            text_color=COLORS['text_primary'],
            anchor='w'
        )
        test_name.pack(anchor='w')
        
        # Date
        meta_text = f"📅 {self.format_date(result.get('test_date', 'N/A'))}"
        meta_label = ctk.CTkLabel(
            name_frame,
            text=meta_text,
            font=FONTS['small'],
            text_color=COLORS['text_secondary'],
            anchor='w'
        )
        meta_label.pack(anchor='w', pady=(2, 0))
        
        # Status badge
        status = result.get('status', 'Completed')
        status_color = COLORS['success'] if status == 'Completed' else COLORS['warning']
        
        status_badge = ctk.CTkLabel(
            header_row,
            text=status,
            font=FONTS['small_bold'],
            text_color='white',
            fg_color=status_color,
            corner_radius=RADIUS['sm'],
            width=80,
            height=25
        )
        status_badge.pack(side='right', padx=(10, 0))
        
        # Result value
        if result.get('result_value'):
            value_text = f"Result: {result['result_value']}"
            if result.get('unit'):
                value_text += f" {result['unit']}"
            
            # Color based on abnormal
            value_color = COLORS['error'] if result.get('is_abnormal') else COLORS['success']
            
            value_label = ctk.CTkLabel(
                content,
                text=value_text,
                font=FONTS['body'],
                text_color=value_color,
                anchor='w'
            )
            value_label.pack(anchor='w', pady=(10, 0))
            
            # Reference range
            if result.get('reference_range'):
                range_label = ctk.CTkLabel(
                    content,
                    text=f"Reference: {result['reference_range']}",
                    font=FONTS['small'],
                    text_color=COLORS['text_secondary'],
                    anchor='w'
                )
                range_label.pack(anchor='w', pady=(3, 0))
        
        # Lab name
        if result.get('lab_name'):
            lab_label = ctk.CTkLabel(
                content,
                text=f"🏥 {result['lab_name']}",
                font=FONTS['small'],
                text_color=COLORS['text_secondary'],
                anchor='w'
            )
            lab_label.pack(anchor='w', pady=(5, 0))
    
    def show_no_results(self, message="No lab results available"):
        """Show no results message"""
        no_results = ctk.CTkFrame(
            self.results_container,
            fg_color=COLORS['bg_medium'],
            corner_radius=RADIUS['md'],
            height=150
        )
        no_results.pack(fill='x', pady=20)
        no_results.pack_propagate(False)
        
        label = ctk.CTkLabel(
            no_results,
            text=f"🧪\n{message}",
            font=FONTS['subheading'],
            text_color=COLORS['text_secondary']
        )
        label.place(relx=0.5, rely=0.5, anchor='center')
    
    def format_date(self, date_str):
        """Format date string for display"""
        try:
            if isinstance(date_str, str):
                date_obj = datetime.strptime(date_str, '%Y-%m-%d')
                return date_obj.strftime('%B %d, %Y')
            return str(date_str)
        except:
            return str(date_str)
    
    def show_add_dialog(self):
        """Show dialog to add lab result"""
        from tkinter import messagebox
        messagebox.showinfo(
            "Add Lab Result",
            "Add Lab Result dialog coming soon!\n\n"
            "This will allow doctors to add new lab results."
        )
    
    def refresh(self):
        """Refresh results list"""
        self.load_results()


# Backwards compatibility alias
class LabResultsManager(EnhancedLabResultsManager):
    """Alias for backwards compatibility"""
    pass