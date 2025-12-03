"""
Emergency Dialog - UPDATED to use shared component
Location: gui/components/emergency_dialog.py

This is just a THIN WRAPPER around EmergencyCardContent.
All UI is defined in emergency_card_content.py
"""
import customtkinter as ctk
from gui.components.emergency_card_content import EmergencyCardContent


class EmergencyDialog(ctk.CTkToplevel):
    """Emergency card display dialog - uses shared EmergencyCardContent"""

    def __init__(self, parent, patient_data):
        super().__init__(parent)

        self.patient_data = patient_data

        # Configure window
        self.title("Emergency Card")
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

        # Create emergency card content with Close button
        self.content = EmergencyCardContent(
            self, 
            patient_data, 
            show_close_button=True  # Dialog needs Close button
        )
        self.content.pack(fill='both', expand=True)

