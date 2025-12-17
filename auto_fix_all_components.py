"""
AUTO-FIX SCRIPT - Fix All 28 GUI Components for Database
Run this to automatically fix ALL uploaded files

Usage:
    python auto_fix_all_components.py
"""

import os
import re
from pathlib import Path

# Converter code to inject
CONVERTER_CODE = '''
        # DATABASE FIX: Convert SQLAlchemy objects to dict
        if hasattr(patient_data, '__dict__') and not isinstance(patient_data, dict):
            if hasattr(patient_data, 'to_dict'):
                self.patient_data = patient_data.to_dict()
            else:
                # Manual conversion
                self.patient_data = {}
                for attr in ['national_id', 'full_name', 'age', 'gender', 'blood_type', 'phone', 'email']:
                    value = getattr(patient_data, attr, None)
                    if hasattr(value, 'value'):  # Enum
                        self.patient_data[attr] = value.value
                    else:
                        self.patient_data[attr] = value
                
                # Handle relationships
                if hasattr(patient_data, 'allergies'):
                    self.patient_data['allergies'] = [a.allergen_name for a in patient_data.allergies]
                if hasattr(patient_data, 'chronic_diseases'):
                    self.patient_data['chronic_diseases'] = [cd.disease_name for cd in patient_data.chronic_diseases]
                if hasattr(patient_data, 'current_medications'):
                    self.patient_data['current_medications'] = [
                        {'name': m.medication_name, 'dosage': m.dosage, 'frequency': m.frequency}
                        for m in patient_data.current_medications if hasattr(m, 'is_active') and m.is_active
                    ]
        else:
            self.patient_data = patient_data
'''

def fix_file(filepath):
    """Fix a single GUI component file"""
    try:
        content = filepath.read_text(encoding='utf-8')
        original = content
        modified = False
        
        # Fix 1: Add converter in __init__ if not exists
        if 'DATABASE FIX' not in content and 'def __init__(' in content:
            # Find __init__ method
            init_match = re.search(r'def __init__\(self[^)]*\):[^\n]*\n', content)
            if init_match:
                # Find super().__init__ call
                init_end = init_match.end()
                super_match = re.search(r'super\(\).__init__\([^)]*\)', content[init_end:])
                
                if super_match:
                    insert_pos = init_end + super_match.end()
                    # Find end of line
                    eol = content.find('\n', insert_pos)
                    if eol != -1:
                        content = content[:eol] + CONVERTER_CODE + content[eol:]
                        modified = True
        
        # Fix 2: Fix method names
        replacements = [
            ('get_patient_results', 'get_patient_lab_results'),
            ('medications[0], dict', 'isinstance(medications[0], dict)'),
        ]
        
        for old, new in replacements:
            if old in content:
                content = content.replace(old, new)
                modified = True
        
        # Fix 3: Fix medication display
        if 'current_medications' in content and 'isinstance(med, dict)' not in content:
            # Add medication handling
            med_pattern = r'for (\w+) in (\w+):\s+(\w+)_text = f"[^"]*{(\1)}[^"]*"'
            def med_replacer(match):
                var, list_var, prefix, var2 = match.groups()
                return f'''for {var} in {list_var}:
                if isinstance({var}, dict):
                    {prefix}_name = {var}.get('name', {var}.get('medication_name', 'Unknown'))
                    {prefix}_text = f"{{{prefix}_name}} - {{{var}.get('dosage', '')}} {{{var}.get('frequency', '')}}"
                else:
                    {prefix}_text = str({var})'''
            
            content = re.sub(med_pattern, med_replacer, content)
            if content != original:
                modified = True
        
        # Write if modified
        if modified:
            filepath.write_text(content, encoding='utf-8')
            return True, "Fixed"
        else:
            return False, "No changes needed"
            
    except Exception as e:
        return False, f"Error: {str(e)}"

def main():
    """Fix all GUI component files"""
    print("="*70)
    print("  AUTO-FIX SCRIPT - Database Compatibility for All GUI Components")
    print("="*70)
    print()
    
    # Get project root
    project_root = Path("D:/My-Projects/Python/Projects/webscraping/MedLink")
    components_dir = project_root / "gui" / "components"
    
    if not components_dir.exists():
        print(f"❌ Components directory not found: {components_dir}")
        print("\n⚠️  Update the project_root path in the script")
        return
    
    print(f"📁 Components directory: {components_dir}")
    print()
    
    # Files to fix (excluding already fixed ones)
    files_to_fix = [
        'patient_profile_tab.py',
        'medical_profile_tab.py',
        'patient_medical_history.py',
        'lab_results_tab.py',
        'lab_results_manager.py',
        'imaging_tab.py',
        'imaging_results_manager.py',
        'emergency_directives_manager.py',
        'lifestyle_manager.py',
        'medical_timeline.py',
        'visit_card.py',
        'history_tab.py',
        'my_history_tab.py',
        'add_surgery_dialog.py',
        'add_hospitalization_dialog.py',
        'add_vaccination_dialog.py',
        'add_visit_dialog.py',
        'disability_dialog.py',
        'family_history_dialog.py',
        'link_accounts_dialog.py',
        'sidebar.py',
        'emergency_card_tab.py'
    ]
    
    print(f"🔧 Files to fix: {len(files_to_fix)}\n")
    
    fixed_count = 0
    skipped_count = 0
    error_count = 0
    
    for filename in files_to_fix:
        filepath = components_dir / filename
        
        if not filepath.exists():
            print(f"⚠️  SKIP: {filename} (not found)")
            skipped_count += 1
            continue
        
        success, message = fix_file(filepath)
        
        if success:
            print(f"✅ FIXED: {filename}")
            fixed_count += 1
        elif "Error" in message:
            print(f"❌ ERROR: {filename} - {message}")
            error_count += 1
        else:
            print(f"📋 SKIP: {filename} - {message}")
            skipped_count += 1
    
    print()
    print("="*70)
    print("  SUMMARY")
    print("="*70)
    print(f"✅ Fixed: {fixed_count} files")
    print(f"📋 Skipped: {skipped_count} files (no changes needed)")
    print(f"❌ Errors: {error_count} files")
    print()
    
    if fixed_count > 0:
        print("🎉 SUCCESS! Files have been fixed.")
        print()
        print("📝 NEXT STEPS:")
        print("1. Test the application: python main.py")
        print("2. Login as doctor or patient")
        print("3. Check each component works")
        print()
        print("💡 If you encounter errors:")
        print("   - Check the specific file")
        print("   - Look at patient_card.py or emergency_card_content.py for examples")
        print("   - Use the db_compat_helper.py for manual fixes")
    
    print()
    print("="*70)

if __name__ == "__main__":
    main()
