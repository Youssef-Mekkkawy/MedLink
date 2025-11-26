"""
Imaging manager - Handle imaging results operations
"""
from typing import List, Dict, Optional
from core.data_manager import data_manager
from utils.date_utils import get_current_datetime
import uuid


class ImagingManager:
    """Manages imaging test results (X-rays, CT, MRI, etc.)"""
    
    def __init__(self):
        self.data_manager = data_manager
    
    def get_patient_imaging_results(self, national_id: str) -> List[Dict]:
        """
        Get all imaging results for a patient, sorted by date (newest first)
        
        Args:
            national_id: Patient's national ID
        
        Returns:
            List of imaging result dictionaries
        """
        results = self.data_manager.find_items(
            'imaging_results',
            'imaging_results',
            'patient_national_id',
            national_id
        )
        
        # Sort by date (newest first)
        return sorted(results, key=lambda x: x.get('date', ''), reverse=True)
    
    def get_imaging_result_by_id(self, imaging_id: str) -> Optional[Dict]:
        """Get single imaging result by ID"""
        return self.data_manager.find_item('imaging_results', 'imaging_results', 'imaging_id', imaging_id)
    
    def add_imaging_result(self, result_data: Dict) -> tuple[bool, str]:
        """
        Add new imaging result
        
        Args:
            result_data: Imaging result information dictionary
        
        Returns:
            (success: bool, message: str)
        """
        try:
            # Generate imaging ID if not provided
            if 'imaging_id' not in result_data:
                result_data['imaging_id'] = f"IMG{uuid.uuid4().hex[:8].upper()}"
            
            # Add timestamp
            if 'created_at' not in result_data:
                result_data['created_at'] = get_current_datetime()
            
            # Validate required fields
            required_fields = ['patient_national_id', 'date', 'imaging_center', 'imaging_type']
            for field in required_fields:
                if field not in result_data:
                    return False, f"Missing required field: {field}"
            
            # Add to database
            success = self.data_manager.add_item('imaging_results', 'imaging_results', result_data)
            
            if success:
                return True, "Imaging result added successfully"
            else:
                return False, "Failed to save imaging result"
        
        except Exception as e:
            return False, f"Error adding imaging result: {str(e)}"
    
    def update_imaging_result(self, imaging_id: str, result_data: Dict) -> tuple[bool, str]:
        """Update existing imaging result"""
        try:
            result_data['updated_at'] = get_current_datetime()
            
            success = self.data_manager.update_item(
                'imaging_results',
                'imaging_results',
                imaging_id,
                'imaging_id',
                result_data
            )
            
            if success:
                return True, "Imaging result updated successfully"
            else:
                return False, "Failed to update imaging result"
        
        except Exception as e:
            return False, f"Error updating imaging result: {str(e)}"
    
    def delete_imaging_result(self, imaging_id: str) -> tuple[bool, str]:
        """Delete imaging result"""
        try:
            success = self.data_manager.delete_item('imaging_results', 'imaging_results', imaging_id, 'imaging_id')
            
            if success:
                return True, "Imaging result deleted successfully"
            else:
                return False, "Failed to delete imaging result"
        
        except Exception as e:
            return False, f"Error deleting imaging result: {str(e)}"
    
    def get_results_by_imaging_type(self, national_id: str, imaging_type: str) -> List[Dict]:
        """Get all results of a specific imaging type for a patient"""
        all_results = self.get_patient_imaging_results(national_id)
        
        filtered = []
        for result in all_results:
            if imaging_type.lower() in result.get('imaging_type', '').lower():
                filtered.append(result)
        
        return filtered
    
    def get_results_count(self, national_id: str) -> int:
        """Get total imaging results count for a patient"""
        results = self.get_patient_imaging_results(national_id)
        return len(results)


# Global instance
imaging_manager = ImagingManager()