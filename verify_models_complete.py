"""
VERIFY ALL MODELS AGAINST YOUR MANAGERS
Checks that every model imported in managers exists in models.py

Run: python verify_models_complete.py
"""

import os
import re
from pathlib import Path

print("="*70)
print("  VERIFYING MODELS COMPLETENESS")
print("="*70)
print()

# Step 1: Check models.py exists
models_file = Path("core/models.py")
if not models_file.exists():
    print("❌ core/models.py not found!")
    print("   Copy from: /mnt/user-data/outputs/FIXED_GUI_COMPONENTS/core/models.py")
    exit(1)

print("✅ Found core/models.py")
print()

# Step 2: Extract all class definitions from models.py
print("📋 Reading models.py...")
models_content = models_file.read_text(encoding='utf-8')

# Find all class definitions
model_classes = re.findall(r'^class (\w+)\(', models_content, re.MULTILINE)
enum_classes = re.findall(r'^class (\w+)\(enum\.Enum\)', models_content, re.MULTILINE)

print(f"   Found {len(model_classes)} model classes")
print(f"   Found {len(enum_classes)} enum classes")
print()

# Step 3: Check all manager files
print("="*70)
print("  CHECKING MANAGER IMPORTS")
print("="*70)
print()

manager_dir = Path("core")
if not manager_dir.exists():
    print("⚠️  core/ directory not found, skipping manager check")
    managers = []
else:
    managers = list(manager_dir.glob("*_manager.py"))
    print(f"Found {len(managers)} manager files:")
    for m in managers:
        print(f"   - {m.name}")
    print()

# Step 4: Extract imports from each manager
all_imports = set()
import_errors = []

for manager_file in managers:
    content = manager_file.read_text(encoding='utf-8')
    
    # Find model imports
    imports = re.findall(
        r'from (?:database\.models|core\.models) import ([A-Za-z, \n]+)',
        content
    )
    
    for import_line in imports:
        # Clean up the import line
        models = [m.strip() for m in import_line.replace('\n', ',').split(',') if m.strip()]
        all_imports.update(models)

print(f"📦 Total unique models imported by managers: {len(all_imports)}")
print()

# Step 5: Check if all imports exist in models.py
print("="*70)
print("  VERIFICATION RESULTS")
print("="*70)
print()

all_available = set(model_classes + enum_classes)
missing = []
found = []

for imported_model in sorted(all_imports):
    if imported_model in all_available:
        print(f"✅ {imported_model:25} → Found in models.py")
        found.append(imported_model)
    else:
        print(f"❌ {imported_model:25} → MISSING from models.py")
        missing.append(imported_model)

print()
print("="*70)
print("  SUMMARY")
print("="*70)
print()
print(f"✅ Found: {len(found)} models")
print(f"❌ Missing: {len(missing)} models")
print()

if missing:
    print("⚠️  MISSING MODELS:")
    for m in missing:
        print(f"   - {m}")
    print()
    print("🔧 ACTION REQUIRED:")
    print("   These models need to be added to core/models.py")
    print()
else:
    print("🎉 ALL MODELS PRESENT!")
    print()
    print("✅ Your models.py is complete!")
    print()

# Step 6: Show what's in the new models.py
print("="*70)
print("  MODELS IN NEW models.py")
print("="*70)
print()

categories = {
    "Core Models": ["User", "Doctor", "Patient"],
    "Medical History": ["Allergy", "ChronicDisease", "CurrentMedication", "Surgery", 
                        "Hospitalization", "Vaccination", "FamilyHistory", "Disability"],
    "Advanced": ["EmergencyDirective", "Lifestyle", "Insurance"],
    "Visits": ["Visit", "Prescription", "VitalSign"],
    "Results": ["LabResult", "ImagingResult"],
    "NFC Cards": ["NFCCard", "DoctorCard", "PatientCard"],
    "Audit": ["HardwareAuditLog"],
    "Enums": ["UserRole", "Gender", "BloodType", "VisitType", "TestStatus",
              "ImagingType", "CardStatus", "AccountStatus", "EventType"]
}

for category, models in categories.items():
    print(f"\n📋 {category} ({len(models)}):")
    for model in models:
        status = "✅" if model in all_available else "❌"
        print(f"   {status} {model}")

print()
print("="*70)
print("  NEXT STEPS")
print("="*70)
print()
print("1. ✅ Copy the new models.py:")
print("   copy /mnt/user-data/outputs/FIXED_GUI_COMPONENTS/core/models.py core/")
print()
print("2. ✅ Recreate database:")
print("   python database/db_manager.py setup")
print()
print("3. ✅ Test the system:")
print("   python test_system.py")
print()
print("4. ✅ Run the application:")
print("   python main.py")
print()
