"""
Visit, Lab Results, Imaging, and NFC Card Managers
"""

from datetime import datetime, date
from database.database_manager import DatabaseManager
from database.models import Visit, Prescription, LabResult, ImagingResult, NFCCard, HardwareAuditLog

# ============================================================================
# VISIT MANAGER
# ============================================================================

class VisitManager:
    """Manage medical visits"""
    
    def create_visit(self, visit_data: dict, prescriptions: list = None):
        """
        Create new visit
        visit_data: dict with visit information
        prescriptions: list of prescription dicts
        """
        with get_db() as db:
            visit = Visit(**visit_data)
            db.add(visit)
            db.flush()  # Get visit ID
            
            # Add prescriptions
            if prescriptions:
                for presc_data in prescriptions:
                    presc = Prescription(
                        visit_id=visit.visit_id,
                        patient_national_id=visit.patient_national_id,
                        **presc_data
                    )
                    db.add(presc)
            
            db.commit()
            db.refresh(visit)
            return visit
    
    def get_visit(self, visit_id: str):
        """Get visit by ID"""
        with get_db() as db:
            return db.query(Visit).filter(Visit.visit_id == visit_id).first()
    
    def get_patient_visits(self, national_id: str, limit=None):
        """Get all visits for a patient"""
        with get_db() as db:
            query = db.query(Visit).filter(
                Visit.patient_national_id == national_id
            ).order_by(Visit.date.desc(), Visit.time.desc())
            
            if limit:
                query = query.limit(limit)
            
            return query.all()
    
    def get_doctor_visits(self, doctor_id: str, limit=None):
        """Get all visits by a doctor"""
        with get_db() as db:
            query = db.query(Visit).filter(
                Visit.doctor_id == doctor_id
            ).order_by(Visit.date.desc())
            
            if limit:
                query = query.limit(limit)
            
            return query.all()
    
    def update_visit(self, visit_id: str, update_data: dict):
        """Update visit information"""
        with get_db() as db:
            visit = db.query(Visit).filter(Visit.visit_id == visit_id).first()
            
            if visit:
                for key, value in update_data.items():
                    if hasattr(visit, key):
                        setattr(visit, key, value)
                
                db.commit()
                db.refresh(visit)
                return visit
            
            return None
    
    def delete_visit(self, visit_id: str):
        """Delete visit"""
        with get_db() as db:
            visit = db.query(Visit).filter(Visit.visit_id == visit_id).first()
            
            if visit:
                db.delete(visit)
                db.commit()
                return True
            
            return False
    
    def get_recent_visits(self, limit=10):
        """Get most recent visits across all patients"""
        with get_db() as db:
            return db.query(Visit).order_by(
                Visit.date.desc(), Visit.time.desc()
            ).limit(limit).all()

# ============================================================================
# LAB RESULTS MANAGER
# ============================================================================

class LabResultsManager:
    """Manage laboratory results"""
    
    def create_lab_result(self, result_data: dict):
        """Create new lab result"""
        with get_db() as db:
            result = LabResult(**result_data)
            db.add(result)
            db.commit()
            db.refresh(result)
            return result
    
    def get_lab_result(self, result_id: str):
        """Get lab result by ID"""
        with get_db() as db:
            return db.query(LabResult).filter(
                LabResult.result_id == result_id
            ).first()
    
    def get_patient_lab_results(self, national_id: str, limit=None):
        """Get all lab results for a patient"""
        with get_db() as db:
            query = db.query(LabResult).filter(
                LabResult.patient_national_id == national_id
            ).order_by(LabResult.date.desc())
            
            if limit:
                query = query.limit(limit)
            
            return query.all()
    
    def get_lab_results_by_type(self, national_id: str, test_type: str):
        """Get lab results by test type"""
        with get_db() as db:
            return db.query(LabResult).filter(
                LabResult.patient_national_id == national_id,
                LabResult.test_type == test_type
            ).order_by(LabResult.date.desc()).all()
    
    def update_lab_result(self, result_id: str, update_data: dict):
        """Update lab result"""
        with get_db() as db:
            result = db.query(LabResult).filter(
                LabResult.result_id == result_id
            ).first()
            
            if result:
                for key, value in update_data.items():
                    if hasattr(result, key):
                        setattr(result, key, value)
                
                db.commit()
                db.refresh(result)
                return result
            
            return None
    
    def delete_lab_result(self, result_id: str):
        """Delete lab result"""
        with get_db() as db:
            result = db.query(LabResult).filter(
                LabResult.result_id == result_id
            ).first()
            
            if result:
                db.delete(result)
                db.commit()
                return True
            
            return False
    
    def get_pending_results(self, national_id: str):
        """Get pending lab results"""
        with get_db() as db:
            return db.query(LabResult).filter(
                LabResult.patient_national_id == national_id,
                LabResult.status == 'pending'
            ).all()

# ============================================================================
# IMAGING RESULTS MANAGER
# ============================================================================

