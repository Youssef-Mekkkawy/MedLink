-- Manual Database Creation Script
-- Use this if you prefer SQL over Python

-- 1. Create Database
CREATE DATABASE IF NOT EXISTS medlink_db 
CHARACTER SET utf8mb4 
COLLATE utf8mb4_unicode_ci;

USE medlink_db;

-- 2. Create Users Table (Doctors/Staff)
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id VARCHAR(50) UNIQUE NOT NULL,
    username VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    role ENUM('doctor', 'patient', 'admin', 'nurse') NOT NULL,
    full_name VARCHAR(200) NOT NULL,
    email VARCHAR(200),
    phone VARCHAR(20),
    national_id VARCHAR(14) UNIQUE,
    
    -- Doctor-specific fields
    specialization VARCHAR(200),
    hospital VARCHAR(200),
    license_number VARCHAR(100),
    
    -- Biometric fields
    fingerprint_id VARCHAR(100),
    fingerprint_enrolled BOOLEAN DEFAULT FALSE,
    fingerprint_enrollment_date DATE,
    last_fingerprint_login DATETIME,
    fingerprint_login_count INT DEFAULT 0,
    biometric_enabled BOOLEAN DEFAULT FALSE,
    
    -- Account management
    account_status ENUM('active', 'inactive', 'suspended') DEFAULT 'active',
    last_login DATETIME,
    login_count INT DEFAULT 0,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    
    INDEX idx_username (username),
    INDEX idx_national_id (national_id),
    INDEX idx_role (role)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 3. Create Patients Table
