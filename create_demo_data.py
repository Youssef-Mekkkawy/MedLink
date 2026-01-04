"""
Demo Data Generator for MedLink
Creates comprehensive sample data for video showcase
"""

from core.database import SessionLocal
from core.patient_manager import PatientManager
from core.doctor_manager import DoctorManager
from core.medical_managers import visit_manager,lab_manager,imaging_manager,nfc_manager,audit_manager
from core.lab_manager import LabResult
from core.imaging_result import ImagingResult
from core.prescription import Prescription
from datetime import datetime, timedelta
import json
import random


def create_demo_doctors(session):
    """Create demo doctors"""
    print("\n👨‍⚕️ Creating Demo Doctors...")
    
    doctor_manager = DoctorManager(session)
    
    doctors = [
        {
            "national_id": "2850312047801",
            "full_name": "Dr. Ahmed Hassan",
            "email": "ahmed.hassan@medlink.com",
            "phone": "01001234567",
            "password": "doctor123",
            "specialization": "Cardiology",
            "license_number": "MED-2015-12345",
            "hospital": "Cairo University Hospital",
            "department": "Cardiology Department",
            "gender": "Male",
            "date_of_birth": "1985-03-12"
        },
        {
            "national_id": "2900615048902",
            "full_name": "Dr. Sara Mohamed",
            "email": "sara.mohamed@medlink.com",
            "phone": "01009876543",
            "password": "doctor123",
            "specialization": "Pediatrics",
            "license_number": "MED-2018-54321",
            "hospital": "Children's Hospital",
            "department": "Pediatrics",
            "gender": "Female",
            "date_of_birth": "1990-06-15"
        },
        {
            "national_id": "2880920049103",
            "full_name": "Dr. Mohamed Ali",
            "email": "mohamed.ali@medlink.com",
            "phone": "01112345678",
            "password": "doctor123",
            "specialization": "Orthopedics",
            "license_number": "MED-2016-67890",
            "hospital": "Orthopedic Center",
            "department": "Orthopedics",
            "gender": "Male",
            "date_of_birth": "1988-09-20"
        }
    ]
    
    for doctor_data in doctors:
        try:
            doctor = doctor_manager.create_doctor(doctor_data)
            print(f"✅ Created: {doctor_data['full_name']} - {doctor_data['specialization']}")
        except Exception as e:
            print(f"⚠️ Doctor already exists or error: {e}")
    
    return doctors


