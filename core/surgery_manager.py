"""
Surgery Manager - Database Operations for Surgeries
Handles all surgery-related database operations

Location: core/surgery_manager.py
"""

from core.database import get_db
from core.models import Surgery
from sqlalchemy import desc
from typing import List, Dict, Optional
from datetime import datetime, date


class SurgeryManager:
    """Manage surgery records"""
    
    def __init__(self):
        pass
    
    def add_surgery(self, surgery_data: dict) -> Surgery:
        """Add new surgery record"""
        with get_db() as db:
            surgery = Surgery(**surgery_data)
            db.add(surgery)
            db.commit()
            db.refresh(surgery)
            return surgery
    
    def get_patient_surgeries(self, national_id: str) -> List[Surgery]:
        """Get all surgeries for a patient"""
        with get_db() as db:
            surgeries = db.query(Surgery).filter(
                Surgery.patient_national_id == national_id
            ).order_by(desc(Surgery.surgery_date)).all()
            
            # Convert to list of dicts to avoid session issues
            return [self._surgery_to_dict(s) for s in surgeries]
    
    def get_recent_surgeries(self, national_id: str, limit: int = 10) -> List[Dict]:
        """Get recent surgeries for a patient"""
        with get_db() as db:
            surgeries = db.query(Surgery).filter(
                Surgery.patient_national_id == national_id
            ).order_by(desc(Surgery.surgery_date)).limit(limit).all()
            
            # Convert to list of dicts
            return [self._surgery_to_dict(s) for s in surgeries]
    
    def get_surgery_by_id(self, surgery_id: int) -> Optional[Dict]:
        """Get surgery by ID"""
        with get_db() as db:
            surgery = db.query(Surgery).filter(
                Surgery.surgery_id == surgery_id
            ).first()
            
            return self._surgery_to_dict(surgery) if surgery else None
    
    def update_surgery(self, surgery_id: int, updates: dict) -> bool:
        """Update surgery information"""
        with get_db() as db:
            surgery = db.query(Surgery).filter(
                Surgery.surgery_id == surgery_id
            ).first()
            
            if not surgery:
                return False
            
            for key, value in updates.items():
                if hasattr(surgery, key):
                    setattr(surgery, key, value)
            
            db.commit()
            return True
    
    def delete_surgery(self, surgery_id: int) -> bool:
        """Delete surgery record"""
        with get_db() as db:
            surgery = db.query(Surgery).filter(
                Surgery.surgery_id == surgery_id
            ).first()
            
            if not surgery:
                return False
            
            db.delete(surgery)
            db.commit()
            return True
    
    def get_surgery_count(self, national_id: str) -> int:
        """Get total number of surgeries for a patient"""
        with get_db() as db:
            return db.query(Surgery).filter(
                Surgery.patient_national_id == national_id
            ).count()
    
    def _surgery_to_dict(self, surgery: Surgery) -> Dict:
        """Convert Surgery object to dictionary"""
        return {
            'surgery_id': surgery.surgery_id if hasattr(surgery, 'surgery_id') else None,
            'patient_national_id': surgery.patient_national_id if hasattr(surgery, 'patient_national_id') else None,
            'procedure_name': surgery.procedure_name if hasattr(surgery, 'procedure_name') else 'Unknown',
            'surgery_date': surgery.surgery_date if hasattr(surgery, 'surgery_date') else None,
            'date': surgery.surgery_date if hasattr(surgery, 'surgery_date') else None,  # Alias for compatibility
            'procedure': surgery.procedure_name if hasattr(surgery, 'procedure_name') else 'Unknown',  # Alias
            'hospital': surgery.hospital if hasattr(surgery, 'hospital') else None,
            'surgeon_name': surgery.surgeon_name if hasattr(surgery, 'surgeon_name') else None,
            'surgeon': surgery.surgeon_name if hasattr(surgery, 'surgeon_name') else None,  # Alias
            'outcome': surgery.outcome if hasattr(surgery, 'outcome') else None,
            'complications': surgery.complications if hasattr(surgery, 'complications') else None,
            'recovery_time': surgery.recovery_time if hasattr(surgery, 'recovery_time') else None,
            'notes': surgery.notes if hasattr(surgery, 'notes') else None,
            'created_at': surgery.created_at if hasattr(surgery, 'created_at') else None
        }


# Global instance
surgery_manager = SurgeryManager()