"""
Vaccination Manager - Database Operations
Location: core/vaccination_manager.py
"""

from core.database import get_db
from core.models import Vaccination
from sqlalchemy import desc
from typing import List, Dict, Optional


class VaccinationManager:
    """Manage vaccination records"""
    
    def __init__(self):
        pass
    
    def add_vaccination(self, vacc_data: dict) -> Vaccination:
        """Add new vaccination record"""
        with get_db() as db:
            vacc = Vaccination(**vacc_data)
            db.add(vacc)
            db.commit()
            db.refresh(vacc)
            return vacc
    
    def get_patient_vaccinations(self, national_id: str) -> List[Dict]:
        """Get all vaccinations for a patient"""
        with get_db() as db:
            vaccs = db.query(Vaccination).filter(
                Vaccination.patient_national_id == national_id
            ).order_by(desc(Vaccination.date_administered)).all()
            
            return [self._vacc_to_dict(v) for v in vaccs]
    
    def _vacc_to_dict(self, vacc: Vaccination) -> Dict:
        """Convert Vaccination to dict"""
        return {
            'vaccination_id': vacc.vaccination_id if hasattr(vacc, 'vaccination_id') else None,
            'patient_national_id': vacc.patient_national_id if hasattr(vacc, 'patient_national_id') else None,
            'vaccine_name': vacc.vaccine_name if hasattr(vacc, 'vaccine_name') else 'Unknown',
            'date_administered': vacc.date_administered if hasattr(vacc, 'date_administered') else None,
            'dose_number': vacc.dose_number if hasattr(vacc, 'dose_number') else None,
            'batch_number': vacc.batch_number if hasattr(vacc, 'batch_number') else None,
            'administered_by': vacc.administered_by if hasattr(vacc, 'administered_by') else None,
            'location': vacc.location if hasattr(vacc, 'location') else None
        }


# Global instance
vaccination_manager = VaccinationManager()