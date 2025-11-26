# 🏥 MedLink - Unified Medical Records System

![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)
![Python](https://img.shields.io/badge/python-3.9+-green.svg)
![License](https://img.shields.io/badge/license-MIT-orange.svg)

## 📖 Table of Contents

- [Overview](#overview)
- [Problem Statement](#problem-statement)
- [Solution](#solution)
- [Features](#features)
- [System Architecture](#system-architecture)
- [Installation](#installation)
- [Usage Guide](#usage-guide)
- [Project Structure](#project-structure)
- [Development Phases](#development-phases)
- [Technical Stack](#technical-stack)
- [Data Models](#data-models)
- [Security](#security)
- [Testing](#testing)
- [Future Enhancements](#future-enhancements)
- [Contributing](#contributing)
- [License](#license)

---

## 🎯 Overview

**MedLink** is a desktop-based Unified Medical Records System designed to centralize and streamline medical information management in Egypt. It provides a secure, user-friendly platform for storing, accessing, and managing patient medical records, addressing the critical gap in healthcare information systems where records are fragmented across multiple facilities.

### **Key Highlights:**

- 🔐 Secure multi-user authentication system
- 👨‍⚕️ Separate portals for doctors and patients
- 📋 Comprehensive medical record management
- 🚨 Emergency card generation with QR codes
- 🔍 Advanced search and filtering capabilities
- 📁 Support for attachments (PDFs, images)
- 🌐 Designed for future API integration

---

## ❗ Problem Statement

In Egypt's healthcare system, several critical challenges exist:

1. **Fragmented Records**: Medical records scattered across hospitals, clinics, and labs
2. **Emergency Delays**: Doctors lack immediate access to patient history in emergencies
3. **Repeated Tests**: Patients undergo duplicate tests due to missing previous results
4. **Communication Gaps**: Poor information sharing between healthcare providers
5. **Paper-Based Systems**: Slow, error-prone, and difficult to search
6. **Patient Control**: Patients have limited access to their own medical data

### **Real-World Impact:**

- ⏱️ **Time Lost**: Patients spend hours explaining medical history at each visit
- 💰 **Money Wasted**: Duplicate tests cost families and healthcare system
- ⚠️ **Safety Risks**: Missed allergies/conditions can lead to dangerous treatments
- 📉 **Inefficiency**: Doctors make decisions without complete information

---

## ✅ Solution

MedLink provides a **Proof of Concept** for a unified medical records system that:

### **For Patients:**

- ✅ Single location for all medical records
- ✅ Easy access to visit history, lab results, and imaging
- ✅ Printable emergency cards with critical information
- ✅ Ability to share records with any doctor instantly
- ✅ Control over their own medical data

### **For Doctors:**

- ✅ Quick patient lookup by National ID
- ✅ Complete medical history at a glance
- ✅ Add visit notes and prescriptions digitally
- ✅ View lab and imaging results in one place
- ✅ Make informed decisions with full context

### **For Healthcare System:**

- ✅ Reduce duplicate tests and procedures
- ✅ Improve treatment quality with complete data
- ✅ Enable better coordination between providers
- ✅ Create foundation for nationwide system
- ✅ Support research and analytics

---

## 🚀 Features

### **Authentication & Security**

- 🔐 Multi-user system (Doctors, Patients)
- 🔒 Password encryption (SHA-256)
- 🎫 Role-based access control
- 📝 Activity logging
- 🔑 Session management

### **Patient Management**

- 👤 Complete patient profiles
- 🆔 Egyptian National ID validation (14 digits)
- 🩸 Blood type, allergies, chronic diseases
- 📞 Emergency contact information
- 💊 Current medications tracking

### **Medical Records**

- 📅 Visit history with dates and doctors
- 🩺 Diagnosis and treatment plans
- 💊 Prescription management
- 📋 Lab results storage (PDFs)
- 🔬 Imaging results (X-rays, CT, MRI)
- 📎 File attachments (reports, documents)

### **Search & Filter**

- 🔍 Search patients by National ID
- 🏥 Filter visits by date, doctor, department
- 💊 Search by disease or medication
- 📊 Advanced query capabilities

### **Emergency Features**

- 🆘 One-click emergency view
- 📄 PDF emergency card generation
- 📱 QR code for quick access
- ⚠️ Critical information highlighting

### **Doctor Portal**

- 👨‍⚕️ Patient search and lookup
- ➕ Add new visits and prescriptions
- 👁️ View complete medical history
- 📊 Access lab and imaging results
- 📝 Digital note-taking

### **Patient Portal**

- 👤 View personal medical records
- 📖 Access visit history
- 🔗 Link external lab/imaging accounts
- 💾 Download emergency cards
- ✏️ Update contact information

### **External Integration (Simulated)**

- 🧪 Lab systems (Al Borg, Bio Lab)
- 📷 Imaging centers (Scan Center, Cairo Scan)
- 💊 Pharmacy networks
- 🔌 API-ready architecture

---

## 🏗️ System Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    MedLink Application                   │
├─────────────────────────────────────────────────────────┤
│                                                          │
│  ┌──────────────┐              ┌──────────────┐        │
│  │ Login System │              │ Auth Manager │        │
│  └──────┬───────┘              └──────┬───────┘        │
│         │                              │                │
│         ├──────────────┬───────────────┤                │
│         ▼              ▼               ▼                │
│  ┌─────────┐    ┌──────────┐   ┌──────────┐           │
│  │ Doctor  │    │ Patient  │   │  Admin   │           │
│  │ Portal  │    │ Portal   │   │ (Future) │           │
│  └────┬────┘    └────┬─────┘   └──────────┘           │
│       │              │                                  │
│       └──────┬───────┘                                  │
│              ▼                                           │
│  ┌───────────────────────────────────┐                 │
│  │    Core Business Logic Layer      │                 │
│  ├───────────────────────────────────┤                 │
│  │ • Patient Manager                 │                 │
│  │ • Visit Manager                   │                 │
│  │ • Lab Manager                     │                 │
│  │ • Imaging Manager                 │                 │
│  │ • Search Engine                   │                 │
│  │ • PDF Generator                   │                 │
│  └───────────────┬───────────────────┘                 │
│                  ▼                                       │
│  ┌───────────────────────────────────┐                 │
│  │    Data Management Layer          │                 │
│  ├───────────────────────────────────┤                 │
│  │ • Data Manager (CRUD)             │                 │
│  │ • Security Manager                │                 │
│  │ • Validators                      │                 │
│  │ • File Handler                    │                 │
│  └───────────────┬───────────────────┘                 │
│                  ▼                                       │
│  ┌───────────────────────────────────┐                 │
│  │      Data Storage Layer           │                 │
│  ├───────────────────────────────────┤                 │
│  │ • users.json                      │                 │
│  │ • patients.json                   │                 │
│  │ • visits.json                     │                 │
│  │ • lab_results.json                │                 │
│  │ • imaging_results.json            │                 │
│  │ • attachments/ (files)            │                 │
│  └───────────────────────────────────┘                 │
└─────────────────────────────────────────────────────────┘
```

---

## 💻 Installation

### **Prerequisites**

- Python 3.9 or higher
- pip (Python package manager)
- Windows 10/11 (primary), macOS, or Linux

### **Step 1: Clone or Download**

```bash
# Download the project files to your computer
# Extract to: C:\MedLink\
```

### **Step 2: Install Dependencies**

```bash
# Open terminal/command prompt
cd C:\MedLink

# Install required packages
pip install -r requirements.txt
```

### **Step 3: Verify Installation**

```bash
# Run the application
python main.py
```

### **Expected Output:**

A login window should appear with MedLink branding.

---

## 📚 Usage Guide

### **First Time Setup**

#### **1. Register Test Doctor Account**

Since this is a PoC, manually add a doctor to `data/users.json`:

```json
{
  "users": [
    {
      "user_id": "D001",
      "username": "dr.ahmed",
      "password_hash": "5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8",
      "role": "doctor",
      "full_name": "Dr. Ahmed Mohamed",
      "specialization": "Cardiology",
      "hospital": "Cairo University Hospital",
      "license_number": "MED12345",
      "email": "ahmed@hospital.eg",
      "phone": "01012345678"
    }
  ]
}
```

**Password:** `password` (hashed)

#### **2. Register Patient Account**

Use the application's registration feature:

- Click "Register New Patient Account"
- Enter National ID: `29501012345678`
- Enter Full Name: `Mohamed Ali Hassan`
- Enter Password: `patient123`
- Click Register

### **Doctor Workflow**

#### **Login as Doctor**

1. Select "Doctor" role
2. Username: `dr.ahmed`
3. Password: `password`
4. Click Login

#### **Search Patient**

1. Enter National ID in search box
2. Press Enter or click Search
3. Patient profile loads

#### **View Medical History**

1. Select patient
2. Click "Medical History" tab
3. Browse chronological visits

#### **Add New Visit**

1. Click "Add Visit" button
2. Fill in:
   - Date and time
   - Chief complaint
   - Diagnosis
   - Treatment plan
   - Prescriptions
3. Attach files (optional)
4. Click Save

#### **Generate Emergency Card**

1. Select patient
2. Click "Emergency Card" tab
3. Review critical information
4. Click "Generate PDF"
5. Save to desktop

### **Patient Workflow**

#### **Login as Patient**

1. Select "Patient" role
2. Username: `patient_29501012345678`
3. Password: `patient123`
4. Click Login

#### **View Own Records**

1. Dashboard shows overview
2. Navigate tabs:
   - Profile
   - Medical History
   - Lab Results
   - Imaging Results

#### **Download Emergency Card**

1. Go to "Emergency Card" tab
2. Review information
3. Click "Download PDF"
4. Print and carry in wallet

#### **Link External Accounts**

1. Click "Link Accounts"
2. Select service type (Lab/Imaging)
3. Enter account ID
4. Click Link

---

## 📂 Project Structure

```
MedLink/
│
├── main.py                          # Application entry point
│
├── config/                          # Configuration
│   ├── __init__.py
│   ├── settings.py                  # App settings
│   └── localization.py              # Multi-language support
│
├── core/                            # Business logic
│   ├── __init__.py
│   ├── auth_manager.py              # Authentication
│   ├── data_manager.py              # JSON operations
│   ├── patient_manager.py           # Patient CRUD
│   ├── visit_manager.py             # Visit management
│   ├── lab_manager.py               # Lab results
│   ├── imaging_manager.py           # Imaging results
│   ├── search_engine.py             # Search/filter
│   └── external_api.py              # API simulation
│
├── gui/                             # User interface
│   ├── __init__.py
│   ├── styles.py                    # Design system
│   ├── login_window.py              # Login screen
│   ├── doctor_dashboard.py          # Doctor UI
│   ├── patient_dashboard.py         # Patient UI
│   │
│   └── components/                  # UI components
│       ├── __init__.py
│       ├── sidebar.py
│       ├── patient_card.py
│       ├── visit_card.py
│       ├── history_tab.py
│       ├── lab_results_tab.py
│       ├── imaging_tab.py
│       ├── file_viewer.py
│       ├── emergency_dialog.py
│       ├── add_visit_dialog.py
│       └── link_accounts_dialog.py
│
├── utils/                           # Utilities
│   ├── __init__.py
│   ├── security.py                  # Encryption
│   ├── validators.py                # Input validation
│   ├── pdf_generator.py             # PDF creation
│   ├── qr_generator.py              # QR codes
│   ├── export_manager.py            # Data export
│   ├── date_utils.py                # Date helpers
│   └── logger.py                    # Activity logging
│
├── data/                            # JSON storage
│   ├── users.json                   # System users
│   ├── patients.json                # Patient records
│   ├── visits.json                  # Medical visits
│   ├── lab_results.json             # Lab data
│   └── imaging_results.json         # Imaging data
│
├── attachments/                     # File storage
│   ├── prescriptions/
│   ├── lab_results/
│   ├── xrays/
│   └── reports/
│
├── assets/                          # Resources
│   ├── icons/
│   ├── images/
│   └── fonts/
│
├── tests/                           # Testing
│   ├── generate_test_data.py        # Test data generator
│   └── test_scenarios.py            # Test cases
│
├── docs/                            # Documentation
│   ├── user_manual.pdf
│   ├── technical_documentation.md
│   └── api_simulation.md
│
├── requirements.txt                 # Dependencies
└── README.md                        # This file
```

---

## 🛠️ Development Phases

### **Phase 1: Foundation (Days 1-2)** ✅

**Status:** Complete

**Deliverables:**

- Project structure
- Authentication system
- Login/registration UI
- Data management
- Security implementation

**Files:** 9 core files created

---

### **Phase 2: Doctor Portal (Days 3-4)** 🚧

**Status:** In Progress

**Objectives:**

- Doctor dashboard
- Patient search
- Profile display
- Test data generation

**Files:** 5 new files

---

### **Phase 3: Medical History (Days 5-6)** ⏳

**Status:** Pending

**Objectives:**

- Visit history display
- Add visit functionality
- Timeline view

**Files:** 5 new files

---

### **Phase 4: Patient Portal (Days 7-8)** ⏳

**Status:** Pending

**Objectives:**

- Patient dashboard
- Self-service features
- Account linking

**Files:** 5 new files

---

### **Phase 5: Lab & Imaging (Days 9-10)** ⏳

**Status:** Pending

**Objectives:**

- Results management
- File handling
- Viewer components

**Files:** 6 new files

---

### **Phase 6: Advanced Features (Days 11-12)** ⏳

**Status:** Pending

**Objectives:**

- Search engine
- PDF generation
- QR codes
- Export functionality

**Files:** 6 new files

---

### **Phase 7: Polish & Testing (Days 13-14)** ⏳

**Status:** Pending

**Objectives:**

- Complete testing
- Bug fixes
- Documentation
- Demo preparation

---

## 💾 Technical Stack

### **Programming Language**

- **Python 3.9+**
  - Object-oriented design
  - Type hints for clarity
  - Modern syntax

### **GUI Framework**

- **CustomTkinter 5.2.0**
  - Modern dark theme
  - Cross-platform
  - Easy to learn
  - Professional appearance

### **Data Storage**

- **JSON Files**
  - Human-readable
  - Easy to debug
  - No database setup required
  - Portable

### **Security**

- **cryptography 41.0.7**
  - Fernet encryption
  - Secure key management
- **hashlib (built-in)**
  - SHA-256 password hashing

### **PDF Generation**

- **ReportLab 4.0.7**
  - Professional PDFs
  - Custom layouts
  - Embedded images

### **Image Processing**

- **Pillow 10.1.0**
  - Image viewing
  - Format conversion
  - Thumbnail generation

### **QR Codes**

- **qrcode 7.4.2**
  - Emergency access codes
  - Patient identification

### **PDF Reading**

- **PyPDF2 3.0.1**
  - Extract PDF text
  - PDF manipulation

### **Additional Libraries**

- **python-dateutil 2.8.2** - Date/time handling

---

## 📊 Data Models

### **User Model**

```json
{
  "user_id": "D001",
  "username": "dr.ahmed",
  "password_hash": "hashed_password",
  "role": "doctor|patient",
  "full_name": "Dr. Ahmed Mohamed",
  "email": "ahmed@hospital.eg",
  "phone": "01012345678",

  // Doctor-specific
  "specialization": "Cardiology",
  "hospital": "Cairo Hospital",
  "license_number": "MED12345",

  // Patient-specific
  "national_id": "29501012345678",
  "linked": true
}
```

### **Patient Model**

```json
{
  "national_id": "29501012345678",
  "full_name": "Mohamed Ali Hassan",
  "date_of_birth": "1995-01-01",
  "age": 28,
  "gender": "Male",
  "blood_type": "A+",
  "phone": "01098765432",

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
      "frequency": "As needed"
    }
  ],

  "insurance": {
    "provider": "Misr Insurance",
    "policy_number": "INS123456",
    "expiry": "2025-12-31"
  },

  "external_links": {
    "lab_account": "LAB789456",
    "imaging_account": "IMG123789"
  }
}
```

### **Visit Model**

```json
{
  "visit_id": "V001",
  "patient_national_id": "29501012345678",
  "date": "2024-11-15",
  "time": "10:30",
  "doctor_id": "D001",
  "doctor_name": "Dr. Ahmed Mohamed",
  "hospital": "Cairo Hospital",
  "department": "Cardiology",
  "visit_type": "Consultation|Emergency|Follow-up",

  "chief_complaint": "Chest pain",
  "diagnosis": "Stable angina",
  "treatment_plan": "Prescribed beta-blockers",

  "prescriptions": [
    {
      "medication": "Concor 5mg",
      "dosage": "1 tablet",
      "frequency": "Once daily",
      "duration": "30 days"
    }
  ],

  "attachments": ["attachments/prescriptions/prescription_V001.pdf"]
}
```

### **Lab Result Model**

```json
{
  "result_id": "LAB001",
  "patient_national_id": "29501012345678",
  "date": "2024-11-10",
  "lab_name": "Al Borg Labs",
  "test_type": "Complete Blood Count (CBC)",
  "status": "completed|pending",

  "results": {
    "Hemoglobin": "14.5 g/dL",
    "WBC": "7.2 x10^3/uL",
    "Platelets": "250 x10^3/uL"
  },

  "external_link": "https://alborg.com/results/LAB001",
  "attachment": "attachments/lab_results/cbc_2024_11_10.pdf",
  "ordered_by": "D001"
}
```

### **Imaging Result Model**

```json
{
  "imaging_id": "IMG001",
  "patient_national_id": "29501012345678",
  "date": "2024-11-12",
  "imaging_center": "Scan Center",
  "imaging_type": "X-Ray|CT|MRI|Ultrasound",
  "body_part": "Chest",

  "findings": "Normal chest x-ray",
  "radiologist": "Dr. Salma Ibrahim",

  "external_link": "https://scancenter.eg/view/IMG001",
  "images": ["attachments/xrays/chest_xray_2024_11_12.jpg"],
  "ordered_by": "D001"
}
```

---

## 🔒 Security

### **Authentication**

- Password hashing using SHA-256
- Session management
- Role-based access control
- Login attempt monitoring

### **Data Protection**

- Sensitive data encryption (Fernet)
- Secure file storage
- Access logging
- Input validation

### **National ID Validation**

Egyptian National ID format:

- 14 digits
- Century: 2 (1900s) or 3 (2000s)
- Birth date embedded (YYMMDD)
- Governorate code
- Gender digit (odd=male, even=female)

### **Best Practices**

- ✅ Never store passwords in plain text
- ✅ Validate all user inputs
- ✅ Log all data access
- ✅ Encrypt sensitive fields
- ✅ Regular security audits

---

## 🧪 Testing

### **Test Data**

Run the test data generator:

```bash
python tests/generate_test_data.py
```

This creates:

- 5 realistic patient profiles
- 3 doctor accounts
- 20+ medical visits
- 10+ lab results
- 5+ imaging results

### **Test Scenarios**

#### **Scenario 1: Emergency Access**

1. Doctor logs in
2. Searches patient: `29501012345678`
3. Opens emergency card
4. Verifies blood type, allergies visible
5. Generates PDF

#### **Scenario 2: Add Visit**

1. Doctor logs in
2. Searches patient
3. Clicks "Add Visit"
4. Fills form
5. Attaches prescription PDF
6. Saves successfully

#### **Scenario 3: Patient Self-Service**

1. Patient logs in
2. Views medical history
3. Downloads emergency card
4. Links lab account
5. Views lab results

### **Test Checklist**

- [ ] Login with valid credentials
- [ ] Login with invalid credentials (should fail)
- [ ] Register new patient
- [ ] Search patient by National ID
- [ ] View patient profile
- [ ] Add new visit
- [ ] Upload attachments
- [ ] View lab results
- [ ] Generate PDF
- [ ] Link external account
- [ ] Logout

---

## 🚀 Future Enhancements

### **Version 2.0 (Potential)**

- [ ] Real database (PostgreSQL/MySQL)
- [ ] Web-based interface
- [ ] Mobile app (iOS/Android)
- [ ] Real API integrations
- [ ] Cloud storage
- [ ] Multi-hospital network
- [ ] Appointment scheduling
- [ ] Telemedicine integration
- [ ] AI diagnosis assistance
- [ ] Prescription verification
- [ ] Insurance claim automation
- [ ] Analytics dashboard
- [ ] Arabic language support
- [ ] Voice commands
- [ ] Biometric authentication

### **Scalability Plan**

1. **Local Network**: Deploy on hospital LAN
2. **Regional System**: Connect multiple facilities
3. **National Platform**: Government integration
4. **International Standard**: WHO compliance

---

## 🤝 Contributing

This is an academic project (CET111 - Fall 2025), but suggestions are welcome:

1. Fork the repository
2. Create feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open Pull Request

---

## 📝 License

This project is created for academic purposes as part of CET111 course requirements.

**Elsewedy University of Technology - Polytechnic of Egypt**
Department of Computer Science Technology
Fall 2025

---

## 👤 Author

**Youssef**

- Computer Science Student
- Specialization: Full-Stack Development
- Skills: Python (5 years), Laravel (2 years), AI, Web Scraping
- Contact: [Your Email]

---

## 🙏 Acknowledgments

- Course: CET111 - Introduction to Computer and Programming
- Institution: Elsewedy University of Technology
- Instructors: [Course instructors]
- Inspiration: Addressing real healthcare challenges in Egypt

---

## 📞 Support

For questions or issues:

1. Check documentation in `docs/`
2. Review test scenarios
3. Contact course TA
4. Email: [support@medlink.eg]

---

## 📅 Project Timeline

**Start Date:** November 2024
**Submission:** Week 14 (2 weeks from now)
**Status:** Phase 1 Complete ✅

---

## 🎓 Academic Requirements Met

✅ **Track 1 - Advanced Python Application**

**Core Requirements:**

- ✅ File and Data Interaction (JSON)
- ✅ GUI using Tkinter (CustomTkinter)
- ✅ Text and Word Analysis (Search)
- ✅ Basic Networking (API simulation)

**Advanced Features:**

- ✅ Encryption and security
- ✅ PDF generation
- ✅ QR code generation
- ✅ Complex data structures
- ✅ Multi-user system
- ✅ File handling
- ✅ Input validation

---

**Built with ❤️ for better healthcare in Egypt**
