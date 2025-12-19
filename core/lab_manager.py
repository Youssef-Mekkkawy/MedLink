"""
Lab Manager - Database Operations for Lab Results
Handles all lab result database operations

Location: core/lab_manager.py
"""

from core.database import get_db
from core.models import LabResult
from sqlalchemy import desc
from typing import List, Dict, Optional
from datetime import datetime, date


class LabManager:
    """Manage lab result records"""
    
    def __init__(self):
        pass
    
    def add_lab_result(self, lab_data: dict) -> LabResult:
        """Add new lab result"""
        with get_db() as db:
            lab = LabResult(**lab_data)
            db.add(lab)
            db.commit()
            db.refresh(lab)
            return lab
    
    def get_patient_lab_results(self, national_id: str, limit: int = 50) -> List[Dict]:
        """Get all lab results for a patient"""
        with get_db() as db:
            results = db.query(LabResult).filter(
                LabResult.patient_national_id == national_id
            ).order_by(desc(LabResult.test_date)).limit(limit).all()
            
            return [self._lab_to_dict(r) for r in results]
    
    def get_recent_lab_results(self, national_id: str, limit: int = 10) -> List[Dict]:
        """Get recent lab results for a patient"""
        with get_db() as db:
            results = db.query(LabResult).filter(
                LabResult.patient_national_id == national_id
            ).order_by(desc(LabResult.test_date)).limit(limit).all()
            
            return [self._lab_to_dict(r) for r in results]
    
    def get_lab_by_id(self, lab_id: int) -> Optional[Dict]:
        """Get lab result by ID"""
        with get_db() as db:
            lab = db.query(LabResult).filter(
                LabResult.lab_result_id == lab_id
            ).first()
            
            return self._lab_to_dict(lab) if lab else None
    
    def get_labs_by_type(self, national_id: str, test_name: str) -> List[Dict]:
        """Get lab results by test type"""
        with get_db() as db:
            results = db.query(LabResult).filter(
                LabResult.patient_national_id == national_id,
                LabResult.test_name.contains(test_name)
            ).order_by(desc(LabResult.test_date)).all()
            
            return [self._lab_to_dict(r) for r in results]
    
    def update_lab_result(self, lab_id: int, updates: dict) -> bool:
        """Update lab result"""
        with get_db() as db:
            lab = db.query(LabResult).filter(
                LabResult.lab_result_id == lab_id
            ).first()
            
            if not lab:
                return False
            
            for key, value in updates.items():
                if hasattr(lab, key):
                    setattr(lab, key, value)
            
            db.commit()
            return True
    
    def delete_lab_result(self, lab_id: int) -> bool:
        """Delete lab result"""
        with get_db() as db:
            lab = db.query(LabResult).filter(
                LabResult.lab_result_id == lab_id
            ).first()
            
            if not lab:
                return False
            
            db.delete(lab)
            db.commit()
            return True
    
    def _lab_to_dict(self, lab: LabResult) -> Dict:
        """Convert LabResult to dictionary"""
        return {
            'lab_result_id': lab.lab_result_id if hasattr(lab, 'lab_result_id') else None,
            'patient_national_id': lab.patient_national_id if hasattr(lab, 'patient_national_id') else None,
            'test_name': lab.test_name if hasattr(lab, 'test_name') else 'Unknown',
            'test_date': lab.test_date if hasattr(lab, 'test_date') else None,
            'date': lab.test_date if hasattr(lab, 'test_date') else None,  # Alias
            'result_value': lab.result_value if hasattr(lab, 'result_value') else None,
            'unit': lab.unit if hasattr(lab, 'unit') else None,
            'reference_range': lab.reference_range if hasattr(lab, 'reference_range') else None,
            'status': lab.status if hasattr(lab, 'status') else None,
            'lab_name': lab.lab_name if hasattr(lab, 'lab_name') else None,
            'ordered_by': lab.ordered_by if hasattr(lab, 'ordered_by') else None,
            'notes': lab.notes if hasattr(lab, 'notes') else None,
            'is_abnormal': lab.is_abnormal if hasattr(lab, 'is_abnormal') else False,
            'created_at': lab.created_at if hasattr(lab, 'created_at') else None
        }


# Global instance
lab_manager = LabManager()