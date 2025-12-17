"""
AUTOMATIC PATCH - Add NFCCard Model
Automatically adds NFCCard to your existing models.py

Run: python add_nfccard_auto.py
"""

from pathlib import Path
import re

print("="*70)
print("  ADDING NFCCard MODEL TO models.py")
print("="*70)
print()

# NFCCard model code
NFCCARD_MODEL = '''
# ==================== NFC CARD BASE MODEL ====================

class NFCCard(Base):
    """Generic NFC Card model (for backward compatibility)"""
    __tablename__ = 'nfc_cards'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    card_uid = Column(String(50), unique=True, nullable=False, index=True)
    card_type = Column(String(50), nullable=False)  # 'doctor' or 'patient'
    owner_id = Column(String(50), nullable=False)  # user_id for doctors, national_id for patients
    owner_name = Column(String(200), nullable=False)
    status = Column(Enum(CardStatus), default=CardStatus.active)
    issue_date = Column(Date)
    expiry_date = Column(Date)
    last_used = Column(DateTime)
    use_count = Column(Integer, default=0)
    metadata = Column(JSON)  # Additional card data
    created_at = Column(DateTime, default=func.now())
    
    def __repr__(self):
        return f"<NFCCard(uid='{self.card_uid}', type='{self.card_type}', owner='{self.owner_name}')>"


'''

# Check models.py exists
models_file = Path("core/models.py")
if not models_file.exists():
    print("❌ core/models.py not found!")
    exit(1)

print("✅ Found core/models.py")

# Read content
content = models_file.read_text(encoding='utf-8')

# Check if NFCCard already exists
if 'class NFCCard(Base):' in content:
    print("⚠️  NFCCard model already exists!")
    print("   No changes needed.")
    exit(0)

print("📝 Adding NFCCard model...")

# Find DoctorCard class
match = re.search(r'(class DoctorCard\(Base\):)', content)

if not match:
    print("❌ Could not find DoctorCard class!")
    print("   Please add NFCCard manually before DoctorCard.")
    exit(1)

# Insert NFCCard before DoctorCard
insert_pos = match.start()
new_content = content[:insert_pos] + NFCCARD_MODEL + content[insert_pos:]

# Backup original
backup_file = Path("core/models.py.backup")
if not backup_file.exists():
    print("💾 Creating backup: core/models.py.backup")
    backup_file.write_text(content, encoding='utf-8')

# Write updated content
models_file.write_text(new_content, encoding='utf-8')

print("✅ NFCCard model added successfully!")
print()
print("="*70)
print("  NEXT STEPS")
print("="*70)
print()
print("1. ✅ Recreate database (adds nfc_cards table):")
print("   python database\\db_manager.py setup")
print()
print("2. ✅ Test the system:")
print("   python test_system.py")
print()
print("3. ✅ Run verification again:")
print("   python verify_models_complete.py")
print()
print("Expected: ✅ NFCCard → Found in models.py")
print()
