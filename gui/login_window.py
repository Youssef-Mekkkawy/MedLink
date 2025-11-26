"""
Login window - Modern and professional design
"""
import customtkinter as ctk
from tkinter import messagebox
from gui.styles import *
from core.auth_manager import auth_manager
from utils.validators import validate_national_id
from config.localization import get_string as _


class LoginWindow(ctk.CTk):
    """Main login window"""

    def __init__(self):
        super().__init__()

        # Configure window
        self.title("MedLink - Login")
        self.geometry("500x600")
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
        """Create login interface"""
        # Main container
        main_frame = ctk.CTkFrame(self, fg_color=COLORS['bg_dark'])
        main_frame.pack(fill='both', expand=True, padx=40, pady=40)

        # Logo/Title section
        title_frame = ctk.CTkFrame(main_frame, fg_color='transparent')
        title_frame.pack(pady=(0, 30))

        # Icon
        icon_label = ctk.CTkLabel(
            title_frame,
            text="🏥",
            font=('Segoe UI', 48)
        )
        icon_label.pack()

        # Title
        title_label = create_label(
            title_frame,
            text="MedLink",
            style='title'
        )
        title_label.pack(pady=(10, 0))

        # Subtitle
        subtitle_label = create_label(
            title_frame,
            text="Medical Records System",
            style='small'
        )
        subtitle_label.configure(text_color=COLORS['text_secondary'])
        subtitle_label.pack()

        # Login form
        form_frame = create_card_frame(main_frame)
        form_frame.pack(fill='both', expand=True, pady=20)
        form_frame.pack_configure(padx=20, pady=30)

        # Role selection
        role_label = create_label(
            form_frame, text="Select Role", style='subheading')
        role_label.pack(anchor='w', pady=(0, 10))

        self.role_var = ctk.StringVar(value="doctor")

        role_frame = ctk.CTkFrame(form_frame, fg_color='transparent')
        role_frame.pack(fill='x', pady=(0, 20))

        doctor_radio = ctk.CTkRadioButton(
            role_frame,
            text="👨‍⚕️ Doctor",
            variable=self.role_var,
            value="doctor",
            font=FONTS['body'],
        )
        doctor_radio.pack(side='left', padx=(0, 20))

        patient_radio = ctk.CTkRadioButton(
            role_frame,
            text="👤 Patient",
            variable=self.role_var,
            value="patient",
            font=FONTS['body'],
        )
        patient_radio.pack(side='left')

        # Username
        username_label = create_label(form_frame, text="Username")
        username_label.pack(anchor='w', pady=(0, 5))

        self.username_entry = create_entry(
            form_frame,
            placeholder="Enter your username"
        )
        self.username_entry.pack(fill='x', pady=(0, 15))

        # Password
        password_label = create_label(form_frame, text="Password")
        password_label.pack(anchor='w', pady=(0, 5))

        self.password_entry = create_entry(
            form_frame,
            placeholder="Enter your password"
        )
        self.password_entry.configure(show="•")
        self.password_entry.pack(fill='x', pady=(0, 25))

        # Bind Enter key
        self.password_entry.bind('<Return>', lambda e: self.handle_login())

        # Login button
        login_btn = create_button(
            form_frame,
            text="Login",
            command=self.handle_login,
            style='primary'
        )
        login_btn.pack(fill='x', ipady=10)

        # Divider
        divider_frame = ctk.CTkFrame(form_frame, fg_color='transparent')
        divider_frame.pack(fill='x', pady=20)

        ctk.CTkFrame(divider_frame, height=1, fg_color=COLORS['bg_hover']).pack(
            side='left', fill='x', expand=True
        )
        ctk.CTkLabel(
            divider_frame,
            text="  OR  ",
            font=FONTS['small'],
            text_color=COLORS['text_muted']
        ).pack(side='left')
        ctk.CTkFrame(divider_frame, height=1, fg_color=COLORS['bg_hover']).pack(
            side='left', fill='x', expand=True
        )

        # Register button
        register_btn = create_button(
            form_frame,
            text="Register New Patient Account",
            command=self.show_register_dialog,
            style='secondary'
        )
        register_btn.pack(fill='x', ipady=8)

        # Footer
        footer_label = ctk.CTkLabel(
            main_frame,
            text="MedLink v1.0 | © 2024",
            font=FONTS['small'],
            text_color=COLORS['text_muted']
        )
        footer_label.pack(pady=(20, 0))

    def handle_login(self):
        """Handle login button click"""
        username = self.username_entry.get().strip()
        password = self.password_entry.get()
        role = self.role_var.get()

        # Validate inputs
        if not username or not password:
            messagebox.showerror("Error", "Please enter username and password")
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

    def open_dashboard(self, role: str, user_data: dict):
        """Open appropriate dashboard based on role"""
        if role == 'doctor':
            from gui.doctor_dashboard import DoctorDashboard
            dashboard = DoctorDashboard(self, user_data)
        else:
            from gui.patient_dashboard import PatientDashboard
            dashboard = PatientDashboard(self, user_data)

        dashboard.protocol("WM_DELETE_WINDOW",
                           lambda: self.on_dashboard_close(dashboard))

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
    """Patient registration dialog"""

    def __init__(self, parent):
        super().__init__(parent)

        self.title("Register Patient Account")
        self.geometry("450x500")
        self.resizable(False, False)

        # Center on parent
        self.transient(parent)
        self.grab_set()

        self.create_ui()

    def create_ui(self):
        """Create registration form"""
        main_frame = ctk.CTkFrame(self, fg_color=COLORS['bg_dark'])
        main_frame.pack(fill='both', expand=True, padx=30, pady=30)

        # Title
        title_label = create_label(
            main_frame, text="Patient Registration", style='heading')
        title_label.pack(pady=(0, 20))

        form_frame = create_card_frame(main_frame)
        form_frame.pack(fill='both', expand=True)
        form_frame.pack_configure(padx=20, pady=20)

        # National ID
        id_label = create_label(form_frame, text="National ID (14 digits)")
        id_label.pack(anchor='w', pady=(0, 5))

        self.id_entry = create_entry(form_frame, placeholder="29501012345678")
        self.id_entry.pack(fill='x', pady=(0, 15))

        # Full name
        name_label = create_label(form_frame, text="Full Name")
        name_label.pack(anchor='w', pady=(0, 5))

        self.name_entry = create_entry(
            form_frame, placeholder="Enter full name")
        self.name_entry.pack(fill='x', pady=(0, 15))

        # Password
        pass_label = create_label(
            form_frame, text="Password (min 6 characters)")
        pass_label.pack(anchor='w', pady=(0, 5))

        self.pass_entry = create_entry(
            form_frame, placeholder="Enter password")
        self.pass_entry.configure(show="•")
        self.pass_entry.pack(fill='x', pady=(0, 15))

        # Confirm password
        confirm_label = create_label(form_frame, text="Confirm Password")
        confirm_label.pack(anchor='w', pady=(0, 5))

        self.confirm_entry = create_entry(
            form_frame, placeholder="Re-enter password")
        self.confirm_entry.configure(show="•")
        self.confirm_entry.pack(fill='x', pady=(0, 25))

        # Buttons
        btn_frame = ctk.CTkFrame(form_frame, fg_color='transparent')
        btn_frame.pack(fill='x')

        cancel_btn = create_button(
            btn_frame,
            text="Cancel",
            command=self.destroy,
            style='danger'
        )
        cancel_btn.pack(side='left', fill='x', expand=True, padx=(0, 5))

        register_btn = create_button(
            btn_frame,
            text="Register",
            command=self.handle_register,
            style='primary'
        )
        register_btn.pack(side='right', fill='x', expand=True, padx=(5, 0))

    def handle_register(self):
        """Handle registration"""
        national_id = self.id_entry.get().strip()
        full_name = self.name_entry.get().strip()
        password = self.pass_entry.get()
        confirm = self.confirm_entry.get()

        # Validate
        if not all([national_id, full_name, password, confirm]):
            messagebox.showerror("Error", "Please fill all fields")
            return

        # Validate National ID
        valid, msg = validate_national_id(national_id)
        if not valid:
            messagebox.showerror("Invalid National ID", msg)
            return

        # Check password match
        if password != confirm:
            messagebox.showerror("Error", "Passwords do not match")
            return

        # Register
        success, message = auth_manager.register_patient(
            national_id, full_name, password)

        if success:
            messagebox.showinfo("Success", message)
            self.destroy()
        else:
            messagebox.showerror("Registration Failed", message)
if __name__ == "__main__":
    app = LoginWindow()
    app.mainloop()