CREATE TABLE IF NOT EXISTS patients (
    id INT AUTO_INCREMENT PRIMARY KEY,
    national_id VARCHAR(14) UNIQUE NOT NULL,
    full_name VARCHAR(200) NOT NULL,
    date_of_birth DATE NOT NULL,
    age INT,
    gender ENUM('Male', 'Female') NOT NULL,
    blood_type ENUM('A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-'),
    phone VARCHAR(20),
    email VARCHAR(200),
    address TEXT,
    city VARCHAR(100),
    governorate VARCHAR(100),
    
    -- JSON fields (MySQL 5.7+)
    emergency_contact JSON,
    chronic_diseases JSON,
    allergies JSON,
    family_history JSON,
    disabilities_special_needs JSON,
    emergency_directives JSON,
    lifestyle JSON,
    insurance JSON,
    external_links JSON,
    
    -- NFC Card info
    nfc_card_uid VARCHAR(50),
    nfc_card_assigned BOOLEAN DEFAULT FALSE,
    nfc_card_status ENUM('active', 'inactive', 'lost', 'stolen'),
    
    -- Timestamps
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    last_updated DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    INDEX idx_national_id (national_id),
    INDEX idx_full_name (full_name),
    INDEX idx_nfc_card (nfc_card_uid)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 4. Create Doctor Cards Table
CREATE TABLE IF NOT EXISTS doctor_cards (
    id INT AUTO_INCREMENT PRIMARY KEY,
    card_uid VARCHAR(50) UNIQUE NOT NULL,
    user_id VARCHAR(50) NOT NULL,
    username VARCHAR(100) NOT NULL,
    full_name VARCHAR(200) NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    assigned_date DATE DEFAULT (CURRENT_DATE),
    last_used DATETIME,
    
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
    INDEX idx_card_uid (card_uid),
    INDEX idx_user_id (user_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 5. Create Patient Cards Table
CREATE TABLE IF NOT EXISTS patient_cards (
    id INT AUTO_INCREMENT PRIMARY KEY,
    card_uid VARCHAR(50) UNIQUE NOT NULL,
    national_id VARCHAR(14) NOT NULL,
    full_name VARCHAR(200) NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    assigned_date DATE DEFAULT (CURRENT_DATE),
    last_used DATETIME,
    
    FOREIGN KEY (national_id) REFERENCES patients(national_id) ON DELETE CASCADE,
    INDEX idx_card_uid (card_uid),
    INDEX idx_national_id (national_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 6. Create Visits Table
CREATE TABLE IF NOT EXISTS visits (
    id INT AUTO_INCREMENT PRIMARY KEY,
    visit_id VARCHAR(50) UNIQUE NOT NULL,
    patient_national_id VARCHAR(14) NOT NULL,
    doctor_id VARCHAR(50) NOT NULL,
    doctor_name VARCHAR(200),
    date DATE NOT NULL,
    time TIME,
    visit_type ENUM('regular', 'emergency', 'followup') NOT NULL,
    chief_complaint TEXT,
    diagnosis TEXT,
    treatment_plan TEXT,
    notes TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (patient_national_id) REFERENCES patients(national_id) ON DELETE CASCADE,
    FOREIGN KEY (doctor_id) REFERENCES users(user_id) ON DELETE CASCADE,
    INDEX idx_patient (patient_national_id),
    INDEX idx_doctor (doctor_id),
    INDEX idx_date (date)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 7. Create Surgeries Table
CREATE TABLE IF NOT EXISTS surgeries (
    id INT AUTO_INCREMENT PRIMARY KEY,
    surgery_id VARCHAR(50) UNIQUE NOT NULL,
    patient_national_id VARCHAR(14) NOT NULL,
    procedure_name VARCHAR(300) NOT NULL,
    date DATE NOT NULL,
    hospital VARCHAR(200),
    surgeon_name VARCHAR(200),
    anesthesia_type VARCHAR(100),
    duration VARCHAR(50),
    complications TEXT,
    recovery_notes TEXT,
    outcome VARCHAR(100),
    
    FOREIGN KEY (patient_national_id) REFERENCES patients(national_id) ON DELETE CASCADE,
    INDEX idx_patient (patient_national_id),
    INDEX idx_date (date)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 8. Create Hospitalizations Table
CREATE TABLE IF NOT EXISTS hospitalizations (
    id INT AUTO_INCREMENT PRIMARY KEY,
    hospitalization_id VARCHAR(50) UNIQUE NOT NULL,
    patient_national_id VARCHAR(14) NOT NULL,
    hospital VARCHAR(200) NOT NULL,
    department VARCHAR(100),
    admission_date DATE NOT NULL,
    discharge_date DATE,
    admission_reason TEXT,
    diagnosis TEXT,
    treatment_summary TEXT,
    discharge_notes TEXT,
    days_stayed INT,
    
    FOREIGN KEY (patient_national_id) REFERENCES patients(national_id) ON DELETE CASCADE,
    INDEX idx_patient (patient_national_id),
    INDEX idx_admission_date (admission_date)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 9. Create Vaccinations Table
CREATE TABLE IF NOT EXISTS vaccinations (
    id INT AUTO_INCREMENT PRIMARY KEY,
    patient_national_id VARCHAR(14) NOT NULL,
    vaccine_name VARCHAR(200) NOT NULL,
    date_administered DATE NOT NULL,
    dose_number VARCHAR(50),
    location VARCHAR(200),
    batch_number VARCHAR(100),
    expiry_date DATE,
    next_dose_due DATE,
    administered_by VARCHAR(200),
    notes TEXT,
    
    FOREIGN KEY (patient_national_id) REFERENCES patients(national_id) ON DELETE CASCADE,
    INDEX idx_patient (patient_national_id),
    INDEX idx_date (date_administered)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 10. Create Current Medications Table
CREATE TABLE IF NOT EXISTS current_medications (
    id INT AUTO_INCREMENT PRIMARY KEY,
    patient_national_id VARCHAR(14) NOT NULL,
    medication_name VARCHAR(300) NOT NULL,
    dosage VARCHAR(100),
    frequency VARCHAR(100),
    started_date DATE,
    prescribed_by VARCHAR(200),
    notes TEXT,
    is_active BOOLEAN DEFAULT TRUE,
    
    FOREIGN KEY (patient_national_id) REFERENCES patients(national_id) ON DELETE CASCADE,
    INDEX idx_patient (patient_national_id),
    INDEX idx_active (is_active)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 11. Create Lab Results Table
CREATE TABLE IF NOT EXISTS lab_results (
    id INT AUTO_INCREMENT PRIMARY KEY,
    result_id VARCHAR(50) UNIQUE NOT NULL,
    patient_national_id VARCHAR(14) NOT NULL,
    test_name VARCHAR(200) NOT NULL,
    test_type VARCHAR(100),
    date DATE NOT NULL,
    result_value VARCHAR(200),
    reference_range VARCHAR(100),
    unit VARCHAR(50),
    status ENUM('normal', 'abnormal', 'critical', 'pending') DEFAULT 'pending',
    notes TEXT,
    
    FOREIGN KEY (patient_national_id) REFERENCES patients(national_id) ON DELETE CASCADE,
    INDEX idx_patient (patient_national_id),
    INDEX idx_date (date)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 12. Create Imaging Results Table
CREATE TABLE IF NOT EXISTS imaging_results (
    id INT AUTO_INCREMENT PRIMARY KEY,
    imaging_id VARCHAR(50) UNIQUE NOT NULL,
    patient_national_id VARCHAR(14) NOT NULL,
    imaging_type ENUM('X-ray', 'CT', 'MRI', 'Ultrasound', 'PET', 'Other') NOT NULL,
    body_part VARCHAR(100),
    date DATE NOT NULL,
    findings TEXT,
    impression TEXT,
    radiologist VARCHAR(200),
    status ENUM('normal', 'abnormal', 'critical', 'pending') DEFAULT 'pending',
    
    FOREIGN KEY (patient_national_id) REFERENCES patients(national_id) ON DELETE CASCADE,
    INDEX idx_patient (patient_national_id),
    INDEX idx_date (date)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 13. Create Prescriptions Table
CREATE TABLE IF NOT EXISTS prescriptions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    prescription_id VARCHAR(50) UNIQUE,
    visit_id VARCHAR(50) NOT NULL,
    patient_national_id VARCHAR(14) NOT NULL,
    medication_name VARCHAR(300) NOT NULL,
    dosage VARCHAR(100),
    frequency VARCHAR(100),
    duration VARCHAR(100),
    instructions TEXT,
    
    FOREIGN KEY (visit_id) REFERENCES visits(visit_id) ON DELETE CASCADE,
    FOREIGN KEY (patient_national_id) REFERENCES patients(national_id) ON DELETE CASCADE,
    INDEX idx_visit (visit_id),
    INDEX idx_patient (patient_national_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 14. Create Vital Signs Table
CREATE TABLE IF NOT EXISTS vital_signs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    visit_id VARCHAR(50) NOT NULL,
    patient_national_id VARCHAR(14) NOT NULL,
    temperature DECIMAL(4,1),
    blood_pressure_systolic INT,
    blood_pressure_diastolic INT,
    heart_rate INT,
    respiratory_rate INT,
    oxygen_saturation INT,
    weight DECIMAL(5,2),
    height DECIMAL(5,2),
    bmi DECIMAL(4,1),
    recorded_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (visit_id) REFERENCES visits(visit_id) ON DELETE CASCADE,
    FOREIGN KEY (patient_national_id) REFERENCES patients(national_id) ON DELETE CASCADE,
    INDEX idx_visit (visit_id),
    INDEX idx_patient (patient_national_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 15. Create Hardware Audit Log Table
CREATE TABLE IF NOT EXISTS hardware_audit_log (
    id INT AUTO_INCREMENT PRIMARY KEY,
    event_id VARCHAR(50) UNIQUE,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    event_type VARCHAR(100),
    user_id VARCHAR(50),
    patient_national_id VARCHAR(14),
    card_uid VARCHAR(50),
    fingerprint_id VARCHAR(100),
    accessed_by VARCHAR(50),
    access_type VARCHAR(50),
    success BOOLEAN,
    details TEXT,
    
    INDEX idx_timestamp (timestamp),
    INDEX idx_user (user_id),
    INDEX idx_patient (patient_national_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Show all tables
SHOW TABLES;

-- Show table counts
SELECT 'users' AS table_name, COUNT(*) AS count FROM users
UNION ALL
SELECT 'patients', COUNT(*) FROM patients
UNION ALL
SELECT 'doctor_cards', COUNT(*) FROM doctor_cards
UNION ALL
SELECT 'patient_cards', COUNT(*) FROM patient_cards
UNION ALL
SELECT 'visits', COUNT(*) FROM visits;
