"""
Data manager for JSON file operations
"""
import json
from pathlib import Path
from typing import Any, Dict, List
from config.settings import DATA_DIR


class DataManager:
    """Handles all JSON file operations"""

    def __init__(self):
        self.data_files = {
            'users': DATA_DIR / 'users.json',
            'patients': DATA_DIR / 'patients.json',
            'visits': DATA_DIR / 'visits.json',
            'lab_results': DATA_DIR / 'lab_results.json',
            'imaging_results': DATA_DIR / 'imaging_results.json',
        }

        # Initialize files if they don't exist
        self._initialize_files()

    def _initialize_files(self):
        """Create empty JSON files if they don't exist"""
        default_structures = {
            'users': {'users': []},
            'patients': {'patients': []},
            'visits': {'visits': []},
            'lab_results': {'lab_results': []},
            'imaging_results': {'imaging_results': []},
        }

        for file_key, file_path in self.data_files.items():
            if not file_path.exists():
                self.save_data(file_key, default_structures[file_key])

    def load_data(self, file_key: str) -> Dict:
        """Load data from JSON file"""
        try:
            with open(self.data_files[file_key], 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading {file_key}: {e}")
            return {}

    def save_data(self, file_key: str, data: Dict):
        """Save data to JSON file"""
        try:
            with open(self.data_files[file_key], 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"Error saving {file_key}: {e}")
            return False

    def add_item(self, file_key: str, list_key: str, item: Dict) -> bool:
        """Add item to a list in JSON file"""
        data = self.load_data(file_key)
        if list_key not in data:
            data[list_key] = []
        data[list_key].append(item)
        return self.save_data(file_key, data)

    def update_item(self, file_key: str, list_key: str,
                    item_id: str, id_field: str, updated_item: Dict) -> bool:
        """Update an item in a list"""
        data = self.load_data(file_key)
        if list_key in data:
            for i, item in enumerate(data[list_key]):
                if item.get(id_field) == item_id:
                    data[list_key][i] = updated_item
                    return self.save_data(file_key, data)
        return False

    def delete_item(self, file_key: str, list_key: str,
                    item_id: str, id_field: str) -> bool:
        """Delete an item from a list"""
        data = self.load_data(file_key)
        if list_key in data:
            data[list_key] = [
                item for item in data[list_key]
                if item.get(id_field) != item_id
            ]
            return self.save_data(file_key, data)
        return False

    def find_item(self, file_key: str, list_key: str,
                  field: str, value: Any) -> Dict:
        """Find single item by field value"""
        data = self.load_data(file_key)
        if list_key in data:
            for item in data[list_key]:
                if item.get(field) == value:
                    return item
        return None

    def find_items(self, file_key: str, list_key: str,
                   field: str, value: Any) -> List[Dict]:
        """Find multiple items by field value"""
        data = self.load_data(file_key)
        if list_key in data:
            return [item for item in data[list_key] if item.get(field) == value]
        return []


# Global instance
data_manager = DataManager()
