"""
Data Manager - General Data Operations
MySQL Version - Compatible with existing GUI
"""

from datetime import datetime, date
from database.database_manager import *
from database.models import *
import json

class DataManager:
    """General data management and utilities"""
    
    def __init__(self):
        pass
    
    def get_all_patients(self):
        """Get all patients"""
        with get_db() as db:
            return db.query(Patient).order_by(Patient.full_name).all()
    
    def get_all_doctors(self):
        """Get all doctors with user info"""
        with get_db() as db:
            doctors = db.query(Doctor).join(User).order_by(User.full_name).all()
            return [{
                'user_id': d.user_id,
                'full_name': d.user.full_name,
                'specialization': d.specialization,
                'hospital': d.hospital,
                'license_number': d.license_number
            } for d in doctors]
    
    def get_patient_count(self):
        """Get total number of patients"""
        with get_db() as db:
            return db.query(Patient).count()
    
    def get_doctor_count(self):
        """Get total number of doctors"""
        with get_db() as db:
            return db.query(Doctor).count()
    
    def get_visit_count(self):
        """Get total number of visits"""
        with get_db() as db:
            return db.query(Visit).count()
    
    def get_lab_result_count(self):
        """Get total number of lab results"""
        with get_db() as db:
            return db.query(LabResult).count()
    
    def get_imaging_count(self):
        """Get total number of imaging results"""
        with get_db() as db:
            return db.query(ImagingResult).count()
    
    def get_dashboard_stats(self):
        """Get dashboard statistics"""
        with get_db() as db:
            return {
                'total_patients': db.query(Patient).count(),
                'total_doctors': db.query(Doctor).count(),
                'total_visits': db.query(Visit).count(),
                'total_lab_results': db.query(LabResult).count(),
                'total_imaging': db.query(ImagingResult).count(),
                'active_cards': db.query(NFCCard).filter(NFCCard.is_active == True).count()
            }
    
    def get_recent_activity(self, limit=10):
        """Get recent system activity"""
        with get_db() as db:
            recent_visits = db.query(Visit).order_by(
                Visit.date.desc(), Visit.time.desc()
            ).limit(limit).all()
            
            return [{
                'type': 'visit',
                'date': v.date,
                'time': v.time,
                'patient': v.patient_national_id,
                'doctor': v.doctor_name,
                'description': f"{v.visit_type} - {v.chief_complaint or 'N/A'}"
            } for v in recent_visits]
    
    def export_patient_data(self, national_id):
        """Export complete patient data as JSON"""
        with get_db() as db:
            patient = db.query(Patient).filter(
                Patient.national_id == national_id
            ).first()
            
            if not patient:
                return None
            
            data = {
                'patient': patient.to_dict(),
                'allergies': [a.allergen for a in patient.allergies],
                'chronic_diseases': [cd.disease_name for cd in patient.chronic_diseases],
                'current_medications': [m.to_dict() for m in patient.current_medications if m.is_active],
                'visits': [v.to_dict() for v in patient.visits],
                'lab_results': [lr.to_dict() for lr in patient.lab_results],
                'imaging_results': [ir.to_dict() for ir in patient.imaging_results],
                'surgeries': [{
                    'procedure': s.procedure_name,
                    'date': s.date.isoformat() if s.date else None,
                    'hospital': s.hospital,
                    'outcome': s.outcome
                } for s in patient.surgeries],
                'hospitalizations': [{
                    'admission_date': h.admission_date.isoformat() if h.admission_date else None,
                    'discharge_date': h.discharge_date.isoformat() if h.discharge_date else None,
                    'hospital': h.hospital,
                    'diagnosis': h.diagnosis
                } for h in patient.hospitalizations],
                'vaccinations': [{
                    'vaccine': v.vaccine_name,
                    'date': v.date_administered.isoformat() if v.date_administered else None
                } for v in patient.vaccinations]
            }
            
            return data
    
    def backup_database(self, backup_path):
        """Create database backup (requires mysqldump)"""
        import subprocess
        import os
        
        try:
            # Get database credentials from environment
            from core.database import Config
            
            cmd = [
                'mysqldump',
                '-h', Config.MYSQL_HOST,
                '-u', Config.MYSQL_USER,
                f'-p{Config.MYSQL_PASSWORD}',
                Config.MYSQL_DATABASE
            ]
            
            with open(backup_path, 'w') as f:
                subprocess.run(cmd, stdout=f, check=True)
            
            return {'success': True, 'message': f'Backup saved to {backup_path}'}
        
        except Exception as e:
            return {'success': False, 'message': f'Backup failed: {str(e)}'}
    
    def get_patients_by_blood_type(self, blood_type):
        """Get patients by blood type"""
        with get_db() as db:
            return db.query(Patient).filter(
                Patient.blood_type == blood_type
            ).order_by(Patient.full_name).all()
    
    def get_patients_by_gender(self, gender):
        """Get patients by gender"""
        with get_db() as db:
            return db.query(Patient).filter(
                Patient.gender == gender
            ).order_by(Patient.full_name).all()
    
    def get_patients_by_age_range(self, min_age, max_age):
        """Get patients within age range"""
        with get_db() as db:
            return db.query(Patient).filter(
                Patient.age.between(min_age, max_age)
            ).order_by(Patient.age).all()
    
    def get_statistics_report(self):
        """Generate comprehensive statistics report"""
        with get_db() as db:
            stats = {
                'patients': {
                    'total': db.query(Patient).count(),
                    'male': db.query(Patient).filter(Patient.gender == 'Male').count(),
                    'female': db.query(Patient).filter(Patient.gender == 'Female').count(),
                    'with_nfc': db.query(Patient).filter(Patient.nfc_card_assigned == True).count()
                },
                'doctors': {
                    'total': db.query(Doctor).count()
                },
                'medical_records': {
                    'visits': db.query(Visit).count(),
                    'lab_results': db.query(LabResult).count(),
                    'imaging_results': db.query(ImagingResult).count(),
                    'surgeries': db.query(Surgery).count(),
                    'hospitalizations': db.query(Hospitalization).count(),
                    'vaccinations': db.query(Vaccination).count()
                },
                'health_data': {
                    'allergies': db.query(Allergy).count(),
                    'chronic_diseases': db.query(ChronicDisease).count(),
                    'current_medications': db.query(CurrentMedication).filter(
                        CurrentMedication.is_active == True
                    ).count()
                }
            }
            
            return stats
    
    def search_all(self, search_term):
        """Search across patients, doctors, and records"""
        with get_db() as db:
            search = f"%{search_term}%"
            
            results = {
                'patients': db.query(Patient).filter(
                    (Patient.full_name.like(search)) |
                    (Patient.national_id.like(search))
                ).limit(10).all(),
                
                'doctors': db.query(Doctor).join(User).filter(
                    (User.full_name.like(search)) |
                    (Doctor.specialization.like(search))
                ).limit(10).all(),
                
                'visits': db.query(Visit).filter(
                    (Visit.visit_id.like(search)) |
                    (Visit.diagnosis.like(search))
                ).limit(10).all()
            }
            
            return results
    
    def clean_old_data(self, days=365):
        """Clean data older than specified days (use with caution!)"""
        from datetime import timedelta
        
        cutoff_date = date.today() - timedelta(days=days)
        
        with get_db() as db:
            # Delete old visits
            old_visits = db.query(Visit).filter(Visit.date < cutoff_date).delete()
            
            # Delete old lab results
            old_labs = db.query(LabResult).filter(LabResult.date < cutoff_date).delete()
            
            # Delete old imaging
            old_imaging = db.query(ImagingResult).filter(ImagingResult.date < cutoff_date).delete()
            
            db.commit()
            
            return {
                'visits_deleted': old_visits,
                'lab_results_deleted': old_labs,
                'imaging_deleted': old_imaging
            }

# Global instance
data_manager = DataManager()