"""
Emergency Card Tab - WORKING VERSION
Location: gui/components/emergency_card_tab.py

REPLACE YOUR ENTIRE emergency_card_tab.py WITH THIS FILE!
"""
import customtkinter as ctk
from gui.components.emergency_card_content import EmergencyCardContent


class EmergencyCardTab(ctk.CTkFrame):
    """Emergency card tab - uses shared EmergencyCardContent"""
    
    def __init__(self, parent, patient_data):
        super().__init__(parent, fg_color='transparent')
        
        self.patient_data = patient_data
        
        # Create emergency card content without Close button
        self.content = EmergencyCardContent(
            self, 
            patient_data, 
            show_close_button=False  # Tab doesn't need Close button
        )
        self.content.pack(fill='both', expand=True)