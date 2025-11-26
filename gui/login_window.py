"""
Login window - Beautiful modern design
"""
import customtkinter as ctk
from tkinter import messagebox
from gui.styles import *
from core.auth_manager import auth_manager
from utils.validators import validate_national_id
from config.localization import get_string as _


class LoginWindow(ctk.CTk):
    """Modern login window with professional design"""

    def __init__(self):
        super().__init__()

        # Configure window
        self.title("MedLink - Medical Records System")
        self.geometry("900x600")
        self.resizable(False, False)

        # Setup theme
        setup_theme()

        # Center window
        self.center_window()

        # Create UI
        self.create_ui()

    def center_window(self):
        """Center window on screen"""
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f'{width}x{height}+{x}+{y}')

    def create_ui(self):
        """Create beautiful login interface"""
        # Main container with gradient effect
        main_container = ctk.CTkFrame(self, fg_color=COLORS['bg_dark'])
        main_container.pack(fill='both', expand=True)

        # Left side - Branding and info
        left_panel = ctk.CTkFrame(
            main_container,
            fg_color=COLORS['primary'],
            corner_radius=0
        )
        left_panel.pack(side='left', fill='both', expand=True)

        # Branding content
        branding_frame = ctk.CTkFrame(left_panel, fg_color='transparent')
        branding_frame.place(relx=0.5, rely=0.5, anchor='center')

        # Large medical icon
        icon_label = ctk.CTkLabel(
            branding_frame,
            text="🏥",
            font=('Segoe UI', 80)
        )
        icon_label.pack(pady=(0, 20))

        # App name with modern styling
        app_name = ctk.CTkLabel(
            branding_frame,
            text="MedLink",
            font=('Segoe UI', 42, 'bold'),
            text_color='white'
        )
        app_name.pack()

        # Tagline
        tagline = ctk.CTkLabel(
            branding_frame,
            text="Unified Medical Records System",
            font=('Segoe UI', 16),
            text_color='#e0e7ff'
        )
        tagline.pack(pady=(10, 40))

        # Features list
        features = [
            "🔐 Secure & Encrypted",
            "⚡ Lightning Fast Access",
            "📱 Emergency Ready",
            "🌐 Multi-Platform"
        ]

        for feature in features:
            feature_label = ctk.CTkLabel(
                branding_frame,
                text=feature,
                font=('Segoe UI', 14),
                text_color='#e0e7ff',
                anchor='w'
            )
            feature_label.pack(pady=5, anchor='w')

        # Right side - Login form
        right_panel = ctk.CTkFrame(
            main_container,
            fg_color=COLORS['bg_dark'],
            corner_radius=0
        )
        right_panel.pack(side='right', fill='both', expand=True)

        # Form container - centered
        form_container = ctk.CTkFrame(right_panel, fg_color='transparent')
        form_container.place(relx=0.5, rely=0.5, anchor='center')

        # Welcome text
        welcome_label = ctk.CTkLabel(
            form_container,
            text="Welcome Back!",
            font=('Segoe UI', 32, 'bold'),
            text_color=COLORS['text_primary']
        )
        welcome_label.pack(pady=(0, 10))

        subtitle_label = ctk.CTkLabel(
            form_container,
            text="Sign in to continue to MedLink",
            font=('Segoe UI', 13),
            text_color=COLORS['text_secondary']
        )
        subtitle_label.pack(pady=(0, 40))

        # Login card
        login_card = ctk.CTkFrame(
            form_container,
            fg_color=COLORS['bg_medium'],
            corner_radius=RADIUS['lg'],
            width=380,
            height=450
        )
        login_card.pack_propagate(False)
        login_card.pack()

        # Card content with padding
        card_content = ctk.CTkFrame(login_card, fg_color='transparent')
        card_content.pack(fill='both', expand=True, padx=35, pady=35)

        # Role selection with modern tabs
        role_label = ctk.CTkLabel(
            card_content,
            text="I am a",
            font=FONTS['subheading'],
            text_color=COLORS['text_primary']
        )
        role_label.pack(anchor='w', pady=(0, 15))

        # Modern segmented button for role
        self.role_var = ctk.StringVar(value="doctor")

        role_segment = ctk.CTkSegmentedButton(
            card_content,
            values=["doctor", "patient"],
            variable=self.role_var,
            font=FONTS['body'],
            height=45
        )
        role_segment.pack(fill='x', pady=(0, 25))

        # Username field with icon
        username_frame = ctk.CTkFrame(card_content, fg_color='transparent')
        username_frame.pack(fill='x', pady=(0, 20))

        username_label = ctk.CTkLabel(
            username_frame,
            text="👤  Username",
            font=FONTS['body_bold'],
            text_color=COLORS['text_primary']
        )
        username_label.pack(anchor='w', pady=(0, 8))

        self.username_entry = ctk.CTkEntry(
            username_frame,
            placeholder_text="Enter your username",
            font=FONTS['body'],
            height=45,
            corner_radius=RADIUS['md'],
            border_width=2,
            fg_color=COLORS['bg_light'],
            border_color=COLORS['bg_hover']
        )
        self.username_entry.pack(fill='x')

        # Password field with icon
        password_frame = ctk.CTkFrame(card_content, fg_color='transparent')
        password_frame.pack(fill='x', pady=(0, 30))

        password_label = ctk.CTkLabel(
            password_frame,
            text="🔒  Password",
            font=FONTS['body_bold'],
            text_color=COLORS['text_primary']
        )
        password_label.pack(anchor='w', pady=(0, 8))

        self.password_entry = ctk.CTkEntry(
            password_frame,
            placeholder_text="Enter your password",
            font=FONTS['body'],
            height=45,
            corner_radius=RADIUS['md'],
            border_width=2,
            show="●",
            fg_color=COLORS['bg_light'],
            border_color=COLORS['bg_hover']
        )
        self.password_entry.pack(fill='x')

        # Bind Enter key
        self.password_entry.bind('<Return>', lambda e: self.handle_login())

        # Login button - large and prominent
        login_btn = ctk.CTkButton(
            card_content,
            text="Sign In",
            command=self.handle_login,
            font=('Segoe UI', 14, 'bold'),
            height=50,
            corner_radius=RADIUS['md'],
            fg_color=COLORS['primary'],
            hover_color=COLORS['primary_hover']
        )
        login_btn.pack(fill='x', pady=(0, 20))

        # Divider
        divider_frame = ctk.CTkFrame(card_content, fg_color='transparent')
        divider_frame.pack(fill='x', pady=(0, 20))

        ctk.CTkFrame(
            divider_frame,
            height=1,
            fg_color=COLORS['bg_hover']
        ).pack(side='left', fill='x', expand=True)

        ctk.CTkLabel(
            divider_frame,
            text="  OR  ",
            font=FONTS['small'],
            text_color=COLORS['text_muted']
        ).pack(side='left')

        ctk.CTkFrame(
            divider_frame,
            height=1,
            fg_color=COLORS['bg_hover']
        ).pack(side='left', fill='x', expand=True)

        # Register button
        register_btn = ctk.CTkButton(
            card_content,
            text="Create Patient Account",
            command=self.show_register_dialog,
            font=FONTS['body'],
            height=45,
            corner_radius=RADIUS['md'],
            fg_color='transparent',
            hover_color=COLORS['bg_light'],
            border_width=2,
            border_color=COLORS['secondary'],
            text_color=COLORS['secondary']
        )
        register_btn.pack(fill='x')

        # Footer
        footer_label = ctk.CTkLabel(
            right_panel,
            text="v1.0.0 | © 2024 MedLink Systems",
            font=FONTS['small'],
            text_color=COLORS['text_muted']
        )
        footer_label.pack(side='bottom', pady=20)

    def handle_login(self):
        """Handle login button click"""
        username = self.username_entry.get().strip()
        password = self.password_entry.get()
        role = self.role_var.get()

        # Validate inputs
        if not username or not password:
            messagebox.showerror(
                "Input Required",
                "Please enter both username and password"
            )
            return

        # Attempt login
        success, message, user_data = auth_manager.login(
            username, password, role)

        if success:
            # Close login window and open appropriate dashboard
            self.withdraw()
            self.open_dashboard(role, user_data)
        else:
            messagebox.showerror("Login Failed", message)
            # Clear password field
            self.password_entry.delete(0, 'end')

    def open_dashboard(self, role: str, user_data: dict):
        """Open appropriate dashboard based on role"""
        try:
            if role == 'doctor':
                from gui.doctor_dashboard import DoctorDashboard
                dashboard = DoctorDashboard(self, user_data)
                dashboard.deiconify()  # Ensure window is visible
            else:
                from gui.patient_dashboard import PatientDashboard
                dashboard = PatientDashboard(self, user_data)
                dashboard.deiconify()  # Ensure window is visible

            dashboard.protocol("WM_DELETE_WINDOW",
                            lambda: self.on_dashboard_close(dashboard))
        except Exception as e:
            messagebox.showerror("Error", f"Failed to open dashboard: {str(e)}")
            print(f"Dashboard error: {e}")  # Debug info
            self.deiconify()  # Show login again

    def on_dashboard_close(self, dashboard):
        """Handle dashboard window close"""
        dashboard.destroy()
        auth_manager.logout()
        self.deiconify()
        self.username_entry.delete(0, 'end')
        self.password_entry.delete(0, 'end')

    def show_register_dialog(self):
        """Show patient registration dialog"""
        dialog = RegisterDialog(self)
        dialog.wait_window()


