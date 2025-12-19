"""
Disability Manager - Database Operations
Location: core/disability_manager.py
"""

from core.database import get_db
from core.models import Disability
from typing import Dict, Optional


class DisabilityManager:
    """Manage disability and special needs records"""
    
    def __init__(self):
        pass
    
    def add_disability(self, disability_data: dict) -> Disability:
        """Add new disability record"""
        with get_db() as db:
            disability = Disability(**disability_data)
            db.add(disability)
            db.commit()
            db.refresh(disability)
            return disability
    
    def get_disability_info(self, national_id: str) -> Dict:
        """Get disability information for a patient"""
        with get_db() as db:
            disabilities = db.query(Disability).filter(
                Disability.patient_national_id == national_id
            ).all()
            
            if not disabilities:
                return {'has_disability': False}
            
            # Combine all disability records
            disability_info = {
                'has_disability': True,
                'disability_type': [],
                'mobility_aids': [],
                'hearing_impairment': False,
                'visual_impairment': False,
                'notes': []
            }
            
            for disability in disabilities:
                if hasattr(disability, 'disability_type') and disability.disability_type:
                    disability_info['disability_type'].append(disability.disability_type)
                
                if hasattr(disability, 'mobility_aids') and disability.mobility_aids:
                    if isinstance(disability.mobility_aids, list):
                        disability_info['mobility_aids'].extend(disability.mobility_aids)
                    else:
                        disability_info['mobility_aids'].append(disability.mobility_aids)
                
                if hasattr(disability, 'notes') and disability.notes:
                    disability_info['notes'].append(disability.notes)
                
                # Check for specific impairments
                if hasattr(disability, 'disability_type'):
                    dtype = str(disability.disability_type).lower()
                    if 'hearing' in dtype or 'deaf' in dtype:
                        disability_info['hearing_impairment'] = True
                    if 'visual' in dtype or 'blind' in dtype or 'sight' in dtype:
                        disability_info['visual_impairment'] = True
            
            # Convert lists to strings/joined values
            disability_info['disability_type'] = ', '.join(disability_info['disability_type']) if disability_info['disability_type'] else None
            disability_info['notes'] = '\n'.join(disability_info['notes']) if disability_info['notes'] else None
            
            return disability_info


# Global instance
disability_manager = DisabilityManager()