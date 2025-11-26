"""
Authentication and session management
"""
from datetime import datetime, timedelta
from typing import Optional, Dict
from core.data_manager import data_manager
from utils.security import security
from utils.validators import validate_password


class AuthManager:
    """Manages user authentication and sessions"""

    def __init__(self):
        self.current_user = None
        self.session_start = None

    def login(self, username: str, password: str, role: str) -> tuple[bool, str, Dict]:
        """
        Authenticate user
        Returns: (success, message, user_data)
        """
        # Load users
        data = data_manager.load_data('users')
        users = data.get('users', [])

        # Find user
        user = None
        for u in users:
            if u.get('username') == username and u.get('role') == role:
                user = u
                break

        if not user:
            return False, "Invalid username or role", None

        # Verify password
        if not security.verify_password(password, user.get('password_hash', '')):
            return False, "Invalid password", None

        # Set session
        self.current_user = user
        self.session_start = datetime.now()

        return True, "Login successful", user

    def logout(self):
        """Clear current session"""
        self.current_user = None
        self.session_start = None

    def is_authenticated(self) -> bool:
        """Check if user is logged in"""
        return self.current_user is not None

    def get_current_user(self) -> Optional[Dict]:
        """Get current user data"""
        return self.current_user

    def register_patient(self, national_id: str, full_name: str,
                         password: str) -> tuple[bool, str]:
        """
        Register new patient account
        Returns: (success, message)
        """
        # Validate password
        valid, msg = validate_password(password)
        if not valid:
            return False, msg

        # Check if user already exists
        existing = data_manager.find_item(
            'users', 'users', 'national_id', national_id)
        if existing:
            return False, "Account with this National ID already exists"

        # Create user account
        username = f"patient_{national_id}"
        user_data = {
            'user_id': f"P{national_id}",
            'username': username,
            'password_hash': security.hash_password(password),
            'role': 'patient',
            'national_id': national_id,
            'full_name': full_name,
            'created_at': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        }

        # Save user
        if data_manager.add_item('users', 'users', user_data):
            return True, f"Account created successfully. Username: {username}"

        return False, "Failed to create account"


# Global instance
auth_manager = AuthManager()
