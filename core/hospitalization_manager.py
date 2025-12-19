"""
Hospitalization Manager - Database Operations
Location: core/hospitalization_manager.py
"""

from core.database import get_db
from core.models import Hospitalization
from sqlalchemy import desc
from typing import List, Dict, Optional
from datetime import datetime, date


class HospitalizationManager:
    """Manage hospitalization records"""
    
    def __init__(self):
        pass
    
    def add_hospitalization(self, hosp_data: dict) -> Hospitalization:
        """Add new hospitalization record"""
        with get_db() as db:
            hosp = Hospitalization(**hosp_data)
            db.add(hosp)
            db.commit()
            db.refresh(hosp)
            return hosp
    
    def get_patient_hospitalizations(self, national_id: str) -> List[Dict]:
        """Get all hospitalizations for a patient"""
        with get_db() as db:
            hosps = db.query(Hospitalization).filter(
                Hospitalization.patient_national_id == national_id
            ).order_by(desc(Hospitalization.admission_date)).all()
            
            return [self._hosp_to_dict(h) for h in hosps]
    
    def calculate_length_of_stay(self, hosp: dict) -> Optional[int]:
        """Calculate length of stay in days"""
        if hosp.get('admission_date') and hosp.get('discharge_date'):
            if isinstance(hosp['admission_date'], str):
                return None
            delta = hosp['discharge_date'] - hosp['admission_date']
            return delta.days
        return hosp.get('days_stayed')
    
    def _hosp_to_dict(self, hosp: Hospitalization) -> Dict:
        """Convert Hospitalization to dict"""
        return {
            'hospitalization_id': hosp.hospitalization_id if hasattr(hosp, 'hospitalization_id') else None,
            'patient_national_id': hosp.patient_national_id if hasattr(hosp, 'patient_national_id') else None,
            'admission_date': hosp.admission_date if hasattr(hosp, 'admission_date') else None,
            'discharge_date': hosp.discharge_date if hasattr(hosp, 'discharge_date') else None,
            'hospital': hosp.hospital if hasattr(hosp, 'hospital') else None,
            'diagnosis': hosp.diagnosis if hasattr(hosp, 'diagnosis') else None,
            'reason': hosp.diagnosis if hasattr(hosp, 'diagnosis') else None,  # Alias
            'treatment_summary': hosp.treatment_summary if hasattr(hosp, 'treatment_summary') else None,
            'days_stayed': hosp.days_stayed if hasattr(hosp, 'days_stayed') else None,
            'department': hosp.department if hasattr(hosp, 'department') else None,
            'attending_doctor': hosp.attending_doctor if hasattr(hosp, 'attending_doctor') else None,
            'outcome': hosp.outcome if hasattr(hosp, 'outcome') else None
        }


# Global instance
hospitalization_manager = HospitalizationManager()