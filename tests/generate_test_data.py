"""
Generate test data for MedLink
Run this once to create sample users
"""
import json
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from config.settings import DATA_DIR
from utils.security import security

def generate_test_users():
    """Create test doctor and patient accounts"""
    
    users = {
        "users": [
            # Test Doctor Account
            {
                "user_id": "D001",
                "username": "dr.ahmed",
                "password_hash": security.hash_password("password"),
                "role": "doctor",
                "full_name": "Dr. Ahmed Mohamed",
                "specialization": "Cardiology",
                "hospital": "Cairo University Hospital",
                "license_number": "MED12345",
                "email": "ahmed@hospital.eg",
                "phone": "01012345678",
                "created_at": "2024-11-01 10:00:00"
            },
            
            # Test Patient Account
            {
                "user_id": "P29501012345678",
                "username": "patient_29501012345678",
                "password_hash": security.hash_password("password123"),
                "role": "patient",
                "national_id": "29501012345678",
                "full_name": "Mohamed Ali Hassan",
                "created_at": "2024-11-15 14:30:00"
            },
            
            # Another Doctor
            {
                "user_id": "D002",
                "username": "dr.salma",
                "password_hash": security.hash_password("password"),
                "role": "doctor",
                "full_name": "Dr. Salma Ibrahim",
                "specialization": "Radiology",
                "hospital": "Qasr El Aini Hospital",
                "license_number": "MED67890",
                "email": "salma@hospital.eg",
                "phone": "01098765432",
                "created_at": "2024-11-01 10:00:00"
            },
            
            # Another Patient
            {
                "user_id": "P29012151234567",
                "username": "patient_29012151234567",
                "password_hash": security.hash_password("password123"),
                "role": "patient",
                "national_id": "29012151234567",
                "full_name": "Fatma Ahmed Ibrahim",
                "created_at": "2024-11-10 09:15:00"
            }
        ]
    }
    
    # Save to users.json
    users_file = DATA_DIR / 'users.json'
    with open(users_file, 'w', encoding='utf-8') as f:
        json.dump(users, f, indent=2, ensure_ascii=False)
    
    print("✅ Test users created successfully!")
    print("\n📋 Test Accounts:")
    print("\n👨‍⚕️ Doctor Accounts:")
    print("  Username: dr.ahmed     | Password: password")
    print("  Username: dr.salma     | Password: password")
    print("\n👤 Patient Accounts:")
    print("  Username: patient_29501012345678 | Password: password123")
    print("  Username: patient_29012151234567 | Password: password123")

def generate_test_patients():
    """Create test patient medical records"""
    
    patients = {
        "patients": [
            {
                "national_id": "29501012345678",
                "full_name": "Mohamed Ali Hassan",
                "date_of_birth": "1995-01-01",
                "age": 29,
                "gender": "Male",
                "blood_type": "A+",
                "phone": "01098765432",
                "email": "mohamed.ali@email.com",
                "address": "15 Tahrir Street, Cairo",
                
                "emergency_contact": {
                    "name": "Fatma Hassan",
                    "relation": "Mother",
                    "phone": "01123456789"
                },
                
                "chronic_diseases": ["Asthma", "Hypertension"],
                "allergies": ["Penicillin", "Peanuts"],
                
                "current_medications": [
                    {
                        "name": "Ventolin Inhaler",
                        "dosage": "2 puffs",
                        "frequency": "As needed",
                        "started_date": "2023-05-10"
                    },
                    {
                        "name": "Concor 5mg",
                        "dosage": "1 tablet",
                        "frequency": "Once daily",
                        "started_date": "2023-08-15"
                    }
                ],
                
                "insurance": {
                    "provider": "Misr Insurance",
                    "policy_number": "INS123456",
                    "expiry": "2025-12-31"
                },
                
                "external_links": {
                    "lab_account": "LAB789456",
                    "imaging_account": "IMG123789",
                    "pharmacy_id": "PHM456123"
                },
                
                "created_at": "2024-11-15 14:30:00",
                "last_updated": "2024-11-27 10:00:00"
            },
            
            {
                "national_id": "29012151234567",
                "full_name": "Fatma Ahmed Ibrahim",
                "date_of_birth": "1990-12-15",
                "age": 33,
                "gender": "Female",
                "blood_type": "O+",
                "phone": "01187654321",
                "email": "fatma.ahmed@email.com",
                "address": "22 Nasr City, Cairo",
                
                "emergency_contact": {
                    "name": "Ahmed Ibrahim",
                    "relation": "Husband",
                    "phone": "01234567890"
                },
                
                "chronic_diseases": ["Type 2 Diabetes"],
                "allergies": [],
                
                "current_medications": [
                    {
                        "name": "Glucophage 500mg",
                        "dosage": "1 tablet",
                        "frequency": "Twice daily",
                        "started_date": "2022-03-20"
                    }
                ],
                
                "insurance": {
                    "provider": "Egyptian General Insurance",
                    "policy_number": "INS789012",
                    "expiry": "2025-06-30"
                },
                
                "external_links": {},
                
                "created_at": "2024-11-10 09:15:00",
                "last_updated": "2024-11-20 15:30:00"
            }
        ]
    }
    
    # Save to patients.json
    patients_file = DATA_DIR / 'patients.json'
    with open(patients_file, 'w', encoding='utf-8') as f:
        json.dump(patients, f, indent=2, ensure_ascii=False)
    
    print("✅ Test patient records created successfully!")

