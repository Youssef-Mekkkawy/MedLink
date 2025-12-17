# 🗄️ **DATABASE SETUP - COMPLETE GUIDE**

## 🚀 **Super Quick Start (1 Minute)**

```bash
# Just run this:
python db_manager.py setup
```

That's it! Your database is ready with test data. 🎉

---

## 📋 **What You Get:**

After running the setup, you'll have:

✅ **Complete database structure** (14 tables)  
✅ **10 doctors** with login credentials  
✅ **30 patients** with realistic Egyptian data  
✅ **NFC cards** for quick login (both doctors and patients)  
✅ **Medical records** (visits, surgeries, vaccinations, etc.)  

---

## 🎯 **Three Ways to Set Up:**

### **Method 1: Interactive CLI (Easiest)** ⭐ Recommended

```bash
python db_manager.py
```

You'll get a menu:
```
============================================================
              MEDLINK DATABASE MANAGER
============================================================

Choose an option:

1. Full Setup (Create database + tables + test data)
2. Create Tables Only
3. Generate Test Data
4. Show Status
5. Reset Database (DELETE ALL!)
6. Test Connection
0. Exit

Enter choice (0-6):
```

**Just press `1` and hit Enter!**

### **Method 2: Direct Command (Fastest)**

```bash
# One command does everything
python db_manager.py setup

# Other useful commands
python db_manager.py status    # Show database info
python db_manager.py test      # Test connection
python db_manager.py reset     # Reset (careful!)
```

### **Method 3: Step-by-Step Manual**

```bash
# 1. Create database
mysql -u root -p -e "CREATE DATABASE medlink_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"

# 2. Run setup script
python setup_database_with_data.py

# 3. Verify
python -c "from core.database import test_connection; test_connection()"
```

---

## 📝 **Before You Start:**

### 1. **Set Your MySQL Password**

Edit `config/database_config.py`:

```python
DATABASE_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'YOUR_PASSWORD_HERE',  # ← Change this!
    'database': 'medlink_db',
    # ...
}
```

### 2. **Make Sure MySQL is Running**

```bash
# Linux
sudo systemctl start mysql

# macOS  
brew services start mysql

# Windows
net start mysql
```

### 3. **Check Python Packages**

```bash
pip install sqlalchemy mysql-connector-python
```

---

## 🎓 **What Gets Created:**

### **Tables (14 Total):**
1. **users** - Doctors and staff accounts
2. **patients** - Patient records
3. **doctor_cards** - NFC cards for doctors
4. **patient_cards** - NFC cards for patients
5. **visits** - Medical visits
6. **prescriptions** - Medications prescribed
7. **vital_signs** - Temperature, BP, etc.
8. **surgeries** - Surgical procedures
9. **hospitalizations** - Hospital admissions
10. **vaccinations** - Vaccine records
11. **current_medications** - Active medications
12. **lab_results** - Lab test results
13. **imaging_results** - X-rays, MRI, etc.
14. **hardware_audit_log** - Security logs

### **Test Data:**

#### **10 Doctors:**
- Egyptian names (Ahmed, Mohamed, Fatima, etc.)
- Realistic specializations (Cardiology, Pediatrics, etc.)
- Cairo hospitals
- Login credentials (username/password)
- NFC cards for quick login

**Example Doctor:**
```
Name: Dr. Ahmed Hassan
Username: dr.ahmed.hassan
Password: password123
Specialization: Cardiology
Hospital: Cairo University Hospital
NFC Card: 0724184100
```

#### **30 Patients:**
- Realistic Egyptian names and national IDs
- Ages 1-80 years
- Egyptian phone numbers (010xxxxxxxx, etc.)
- Blood types
- Some with chronic diseases (30%)
- Some with allergies (25%)
- Emergency contacts
- 70% have NFC cards

**Example Patient:**
```
Name: Ahmed Mohamed
National ID: 30003150134340
Age: 24
Blood Type: A+
Phone: 01012345678
City: Cairo
NFC Card: 0725755100
```

#### **Medical Records:**
- **45+ visits** with diagnoses
- **6+ surgeries** (Appendectomy, Cholecystectomy, etc.)
- **4+ hospitalizations** (Pneumonia, Heart Attack, etc.)
- **80+ vaccinations** (COVID-19, Hepatitis B, MMR, etc.)

---

## 🧪 **Testing Your Setup:**

### **Test 1: Check Connection**
```bash
python db_manager.py test
```

Expected: ✅ Connection successful!

### **Test 2: View Status**
```bash
python db_manager.py status
```

Expected output:
```
Database Status:
   Doctors: 10
   Patients: 30
   Doctor Cards: 10
   Patient Cards: 21
   Visits: 45

Sample Login Credentials:
   Username: dr.ahmed.hassan / Password: password123
   Username: dr.mohamed.ali / Password: password123
   ...

Sample NFC Cards:
   Card UID: 0724184100 - Dr. Ahmed Hassan
   Card UID: 0724184101 - Dr. Mohamed Ali
   ...
```

### **Test 3: Login to GUI**
```bash
python main.py
```

Try logging in with:
- **Username:** dr.ahmed.hassan
- **Password:** password123

Or scan NFC card: **0724184100**

---

## 🎮 **Using Test Credentials:**

### **Doctor Logins:**