class ImagingManager:
    """Manage imaging results"""
    
    def create_imaging_result(self, result_data: dict):
        """Create new imaging result"""
        with get_db() as db:
            result = ImagingResult(**result_data)
            db.add(result)
            db.commit()
            db.refresh(result)
            return result
    
    def get_imaging_result(self, imaging_id: str):
        """Get imaging result by ID"""
        with get_db() as db:
            return db.query(ImagingResult).filter(
                ImagingResult.imaging_id == imaging_id
            ).first()
    
    def get_patient_imaging_results(self, national_id: str, limit=None):
        """Get all imaging results for a patient"""
        with get_db() as db:
            query = db.query(ImagingResult).filter(
                ImagingResult.patient_national_id == national_id
            ).order_by(ImagingResult.date.desc())
            
            if limit:
                query = query.limit(limit)
            
            return query.all()
    
    def get_imaging_by_type(self, national_id: str, imaging_type: str):
        """Get imaging results by type"""
        with get_db() as db:
            return db.query(ImagingResult).filter(
                ImagingResult.patient_national_id == national_id,
                ImagingResult.imaging_type == imaging_type
            ).order_by(ImagingResult.date.desc()).all()
    
    def update_imaging_result(self, imaging_id: str, update_data: dict):
        """Update imaging result"""
        with get_db() as db:
            result = db.query(ImagingResult).filter(
                ImagingResult.imaging_id == imaging_id
            ).first()
            
            if result:
                for key, value in update_data.items():
                    if hasattr(result, key):
                        setattr(result, key, value)
                
                db.commit()
                db.refresh(result)
                return result
            
            return None
    
    def delete_imaging_result(self, imaging_id: str):
        """Delete imaging result"""
        with get_db() as db:
            result = db.query(ImagingResult).filter(
                ImagingResult.imaging_id == imaging_id
            ).first()
            
            if result:
                db.delete(result)
                db.commit()
                return True
            
            return False

# ============================================================================
# NFC CARD MANAGER
# ============================================================================

class NFCManager:
    """Manage NFC cards"""
    
    def register_card(self, card_data: dict):
        """Register new NFC card"""
        with get_db() as db:
            card = NFCCard(**card_data)
            db.add(card)
            db.commit()
            db.refresh(card)
            return card
    
    def get_card(self, card_uid: str):
        """Get card by UID"""
        with get_db() as db:
            return db.query(NFCCard).filter(
                NFCCard.card_uid == card_uid
            ).first()
    
    def get_card_by_linked_to(self, linked_to: str):
        """Get card by linked user/patient"""
        with get_db() as db:
            return db.query(NFCCard).filter(
                NFCCard.linked_to == linked_to,
                NFCCard.is_active == True
            ).first()
    
    def update_card_scan(self, card_uid: str):
        """Update card last scan time and count"""
        with get_db() as db:
            card = db.query(NFCCard).filter(
                NFCCard.card_uid == card_uid
            ).first()
            
            if card:
                card.last_scan = datetime.now()
                card.scan_count += 1
                db.commit()
                return card
            
            return None
    
    def deactivate_card(self, card_uid: str):
        """Deactivate card"""
        with get_db() as db:
            card = db.query(NFCCard).filter(
                NFCCard.card_uid == card_uid
            ).first()
            
            if card:
                card.is_active = False
                db.commit()
                return True
            
            return False
    
    def get_all_cards(self, card_type=None):
        """Get all cards, optionally filtered by type"""
        with get_db() as db:
            query = db.query(NFCCard)
            
            if card_type:
                query = query.filter(NFCCard.card_type == card_type)
            
            return query.all()

# ============================================================================
# HARDWARE AUDIT LOG MANAGER
# ============================================================================

class HardwareAuditManager:
    """Manage hardware audit logs"""
    
    def log_event(self, event_data: dict):
        """Log hardware event"""
        with get_db() as db:
            log = HardwareAuditLog(**event_data)
            db.add(log)
            db.commit()
            return log
    
    def get_logs(self, limit=100):
        """Get recent logs"""
        with get_db() as db:
            return db.query(HardwareAuditLog).order_by(
                HardwareAuditLog.timestamp.desc()
            ).limit(limit).all()
    
    def get_user_logs(self, user_id: str, limit=50):
        """Get logs for specific user"""
        with get_db() as db:
            return db.query(HardwareAuditLog).filter(
                HardwareAuditLog.user_id == user_id
            ).order_by(HardwareAuditLog.timestamp.desc()).limit(limit).all()
    
    def get_patient_access_logs(self, national_id: str, limit=50):
        """Get access logs for specific patient"""
        with get_db() as db:
            return db.query(HardwareAuditLog).filter(
                HardwareAuditLog.patient_national_id == national_id
            ).order_by(HardwareAuditLog.timestamp.desc()).limit(limit).all()

# Global instances
visit_manager = VisitManager()
lab_manager = LabResultsManager()
imaging_manager = ImagingManager()
nfc_manager = NFCManager()
audit_manager = HardwareAuditManager()