def create_demo_patients(session):
    """Create demo patients with COMPLETE data"""
    print("\n👥 Creating Demo Patients...")
    
    patient_manager = PatientManager(session)
    
    patients = [
        {
            "national_id": "3800419046601",
            "full_name": "Mona Said",
            "date_of_birth": "1980-04-19",
            "age": 45,
            "gender": "Female",
            "blood_type": "A+",
            "phone": "01124458479",
            "email": "mona.said@email.com",
            "address": "15 Tahrir Street, Cairo, Egypt",
            "emergency_contact_name": "Ahmed Said",
            "emergency_contact_phone": "01234567890",
            "height": 165.0,
            "weight": 68.5,
            
            # Chronic Conditions
            "chronic_conditions": [
                {
                    "condition": "Type 2 Diabetes",
                    "diagnosed_date": "2015-06-20",
                    "severity": "Moderate",
                    "status": "Controlled",
                    "notes": "Well controlled with medication and diet"
                },
                {
                    "condition": "Hypertension",
                    "diagnosed_date": "2018-03-15",
                    "severity": "Mild",
                    "status": "Controlled",
                    "notes": "Managed with lifestyle changes and medication"
                }
            ],
            
            # Allergies
            "allergies": [
                {
                    "allergen": "Penicillin",
                    "type": "Medication",
                    "severity": "Severe",
                    "reaction": "Anaphylaxis",
                    "diagnosed_date": "2010-05-12"
                },
                {
                    "allergen": "Peanuts",
                    "type": "Food",
                    "severity": "Moderate",
                    "reaction": "Hives and swelling",
                    "diagnosed_date": "2005-08-22"
                },
                {
                    "allergen": "Dust Mites",
                    "type": "Environmental",
                    "severity": "Mild",
                    "reaction": "Sneezing, runny nose",
                    "diagnosed_date": "2012-02-10"
                }
            ],
            
            # Current Medications
            "current_medications": [
                {
                    "name": "Metformin",
                    "dosage": "500mg",
                    "frequency": "Twice daily",
                    "route": "Oral",
                    "start_date": "2015-06-25",
                    "prescribed_by": "Dr. Ahmed Hassan",
                    "purpose": "Diabetes management",
                    "notes": "Take with meals"
                },
                {
                    "name": "Amlodipine",
                    "dosage": "5mg",
                    "frequency": "Once daily",
                    "route": "Oral",
                    "start_date": "2018-03-20",
                    "prescribed_by": "Dr. Ahmed Hassan",
                    "purpose": "Blood pressure control",
                    "notes": "Take in the morning"
                },
                {
                    "name": "Atorvastatin",
                    "dosage": "20mg",
                    "frequency": "Once daily at bedtime",
                    "route": "Oral",
                    "start_date": "2020-01-15",
                    "prescribed_by": "Dr. Ahmed Hassan",
                    "purpose": "Cholesterol management",
                    "notes": "Monitor liver function"
                }
            ],
            
            # Surgeries
            "surgeries": [
                {
                    "procedure": "Appendectomy",
                    "date": "2010-09-15",
                    "hospital": "Cairo University Hospital",
                    "surgeon": "Dr. Mohamed Ibrahim",
                    "outcome": "Successful",
                    "complications": "None",
                    "notes": "Emergency surgery, quick recovery"
                },
                {
                    "procedure": "Cholecystectomy (Gallbladder Removal)",
                    "date": "2019-05-22",
                    "hospital": "Cairo University Hospital",
                    "surgeon": "Dr. Hany Salah",
                    "outcome": "Successful",
                    "complications": "Minor post-op infection, resolved",
                    "notes": "Laparoscopic procedure"
                }
            ],
            
            # Hospitalizations
            "hospitalizations": [
                {
                    "reason": "Severe Dehydration",
                    "admission_date": "2022-07-10",
                    "discharge_date": "2022-07-13",
                    "hospital": "Cairo University Hospital",
                    "department": "Emergency Medicine",
                    "attending_doctor": "Dr. Ahmed Hassan",
                    "diagnosis": "Acute gastroenteritis with dehydration",
                    "treatment": "IV fluids, antibiotics",
                    "outcome": "Full recovery"
                },
                {
                    "reason": "Blood Sugar Control",
                    "admission_date": "2021-11-05",
                    "discharge_date": "2021-11-08",
                    "hospital": "Cairo University Hospital",
                    "department": "Endocrinology",
                    "attending_doctor": "Dr. Laila Mahmoud",
                    "diagnosis": "Hyperglycemia",
                    "treatment": "Insulin adjustment, diet counseling",
                    "outcome": "Stabilized"
                }
            ],
            
            # Vaccinations
            "vaccinations": [
                {
                    "vaccine": "Influenza (Flu Shot)",
                    "date": "2024-10-15",
                    "provider": "Cairo Health Clinic",
                    "lot_number": "FLU2024-001",
                    "next_dose": "2025-10-15"
                },
                {
                    "vaccine": "COVID-19 Booster",
                    "date": "2024-03-20",
                    "provider": "Ministry of Health Center",
                    "lot_number": "COV2024-456",
                    "next_dose": "2024-09-20"
                },
                {
                    "vaccine": "Hepatitis B",
                    "date": "2020-01-10",
                    "provider": "Cairo University Hospital",
                    "lot_number": "HEPB2020-789",
                    "next_dose": "N/A - Series complete"
                },
                {
                    "vaccine": "Tetanus/Diphtheria",
                    "date": "2019-06-15",
                    "provider": "Local Health Center",
                    "lot_number": "TD2019-123",
                    "next_dose": "2029-06-15"
                }
            ],
            
            # Family History
            "family_history": {
                "father": {
                    "conditions": ["Diabetes Type 2", "Heart Disease"],
                    "age_of_diagnosis": {"Diabetes Type 2": 55, "Heart Disease": 62},
                    "status": "Deceased at 70",
                    "cause_of_death": "Myocardial Infarction"
                },
                "mother": {
                    "conditions": ["Hypertension", "Osteoporosis"],
                    "age_of_diagnosis": {"Hypertension": 50, "Osteoporosis": 65},
                    "status": "Living at 75",
                    "notes": "Generally healthy, manages conditions well"
                },
                "siblings": [
                    {
                        "relation": "Brother",
                        "age": 48,
                        "conditions": ["None reported"],
                        "notes": "Healthy"
                    },
                    {
                        "relation": "Sister",
                        "age": 42,
                        "conditions": ["Asthma"],
                        "notes": "Well controlled"
                    }
                ],
                "genetic_risks": [
                    "Cardiovascular Disease - High Risk",
                    "Type 2 Diabetes - High Risk",
                    "Hypertension - Moderate Risk"
                ]
            },
            
            # Disabilities/Special Needs
            "disabilities_special_needs": {
                "physical_disabilities": [],
                "mental_health": [
                    {
                        "condition": "Mild Anxiety",
                        "diagnosed_date": "2020-08-10",
                        "treatment": "Counseling",
                        "status": "Managed"
                    }
                ],
                "special_needs": [],
                "mobility_aids": "None",
                "communication_needs": "None",
                "notes": "No significant disabilities"
            },
            
            # Emergency Directives
            "emergency_directives": {
                "dnr_order": False,
                "organ_donor": True,
                "power_of_attorney": {
                    "name": "Ahmed Said",
                    "relationship": "Husband",
                    "phone": "01234567890",
                    "email": "ahmed.said@email.com"
                },
                "healthcare_proxy": {
                    "name": "Ahmed Said",
                    "relationship": "Husband",
                    "phone": "01234567890"
                },
                "living_will": True,
                "religious_preferences": {
                    "religion": "Islam",
                    "dietary_restrictions": "Halal food only",
                    "prayer_needs": "5 times daily",
                    "end_of_life_wishes": "Religious funeral rites"
                },
                "advance_directives_file": "advance_directives_mona_said.pdf"
            },
            
            # Lifestyle
            "lifestyle": {
                "smoking": {
                    "status": "Never",
                    "packs_per_day": 0,
                    "years_smoked": 0,
                    "quit_date": None
                },
                "alcohol": {
                    "status": "Never",
                    "drinks_per_week": 0,
                    "type": None
                },
                "exercise": {
                    "frequency": "3-4 times per week",
                    "type": ["Walking", "Swimming", "Yoga"],
                    "duration_minutes": 45,
                    "notes": "Regular exercise routine"
                },
                "diet": {
                    "type": "Balanced Mediterranean diet",
                    "restrictions": ["Low sugar", "Low sodium"],
                    "preferences": "Prefers fresh vegetables and fish",
                    "notes": "Following diabetic meal plan"
                },
                "sleep": {
                    "hours_per_night": 7,
                    "quality": "Good",
                    "issues": "Occasional insomnia during stress"
                },
                "stress_level": "Moderate",
                "occupation": "School Teacher",
                "occupational_hazards": "None significant"
            }
        },
        
        # Second Patient - Younger Male
        {
            "national_id": "3950815047702",
            "full_name": "Karim Mostafa",
            "date_of_birth": "1995-08-15",
            "age": 29,
            "gender": "Male",
            "blood_type": "O+",
            "phone": "01187654321",
            "email": "karim.mostafa@email.com",
            "address": "42 Nasr City, Cairo, Egypt",
            "emergency_contact_name": "Fatima Mostafa",
            "emergency_contact_phone": "01098765432",
            "height": 178.0,
            "weight": 82.0,
            
            "chronic_conditions": [
                {
                    "condition": "Asthma",
                    "diagnosed_date": "2010-03-10",
                    "severity": "Mild",
                    "status": "Controlled",
                    "notes": "Exercise-induced, well managed"
                }
            ],
            
            "allergies": [
                {
                    "allergen": "Latex",
                    "type": "Contact",
                    "severity": "Moderate",
                    "reaction": "Skin rash",
                    "diagnosed_date": "2018-07-05"
                }
            ],
            
            "current_medications": [
                {
                    "name": "Albuterol Inhaler",
                    "dosage": "90mcg",
                    "frequency": "As needed",
                    "route": "Inhalation",
                    "start_date": "2010-03-15",
                    "prescribed_by": "Dr. Sara Mohamed",
                    "purpose": "Asthma relief",
                    "notes": "Use before exercise"
                }
            ],
            
            "surgeries": [
                {
                    "procedure": "ACL Reconstruction",
                    "date": "2020-11-10",
                    "hospital": "Orthopedic Center",
                    "surgeon": "Dr. Mohamed Ali",
                    "outcome": "Successful",
                    "complications": "None",
                    "notes": "Sports injury, full recovery after 8 months"
                }
            ],
            
            "hospitalizations": [],
            
            "vaccinations": [
                {
                    "vaccine": "COVID-19 Primary Series",
                    "date": "2021-06-15",
                    "provider": "Ministry of Health Center",
                    "lot_number": "COV2021-123",
                    "next_dose": "Booster recommended 2024"
                },
                {
                    "vaccine": "Hepatitis B Series",
                    "date": "2015-05-20",
                    "provider": "University Health Center",
                    "lot_number": "HEPB2015-456",
                    "next_dose": "N/A - Complete"
                }
            ],
            
            "family_history": {
                "father": {
                    "conditions": ["None reported"],
                    "status": "Living at 58",
                    "notes": "Healthy"
                },
                "mother": {
                    "conditions": ["Asthma"],
                    "age_of_diagnosis": {"Asthma": 25},
                    "status": "Living at 55",
                    "notes": "Well controlled"
                },
                "siblings": [],
                "genetic_risks": ["Asthma - Moderate Risk"]
            },
            
            "disabilities_special_needs": {
                "physical_disabilities": [],
                "mental_health": [],
                "special_needs": [],
                "mobility_aids": "None",
                "communication_needs": "None",
                "notes": "No disabilities"
            },
            
            "emergency_directives": {
                "dnr_order": False,
                "organ_donor": True,
                "power_of_attorney": {
                    "name": "Fatima Mostafa",
                    "relationship": "Mother",
                    "phone": "01098765432",
                    "email": "fatima.mostafa@email.com"
                },
                "healthcare_proxy": {
                    "name": "Fatima Mostafa",
                    "relationship": "Mother",
                    "phone": "01098765432"
                },
                "living_will": False,
                "religious_preferences": {
                    "religion": "Islam",
                    "dietary_restrictions": "Halal preferred",
                    "prayer_needs": "Yes",
                    "end_of_life_wishes": "Standard Islamic practices"
                },
                "advance_directives_file": None
            },
            
            "lifestyle": {
                "smoking": {
                    "status": "Never",
                    "packs_per_day": 0,
                    "years_smoked": 0,
                    "quit_date": None
                },
                "alcohol": {
                    "status": "Occasional",
                    "drinks_per_week": 2,
                    "type": "Social drinking"
                },
                "exercise": {
                    "frequency": "5-6 times per week",
                    "type": ["Gym", "Football", "Running"],
                    "duration_minutes": 90,
                    "notes": "Very active lifestyle"
                },
                "diet": {
                    "type": "High protein",
                    "restrictions": [],
                    "preferences": "Athlete diet, lots of lean protein",
                    "notes": "Tracks macros"
                },
                "sleep": {
                    "hours_per_night": 8,
                    "quality": "Excellent",
                    "issues": "None"
                },
                "stress_level": "Low",
                "occupation": "Software Engineer",
                "occupational_hazards": "Prolonged sitting"
            }
        }
    ]
    
    created_patients = []
    for patient_data in patients:
        try:
            patient = patient_manager.create_patient(patient_data)
            created_patients.append(patient_data)
            print(f"✅ Created: {patient_data['full_name']} - {patient_data['age']} years old")
        except Exception as e:
            print(f"⚠️ Patient already exists or error: {e}")
    
    return created_patients


