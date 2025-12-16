"""
MedLink Managers Package
Import all managers here for easy access
"""

from core.auth_manager import AuthManager, auth_manager
from core.patient_manager import PatientManager, patient_manager
from core.doctor_manager import DoctorManager, doctor_manager
from core.medical_managers import (
    VisitManager, LabResultsManager, ImagingManager,
    NFCManager, HardwareAuditManager,
    visit_manager, lab_manager, imaging_manager,
    nfc_manager, audit_manager
)

__all__ = [
    'AuthManager',
    'PatientManager',
    'DoctorManager',
    'VisitManager',
    'LabResultsManager',
    'ImagingManager',
    'NFCManager',
    'HardwareAuditManager',
    'auth_manager',
    'patient_manager',
    'doctor_manager',
    'visit_manager',
    'lab_manager',
    'imaging_manager',
    'nfc_manager',
    'audit_manager',
]