"""
Visit manager - Handle medical visit operations
"""
from typing import List, Dict, Optional
from core.data_manager import data_manager
from utils.date_utils import get_current_datetime
import uuid


class VisitManager:
    """Manages medical visit records"""
    
    def __init__(self):
        self.data_manager = data_manager
    
    def get_patient_visits(self, national_id: str) -> List[Dict]:
        """
        Get all visits for a patient, sorted by date (newest first)
        
        Args:
            national_id: Patient's national ID
        
        Returns:
            List of visit dictionaries
        """
        visits = self.data_manager.find_items(
            'visits', 
            'visits', 
            'patient_national_id', 
            national_id
        )
        
        # Sort by date (newest first)
        return sorted(
            visits, 
            key=lambda x: (x.get('date', ''), x.get('time', '')), 
            reverse=True
        )
    
    def get_visit_by_id(self, visit_id: str) -> Optional[Dict]:
        """Get single visit by ID"""
        return self.data_manager.find_item('visits', 'visits', 'visit_id', visit_id)
    
    def add_visit(self, visit_data: Dict) -> tuple[bool, str]:
        """
        Add new visit record
        
        Args:
            visit_data: Visit information dictionary
        
        Returns:
            (success: bool, message: str)
        """
        try:
            # Generate visit ID if not provided
            if 'visit_id' not in visit_data:
                visit_data['visit_id'] = f"V{uuid.uuid4().hex[:8].upper()}"
            
            # Add timestamp
            if 'created_at' not in visit_data:
                visit_data['created_at'] = get_current_datetime()
            
            # Validate required fields
            required_fields = ['patient_national_id', 'date', 'doctor_id', 'doctor_name']
            for field in required_fields:
                if field not in visit_data:
                    return False, f"Missing required field: {field}"
            
            # Add to database
            success = self.data_manager.add_item('visits', 'visits', visit_data)
            
            if success:
                return True, "Visit added successfully"
            else:
                return False, "Failed to save visit"
        
        except Exception as e:
            return False, f"Error adding visit: {str(e)}"
    
    def update_visit(self, visit_id: str, visit_data: Dict) -> tuple[bool, str]:
        """
        Update existing visit
        
        Args:
            visit_id: Visit ID to update
            visit_data: Updated visit information
        
        Returns:
            (success: bool, message: str)
        """
        try:
            # Add update timestamp
            visit_data['updated_at'] = get_current_datetime()
            
            success = self.data_manager.update_item(
                'visits', 
                'visits', 
                visit_id, 
                'visit_id', 
                visit_data
            )
            
            if success:
                return True, "Visit updated successfully"
            else:
                return False, "Failed to update visit"
        
        except Exception as e:
            return False, f"Error updating visit: {str(e)}"
    
    def delete_visit(self, visit_id: str) -> tuple[bool, str]:
        """
        Delete visit record
        
        Args:
            visit_id: Visit ID to delete
        
        Returns:
            (success: bool, message: str)
        """
        try:
            success = self.data_manager.delete_item('visits', 'visits', visit_id, 'visit_id')
            
            if success:
                return True, "Visit deleted successfully"
            else:
                return False, "Failed to delete visit"
        
        except Exception as e:
            return False, f"Error deleting visit: {str(e)}"
    
    def get_visits_by_doctor(self, doctor_id: str) -> List[Dict]:
        """Get all visits by a specific doctor"""
        visits = self.data_manager.find_items('visits', 'visits', 'doctor_id', doctor_id)
        return sorted(visits, key=lambda x: x.get('date', ''), reverse=True)
    
    def get_visits_by_date_range(self, national_id: str, start_date: str, end_date: str) -> List[Dict]:
        """Get visits within a date range"""
        all_visits = self.get_patient_visits(national_id)
        
        filtered = []
        for visit in all_visits:
            visit_date = visit.get('date', '')
            if start_date <= visit_date <= end_date:
                filtered.append(visit)
        
        return filtered
    
    def get_recent_visits(self, national_id: str, limit: int = 5) -> List[Dict]:
        """Get most recent visits for a patient"""
        visits = self.get_patient_visits(national_id)
        return visits[:limit]
    
    def get_visit_count(self, national_id: str) -> int:
        """Get total visit count for a patient"""
        visits = self.get_patient_visits(national_id)
        return len(visits)


# Global instance
visit_manager = VisitManager()