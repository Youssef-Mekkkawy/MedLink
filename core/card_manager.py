"""
FIXED Card Manager - Works with GUI NFC Login
Location: core/card_manager.py (REPLACE YOUR FILE)
"""

from core.database import get_db
from core.models import DoctorCard, PatientCard, User, Patient
from datetime import datetime


class CardManager:
    """Manage NFC card operations - COMPLETE FIX"""

    def __init__(self):
        """Initialize card manager"""
        pass

    def get_card(self, card_uid):
        """
        Get card information by UID (works for both doctor and patient cards)
        Returns dict with card_type, user/patient data

        Args:
            card_uid (str): NFC card UID

        Returns:
            dict: {
                'card_type': 'doctor'/'patient',
                'card_uid': str,
                'full_name': str,
                'user': User object (for doctors),
                'patient': Patient object (for patients),
                'card': Card object
            } or None
        """
        db = get_db()
        try:
            # Try to find doctor card first
            doctor_card = db.query(DoctorCard).filter_by(
                card_uid=card_uid,
                is_active=True

            ).first()

            if doctor_card:
                # Get associated user
                user = db.query(User).filter_by(
                    user_id=doctor_card.user_id).first()

                if user:
                    # Update last used
                    doctor_card.last_used = datetime.now()
                    db.commit()
                    doctor_card.last_used = datetime.now()
                    print(f"Doctor card last used: {doctor_card}")
                    # Convert to dict for GUI (CRITICAL!)

                    return {
                        "card_type": "doctor",
                        "card_uid": doctor_card.card_uid,
                        "user_id": doctor_card.user_id,
                        "username": doctor_card.username,
                        "full_name": doctor_card.full_name,
                        "is_active": doctor_card.is_active,
                        "card": {
                            "is_active": doctor_card.is_active,
                            "issued_date": doctor_card.issued_date,
                            "last_used": doctor_card.last_used,
                        }
                    }

            # Try to find patient card
            patient_card = db.query(PatientCard).filter_by(
                card_uid=card_uid,
                is_active=True
            ).first()

            if patient_card:
                # Get associated patient
                patient = db.query(Patient).filter_by(
                    national_id=patient_card.national_id
                ).first()

                if patient:
                    # Update last used
                    patient_card.last_used = datetime.now()
                    db.commit()

                    # Convert to dict for GUI (CRITICAL!)
                    return {
                        'card_type': 'patient',
                        'card_uid': patient_card.card_uid,
                        'national_id': patient_card.national_id,
                        'full_name': patient_card.full_name,
                        'patient': {  # Dict instead of ORM object
                            'id': patient.id,
                            'national_id': patient.national_id,
                            'full_name': patient.full_name,
                            'date_of_birth': patient.date_of_birth,
                            'age': patient.age,
                            'gender': patient.gender.value if patient.gender else None,
                            'blood_type': patient.blood_type.value if patient.blood_type else None,
                            'phone': patient.phone,
                            'email': patient.email
                        },
                        'card': {
                            'card_uid': patient_card.card_uid,
                            'is_active': patient_card.is_active,
                            'last_used': patient_card.last_used
                        }
                    }

            # Card not found
            return None

        finally:
            db.close()

    def authenticate_card(self, card_uid):
        """
        Authenticate a card and return user/patient information

        Args:
            card_uid (str): NFC card UID

        Returns:
            tuple: (success: bool, data: dict, message: str)
        """
        card_info = self.get_card(card_uid)

        if not card_info:
            return False, None, "Card not found or inactive"

        if card_info['card_type'] == 'doctor':
            return True, card_info, f"Welcome, Dr. {card_info['full_name']}"
        else:
            return True, card_info, f"Welcome, {card_info['full_name']}"

    def is_doctor_card(self, card_uid):
        """Check if card is a doctor card"""
        db = get_db()
        try:
            card = db.query(DoctorCard).filter_by(card_uid=card_uid).first()
            return card is not None
        finally:
            db.close()

    def is_patient_card(self, card_uid):
        """Check if card is a patient card"""
        db = get_db()
        try:
            card = db.query(PatientCard).filter_by(card_uid=card_uid).first()
            return card is not None
        finally:
            db.close()

    def get_doctor_by_card(self, card_uid):
        """
        Get doctor (User dict) by card UID
        Returns dict for GUI compatibility
        """
        db = get_db()
        try:
            doctor_card = db.query(DoctorCard).filter_by(
                card_uid=card_uid,
                is_active=True
            ).first()

            if doctor_card:
                user = db.query(User).filter_by(
                    user_id=doctor_card.user_id).first()
                if user:
                    return {
                        'user_id': user.user_id,
                        'username': user.username,
                        'full_name': user.full_name,
                        'role': user.role.value,
                        'national_id': user.national_id,
                        'specialization': user.specialization,
                        'hospital': user.hospital
                    }
            return None
        finally:
            db.close()

    def get_patient_by_card(self, card_uid):
        """
        Get patient (dict) by card UID
        Returns dict for GUI compatibility
        """
        db = get_db()
        try:
            patient_card = db.query(PatientCard).filter_by(
                card_uid=card_uid,
                is_active=True
            ).first()

            if patient_card:
                patient = db.query(Patient).filter_by(
                    national_id=patient_card.national_id
                ).first()
                if patient:
                    return {
                        'id': patient.id,
                        'national_id': patient.national_id,
                        'full_name': patient.full_name,
                        'date_of_birth': patient.date_of_birth,
                        'age': patient.age,
                        'gender': patient.gender.value if patient.gender else None,
                        'blood_type': patient.blood_type.value if patient.blood_type else None,
                        'phone': patient.phone,
                        'email': patient.email,
                        'address': patient.address
                    }
            return None
        finally:
            db.close()

    def register_doctor_card(self, card_uid, user_id, username, full_name):
        """Register a new doctor card"""
        db = get_db()
        try:
            # Check if card already exists
            existing = db.query(DoctorCard).filter_by(
                card_uid=card_uid).first()
            if existing:
                return False, "Card already registered"

            # Create new doctor card
            card = DoctorCard(
                card_uid=card_uid,
                user_id=user_id,
                username=username,
                full_name=full_name,
                is_active=True
            )
            db.add(card)
            db.commit()

            return True, "Doctor card registered successfully"
        except Exception as e:
            db.rollback()
            return False, f"Error: {str(e)}"
        finally:
            db.close()

    def register_patient_card(self, card_uid, national_id, full_name):
        """Register a new patient card"""
        db = get_db()
        try:
            # Check if card already exists
            existing = db.query(PatientCard).filter_by(
                card_uid=card_uid).first()
            if existing:
                return False, "Card already registered"

            # Create new patient card
            card = PatientCard(
                card_uid=card_uid,
                national_id=national_id,
                full_name=full_name,
                is_active=True
            )
            db.add(card)
            db.commit()

            return True, "Patient card registered successfully"
        except Exception as e:
            db.rollback()
            return False, f"Error: {str(e)}"
        finally:
            db.close()

    def deactivate_card(self, card_uid):
        """Deactivate a card"""
        db = get_db()
        try:
            # Try doctor card
            doctor_card = db.query(DoctorCard).filter_by(
                card_uid=card_uid).first()
            if doctor_card:
                doctor_card.is_active = False
                db.commit()
                return True, "Doctor card deactivated"

            # Try patient card
            patient_card = db.query(PatientCard).filter_by(
                card_uid=card_uid).first()
            if patient_card:
                patient_card.is_active = False
                db.commit()
                return True, "Patient card deactivated"

            return False, "Card not found"
        except Exception as e:
            db.rollback()
            return False, f"Error: {str(e)}"
        finally:
            db.close()

    def activate_card(self, card_uid):
        """Activate a card"""
        db = get_db()
        try:
            # Try doctor card
            doctor_card = db.query(DoctorCard).filter_by(
                card_uid=card_uid).first()
            if doctor_card:
                doctor_card.is_active = True
                db.commit()
                return True, "Doctor card activated"

            # Try patient card
            patient_card = db.query(PatientCard).filter_by(
                card_uid=card_uid).first()
            if patient_card:
                patient_card.is_active = True
                db.commit()
                return True, "Patient card activated"

            return False, "Card not found"
        except Exception as e:
            db.rollback()
            return False, f"Error: {str(e)}"
        finally:
            db.close()


# Create global instance
card_manager = CardManager()
