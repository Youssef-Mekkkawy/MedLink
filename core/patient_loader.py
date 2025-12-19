"""
Patient Data Loader - Properly loads patient with all relationships
Fixes SQLAlchemy DetachedInstanceError

Location: core/patient_loader.py
"""

from core.database import get_db
from core.models import Patient
from typing import Optional, Dict


def load_patient_with_relationships(national_id: str) -> Optional[Dict]:
    """
    Load patient with ALL relationships as a dictionary
    This prevents SQLAlchemy lazy load errors
    
    Returns: Dictionary with all patient data and relationships
    """
    with get_db() as db:
        patient = db.query(Patient).filter(
            Patient.national_id == national_id
        ).first()
        
        if not patient:
            return None
        
        # Convert to dict WHILE session is open
        patient_dict = {
            # Basic info - only include attributes that exist
            'national_id': patient.national_id,
            'full_name': patient.full_name,
            'date_of_birth': patient.date_of_birth if hasattr(patient, 'date_of_birth') else None,
            'age': patient.age if hasattr(patient, 'age') else None,
            'gender': patient.gender.value if hasattr(patient, 'gender') and patient.gender else None,
            'blood_type': patient.blood_type.value if hasattr(patient, 'blood_type') and patient.blood_type else None,
            'phone': patient.phone if hasattr(patient, 'phone') else None,
            'email': patient.email if hasattr(patient, 'email') else None,
            'address': patient.address if hasattr(patient, 'address') else None,
            'city': patient.city if hasattr(patient, 'city') else None,
            'governorate': patient.governorate if hasattr(patient, 'governorate') else None,
            'emergency_contact': patient.emergency_contact if hasattr(patient, 'emergency_contact') else None,
            'created_at': patient.created_at if hasattr(patient, 'created_at') else None,
            
            # Relationships - Load while session is open! (with safety checks)
            'allergies': [
                {
                    'allergy_id': a.allergy_id if hasattr(a, 'allergy_id') else None,
                    'allergen_name': a.allergen_name if hasattr(a, 'allergen_name') else 'Unknown',
                    'severity': a.severity if hasattr(a, 'severity') else None,
                    'reaction': a.reaction if hasattr(a, 'reaction') else None,
                    'date_identified': a.date_identified if hasattr(a, 'date_identified') else None
                }
                for a in patient.allergies
            ] if hasattr(patient, 'allergies') and patient.allergies else [],
            
            'chronic_diseases': [
                {
                    'disease_id': cd.disease_id if hasattr(cd, 'disease_id') else None,
                    'disease_name': cd.disease_name if hasattr(cd, 'disease_name') else 'Unknown',
                    'date_diagnosed': cd.date_diagnosed if hasattr(cd, 'date_diagnosed') else None,
                    'severity': cd.severity if hasattr(cd, 'severity') else None,
                    'treatment': cd.treatment if hasattr(cd, 'treatment') else None,
                    'is_active': cd.is_active if hasattr(cd, 'is_active') else True
                }
                for cd in patient.chronic_diseases
            ] if hasattr(patient, 'chronic_diseases') and patient.chronic_diseases else [],
            
            'current_medications': [
                {
                    'medication_id': cm.medication_id if hasattr(cm, 'medication_id') else None,
                    'medication_name': cm.medication_name if hasattr(cm, 'medication_name') else 'Unknown',
                    'dosage': cm.dosage if hasattr(cm, 'dosage') else None,
                    'frequency': cm.frequency if hasattr(cm, 'frequency') else None,
                    'start_date': cm.start_date if hasattr(cm, 'start_date') else None,
                    'is_active': cm.is_active if hasattr(cm, 'is_active') else True
                }
                for cm in patient.current_medications if cm.is_active
            ] if hasattr(patient, 'current_medications') and patient.current_medications else [],
            
            'surgeries': [
                {
                    'surgery_id': s.surgery_id,
                    'procedure_name': s.procedure_name,
                    'surgery_date': s.surgery_date,
                    'hospital': s.hospital,
                    'surgeon_name': s.surgeon_name,
                    'outcome': s.outcome,
                    'complications': s.complications
                }
                for s in patient.surgeries
            ],
            
            'hospitalizations': [
                {
                    'hospitalization_id': h.hospitalization_id,
                    'admission_date': h.admission_date,
                    'discharge_date': h.discharge_date,
                    'hospital': h.hospital,
                    'diagnosis': h.diagnosis,
                    'treatment_summary': h.treatment_summary,
                    'days_stayed': h.days_stayed
                }
                for h in patient.hospitalizations
            ],
            
            'vaccinations': [
                {
                    'vaccination_id': v.vaccination_id,
                    'vaccine_name': v.vaccine_name,
                    'date_administered': v.date_administered,
                    'dose_number': v.dose_number,
                    'batch_number': v.batch_number,
                    'administered_by': v.administered_by
                }
                for v in patient.vaccinations
            ],
            
            'family_history': [
                {
                    'family_id': fh.family_id,
                    'relation': fh.relation,
                    'is_alive': fh.is_alive,
                    'medical_conditions': fh.medical_conditions,
                    'genetic_conditions': fh.genetic_conditions,
                    'age_at_death': fh.age_at_death,
                    'cause_of_death': fh.cause_of_death
                }
                for fh in patient.family_history
            ],
            
            'disabilities': [
                {
                    'disability_id': d.disability_id,
                    'disability_type': d.disability_type,
                    'severity': d.severity,
                    'date_diagnosed': d.date_diagnosed,
                    'mobility_aids': d.mobility_aids,
                    'accessibility_requirements': d.accessibility_requirements
                }
                for d in patient.disabilities
            ]
        }
        
        # Add emergency directive if exists
        if patient.emergency_directives:
            ed = patient.emergency_directives[0] if patient.emergency_directives else None
            if ed:
                patient_dict['emergency_directives'] = {
                    'dnr_status': ed.dnr_status,
                    'organ_donor': ed.organ_donor,
                    'power_of_attorney': ed.power_of_attorney,
                    'power_of_attorney_name': ed.power_of_attorney_name,
                    'power_of_attorney_contact': ed.power_of_attorney_contact,
                    'end_of_life_wishes': ed.end_of_life_wishes,
                    'religious_preferences': ed.religious_preferences
                }
        
        # Add lifestyle if exists
        if patient.lifestyle:
            ls = patient.lifestyle[0] if patient.lifestyle else None
            if ls:
                patient_dict['lifestyle'] = {
                    'smoking_status': ls.smoking_status,
                    'alcohol_use': ls.alcohol_use,
                    'exercise_frequency': ls.exercise_frequency,
                    'diet_type': ls.diet_type,
                    'occupation': ls.occupation,
                    'stress_level': ls.stress_level
                }
        
        # Add insurance if exists
        if patient.insurance:
            ins = patient.insurance[0] if patient.insurance else None
            if ins:
                patient_dict['insurance'] = {
                    'insurance_provider': ins.insurance_provider,
                    'policy_number': ins.policy_number,
                    'coverage_type': ins.coverage_type,
                    'coverage_details': ins.coverage_details,
                    'copay_amount': ins.copay_amount,
                    'expiry_date': ins.expiry_date
                }
        
        return patient_dict


def get_patient_dict(national_id: str) -> Optional[Dict]:
    """
    Alias for load_patient_with_relationships
    Use this in your GUI code
    """
    return load_patient_with_relationships(national_id)