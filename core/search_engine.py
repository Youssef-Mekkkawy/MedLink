"""
Search engine for medical records
"""
from typing import List, Dict
from core.patient_manager import patient_manager
from core.data_manager import data_manager


class SearchEngine:
    """Advanced search functionality"""
    
    def __init__(self):
        self.patient_manager = patient_manager
        self.data_manager = data_manager
    
    def search_by_national_id(self, national_id: str) -> Dict:
        """Quick search by exact National ID"""
        return self.patient_manager.get_patient_by_id(national_id)
    
    def search_patients(self, query: str) -> List[Dict]:
        """Search patients by various criteria"""
        if not query:
            return []
        
        return self.patient_manager.search_patients(query)
    
    def search_by_disease(self, disease: str) -> List[Dict]:
        """Find patients with specific chronic disease"""
        all_patients = self.patient_manager.get_all_patients()
        disease_lower = disease.lower()
        
        results = []
        for patient in all_patients:
            chronic_diseases = patient.get('chronic_diseases', [])
            for d in chronic_diseases:
                if disease_lower in d.lower():
                    results.append(patient)
                    break
        
        return results
    
    def search_by_medication(self, medication: str) -> List[Dict]:
        """Find patients taking specific medication"""
        all_patients = self.patient_manager.get_all_patients()
        med_lower = medication.lower()
        
        results = []
        for patient in all_patients:
            current_meds = patient.get('current_medications', [])
            for med in current_meds:
                if med_lower in med.get('name', '').lower():
                    results.append(patient)
                    break
        
        return results
    
    def search_by_blood_type(self, blood_type: str) -> List[Dict]:
        """Find patients by blood type"""
        all_patients = self.patient_manager.get_all_patients()
        return [p for p in all_patients if p.get('blood_type') == blood_type]


# Global instance
search_engine = SearchEngine()