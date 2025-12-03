"""
Sidebar navigation component - MINIMAL FIX VERSION
Only makes buttons work, keeps original design!
"""
import customtkinter as ctk
from tkinter import messagebox
from gui.styles import *


class Sidebar(ctk.CTkFrame):
    """Modern sidebar with navigation"""
    
    def __init__(self, parent, user_data, on_logout):
        super().__init__(
            parent,
            fg_color=COLORS['bg_medium'],
            corner_radius=0,
            width=260
        )
        
        self.user_data = user_data
        self.on_logout = on_logout
        
        self.pack_propagate(False)
        self.create_ui()
    
    def create_ui(self):
        """Create sidebar content"""
        # Header with logo
        header_frame = ctk.CTkFrame(self, fg_color='transparent')
        header_frame.pack(fill='x', padx=20, pady=(30, 20))
        
        logo_label = ctk.CTkLabel(
            header_frame,
            text="🏥",
            font=('Segoe UI', 36)
        )
        logo_label.pack()
        
        app_name = ctk.CTkLabel(
            header_frame,
            text="MedLink",
            font=('Segoe UI', 20, 'bold'),
            text_color=COLORS['text_primary']
        )
        app_name.pack(pady=(5, 0))
        
        # Divider
        ctk.CTkFrame(
            self,
            height=1,
            fg_color=COLORS['bg_hover']
        ).pack(fill='x', padx=20, pady=20)
        
        # User info card
        user_card = ctk.CTkFrame(
            self,
            fg_color=COLORS['bg_light'],
            corner_radius=RADIUS['md']
        )
        user_card.pack(fill='x', padx=20, pady=(0, 30))
        
        user_content = ctk.CTkFrame(user_card, fg_color='transparent')
        user_content.pack(fill='x', padx=15, pady=15)
        
        # User icon
        icon = ctk.CTkLabel(
            user_content,
            text="👨‍⚕️",
            font=('Segoe UI', 32)
        )
        icon.pack()
        
        # User name
        name_label = ctk.CTkLabel(
            user_content,
            text=self.user_data.get('full_name', 'Doctor'),
            font=FONTS['body_bold'],
            text_color=COLORS['text_primary']
        )
        name_label.pack(pady=(5, 0))
        
        # Specialization
        spec_label = ctk.CTkLabel(
            user_content,
            text=self.user_data.get('specialization', 'General'),
            font=FONTS['small'],
            text_color=COLORS['text_secondary']
        )
        spec_label.pack()
        
        # Navigation menu
        nav_frame = ctk.CTkFrame(self, fg_color='transparent')
        nav_frame.pack(fill='both', expand=True, padx=20)
        
        # Menu items with working commands
        self.create_nav_button(
            nav_frame, "🏠  Dashboard", active=True,
            command=lambda: messagebox.showinfo(
                "Dashboard", 
                "You're already on the Dashboard!"
            )
        )
        
        self.create_nav_button(
            nav_frame, "👥  All Patients",
            command=lambda: messagebox.showinfo(
                "All Patients",
                "All Patients view coming soon!\n\n"
                "This will show a list of all patients\n"
                "in the system."
            )
        )
        
        self.create_nav_button(
            nav_frame, "📅  Appointments",
            command=lambda: messagebox.showinfo(
                "Appointments",
                "Appointment scheduling coming soon!\n\n"
                "Features:\n"
                "• Schedule appointments\n"
                "• View calendar\n"
                "• Send reminders"
            )
        )
        
        self.create_nav_button(
            nav_frame, "📊  Statistics",
            command=lambda: messagebox.showinfo(
                "Statistics",
                "Statistics dashboard coming soon!\n\n"
                "Features:\n"
                "• Patient statistics\n"
                "• Visit trends\n"
                "• Performance metrics"
            )
        )
        
        self.create_nav_button(
            nav_frame, "⚙️  Settings",
            command=lambda: messagebox.showinfo(
                "Settings",
                "Settings panel coming soon!\n\n"
                "Features:\n"
                "• Profile settings\n"
                "• System preferences\n"
                "• Security options"
            )
        )
        
        # Spacer
        ctk.CTkFrame(nav_frame, fg_color='transparent', height=20).pack()
        
        # Logout button at bottom
        logout_btn = ctk.CTkButton(
            self,
            text="🚪  Logout",
            command=self.on_logout,
            font=FONTS['body'],
            height=45,
            corner_radius=RADIUS['md'],
            fg_color=COLORS['danger'],
            hover_color='#b91c1c',
            text_color=COLORS['text_primary']
        )
        logout_btn.pack(side='bottom', fill='x', padx=20, pady=20)
    
    def create_nav_button(self, parent, text, active=False, command=None):
        """Create a navigation button"""
        btn = ctk.CTkButton(
            parent,
            text=text,
            command=command,
            font=FONTS['body'],
            height=45,
            corner_radius=RADIUS['md'],
            fg_color=COLORS['primary'] if active else 'transparent',
            hover_color=COLORS['bg_hover'],
            anchor='w',
            text_color=COLORS['text_primary']
        )
        btn.pack(fill='x', pady=(0, 8))
        return btn