"""
Visit Manager - Database Operations for Visits
Handles all visit-related database operations

Location: core/visit_manager.py
"""

from core.database import get_db
from core.models import Visit
from sqlalchemy import desc
from typing import List, Dict, Optional
from datetime import datetime, date


class VisitManager:
    """Manage patient visit records"""
    
    def __init__(self):
        pass
    
    def add_visit(self, visit_data: dict) -> Visit:
        """Add new visit record"""
        with get_db() as db:
            visit = Visit(**visit_data)
            db.add(visit)
            db.commit()
            db.refresh(visit)
            return visit
    
    def get_patient_visits(self, national_id: str, limit: int = 50) -> List[Dict]:
        """Get all visits for a patient"""
        with get_db() as db:
            visits = db.query(Visit).filter(
                Visit.patient_national_id == national_id
            ).order_by(desc(Visit.visit_date), desc(Visit.visit_time)).limit(limit).all()
            
            # Convert to list of dicts to avoid session issues
            return [self._visit_to_dict(v) for v in visits]
    
    def get_recent_visits(self, national_id: str, limit: int = 10) -> List[Dict]:
        """Get recent visits for a patient"""
        with get_db() as db:
            visits = db.query(Visit).filter(
                Visit.patient_national_id == national_id
            ).order_by(desc(Visit.visit_date), desc(Visit.visit_time)).limit(limit).all()
            
            return [self._visit_to_dict(v) for v in visits]
    
    def get_visit_by_id(self, visit_id: int) -> Optional[Dict]:
        """Get visit by ID"""
        with get_db() as db:
            visit = db.query(Visit).filter(
                Visit.visit_id == visit_id
            ).first()
            
            return self._visit_to_dict(visit) if visit else None
    
    def update_visit(self, visit_id: int, updates: dict) -> bool:
        """Update visit information"""
        with get_db() as db:
            visit = db.query(Visit).filter(
                Visit.visit_id == visit_id
            ).first()
            
            if not visit:
                return False
            
            for key, value in updates.items():
                if hasattr(visit, key):
                    setattr(visit, key, value)
            
            db.commit()
            return True
    
    def delete_visit(self, visit_id: int) -> bool:
        """Delete visit record"""
        with get_db() as db:
            visit = db.query(Visit).filter(
                Visit.visit_id == visit_id
            ).first()
            
            if not visit:
                return False
            
            db.delete(visit)
            db.commit()
            return True
    
    def get_visit_count(self, national_id: str) -> int:
        """Get total number of visits for a patient"""
        with get_db() as db:
            return db.query(Visit).filter(
                Visit.patient_national_id == national_id
            ).count()
    
    def _visit_to_dict(self, visit: Visit) -> Dict:
        """Convert Visit object to dictionary"""
        return {
            'visit_id': visit.visit_id if hasattr(visit, 'visit_id') else None,
            'patient_national_id': visit.patient_national_id if hasattr(visit, 'patient_national_id') else None,
            'doctor_id': visit.doctor_id if hasattr(visit, 'doctor_id') else None,
            'visit_date': visit.visit_date if hasattr(visit, 'visit_date') else None,
            'date': visit.visit_date if hasattr(visit, 'visit_date') else None,  # Alias for compatibility
            'visit_time': visit.visit_time if hasattr(visit, 'visit_time') else None,
            'time': visit.visit_time if hasattr(visit, 'visit_time') else None,  # Alias
            'chief_complaint': visit.chief_complaint if hasattr(visit, 'chief_complaint') else None,
            'diagnosis': visit.diagnosis if hasattr(visit, 'diagnosis') else None,
            'treatment': visit.treatment if hasattr(visit, 'treatment') else None,
            'prescription': visit.prescription if hasattr(visit, 'prescription') else None,
            'notes': visit.notes if hasattr(visit, 'notes') else None,
            'follow_up_date': visit.follow_up_date if hasattr(visit, 'follow_up_date') else None,
            'visit_type': visit.visit_type if hasattr(visit, 'visit_type') else None,
            'vital_signs': visit.vital_signs if hasattr(visit, 'vital_signs') else None,
            'created_at': visit.created_at if hasattr(visit, 'created_at') else None
        }


# Global instance
visit_manager = VisitManager()