"""
Patient's own medical history view (read-only)
"""
import customtkinter as ctk
from gui.styles import *
from gui.components.visit_card import VisitCard
from core.visit_manager import visit_manager


class MyHistoryTab(ctk.CTkFrame):
    """Patient's medical history view (read-only)"""
    
    def __init__(self, parent, patient_data):
        super().__init__(parent, fg_color='transparent')
        
        self.patient_data = patient_data
        
        self.create_ui()
        self.load_visits()
    
    def create_ui(self):
        """Create history view UI"""
        # Header
        header = ctk.CTkFrame(self, fg_color=COLORS['bg_medium'], height=80)
        header.pack(fill='x', pady=(0, 20))
        header.pack_propagate(False)
        
        header_content = ctk.CTkFrame(header, fg_color='transparent')
        header_content.pack(fill='both', expand=True, padx=20, pady=15)
        
        title_label = ctk.CTkLabel(
            header_content,
            text="📋  My Medical History",
            font=FONTS['heading'],
            text_color=COLORS['text_primary']
        )
        title_label.pack(side='left')
        
        # Visit count
        self.count_label = ctk.CTkLabel(
            header_content,
            text="",
            font=FONTS['body'],
            text_color=COLORS['text_secondary']
        )
        self.count_label.pack(side='right')
        
        # Scrollable visits container
        self.visits_scroll = ctk.CTkScrollableFrame(
            self,
            fg_color='transparent'
        )
        self.visits_scroll.pack(fill='both', expand=True)
    
    def load_visits(self):
        """Load and display visit history"""
        # Clear existing
        for widget in self.visits_scroll.winfo_children():
            widget.destroy()
        
        # Get visits
        national_id = self.patient_data.get('national_id')
        visits = visit_manager.get_patient_visits(national_id)
        
        # Update count
        self.count_label.configure(text=f"{len(visits)} total visits")
        
        if not visits:
            self.show_empty_state()
            return
        
        # Display visits
        for visit in visits:
            visit_card = VisitCard(self.visits_scroll, visit)
            visit_card.pack(fill='x', pady=10)
    
    def show_empty_state(self):
        """Show empty state"""
        empty_frame = ctk.CTkFrame(
            self.visits_scroll,
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
            text="📋",
            font=('Segoe UI', 64)
        )
        icon_label.pack()
        
        text_label = ctk.CTkLabel(
            empty_content,
            text="No Medical History Yet",
            font=FONTS['heading'],
            text_color=COLORS['text_muted']
        )
        text_label.pack(pady=(10, 5))
        
        hint_label = ctk.CTkLabel(
            empty_content,
            text="Your visit records will appear here",
            font=FONTS['body'],
            text_color=COLORS['text_muted']
        )
        hint_label.pack()