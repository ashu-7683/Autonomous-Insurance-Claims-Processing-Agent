# src/validator.py - UPDATED
from typing import List, Dict, Any
import re


class FieldValidator:
    """Validate extracted fields and identify missing ones"""
    
    def __init__(self):
        self.mandatory_fields = [
            'policy_number',
            'policyholder_name', 
            'incident_date',
            'incident_time',
            'location',
            'description',
            'claimant',
            'asset_type',
            'estimated_damage',  # Accepts both estimated_damage and estimate_amount
            'claim_type',
            'initial_estimate'
        ]
    
    def validate(self, extracted_data: Dict[str, Any]) -> List[str]:
        """Identify missing mandatory fields"""
        missing_fields = []
        
        # Map estimate_amount to estimated_damage if present
        if 'estimate_amount' in extracted_data and 'estimated_damage' not in extracted_data:
            extracted_data['estimated_damage'] = extracted_data['estimate_amount']
        
        for field in self.mandatory_fields:
            value = extracted_data.get(field)
            
            # For description, check if it's not just a single word
            if field == 'description' and value:
                if len(value.strip().split()) < 3:  # If less than 3 words
                    missing_fields.append(field)
                else:
                    continue
            
            if not value or (isinstance(value, str) and not value.strip()):
                missing_fields.append(field)
        
        return missing_fields
    
    def check_inconsistencies(self, extracted_data: Dict[str, Any]) -> List[str]:
        """Check for data inconsistencies"""
        inconsistencies = []
        
        # Check date format
        date_fields = ['incident_date', 'effective_dates']
        for field in date_fields:
            value = extracted_data.get(field)
            if value and isinstance(value, str):
                if not self._is_valid_date(value):
                    inconsistencies.append(f"Invalid date format in {field}: {value}")
        
        # Check numeric values
        estimate_fields = ['estimated_damage', 'estimate_amount', 'initial_estimate']
        for field in estimate_fields:
            value = extracted_data.get(field)
            if value:
                if not self._is_numeric(value):
                    inconsistencies.append(f"{field} is not a valid number: {value}")
        
        return inconsistencies
    
    def _is_valid_date(self, date_str: str) -> bool:
        """Simple date validation"""
        patterns = [
            r'\d{1,2}/\d{1,2}/\d{4}',
            r'\d{4}-\d{2}-\d{2}',
        ]
        
        for pattern in patterns:
            if re.match(pattern, str(date_str)):
                return True
        return False
    
    def _is_numeric(self, value: Any) -> bool:
        """Check if value is numeric"""
        try:
            if isinstance(value, str):
                # Remove commas and currency symbols
                cleaned = re.sub(r'[^\d\.]', '', value)
                float(cleaned)
            elif isinstance(value, (int, float)):
                return True
            return True
        except (ValueError, TypeError):
            return False