"""
Search Engine - Patient and Medical Record Search
Provides comprehensive search functionality

Location: core/search_engine.py
"""

from core.database import get_db
from core.models import (
    Patient, Doctor, Visit, LabResult, ImagingResult,
    Surgery, Hospitalization, Vaccination, Allergy,
    ChronicDisease, CurrentMedication
)
from sqlalchemy import or_, and_, desc, func
from typing import List, Dict, Optional
from datetime import datetime, date, timedelta


class SearchEngine:
    """Advanced search for patients and medical records"""
    
    def __init__(self):
        pass
    
    # ==================== PATIENT SEARCH ====================
    
    def search_by_national_id(self, national_id: str) -> Optional[dict]:
        """Search patient by national ID (exact match) - Returns dict to avoid session errors"""
        from core.patient_loader import load_patient_with_relationships
        return load_patient_with_relationships(national_id)
    
    def search_by_name(self, name: str, limit: int = 50) -> List[Patient]:
        """Search patients by name (partial match)"""
        with get_db() as db:
            return db.query(Patient).filter(
                Patient.full_name.contains(name)
            ).limit(limit).all()
    
    def search_by_phone(self, phone: str, limit: int = 50) -> List[Patient]:
        """Search patients by phone number"""
        with get_db() as db:
            return db.query(Patient).filter(
                Patient.phone.contains(phone)
            ).limit(limit).all()
    
    def search_patients(self, query: str, limit: int = 50) -> List[Patient]:
        """Universal patient search (name, national_id, or phone)"""
        with get_db() as db:
            return db.query(Patient).filter(
                or_(
                    Patient.full_name.contains(query),
                    Patient.national_id.contains(query),
                    Patient.phone.contains(query),
                    Patient.email.contains(query)
                )
            ).limit(limit).all()
    
    def get_patient_statistics(self, national_id: str) -> dict:
        """Get comprehensive patient statistics"""
        with get_db() as db:
            patient = db.query(Patient).filter(
                Patient.national_id == national_id
            ).first()
            
            if not patient:
                return {}
            
            stats = {
                'total_visits': db.query(Visit).filter(
                    Visit.patient_national_id == national_id
                ).count(),
                'total_lab_tests': db.query(LabResult).filter(
                    LabResult.patient_national_id == national_id
                ).count(),
                'total_imaging': db.query(ImagingResult).filter(
                    ImagingResult.patient_national_id == national_id
                ).count(),
                'total_surgeries': db.query(Surgery).filter(
                    Surgery.patient_national_id == national_id
                ).count()
            }
            
            return stats


# Global instance
search_engine = SearchEngine()