| Username | Password | Specialization | NFC Card |
|----------|----------|----------------|----------|
| dr.ahmed.hassan | password123 | Cardiology | 0724184100 |
| dr.mohamed.ali | password123 | Pediatrics | 0724184101 |
| dr.mahmoud.ibrahim | password123 | Internal Medicine | 0724184102 |
| dr.omar.mohamed | password123 | Orthopedics | 0724184103 |
| dr.youssef.said | password123 | Dermatology | 0724184104 |

### **Testing NFC Cards:**

**Doctor Cards:**
```
0724184100 → Dr. Ahmed Hassan
0724184101 → Dr. Mohamed Ali
0724184102 → Dr. Mahmoud Ibrahim
0724184103 → Dr. Omar Mohamed
0724184104 → Dr. Youssef Said
```

**Patient Cards:**
```
0725755100 → First patient
0725755101 → Second patient
0725755102 → Third patient
... (21 total patient cards)
```

---

## 🔧 **Customization:**

### **Change Number of Records:**

```bash
# Create more doctors and patients
python setup_database_with_data.py --doctors 20 --patients 100
```

### **Reset and Recreate:**

```bash
# Delete everything and start fresh
python setup_database_with_data.py --reset
```

Or use CLI:
```bash
python db_manager.py
# Then choose option 5 (Reset Database)
```

---

## 🛠️ **Troubleshooting:**

### **Problem: "Access denied"**

**Solution:** Check password in `config/database_config.py`

```python
'password': 'YOUR_ACTUAL_PASSWORD',  # Not 'YOUR_MYSQL_PASSWORD'!
```

### **Problem: "Unknown database 'medlink_db'"**

**Solution:** Create database first:

```bash
mysql -u root -p -e "CREATE DATABASE medlink_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"
```

Or just run:
```bash
python db_manager.py setup  # It creates the database automatically
```

### **Problem: "Can't connect to MySQL server"**

**Solution:** Start MySQL:

```bash
# Check if running
sudo systemctl status mysql

# Start it
sudo systemctl start mysql
```

### **Problem: "Table already exists"**

**Solution:** Reset database:

```bash
python db_manager.py
# Choose option 5 (Reset Database)
```

---

## 📊 **Useful SQL Queries:**

### **View all doctors:**
```sql
SELECT user_id, full_name, specialization, hospital 
FROM users 
WHERE role = 'doctor';
```

### **View all patients:**
```sql
SELECT national_id, full_name, age, blood_type, phone 
FROM patients 
ORDER BY full_name;
```

### **View recent visits:**
```sql
SELECT v.visit_id, p.full_name AS patient, v.doctor_name, v.date, v.diagnosis
FROM visits v
JOIN patients p ON v.patient_national_id = p.national_id
ORDER BY v.date DESC
LIMIT 10;
```

### **Count everything:**
```sql
SELECT 
    (SELECT COUNT(*) FROM users WHERE role='doctor') AS doctors,
    (SELECT COUNT(*) FROM patients) AS patients,
    (SELECT COUNT(*) FROM visits) AS visits,
    (SELECT COUNT(*) FROM surgeries) AS surgeries,
    (SELECT COUNT(*) FROM vaccinations) AS vaccinations;
```

---

## 💾 **Backup & Restore:**

### **Backup:**
```bash
mysqldump -u root -p medlink_db > backup_$(date +%Y%m%d).sql
```

### **Restore:**
```bash
mysql -u root -p medlink_db < backup_20241217.sql
```

---

## 🎯 **Complete Workflow:**

```bash
# 1. Setup everything
python db_manager.py setup

# 2. Check status
python db_manager.py status

# 3. Test login
python main.py
# Login with: dr.ahmed.hassan / password123

# 4. Test NFC
# Scan card: 0724184100

# 5. Add more data if needed
python setup_database_with_data.py --doctors 5 --patients 10

# 6. Backup
mysqldump -u root -p medlink_db > my_backup.sql
```

---

## 📁 **Files Provided:**

```
DATABASE_SETUP/
├── db_manager.py                      # Interactive CLI tool ⭐
├── setup_database_with_data.py        # Setup script with test data
├── create_tables.sql                  # Manual SQL script
├── SETUP_GUIDE.md                     # Detailed guide
└── README.md                          # This file
```

### **Which File to Use?**

- **Easiest:** `python db_manager.py` (Interactive menu)
- **Fastest:** `python db_manager.py setup` (One command)
- **Manual:** `python setup_database_with_data.py`
- **SQL Only:** `mysql -u root -p < create_tables.sql`

---

## 🎉 **Success Checklist:**

- [ ] MySQL is running
- [ ] Password set in `config/database_config.py`
- [ ] Ran `python db_manager.py setup`
- [ ] Got "SETUP COMPLETE!" message
- [ ] Can see login credentials in output
- [ ] `python main.py` launches without errors
- [ ] Can login with dr.ahmed.hassan / password123
- [ ] NFC card 0724184100 works
- [ ] Dashboard opens and shows data

---

## 💡 **Pro Tips:**

1. **Save the output** - The setup script shows all credentials
2. **Test incrementally** - Check each step works before moving on
3. **Use db_manager.py** - It's the easiest way
4. **Keep backups** - Export data before experimenting
5. **Reset when needed** - Fresh start is just one command away

---

## 🆘 **Still Having Issues?**

1. Run: `python db_manager.py test` (test connection)
2. Run: `python db_manager.py status` (check data)
3. Check MySQL is running: `sudo systemctl status mysql`
4. Verify password in config file
5. Try: `python db_manager.py reset` then `python db_manager.py setup`

---

**Your database is ready! 🚀**

Just run `python main.py` and start testing!