def create_medical_visits(session, patients, doctors):
    """Create medical visit history"""
    print("\n📋 Creating Medical Visits...")
    
    visits = [
        # Mona's visits
        {
            "patient_id": "3800419046601",
            "doctor_id": "2850312047801",
            "visit_date": (datetime.now() - timedelta(days=7)).date(),
            "visit_type": "Follow-up",
            "chief_complaint": "Routine diabetes check-up",
            "vital_signs": json.dumps({
                "blood_pressure": "128/82",
                "heart_rate": 78,
                "temperature": 36.8,
                "respiratory_rate": 16,
                "oxygen_saturation": 98,
                "weight": 68.5,
                "height": 165
            }),
            "diagnosis": "Type 2 Diabetes - Well controlled, Hypertension - Stable",
            "treatment_plan": "Continue current medications, maintain diet and exercise",
            "notes": "Patient reports good compliance with medication. Blood sugar levels improved.",
            "follow_up_date": (datetime.now() + timedelta(days=90)).date(),
            "status": "Completed"
        },
        {
            "patient_id": "3800419046601",
            "doctor_id": "2850312047801",
            "visit_date": (datetime.now() - timedelta(days=95)).date(),
            "visit_type": "Follow-up",
            "chief_complaint": "Blood pressure monitoring",
            "vital_signs": json.dumps({
                "blood_pressure": "132/85",
                "heart_rate": 80,
                "temperature": 36.9,
                "respiratory_rate": 16,
                "oxygen_saturation": 97,
                "weight": 69.0,
                "height": 165
            }),
            "diagnosis": "Hypertension - Requires medication adjustment",
            "treatment_plan": "Increased Amlodipine to 5mg, lifestyle modifications",
            "notes": "Slight elevation in BP, increased medication dosage",
            "follow_up_date": (datetime.now() - timedelta(days=7)).date(),
            "status": "Completed"
        },
        
        # Karim's visits
        {
            "patient_id": "3950815047702",
            "doctor_id": "2880920049103",
            "visit_date": (datetime.now() - timedelta(days=14)).date(),
            "visit_type": "Follow-up",
            "chief_complaint": "Post-surgery knee check",
            "vital_signs": json.dumps({
                "blood_pressure": "118/75",
                "heart_rate": 65,
                "temperature": 36.7,
                "respiratory_rate": 14,
                "oxygen_saturation": 99,
                "weight": 82.0,
                "height": 178
            }),
            "diagnosis": "ACL reconstruction - Excellent recovery",
            "treatment_plan": "Continue physical therapy, gradual return to sports",
            "notes": "Full range of motion restored, no pain reported",
            "follow_up_date": (datetime.now() + timedelta(days=180)).date(),
            "status": "Completed"
        }
    ]
    
    for visit_data in visits:
        try:
            visit = MedicalVisit(**visit_data)
            session.add(visit)
            session.commit()
            print(f"✅ Created visit for patient {visit_data['patient_id']} on {visit_data['visit_date']}")
        except Exception as e:
            session.rollback()
            print(f"⚠️ Visit creation error: {e}")


