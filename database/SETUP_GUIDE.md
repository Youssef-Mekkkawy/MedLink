# 🗄️ **DATABASE SETUP GUIDE WITH TEST DATA**

## 🎯 **Quick Start (2 Minutes)**

```bash
# 1. Make sure MySQL is running
sudo systemctl start mysql

# 2. Create the database
mysql -u root -p -e "CREATE DATABASE IF NOT EXISTS medlink_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"

# 3. Run setup script
python setup_database_with_data.py

# 4. Launch your app
python main.py
```

**That's it! 🎉** Your database is now ready with:
- ✅ 10 Doctors with login credentials
- ✅ 30 Patients with medical histories
- ✅ NFC cards for quick login
- ✅ Visits, surgeries, vaccinations, hospitalizations

---

## 📋 **Detailed Setup Steps**

### **Step 1: Prerequisites** ⏱️ 1 min

Make sure you have:
```bash
# Check MySQL is installed
mysql --version

# Check Python packages
pip list | grep -E "sqlalchemy|mysql-connector-python"

# Install if missing
pip install sqlalchemy mysql-connector-python
```

### **Step 2: Configure Database** ⏱️ 1 min

Edit `config/database_config.py`:

```python
DATABASE_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'YOUR_PASSWORD',  # ← Change this!
    'database': 'medlink_db',
    'charset': 'utf8mb4',
    'collation': 'utf8mb4_unicode_ci',
    'autocommit': False
}
```

### **Step 3: Create Database** ⏱️ 30 sec

```bash
# Option A: Command line
mysql -u root -p -e "CREATE DATABASE medlink_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"

# Option B: MySQL prompt
mysql -u root -p
CREATE DATABASE medlink_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
exit
```

### **Step 4: Run Setup Script** ⏱️ 30 sec

```bash
# Basic setup (10 doctors, 30 patients)
python setup_database_with_data.py

# Custom numbers
python setup_database_with_data.py --doctors 20 --patients 50

# Reset and recreate everything
python setup_database_with_data.py --reset
```

**Output example:**
```
============================================================
🏥 MEDLINK DATABASE SETUP WITH TEST DATA
============================================================

📊 Creating database tables...
✅ Tables created

📋 Creating 10 doctors...
   ✅ Dr. Ahmed Hassan - Username: dr.ahmed.hassan - Card: 0724184100
   ✅ Dr. Mohamed Ali - Username: dr.mohamed.ali - Card: 0724184101
   ...
✅ Created 10 doctors with NFC cards

👥 Creating 30 patients...
   ✅ Ahmed Mohamed - 30003150134340 - Cairo - Card: 0725755100
   ✅ Fatima Hassan - 29508231234561 - Giza - Card: 0725755101
   ...
✅ Created 30 patients

🏥 Creating medical records...
   ✅ Created 45 visits
   ✅ Created 6 surgeries
   ✅ Created 4 hospitalizations
   ✅ Created 80 vaccinations
✅ Medical records created

============================================================
📊 SETUP COMPLETE!
============================================================

✅ Created 10 doctors
✅ Created 30 patients
✅ Created medical records

🔑 LOGIN CREDENTIALS:

Doctors (username / password):
   1. dr.ahmed.hassan / password123
   2. dr.mohamed.ali / password123
   3. dr.mahmoud.ibrahim / password123
   4. dr.omar.mohamed / password123
   5. dr.youssef.said / password123

💳 NFC CARDS:

Doctor Cards:
   1. Card UID: 0724184100
   2. Card UID: 0724184101
   3. Card UID: 0724184102
   4. Card UID: 0724184103
   5. Card UID: 0724184104

Patient Cards (first 5 with cards):
   1. Ahmed Mohamed - Card: 0725755100
   2. Fatima Hassan - Card: 0725755101
   3. Sara Ali - Card: 0725755102
   4. Hassan Ibrahim - Card: 0725755103
   5. Mariam Said - Card: 0725755104

============================================================

🚀 Ready to test! Run: python main.py
============================================================
```

---

## 🧪 **Verify Setup**

### Test 1: Check Tables
```bash
mysql -u root -p medlink_db -e "SHOW TABLES;"
```

**Expected output:**
```
+----------------------+
| Tables_in_medlink_db |
+----------------------+
| current_medications  |
| doctor_cards        |
| hardware_audit_log  |
| hospitalizations    |
| imaging_results     |
| lab_results         |
| patient_cards       |
| patients            |
| prescriptions       |
| surgeries           |
| users               |
| vaccinations        |
| visits              |
| vital_signs         |
+----------------------+
```

### Test 2: Check Data
```bash
mysql -u root -p medlink_db -e "SELECT COUNT(*) FROM users; SELECT COUNT(*) FROM patients;"
```

### Test 3: Test Login
```python
# test_login.py
from core.auth_manager import auth_manager

success, msg, user = auth_manager.login("dr.ahmed.hassan", "password123", "doctor")
print(f"Login: {success}")
print(f"User: {user['full_name']}" if success else f"Error: {msg}")
```

### Test 4: Test NFC Card
```python
# test_nfc.py
from core.card_manager import card_manager

card = card_manager.get_card("0724184100")
if card:
    print(f"✅ Card works! Type: {card['card_type']}")
    print(f"   Name: {card['full_name']}")
else:
    print("❌ Card not found")
```

---

## 📊 **What Data Gets Created**

