"""
Imaging Manager - Database Operations for Imaging Results
Handles all imaging result database operations

Location: core/imaging_manager.py
"""

from core.database import get_db
from core.models import ImagingResult
from sqlalchemy import desc
from typing import List, Dict, Optional
from datetime import datetime, date


class ImagingManager:
    """Manage imaging result records"""
    
    def __init__(self):
        pass
    
    def add_imaging_result(self, imaging_data: dict) -> ImagingResult:
        """Add new imaging result"""
        with get_db() as db:
            imaging = ImagingResult(**imaging_data)
            db.add(imaging)
            db.commit()
            db.refresh(imaging)
            return imaging
    
    def get_patient_imaging_results(self, national_id: str, limit: int = 50) -> List[Dict]:
        """Get all imaging results for a patient"""
        with get_db() as db:
            results = db.query(ImagingResult).filter(
                ImagingResult.patient_national_id == national_id
            ).order_by(desc(ImagingResult.imaging_date)).limit(limit).all()
            
            return [self._imaging_to_dict(r) for r in results]
    
    def get_recent_imaging_results(self, national_id: str, limit: int = 10) -> List[Dict]:
        """Get recent imaging results for a patient"""
        with get_db() as db:
            results = db.query(ImagingResult).filter(
                ImagingResult.patient_national_id == national_id
            ).order_by(desc(ImagingResult.imaging_date)).limit(limit).all()
            
            return [self._imaging_to_dict(r) for r in results]
    
    def get_imaging_by_id(self, imaging_id: int) -> Optional[Dict]:
        """Get imaging result by ID"""
        with get_db() as db:
            imaging = db.query(ImagingResult).filter(
                ImagingResult.imaging_result_id == imaging_id
            ).first()
            
            return self._imaging_to_dict(imaging) if imaging else None
    
    def get_imaging_by_type(self, national_id: str, imaging_type: str) -> List[Dict]:
        """Get imaging results by type"""
        with get_db() as db:
            results = db.query(ImagingResult).filter(
                ImagingResult.patient_national_id == national_id,
                ImagingResult.imaging_type.contains(imaging_type)
            ).order_by(desc(ImagingResult.imaging_date)).all()
            
            return [self._imaging_to_dict(r) for r in results]
    
    def update_imaging_result(self, imaging_id: int, updates: dict) -> bool:
        """Update imaging result"""
        with get_db() as db:
            imaging = db.query(ImagingResult).filter(
                ImagingResult.imaging_result_id == imaging_id
            ).first()
            
            if not imaging:
                return False
            
            for key, value in updates.items():
                if hasattr(imaging, key):
                    setattr(imaging, key, value)
            
            db.commit()
            return True
    
    def delete_imaging_result(self, imaging_id: int) -> bool:
        """Delete imaging result"""
        with get_db() as db:
            imaging = db.query(ImagingResult).filter(
                ImagingResult.imaging_result_id == imaging_id
            ).first()
            
            if not imaging:
                return False
            
            db.delete(imaging)
            db.commit()
            return True
    
    def _imaging_to_dict(self, imaging: ImagingResult) -> Dict:
        """Convert ImagingResult to dictionary"""
        return {
            'imaging_result_id': imaging.imaging_result_id if hasattr(imaging, 'imaging_result_id') else None,
            'patient_national_id': imaging.patient_national_id if hasattr(imaging, 'patient_national_id') else None,
            'imaging_type': imaging.imaging_type if hasattr(imaging, 'imaging_type') else 'Unknown',
            'imaging_date': imaging.imaging_date if hasattr(imaging, 'imaging_date') else None,
            'date': imaging.imaging_date if hasattr(imaging, 'imaging_date') else None,  # Alias
            'body_part': imaging.body_part if hasattr(imaging, 'body_part') else None,
            'findings': imaging.findings if hasattr(imaging, 'findings') else None,
            'impression': imaging.impression if hasattr(imaging, 'impression') else None,
            'radiologist_name': imaging.radiologist_name if hasattr(imaging, 'radiologist_name') else None,
            'facility_name': imaging.facility_name if hasattr(imaging, 'facility_name') else None,
            'image_path': imaging.image_path if hasattr(imaging, 'image_path') else None,
            'notes': imaging.notes if hasattr(imaging, 'notes') else None,
            'is_abnormal': imaging.is_abnormal if hasattr(imaging, 'is_abnormal') else False,
            'created_at': imaging.created_at if hasattr(imaging, 'created_at') else None
        }


# Global instance
imaging_manager = ImagingManager()