def generate_test_visits():
    """Create sample medical visits"""
    
    visits = {
        "visits": [
            {
                "visit_id": "V001",
                "patient_national_id": "29501012345678",
                "date": "2024-11-15",
                "time": "10:30",
                "doctor_id": "D001",
                "doctor_name": "Dr. Ahmed Mohamed",
                "hospital": "Cairo University Hospital",
                "department": "Cardiology",
                "visit_type": "Consultation",
                
                "chief_complaint": "Chest pain and shortness of breath",
                "diagnosis": "Stable angina",
                "treatment_plan": "Prescribed beta-blockers, advised lifestyle changes, follow-up in 2 weeks",
                
                "vital_signs": {
                    "blood_pressure": "140/90 mmHg",
                    "heart_rate": "88 bpm",
                    "temperature": "37.0°C",
                    "weight": "78 kg"
                },
                
                "prescriptions": [
                    {
                        "medication": "Concor 5mg",
                        "dosage": "1 tablet",
                        "frequency": "Once daily",
                        "duration": "30 days"
                    }
                ],
                
                "notes": "Patient reports improvement with current asthma treatment. Blood pressure slightly elevated.",
                "attachments": []
            },
            
            {
                "visit_id": "V002",
                "patient_national_id": "29501012345678",
                "date": "2024-10-20",
                "time": "14:00",
                "doctor_id": "D001",
                "doctor_name": "Dr. Ahmed Mohamed",
                "hospital": "Cairo University Hospital",
                "department": "Cardiology",
                "visit_type": "Follow-up",
                
                "chief_complaint": "Routine check-up",
                "diagnosis": "Asthma - controlled",
                "treatment_plan": "Continue current medications",
                
                "vital_signs": {
                    "blood_pressure": "130/85 mmHg",
                    "heart_rate": "75 bpm",
                    "temperature": "36.8°C",
                    "weight": "79 kg"
                },
                
                "prescriptions": [],
                "notes": "Patient doing well. No complaints.",
                "attachments": []
            }
        ]
    }
    
    # Save to visits.json
    visits_file = DATA_DIR / 'visits.json'
    with open(visits_file, 'w', encoding='utf-8') as f:
        json.dump(visits, f, indent=2, ensure_ascii=False)
    
    print("✅ Test visits created successfully!")

def main():
    """Generate all test data"""
    print("🔄 Generating test data for MedLink...\n")
    
    # Create data directory if it doesn't exist
    DATA_DIR.mkdir(exist_ok=True)
    
    # Generate test data
    generate_test_users()
    generate_test_patients()
    generate_test_visits()
    
    print("\n" + "="*50)
    print("✅ All test data generated successfully!")
    print("="*50)
    print("\n🚀 You can now login with:")
    print("\n👨‍⚕️ Doctor Login:")
    print("   Username: dr.ahmed")
    print("   Password: password")
    print("\n👤 Patient Login:")
    print("   Username: patient_29501012345678")
    print("   Password: password123")

if __name__ == "__main__":
    main()