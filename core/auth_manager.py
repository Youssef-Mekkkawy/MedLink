"""
Authentication Manager - FIXED with logout method
Location: core/auth_manager.py
"""

from core.database import get_db
from core.models import User
from utils.security import hash_password, verify_password
from typing import Tuple, Optional, Dict


class AuthManager:
    """Manages user authentication"""
    
    def __init__(self):
        self.current_user = None
    
    def login(self, username: str, password: str) -> Tuple[bool, str, Optional[Dict]]:
        """
        Authenticate user with username and password
        
        Returns:
            (success, message, user_data)
        """
        try:
            with get_db() as db:
                # Query by username ONLY
                user = db.query(User).filter(
                    User.username == username
                ).first()
                
                if not user:
                    return False, "Invalid username or password", None
                
                # Verify password
                if not verify_password(password, user.password_hash):
                    return False, "Invalid username or password", None
                
                # Check account status
                if hasattr(user, 'account_status'):
                    if user.account_status.value == 'inactive':
                        return False, "Account is inactive", None
                    elif user.account_status.value == 'suspended':
                        return False, "Account is suspended", None
                
                # Convert to dict
                user_data = {
                    'user_id': user.user_id,
                    'username': user.username,
                    'full_name': user.full_name,
                    'role': user.role.value if hasattr(user.role, 'value') else str(user.role),
                    'specialization': user.specialization if hasattr(user, 'specialization') else None,
                    'license_number': user.license_number if hasattr(user, 'license_number') else None,
                    'hospital': user.hospital if hasattr(user, 'hospital') else None,
                    'department': user.department if hasattr(user, 'department') else None,
                    'email': user.email if hasattr(user, 'email') else None,
                    'phone': user.phone if hasattr(user, 'phone') else None
                }
                
                # Store current user
                self.current_user = user_data
                
                return True, "Login successful", user_data
        
        except Exception as e:
            print(f"Login error: {e}")
            return False, f"Login error: {str(e)}", None
    
    def logout(self):
        """Logout current user"""
        self.current_user = None
    
    def register_patient(self, patient_data: dict) -> Tuple[bool, str]:
        """
        Register a new patient account
        
        Args:
            patient_data: Dictionary containing patient registration data
            
        Returns:
            (success, message)
        """
        try:
            from core.models import Patient
            
            with get_db() as db:
                # Check if national ID already exists
                existing = db.query(Patient).filter(
                    Patient.national_id == patient_data['national_id']
                ).first()
                
                if existing:
                    return False, "National ID already registered"
                
                # Check if username already exists
                existing_user = db.query(User).filter(
                    User.username == patient_data['username']
                ).first()
                
                if existing_user:
                    return False, "Username already taken"
                
                # Create user account
                user = User(
                    username=patient_data['username'],
                    password_hash=hash_password(patient_data['password']),
                    full_name=patient_data['full_name'],
                    role='patient',
                    email=patient_data.get('email'),
                    phone=patient_data.get('phone')
                )
                db.add(user)
                db.flush()
                
                # Create patient record
                from core.models import Gender, BloodType
                patient = Patient(
                    national_id=patient_data['national_id'],
                    user_id=user.user_id,
                    full_name=patient_data['full_name'],
                    date_of_birth=patient_data['date_of_birth'],
                    gender=Gender(patient_data['gender']),
                    blood_type=BloodType(patient_data.get('blood_type', 'Unknown')),
                    phone=patient_data.get('phone'),
                    email=patient_data.get('email'),
                    address=patient_data.get('address')
                )
                db.add(patient)
                
                db.commit()
                
                return True, "Registration successful"
        
        except Exception as e:
            print(f"Registration error: {e}")
            return False, f"Registration failed: {str(e)}"
    
    def change_password(self, username: str, old_password: str, new_password: str) -> Tuple[bool, str]:
        """Change user password"""
        try:
            with get_db() as db:
                user = db.query(User).filter(
                    User.username == username
                ).first()
                
                if not user:
                    return False, "User not found"
                
                # Verify old password
                if not verify_password(old_password, user.password_hash):
                    return False, "Current password is incorrect"
                
                # Update password
                user.password_hash = hash_password(new_password)
                db.commit()
                
                return True, "Password changed successfully"
        
        except Exception as e:
            print(f"Change password error: {e}")
            return False, f"Failed to change password: {str(e)}"
    
    def get_current_user(self) -> Optional[Dict]:
        """Get currently logged in user"""
        return self.current_user
    
    def is_logged_in(self) -> bool:
        """Check if user is logged in"""
        return self.current_user is not None