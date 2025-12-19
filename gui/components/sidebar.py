"""
Sidebar navigation component - FIXED VERSION
Location: gui/components/sidebar.py
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
        
        # DATABASE FIX: Convert user_data (not patient_data!)
        from gui.components.db_converter import convert_to_dict
        self.user_data = convert_to_dict(user_data)
        self.on_logout = on_logout
        
        self.pack_propagate(False)
        
        self.create_header()
        self.create_navigation()
        self.create_footer()
    
    def create_header(self):
        """Create user info header"""
        header = ctk.CTkFrame(
            self,
            fg_color='transparent',
            height=120
        )
        header.pack(fill='x', pady=(20, 30), padx=20)
        header.pack_propagate(False)
        
        # Profile icon
        icon_frame = ctk.CTkFrame(
            header,
            fg_color=COLORS['primary'],
            corner_radius=35,
            width=70,
            height=70
        )
        icon_frame.pack()
        icon_frame.pack_propagate(False)
        
        icon_label = ctk.CTkLabel(
            icon_frame,
            text="👤",
            font=('Segoe UI', 32)
        )
        icon_label.place(relx=0.5, rely=0.5, anchor='center')
        
        # User name
        name = self.user_data.get('full_name', 'User')
        name_label = ctk.CTkLabel(
            header,
            text=name,
            font=FONTS['subheading'],
            text_color=COLORS['text_primary']
        )
        name_label.pack(pady=(10, 2))
        
        # Role
        role = self.user_data.get('role', 'User')
        role_label = ctk.CTkLabel(
            header,
            text=role.title(),
            font=FONTS['small'],
            text_color=COLORS['text_secondary']
        )
        role_label.pack()
    
    def create_navigation(self):
        """Create navigation buttons"""
        nav_frame = ctk.CTkFrame(self, fg_color='transparent')
        nav_frame.pack(fill='both', expand=True, pady=(0, 20))
        
        # Navigation items based on role
        role = self.user_data.get('role', 'user')
        
        if role.lower() == 'doctor':
            nav_items = [
                ("🏠", "Dashboard", self.show_dashboard),
                ("👥", "Patients", self.show_patients),
                ("📋", "My Schedule", self.show_schedule),
                ("⚙️", "Settings", self.show_settings)
            ]
        elif role.lower() == 'patient':
            nav_items = [
                ("🏠", "Dashboard", self.show_dashboard),
                ("📋", "My Records", self.show_records),
                ("🗓️", "Appointments", self.show_appointments),
                ("⚙️", "Settings", self.show_settings)
            ]
        else:
            nav_items = [
                ("🏠", "Dashboard", self.show_dashboard),
                ("⚙️", "Settings", self.show_settings)
            ]
        
        for icon, text, command in nav_items:
            self.create_nav_button(nav_frame, icon, text, command)
    
    def create_nav_button(self, parent, icon, text, command):
        """Create a navigation button"""
        btn = ctk.CTkButton(
            parent,
            text=f"{icon}  {text}",
            command=command,
            font=FONTS['body'],
            fg_color='transparent',
            hover_color=COLORS['bg_light'],
            anchor='w',
            height=45
        )
        btn.pack(fill='x', padx=15, pady=2)
    
    def create_footer(self):
        """Create footer with logout"""
        footer = ctk.CTkFrame(
            self,
            fg_color='transparent',
            height=80
        )
        footer.pack(fill='x', side='bottom', pady=20, padx=20)
        footer.pack_propagate(False)
        
        # Logout button
        logout_btn = ctk.CTkButton(
            footer,
            text="🚪 Logout",
            command=self.handle_logout,
            font=FONTS['body_bold'],
            fg_color=COLORS['danger'],
            hover_color='#991b1b',
            height=45
        )
        logout_btn.pack(fill='x')
    
    def show_dashboard(self):
        """Show dashboard"""
        messagebox.showinfo("Navigation", "Dashboard")
    
    def show_patients(self):
        """Show patients list"""
        messagebox.showinfo("Navigation", "Patients List")
    
    def show_schedule(self):
        """Show schedule"""
        messagebox.showinfo("Navigation", "My Schedule")
    
    def show_records(self):
        """Show medical records"""
        messagebox.showinfo("Navigation", "My Medical Records")
    
    def show_appointments(self):
        """Show appointments"""
        messagebox.showinfo("Navigation", "My Appointments")
    
    def show_settings(self):
        """Show settings"""
        messagebox.showinfo("Navigation", "Settings")
    
    def handle_logout(self):
        """Handle logout"""
        result = messagebox.askyesno(
            "Logout",
            "Are you sure you want to logout?",
            parent=self
        )
        if result and self.on_logout:
            self.on_logout()