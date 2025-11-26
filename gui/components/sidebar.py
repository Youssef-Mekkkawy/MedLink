"""
Sidebar navigation component
"""
import customtkinter as ctk
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
        
        # Menu items
        self.create_nav_button(nav_frame, "🏠  Dashboard", active=True)
        self.create_nav_button(nav_frame, "👥  All Patients")
        self.create_nav_button(nav_frame, "📅  Appointments")
        self.create_nav_button(nav_frame, "📊  Statistics")
        self.create_nav_button(nav_frame, "⚙️  Settings")
        
        # Spacer
        ctk.CTkFrame(nav_frame, fg_color='transparent').pack(expand=True)
        
        # Logout button at bottom
        logout_btn = ctk.CTkButton(
            self,
            text="🚪  Logout",
            command=self.on_logout,
            font=FONTS['body'],
            fg_color='transparent',
            hover_color=COLORS['danger'],
            height=45,
            anchor='w'
        )
        logout_btn.pack(fill='x', padx=20, pady=20, side='bottom')
    
    def create_nav_button(self, parent, text, active=False):
        """Create navigation button"""
        fg_color = COLORS['primary'] if active else 'transparent'
        hover_color = COLORS['primary_hover'] if active else COLORS['bg_light']
        
        btn = ctk.CTkButton(
            parent,
            text=text,
            font=FONTS['body'],
            fg_color=fg_color,
            hover_color=hover_color,
            height=45,
            corner_radius=RADIUS['md'],
            anchor='w'
        )
        btn.pack(fill='x', pady=5)
        return btn