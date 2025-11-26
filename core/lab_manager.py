"""
Lab manager - Handle lab results operations
"""
from typing import List, Dict, Optional
from core.data_manager import data_manager
from utils.date_utils import get_current_datetime
import uuid


class LabManager:
    """Manages lab test results"""
    
    def __init__(self):
        self.data_manager = data_manager
    
    def get_patient_lab_results(self, national_id: str) -> List[Dict]:
        """
        Get all lab results for a patient, sorted by date (newest first)
        
        Args:
            national_id: Patient's national ID
        
        Returns:
            List of lab result dictionaries
        """
        results = self.data_manager.find_items(
            'lab_results',
            'lab_results',
            'patient_national_id',
            national_id
        )
        
        # Sort by date (newest first)
        return sorted(results, key=lambda x: x.get('date', ''), reverse=True)
    
    def get_lab_result_by_id(self, result_id: str) -> Optional[Dict]:
        """Get single lab result by ID"""
        return self.data_manager.find_item('lab_results', 'lab_results', 'result_id', result_id)
    
    def add_lab_result(self, result_data: Dict) -> tuple[bool, str]:
        """
        Add new lab result
        
        Args:
            result_data: Lab result information dictionary
        
        Returns:
            (success: bool, message: str)
        """
        try:
            # Generate result ID if not provided
            if 'result_id' not in result_data:
                result_data['result_id'] = f"LAB{uuid.uuid4().hex[:8].upper()}"
            
            # Add timestamp
            if 'created_at' not in result_data:
                result_data['created_at'] = get_current_datetime()
            
            # Validate required fields
            required_fields = ['patient_national_id', 'date', 'lab_name', 'test_type']
            for field in required_fields:
                if field not in result_data:
                    return False, f"Missing required field: {field}"
            
            # Add to database
            success = self.data_manager.add_item('lab_results', 'lab_results', result_data)
            
            if success:
                return True, "Lab result added successfully"
            else:
                return False, "Failed to save lab result"
        
        except Exception as e:
            return False, f"Error adding lab result: {str(e)}"
    
    def update_lab_result(self, result_id: str, result_data: Dict) -> tuple[bool, str]:
        """Update existing lab result"""
        try:
            result_data['updated_at'] = get_current_datetime()
            
            success = self.data_manager.update_item(
                'lab_results',
                'lab_results',
                result_id,
                'result_id',
                result_data
            )
            
            if success:
                return True, "Lab result updated successfully"
            else:
                return False, "Failed to update lab result"
        
        except Exception as e:
            return False, f"Error updating lab result: {str(e)}"
    
    def delete_lab_result(self, result_id: str) -> tuple[bool, str]:
        """Delete lab result"""
        try:
            success = self.data_manager.delete_item('lab_results', 'lab_results', result_id, 'result_id')
            
            if success:
                return True, "Lab result deleted successfully"
            else:
                return False, "Failed to delete lab result"
        
        except Exception as e:
            return False, f"Error deleting lab result: {str(e)}"
    
    def get_results_by_test_type(self, national_id: str, test_type: str) -> List[Dict]:
        """Get all results of a specific test type for a patient"""
        all_results = self.get_patient_lab_results(national_id)
        
        filtered = []
        for result in all_results:
            if test_type.lower() in result.get('test_type', '').lower():
                filtered.append(result)
        
        return filtered
    
    def get_results_count(self, national_id: str) -> int:
        """Get total lab results count for a patient"""
        results = self.get_patient_lab_results(national_id)
        return len(results)


# Global instance
lab_manager = LabManager()