# src/processor.py
import json
from typing import Dict, Any
from pathlib import Path

from .parser import DocumentParser
from .validator import FieldValidator
from .router import RoutingEngine


class FNOLProcessor:
    """Main FNOL processing pipeline"""
    
    def __init__(self):
        self.parser = DocumentParser()
        self.validator = FieldValidator()
        self.router = RoutingEngine()
    
    def process_document(self, file_path: str) -> Dict[str, Any]:
        """Process a single FNOL document"""
        
        # Step 1: Parse document
        extracted_data = self.parser.parse_document(file_path)
        
        # Step 2: Validate and find missing fields
        missing_fields = self.validator.validate(extracted_data)
        
        # Step 3: Determine routing
        routing_info = self.router.determine_route(extracted_data, missing_fields)
        
        # Step 4: Prepare result in required format
        result = {
            "extractedFields": extracted_data,
            "missingFields": missing_fields,
            "recommendedRoute": routing_info['route'],
            "reasoning": routing_info['reasoning']
        }
        
        return result
    
    def save_result(self, result: Dict[str, Any], output_file: str = "result.json"):
        """Save result to JSON file"""
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(result, f, indent=2, ensure_ascii=False)
        
        print(f"Result saved to {output_file}")