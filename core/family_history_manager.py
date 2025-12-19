"""
Family History Manager - Database Operations
Location: core/family_history_manager.py
"""

from core.database import get_db
from core.models import FamilyHistory
from typing import List, Dict, Optional


class FamilyHistoryManager:
    """Manage family medical history records"""
    
    def __init__(self):
        pass
    
    def add_family_history(self, family_data: dict) -> FamilyHistory:
        """Add new family history record"""
        with get_db() as db:
            family = FamilyHistory(**family_data)
            db.add(family)
            db.commit()
            db.refresh(family)
            return family
    
    def get_family_history(self, national_id: str) -> Dict:
        """Get family history for a patient"""
        with get_db() as db:
            family_records = db.query(FamilyHistory).filter(
                FamilyHistory.patient_national_id == national_id
            ).all()
            
            # Organize by relation
            family_dict = {}
            genetic_conditions = set()
            
            for record in family_records:
                relation = record.relation.lower() if hasattr(record, 'relation') else 'other'
                
                family_dict[relation] = {
                    'relation': record.relation if hasattr(record, 'relation') else None,
                    'alive': record.is_alive if hasattr(record, 'is_alive') else None,
                    'age': record.age if hasattr(record, 'age') else None,
                    'medical_conditions': record.medical_conditions if hasattr(record, 'medical_conditions') else [],
                    'genetic_conditions': record.genetic_conditions if hasattr(record, 'genetic_conditions') else []
                }
                
                # Collect genetic conditions
                if hasattr(record, 'genetic_conditions') and record.genetic_conditions:
                    if isinstance(record.genetic_conditions, list):
                        genetic_conditions.update(record.genetic_conditions)
                    else:
                        genetic_conditions.add(record.genetic_conditions)
            
            # Add genetic conditions list
            family_dict['genetic_conditions'] = list(genetic_conditions)
            
            return family_dict if family_dict else {}


# Global instance
family_history_manager = FamilyHistoryManager()