def create_lab_results(session):
    """Create lab results"""
    print("\n🔬 Creating Lab Results...")
    
    lab_results = [
        # Mona's labs
        {
            "patient_id": "3800419046601",
            "doctor_id": "2850312047801",
            "test_date": (datetime.now() - timedelta(days=7)).date(),
            "test_type": "Complete Blood Count (CBC)",
            "results": json.dumps({
                "WBC": {"value": 7.2, "unit": "10^3/μL", "normal_range": "4.5-11.0", "status": "Normal"},
                "RBC": {"value": 4.5, "unit": "10^6/μL", "normal_range": "4.0-5.5", "status": "Normal"},
                "Hemoglobin": {"value": 13.5, "unit": "g/dL", "normal_range": "12.0-16.0", "status": "Normal"},
                "Hematocrit": {"value": 40.5, "unit": "%", "normal_range": "36-46", "status": "Normal"},
                "Platelets": {"value": 245, "unit": "10^3/μL", "normal_range": "150-400", "status": "Normal"}
            }),
            "lab_name": "Cairo Medical Labs",
            "notes": "All values within normal limits",
            "status": "Final"
        },
        {
            "patient_id": "3800419046601",
            "doctor_id": "2850312047801",
            "test_date": (datetime.now() - timedelta(days=7)).date(),
            "test_type": "Hemoglobin A1C (Diabetes)",
            "results": json.dumps({
                "HbA1c": {"value": 6.8, "unit": "%", "normal_range": "<7.0", "status": "Good Control"},
                "Fasting_Glucose": {"value": 118, "unit": "mg/dL", "normal_range": "70-130", "status": "Normal"}
            }),
            "lab_name": "Cairo Medical Labs",
            "notes": "Diabetes well controlled, continue current treatment",
            "status": "Final"
        },
        {
            "patient_id": "3800419046601",
            "doctor_id": "2850312047801",
            "test_date": (datetime.now() - timedelta(days=7)).date(),
            "test_type": "Lipid Panel",
            "results": json.dumps({
                "Total_Cholesterol": {"value": 195, "unit": "mg/dL", "normal_range": "<200", "status": "Normal"},
                "LDL": {"value": 115, "unit": "mg/dL", "normal_range": "<100", "status": "Slightly High"},
                "HDL": {"value": 58, "unit": "mg/dL", "normal_range": ">40", "status": "Normal"},
                "Triglycerides": {"value": 142, "unit": "mg/dL", "normal_range": "<150", "status": "Normal"}
            }),
            "lab_name": "Cairo Medical Labs",
            "notes": "LDL slightly elevated, continue statin therapy",
            "status": "Final"
        },
        
        # Karim's labs
        {
            "patient_id": "3950815047702",
            "doctor_id": "2880920049103",
            "test_date": (datetime.now() - timedelta(days=14)).date(),
            "test_type": "Complete Blood Count (CBC)",
            "results": json.dumps({
                "WBC": {"value": 6.8, "unit": "10^3/μL", "normal_range": "4.5-11.0", "status": "Normal"},
                "RBC": {"value": 5.2, "unit": "10^6/μL", "normal_range": "4.5-5.9", "status": "Normal"},
                "Hemoglobin": {"value": 15.2, "unit": "g/dL", "normal_range": "13.5-17.5", "status": "Normal"},
                "Hematocrit": {"value": 45.0, "unit": "%", "normal_range": "41-50", "status": "Normal"},
                "Platelets": {"value": 235, "unit": "10^3/μL", "normal_range": "150-400", "status": "Normal"}
            }),
            "lab_name": "Sports Medicine Lab",
            "notes": "Excellent values for active athlete",
            "status": "Final"
        }
    ]
    
    for lab_data in lab_results:
        try:
            lab = LabResult(**lab_data)
            session.add(lab)
            session.commit()
            print(f"✅ Created lab result: {lab_data['test_type']} for patient {lab_data['patient_id']}")
        except Exception as e:
            session.rollback()
            print(f"⚠️ Lab result creation error: {e}")