class RegisterDialog(ctk.CTkToplevel):
    """Modern patient registration dialog"""

    def __init__(self, parent):
        super().__init__(parent)

        self.title("Create Patient Account")
        self.geometry("500x650")
        self.resizable(False, False)

        # Center on parent
        self.transient(parent)
        self.grab_set()

        # Center window
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = parent.winfo_x() + (parent.winfo_width() // 2) - (width // 2)
        y = parent.winfo_y() + (parent.winfo_height() // 2) - (height // 2)
        self.geometry(f'{width}x{height}+{x}+{y}')

        self.create_ui()

    def create_ui(self):
        """Create registration form"""
        main_frame = ctk.CTkFrame(self, fg_color=COLORS['bg_dark'])
        main_frame.pack(fill='both', expand=True, padx=40, pady=40)

        # Header
        header_frame = ctk.CTkFrame(main_frame, fg_color='transparent')
        header_frame.pack(fill='x', pady=(0, 30))

        # Icon
        icon_label = ctk.CTkLabel(
            header_frame,
            text="📝",
            font=('Segoe UI', 48)
        )
        icon_label.pack()

        # Title
        title_label = ctk.CTkLabel(
            header_frame,
            text="Patient Registration",
            font=('Segoe UI', 28, 'bold'),
            text_color=COLORS['text_primary']
        )
        title_label.pack(pady=(10, 0))

        subtitle_label = ctk.CTkLabel(
            header_frame,
            text="Create your medical records account",
            font=FONTS['body'],
            text_color=COLORS['text_secondary']
        )
        subtitle_label.pack(pady=(5, 0))

        # Form card
        form_card = ctk.CTkFrame(
            main_frame,
            fg_color=COLORS['bg_medium'],
            corner_radius=RADIUS['lg']
        )
        form_card.pack(fill='both', expand=True)

        form_content = ctk.CTkFrame(form_card, fg_color='transparent')
        form_content.pack(fill='both', expand=True, padx=30, pady=30)

        # National ID
        id_label = ctk.CTkLabel(
            form_content,
            text="🆔  National ID (14 digits)",
            font=FONTS['body_bold'],
            text_color=COLORS['text_primary']
        )
        id_label.pack(anchor='w', pady=(0, 8))

        self.id_entry = ctk.CTkEntry(
            form_content,
            placeholder_text="29501012345678",
            font=FONTS['body'],
            height=45,
            corner_radius=RADIUS['md'],
            border_width=2,
            fg_color=COLORS['bg_light'],
            border_color=COLORS['bg_hover']
        )
        self.id_entry.pack(fill='x', pady=(0, 20))

        # Full name
        name_label = ctk.CTkLabel(
            form_content,
            text="👤  Full Name",
            font=FONTS['body_bold'],
            text_color=COLORS['text_primary']
        )
        name_label.pack(anchor='w', pady=(0, 8))

        self.name_entry = ctk.CTkEntry(
            form_content,
            placeholder_text="Mohamed Ali Hassan",
            font=FONTS['body'],
            height=45,
            corner_radius=RADIUS['md'],
            border_width=2,
            fg_color=COLORS['bg_light'],
            border_color=COLORS['bg_hover']
        )
        self.name_entry.pack(fill='x', pady=(0, 20))

        # Password
        pass_label = ctk.CTkLabel(
            form_content,
            text="🔒  Password (minimum 6 characters)",
            font=FONTS['body_bold'],
            text_color=COLORS['text_primary']
        )
        pass_label.pack(anchor='w', pady=(0, 8))

        self.pass_entry = ctk.CTkEntry(
            form_content,
            placeholder_text="Enter password",
            font=FONTS['body'],
            height=45,
            corner_radius=RADIUS['md'],
            border_width=2,
            show="●",
            fg_color=COLORS['bg_light'],
            border_color=COLORS['bg_hover']
        )
        self.pass_entry.pack(fill='x', pady=(0, 20))

        # Confirm password
        confirm_label = ctk.CTkLabel(
            form_content,
            text="🔒  Confirm Password",
            font=FONTS['body_bold'],
            text_color=COLORS['text_primary']
        )
        confirm_label.pack(anchor='w', pady=(0, 8))

        self.confirm_entry = ctk.CTkEntry(
            form_content,
            placeholder_text="Re-enter password",
            font=FONTS['body'],
            height=45,
            corner_radius=RADIUS['md'],
            border_width=2,
            show="●",
            fg_color=COLORS['bg_light'],
            border_color=COLORS['bg_hover']
        )
        self.confirm_entry.pack(fill='x', pady=(0, 30))

        # Buttons
        btn_frame = ctk.CTkFrame(form_content, fg_color='transparent')
        btn_frame.pack(fill='x')

        cancel_btn = ctk.CTkButton(
            btn_frame,
            text="Cancel",
            command=self.destroy,
            font=FONTS['body_bold'],
            height=50,
            corner_radius=RADIUS['md'],
            fg_color='transparent',
            hover_color=COLORS['bg_light'],
            border_width=2,
            border_color=COLORS['danger'],
            text_color=COLORS['danger']
        )
        cancel_btn.pack(side='left', fill='x', expand=True, padx=(0, 10))

        register_btn = ctk.CTkButton(
            btn_frame,
            text="Create Account",
            command=self.handle_register,
            font=FONTS['body_bold'],
            height=50,
            corner_radius=RADIUS['md'],
            fg_color=COLORS['secondary'],
            hover_color='#059669'
        )
        register_btn.pack(side='right', fill='x', expand=True, padx=(10, 0))

    def handle_register(self):
        """Handle registration"""
        national_id = self.id_entry.get().strip()
        full_name = self.name_entry.get().strip()
        password = self.pass_entry.get()
        confirm = self.confirm_entry.get()

        # Validate
        if not all([national_id, full_name, password, confirm]):
            messagebox.showerror("Input Required", "Please fill all fields")
            return

        # Validate National ID
        valid, msg = validate_national_id(national_id)
        if not valid:
            messagebox.showerror("Invalid National ID", msg)
            return

        # Check password match
        if password != confirm:
            messagebox.showerror("Password Mismatch", "Passwords do not match")
            return

        # Register
        success, message = auth_manager.register_patient(
            national_id, full_name, password
        )

        if success:
            messagebox.showinfo("Success", message)
            self.destroy()
        else:
            messagebox.showerror("Registration Failed", message)


if __name__ == "__main__":
    app = LoginWindow()
    app.mainloop()
