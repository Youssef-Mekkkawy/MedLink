"""
Complete Database Setup with Test Data
Creates tables and populates with realistic Egyptian medical data
"""

import sys
from pathlib import Path
from datetime import datetime, date, timedelta
import random
import hashlib

# Add project to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from core.database import Base, engine, get_db_context, init_db
from core.models import (
    User, Patient, DoctorCard, PatientCard,
    Surgery, Hospitalization, Vaccination, CurrentMedication,
    Visit, Prescription, VitalSign, LabResult, ImagingResult
)

def hash_password(password):
    """Hash password using SHA-256"""
    return hashlib.sha256(password.encode()).hexdigest()

class DatabaseSeeder:
    """Generate realistic test data"""
    
    # Egyptian names
    MALE_FIRST_NAMES = [
        "Ahmed", "Mohamed", "Mahmoud", "Ali", "Hassan",
        "Omar", "Youssef", "Ibrahim", "Mostafa", "Khaled"
    ]
    
    FEMALE_FIRST_NAMES = [
        "Fatima", "Aisha", "Mariam", "Nour", "Sara",
        "Heba", "Mona", "Dina", "Layla", "Yasmin"
    ]
    
    LAST_NAMES = [
        "Hassan", "Mohamed", "Ahmed", "Ali", "Ibrahim",
        "Mahmoud", "Said", "Abdel Rahman", "El-Sayed", "Farouk"
    ]
    
    SPECIALIZATIONS = [
        "Cardiology", "Pediatrics", "Internal Medicine",
        "Orthopedics", "Dermatology", "Neurology",
        "Obstetrics & Gynecology", "ENT", "Ophthalmology"
    ]
    
    HOSPITALS = [
        "Cairo University Hospital",
        "Ain Shams University Hospital",
        "Kasr Al Ainy Hospital",
        "El Demerdash Hospital",
        "Sheikh Zayed Specialized Hospital",
        "October 6 University Hospital"
    ]
    
    CITIES = [
        "Cairo", "Giza", "Alexandria", "Tanta",
        "Mansoura", "Ismailia", "Port Said"
    ]
    
    BLOOD_TYPES = ["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"]
    
    CHRONIC_DISEASES = [
        "Diabetes Type 2", "Hypertension", "Asthma",
        "Hypothyroidism", "Rheumatoid Arthritis"
    ]
    
    ALLERGIES = [
        "Penicillin", "Aspirin", "Ibuprofen",
        "Pollen", "Peanuts", "Shellfish"
    ]
    
    VACCINES = [
        "Hepatitis B", "MMR", "Tetanus", "Influenza",
        "COVID-19", "Pneumococcal", "Varicella"
    ]
    
    def __init__(self):
        self.doctors = []
        self.patients = []
    
    def generate_national_id(self):
        """Generate realistic Egyptian national ID - EXACTLY 14 digits"""
        century = random.choice([2, 3])
        year = random.randint(50, 99) if century == 2 else random.randint(0, 5)
        month = random.randint(1, 12)
        day = random.randint(1, 28)
        governorate = random.randint(1, 35)
        sequence = random.randint(1, 9999)  # ✅ 4 digits now
        check = random.randint(0, 9)
        
        # Format: CYYMMDDSGGSSSC (14 digits total)
        national_id = f"{century}{year:02d}{month:02d}{day:02d}{governorate:02d}{sequence:04d}{check}"
        
        # Verify it's exactly 14 digits
        assert len(national_id) == 14, f"Must be 14 digits, got {len(national_id)}"
        
        return national_id
    
    def generate_phone(self):
        """Generate Egyptian mobile number"""
        operators = ['010', '011', '012', '015']
        return f"{random.choice(operators)}{random.randint(10000000, 99999999)}"
    
    def create_doctors(self, count=10):
        """Create doctor users"""
        print(f"\n📋 Creating {count} doctors...")
        
        with get_db_context() as db:
            for i in range(count):
                # Generate doctor data
                gender = random.choice(['Male', 'Female'])
                first_name = random.choice(
                    self.MALE_FIRST_NAMES if gender == 'Male' else self.FEMALE_FIRST_NAMES
                )
                last_name = random.choice(self.LAST_NAMES)
                full_name = f"Dr. {first_name} {last_name}"
                
                username = f"dr.{first_name.lower()}.{last_name.lower().replace(' ', '')}"
                
                national_id = self.generate_national_id()
                
                # Create user
                user = User(
                    user_id=f"DOC{i+1:03d}",
                    username=username,
                    password_hash=hash_password("password123"),  # Default password
                    role='doctor',
                    full_name=full_name,
                    email=f"{username}@medlink.com",
                    phone=self.generate_phone(),
                    national_id=national_id,
                    specialization=random.choice(self.SPECIALIZATIONS),
                    hospital=random.choice(self.HOSPITALS),
                    license_number=f"LIC{random.randint(100000, 999999)}",
                    account_status='active'
                )
                
                db.add(user)
                self.doctors.append(user)
                
                # Create NFC card for doctor
                card_uid = f"07241841{i:02d}"
                doctor_card = DoctorCard(
                    card_uid=card_uid,
                    user_id=user.user_id,
                    username=user.username,
                    full_name=user.full_name,
                    is_active=True
                )
                db.add(doctor_card)
                
                print(f"   ✅ {full_name} - Username: {username} - Card: {card_uid}")
            
            db.flush()
        
        print(f"✅ Created {count} doctors with NFC cards")
    
    def create_patients(self, count=30):
        """Create patient records"""
        print(f"\n👥 Creating {count} patients...")
        
        with get_db_context() as db:
            for i in range(count):
                # Generate patient data
                gender = random.choice(['Male', 'Female'])
                first_name = random.choice(
                    self.MALE_FIRST_NAMES if gender == 'Male' else self.FEMALE_FIRST_NAMES
                )
                last_name = random.choice(self.LAST_NAMES)
                full_name = f"{first_name} {last_name}"
                
                # Birth date (between 1 and 80 years old)
                birth_year = datetime.now().year - random.randint(1, 80)
                birth_date = date(birth_year, random.randint(1, 12), random.randint(1, 28))
                age = datetime.now().year - birth_year
                
                national_id = self.generate_national_id()
                city = random.choice(self.CITIES)
                
                # Random chronic diseases and allergies
                has_chronic = random.random() < 0.3
                chronic_diseases = random.sample(self.CHRONIC_DISEASES, random.randint(0, 2)) if has_chronic else []
                
                has_allergies = random.random() < 0.25
                allergies = random.sample(self.ALLERGIES, random.randint(1, 3)) if has_allergies else []
                
                # Create patient
                patient = Patient(
                    national_id=national_id,
                    full_name=full_name,
                    date_of_birth=birth_date,
                    age=age,
                    gender=gender,
                    blood_type=random.choice(self.BLOOD_TYPES),
                    phone=self.generate_phone(),
                    email=f"{first_name.lower()}.{last_name.lower().replace(' ', '')}@email.com",
                    address=f"{random.randint(1, 200)} {random.choice(['Tahrir', 'Ramses', 'Nasr', 'Heliopolis'])} Street",
                    city=city,
                    governorate=city,
                    
                    # JSON fields
                    chronic_diseases=chronic_diseases,
                    allergies=allergies,
                    emergency_contact={
                        "name": f"{random.choice(self.MALE_FIRST_NAMES)} {last_name}",
                        "relationship": random.choice(["Spouse", "Parent", "Sibling"]),
                        "phone": self.generate_phone()
                    },
                    family_history={
                        "diabetes": random.choice([True, False]),
                        "heart_disease": random.choice([True, False]),
                        "cancer": random.choice([True, False])
                    },
                    lifestyle={
                        "smoking": random.choice(["never", "former", "current"]),
                        "alcohol": random.choice(["never", "occasional", "regular"]),
                        "exercise": random.choice(["sedentary", "moderate", "active"])
                    },
                    
                    # NFC card
                    nfc_card_assigned=random.random() < 0.7,  # 70% have cards
                    nfc_card_uid=f"07257551{i:02d}" if random.random() < 0.7 else None,
                    nfc_card_status='active' if random.random() < 0.7 else None
                )
                
                db.add(patient)
                self.patients.append(patient)
                
                # Create NFC card for some patients
                if patient.nfc_card_uid:
                    patient_card = PatientCard(
                        card_uid=patient.nfc_card_uid,
                        national_id=patient.national_id,
                        full_name=patient.full_name,
                        is_active=True
                    )
                    db.add(patient_card)
                
                print(f"   ✅ {full_name} - {national_id} - {city}" + 
                      (f" - Card: {patient.nfc_card_uid}" if patient.nfc_card_uid else ""))
            
            db.flush()
        
        print(f"✅ Created {count} patients")
    
    def create_medical_records(self):
        """Create medical records for patients"""
        print(f"\n🏥 Creating medical records...")
        
        with get_db_context() as db:
            visit_count = 0
            surgery_count = 0
            hosp_count = 0
            vacc_count = 0
            
            for patient in self.patients[:20]:  # Add records for first 20 patients
                
                # Surgeries (20% chance)
                if random.random() < 0.2:
                    surgery = Surgery(
                        surgery_id=f"SURG{surgery_count+1:04d}",
                        patient_national_id=patient.national_id,
                        procedure_name=random.choice([
                            "Appendectomy", "Cholecystectomy", "Hernia Repair",
                            "Cesarean Section", "Knee Arthroscopy"
                        ]),
                        date=date.today() - timedelta(days=random.randint(30, 365*3)),
                        hospital=random.choice(self.HOSPITALS),
                        surgeon_name=random.choice(self.doctors).full_name if self.doctors else "Dr. Smith",
                        outcome=random.choice(["successful", "successful", "successful", "complicated"])
                    )
                    db.add(surgery)
                    surgery_count += 1
                
                # Hospitalizations (15% chance)
                if random.random() < 0.15:
                    admission_date = date.today() - timedelta(days=random.randint(60, 365))
                    discharge_date = admission_date + timedelta(days=random.randint(2, 10))
                    
                    hosp = Hospitalization(
                        hospitalization_id=f"HOSP{hosp_count+1:04d}",
                        patient_national_id=patient.national_id,
                        hospital=random.choice(self.HOSPITALS),
                        admission_date=admission_date,
                        discharge_date=discharge_date,
                        admission_reason=random.choice([
                            "Pneumonia", "Heart Attack", "Stroke",
                            "Severe Infection", "Diabetic Crisis"
                        ]),
                        days_stayed=(discharge_date - admission_date).days
                    )
                    db.add(hosp)
                    hosp_count += 1
                
                # Vaccinations (each patient gets 2-4)
                for _ in range(random.randint(2, 4)):
                    vacc = Vaccination(
                        patient_national_id=patient.national_id,
                        vaccine_name=random.choice(self.VACCINES),
                        date_administered=date.today() - timedelta(days=random.randint(30, 365*5)),
                        dose_number=random.choice(["1st dose", "2nd dose", "Booster"]),
                        location=random.choice(self.HOSPITALS)
                    )
                    db.add(vacc)
                    vacc_count += 1
                
                # Visits (each patient gets 1-3 visits)
                for _ in range(random.randint(1, 3)):
                    doctor = random.choice(self.doctors) if self.doctors else None
                    visit_date = date.today() - timedelta(days=random.randint(1, 180))
                    
                    visit = Visit(
                        visit_id=f"V{visit_count+1:05d}",
                        patient_national_id=patient.national_id,
                        doctor_id=doctor.user_id if doctor else "DOC001",
                        doctor_name=doctor.full_name if doctor else "Dr. Unknown",
                        date=visit_date,
                        time=datetime.now().time(),
                        visit_type=random.choice(['regular', 'emergency', 'followup']),
                        chief_complaint=random.choice([
                            "Fever and cough", "Chest pain", "Headache",
                            "Abdominal pain", "Joint pain", "Fatigue"
                        ]),
                        diagnosis=random.choice([
                            "Upper Respiratory Infection", "Hypertension",
                            "Gastritis", "Migraine", "Arthritis"
                        ])
                    )
                    db.add(visit)
                    visit_count += 1
            
            print(f"   ✅ Created {visit_count} visits")
            print(f"   ✅ Created {surgery_count} surgeries")
            print(f"   ✅ Created {hosp_count} hospitalizations")
            print(f"   ✅ Created {vacc_count} vaccinations")
        
        print(f"✅ Medical records created")
    
    def create_all(self, doctors=10, patients=30):
        """Create everything"""
        print("\n" + "="*60)
        print("🏥 MEDLINK DATABASE SETUP WITH TEST DATA")
        print("="*60)
        
        # Create tables
        print("\n📊 Creating database tables...")
        init_db()
        print("✅ Tables created")
        
        # Create data
        self.create_doctors(doctors)
        self.create_patients(patients)
        self.create_medical_records()
        
        # Summary
        print("\n" + "="*60)
        print("📊 SETUP COMPLETE!")
        print("="*60)
        print(f"\n✅ Created {len(self.doctors)} doctors")
        print(f"✅ Created {len(self.patients)} patients")
        print(f"✅ Created medical records")
        
        print("\n🔑 LOGIN CREDENTIALS:")
        print("\nDoctors (username / password):")
        for i, doc in enumerate(self.doctors[:5], 1):
            print(f"   {i}. {doc.username} / password123")
        
        print("\n💳 NFC CARDS:")
        print("\nDoctor Cards:")
        for i in range(min(5, len(self.doctors))):
            print(f"   {i+1}. Card UID: 07241841{i:02d}")
        
        print("\nPatient Cards (first 5 with cards):")
        cards_shown = 0
        for i, patient in enumerate(self.patients):
            if patient.nfc_card_uid and cards_shown < 5:
                print(f"   {cards_shown+1}. {patient.full_name} - Card: {patient.nfc_card_uid}")
                cards_shown += 1
        
        print("\n" + "="*60)
        print("\n🚀 Ready to test! Run: python main.py")
        print("="*60 + "\n")


def main():
    """Main setup function"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Setup MedLink database with test data')
    parser.add_argument('--doctors', type=int, default=10, help='Number of doctors to create')
    parser.add_argument('--patients', type=int, default=30, help='Number of patients to create')
    parser.add_argument('--reset', action='store_true', help='Drop existing tables first')
    
    args = parser.parse_args()
    
    # Reset database if requested
    if args.reset:
        print("\n⚠️  WARNING: This will delete all existing data!")
        confirm = input("Type 'yes' to continue: ")
        if confirm.lower() == 'yes':
            from core.database import drop_db
            drop_db()
            print("✅ Database reset")
        else:
            print("❌ Cancelled")
            return
    
    # Create seeder and run
    seeder = DatabaseSeeder()
    seeder.create_all(doctors=args.doctors, patients=args.patients)


if __name__ == "__main__":
    main()