def create_imaging_results(session):
    """Create imaging/radiology results"""
    print("\n🏥 Creating Imaging Results...")
    
    imaging_results = [
        # Mona's imaging
        {
            "patient_id": "3800419046601",
            "doctor_id": "2850312047801",
            "imaging_date": (datetime.now() - timedelta(days=95)).date(),
            "imaging_type": "Chest X-Ray",
            "body_part": "Chest",
            "findings": "Heart size normal. Lungs clear. No acute disease.",
            "impression": "Normal chest radiograph",
            "radiologist": "Dr. Hossam Radiology",
            "facility": "Cairo Imaging Center",
            "image_path": "chest_xray_mona_20240101.dcm",
            "status": "Final"
        },
        {
            "patient_id": "3800419046601",
            "doctor_id": "2850312047801",
            "imaging_date": (datetime.now() - timedelta(days=180)).date(),
            "imaging_type": "Echocardiogram",
            "body_part": "Heart",
            "findings": "Normal left ventricular size and function. LVEF 60%. No valvular abnormalities.",
            "impression": "Normal echocardiogram. No evidence of cardiovascular disease.",
            "radiologist": "Dr. Kareem Cardiology",
            "facility": "Cairo Heart Center",
            "image_path": "echo_mona_20231115.dcm",
            "status": "Final"
        },
        
        # Karim's imaging
        {
            "patient_id": "3950815047702",
            "doctor_id": "2880920049103",
            "imaging_date": (datetime.now() - timedelta(days=30)).date(),
            "imaging_type": "MRI Knee",
            "body_part": "Left Knee",
            "findings": "Post-surgical changes consistent with ACL reconstruction. Graft intact and well-positioned. No evidence of re-injury. Full healing noted.",
            "impression": "Successful ACL reconstruction with excellent graft incorporation. No complications.",
            "radiologist": "Dr. Nabil Orthopedics",
            "facility": "Orthopedic Imaging Center",
            "image_path": "mri_knee_karim_20241120.dcm",
            "status": "Final"
        }
    ]
    
    for imaging_data in imaging_results:
        try:
            imaging = ImagingResult(**imaging_data)
            session.add(imaging)
            session.commit()
            print(f"✅ Created imaging: {imaging_data['imaging_type']} for patient {imaging_data['patient_id']}")
        except Exception as e:
            session.rollback()
            print(f"⚠️ Imaging creation error: {e}")