### **Doctors (10 by default)**
- ✅ Egyptian names (e.g., Dr. Ahmed Hassan, Dr. Fatima Mohamed)
- ✅ Realistic specializations (Cardiology, Pediatrics, etc.)
- ✅ Cairo hospitals (Cairo University Hospital, Kasr Al Ainy, etc.)
- ✅ Login credentials (username: dr.ahmed.hassan, password: password123)
- ✅ NFC cards (UIDs: 0724184100, 0724184101, etc.)

### **Patients (30 by default)**
- ✅ Egyptian names and national IDs
- ✅ Ages from 1 to 80 years old
- ✅ Egyptian phone numbers (010xxxxxxxx, 011xxxxxxxx)
- ✅ Blood types (A+, O-, etc.)
- ✅ Chronic diseases (30% of patients)
- ✅ Allergies (25% of patients)
- ✅ Emergency contacts
- ✅ NFC cards (70% of patients)

### **Medical Records (for first 20 patients)**
- ✅ **Visits:** 1-3 visits per patient with diagnoses
- ✅ **Surgeries:** 20% chance (Appendectomy, Cholecystectomy, etc.)
- ✅ **Hospitalizations:** 15% chance (Pneumonia, Heart Attack, etc.)
- ✅ **Vaccinations:** 2-4 vaccines per patient (COVID-19, Hepatitis B, etc.)

---

## 🎛️ **Customization Options**

### **Option 1: More Doctors and Patients**
```bash
# Create 20 doctors and 50 patients
python setup_database_with_data.py --doctors 20 --patients 50
```

### **Option 2: Reset Everything**
```bash
# Drop all tables and recreate with fresh data
python setup_database_with_data.py --reset
```

### **Option 3: Add More Data Later**
```bash
# Run again without --reset to add more
python setup_database_with_data.py --doctors 5 --patients 10
```

---

## 🔧 **Troubleshooting**

### Problem: "Access denied for user"
**Solution:** Check password in `config/database_config.py`

### Problem: "Unknown database 'medlink_db'"
**Solution:** Create database first:
```bash
mysql -u root -p -e "CREATE DATABASE medlink_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"
```

### Problem: "Can't connect to MySQL server"
**Solution:** Start MySQL:
```bash
# Linux
sudo systemctl start mysql

# macOS
brew services start mysql

# Windows
net start mysql
```

### Problem: "Table already exists"
**Solution:** Use --reset flag:
```bash
python setup_database_with_data.py --reset
```

---

## 🎯 **Test Login Credentials**

After setup, you can login with:

### **Doctor Login (Username/Password):**
| Username | Password | Specialization |
|----------|----------|----------------|
| dr.ahmed.hassan | password123 | Cardiology |
| dr.mohamed.ali | password123 | Pediatrics |
| dr.mahmoud.ibrahim | password123 | Internal Medicine |
| dr.omar.mohamed | password123 | Orthopedics |
| dr.youssef.said | password123 | Dermatology |

### **Doctor NFC Cards:**
| Card UID | Doctor |
|----------|--------|
| 0724184100 | Dr. Ahmed Hassan |
| 0724184101 | Dr. Mohamed Ali |
| 0724184102 | Dr. Mahmoud Ibrahim |
| 0724184103 | Dr. Omar Mohamed |
| 0724184104 | Dr. Youssef Said |

### **Patient NFC Cards:**
| Card UID | Patient |
|----------|---------|
| 0725755100 | First patient |
| 0725755101 | Second patient |
| 0725755102 | Third patient |
| ... | ... |

---

## 📝 **Sample SQL Queries**

### View all doctors:
```sql
SELECT user_id, full_name, specialization, hospital 
FROM users 
WHERE role = 'doctor';
```

### View all patients:
```sql
SELECT national_id, full_name, age, blood_type, phone 
FROM patients 
ORDER BY full_name;
```

### View recent visits:
```sql
SELECT v.visit_id, p.full_name, v.doctor_name, v.date, v.diagnosis
FROM visits v
JOIN patients p ON v.patient_national_id = p.national_id
ORDER BY v.date DESC
LIMIT 10;
```

### View NFC cards:
```sql
-- Doctor cards
SELECT card_uid, username, full_name, is_active FROM doctor_cards;

-- Patient cards
SELECT card_uid, national_id, full_name, is_active FROM patient_cards;
```

---

## 🚀 **Quick Test Workflow**

```bash
# 1. Setup database
python setup_database_with_data.py

# 2. Verify
mysql -u root -p medlink_db -e "SELECT COUNT(*) FROM users; SELECT COUNT(*) FROM patients;"

# 3. Test auth
python -c "from core.auth_manager import auth_manager; print(auth_manager.login('dr.ahmed.hassan', 'password123', 'doctor'))"

# 4. Test card
python -c "from core.card_manager import card_manager; print(card_manager.get_card('0724184100'))"

# 5. Launch app
python main.py

# 6. Test login with:
#    - Username: dr.ahmed.hassan
#    - Password: password123
#    - OR scan NFC card: 0724184100
```

---

## 💡 **Pro Tips**

1. **Use --reset carefully** - It deletes ALL data!
2. **Save the output** - It shows all credentials
3. **Test incrementally** - Verify each step
4. **Keep backups** - Export data before experimenting
5. **Use NFC cards** - They're pre-configured for quick testing

---

## 📦 **Export/Import Data**

### Export data:
```bash
mysqldump -u root -p medlink_db > medlink_backup.sql
```

### Import data:
```bash
mysql -u root -p medlink_db < medlink_backup.sql
```

---

**Your database is now ready for testing! 🎉**

Run `python main.py` and login with any of the credentials above!