def create_prescriptions(session):
    """Create prescription history"""
    print("\n💊 Creating Prescriptions...")
    
    prescriptions = [
        # Mona's prescriptions
        {
            "patient_id": "3800419046601",
            "doctor_id": "2850312047801",
            "prescription_date": (datetime.now() - timedelta(days=7)).date(),
            "medications": json.dumps([
                {
                    "name": "Metformin",
                    "dosage": "500mg",
                    "frequency": "Twice daily",
                    "duration": "3 months",
                    "quantity": 180,
                    "refills": 2,
                    "instructions": "Take with meals"
                },
                {
                    "name": "Amlodipine",
                    "dosage": "5mg",
                    "frequency": "Once daily",
                    "duration": "3 months",
                    "quantity": 90,
                    "refills": 2,
                    "instructions": "Take in the morning"
                },
                {
                    "name": "Atorvastatin",
                    "dosage": "20mg",
                    "frequency": "Once daily at bedtime",
                    "duration": "3 months",
                    "quantity": 90,
                    "refills": 2,
                    "instructions": "Take at night, monitor liver function"
                }
            ]),
            "diagnosis": "Type 2 Diabetes, Hypertension, Hyperlipidemia",
            "notes": "Continue current regimen, patient tolerating well",
            "pharmacy": "El Ezaby Pharmacy",
            "status": "Active"
        },
        
        # Karim's prescriptions
        {
            "patient_id": "3950815047702",
            "doctor_id": "2880920049103",
            "prescription_date": (datetime.now() - timedelta(days=14)).date(),
            "medications": json.dumps([
                {
                    "name": "Albuterol Inhaler",
                    "dosage": "90mcg",
                    "frequency": "As needed",
                    "duration": "6 months",
                    "quantity": 1,
                    "refills": 3,
                    "instructions": "Use before exercise or as needed for symptoms"
                }
            ]),
            "diagnosis": "Exercise-induced Asthma",
            "notes": "For asthma management, use as needed",
            "pharmacy": "Seif Pharmacy",
            "status": "Active"
        }
    ]
    
    for prescription_data in prescriptions:
        try:
            prescription = Prescription(**prescription_data)
            session.add(prescription)
            session.commit()
            print(f"✅ Created prescription for patient {prescription_data['patient_id']}")
        except Exception as e:
            session.rollback()
            print(f"⚠️ Prescription creation error: {e}")


def main():
    """Main function to create all demo data"""
    print("=" * 60)
    print("🎬 MEDLINK DEMO DATA GENERATOR")
    print("=" * 60)
    
    session = SessionLocal()
    
    try:
        # Create doctors
        doctors = create_demo_doctors(session)
        
        # Create patients with comprehensive data
        patients = create_demo_patients(session)
        
        # Create medical visits
        create_medical_visits(session, patients, doctors)
        
        # Create lab results
        create_lab_results(session)
        
        # Create imaging results
        create_imaging_results(session)
        
        # Create prescriptions
        create_prescriptions(session)
        
        print("\n" + "=" * 60)
        print("✅ DEMO DATA CREATION COMPLETE!")
        print("=" * 60)
        print("\n📊 Summary:")
        print(f"   👨‍⚕️ Doctors: 3")
        print(f"   👥 Patients: 2 (with complete medical history)")
        print(f"   📋 Medical Visits: Multiple")
        print(f"   🔬 Lab Results: Comprehensive panels")
        print(f"   🏥 Imaging Results: X-ray, MRI, Echo")
        print(f"   💊 Prescriptions: Active medications")
        print("\n🎥 Ready for video showcase!")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        session.rollback()
    finally:
        session.close()


if __name__ == "__main__":
    main()