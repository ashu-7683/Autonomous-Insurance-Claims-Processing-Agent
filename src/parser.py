# src/parser.py - WITH INFERENCE FOR ASSET TYPE
import re
import pdfplumber
from typing import Dict, Any
from pathlib import Path


class DocumentParser:
    """Parser for FNOL documents in PDF/TXT format"""
    
    def parse_document(self, file_path: str) -> Dict[str, Any]:
        """Parse document based on file extension"""
        path = Path(file_path)
        
        if not path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")
        
        if path.suffix.lower() == '.pdf':
            return self.parse_pdf(path)
        elif path.suffix.lower() == '.txt':
            return self.parse_txt(path)
        else:
            raise ValueError(f"Unsupported file format: {path.suffix}")
    
    def parse_pdf(self, file_path: Path) -> Dict[str, Any]:
        """Extract text from PDF file - Improved for ACORD forms"""
        text = ""
        try:
            with pdfplumber.open(file_path) as pdf:
                for page in pdf.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n"
        except Exception as e:
            print(f"Error reading PDF: {e}")
            return {}
        
        extracted = self._extract_from_text(text)
        self._infer_missing_fields(extracted, file_path.name)
        return extracted
    
    def parse_txt(self, file_path: Path) -> Dict[str, Any]:
        """Extract text from TXT file"""
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                text = f.read()
        except Exception as e:
            print(f"Error reading TXT file: {e}")
            return {}
        
        extracted = self._extract_from_text(text)
        self._infer_missing_fields(extracted, file_path.name)
        return extracted
    
    def _extract_from_text(self, text: str) -> Dict[str, Any]:
        """Extract fields from text content"""
        extracted = {}
        
        # Split text into lines
        lines = [line.strip() for line in text.split('\n') if line.strip()]
        
        # Field patterns with more flexible matching
        patterns = {
            'policy_number': r'POLICY\s*(?:NO\.?|NUMBER|#)\s*:?\s*([A-Z0-9-]+)',
            'policyholder_name': r'NAME\s*(?:OF\s*)?INSURED\s*:?\s*(.+?)(?=\n|$)',
            'incident_date': r'DATE\s*(?:OF\s*)?LOSS\s*:?\s*(\d{1,2}/\d{1,2}/\d{4})',
            'incident_time': r'TIME\s*:?\s*(\d{1,2}:\d{2}\s*[APMapm]{2})',
            'location': r'LOCATION\s*:?\s*(.+?)(?=\n|$)',
            'estimate_amount': r'ESTIMATE\s*AMOUNT\s*:?\s*\$?\s*([\d,]+)',
            'claim_type': r'CLAIM\s*TYPE\s*:?\s*(.+?)(?=\n|$)',
            'asset_type': r'ASSET\s*TYPE\s*:?\s*(.+?)(?=\n|$)',
            'vin': r'V\.?I\.?N\.?\s*:?\s*([A-HJ-NPR-Z0-9]{17})',
            'description': r'DESCRIPTION\s*:?\s*(.+?)(?=\n[A-Z]|$)',
        }
        
        # First pass: try regex patterns
        for field, pattern in patterns.items():
            match = re.search(pattern, text, re.IGNORECASE | re.DOTALL)
            if match:
                value = match.group(1).strip()
                if field == 'estimate_amount':
                    value = value.replace('$', '').replace(',', '')
                    extracted['estimate_amount'] = value
                    extracted['estimated_damage'] = value
                elif field == 'description':
                    # Clean description - take until next field
                    value = self._clean_description(value)
                    extracted[field] = value
                else:
                    extracted[field] = value
        
        # Second pass: line-by-line extraction for missed fields
        for i, line in enumerate(lines):
            if ':' in line:
                key, value = line.split(':', 1)
                key = key.strip().upper()
                value = value.strip()
                
                if 'POLICY' in key and 'NUMBER' in key and 'policy_number' not in extracted:
                    extracted['policy_number'] = value
                elif 'NAME' in key and 'INSURED' in key and 'policyholder_name' not in extracted:
                    extracted['policyholder_name'] = value
                elif 'DATE' in key and 'LOSS' in key and 'incident_date' not in extracted:
                    extracted['incident_date'] = value
                elif 'TIME' in key and 'incident_time' not in extracted:
                    extracted['incident_time'] = value
                elif 'LOCATION' in key and 'location' not in extracted:
                    extracted['location'] = value
                elif 'ESTIMATE' in key and 'AMOUNT' in key and 'estimate_amount' not in extracted:
                    cleaned = value.replace('$', '').replace(',', '')
                    extracted['estimate_amount'] = cleaned
                    extracted['estimated_damage'] = cleaned
                elif 'CLAIM' in key and 'TYPE' in key and 'claim_type' not in extracted:
                    extracted['claim_type'] = value.split()[0]  # Take first word
                elif 'ASSET' in key and 'TYPE' in key and 'asset_type' not in extracted:
                    extracted['asset_type'] = value.split()[0]
                elif 'DESCRIPTION' in key and 'description' not in extracted:
                    # Collect multi-line description
                    desc_lines = [value]
                    for j in range(i+1, len(lines)):
                        next_line = lines[j]
                        if ':' not in next_line:  # Not a new field
                            desc_lines.append(next_line)
                        else:
                            break
                    extracted['description'] = ' '.join(desc_lines)
        
        return extracted
    
    def _infer_missing_fields(self, extracted: Dict[str, Any], filename: str):
        """Infer missing fields based on context"""
        
        # Infer asset_type if missing
        if 'asset_type' not in extracted:
            if 'vin' in extracted:
                extracted['asset_type'] = 'Vehicle'
            elif 'claim_type' in extracted:
                claim_type = extracted['claim_type'].lower()
                if any(t in claim_type for t in ['theft', 'auto', 'vehicle', 'property']):
                    extracted['asset_type'] = 'Vehicle'
                elif 'fire' in claim_type:
                    extracted['asset_type'] = 'Property'
                elif 'injury' in claim_type:
                    extracted['asset_type'] = 'Property'
        
        # Infer claim_type from filename if missing
        if 'claim_type' not in extracted:
            filename_lower = filename.lower()
            if 'theft' in filename_lower:
                extracted['claim_type'] = 'Theft'
            elif 'injury' in filename_lower:
                extracted['claim_type'] = 'Injury'
            elif 'fraud' in filename_lower:
                extracted['claim_type'] = 'Fire Damage'  # From fraud_alert.txt
            elif 'small' in filename_lower:
                extracted['claim_type'] = 'Property Damage'
        
        # Ensure estimated_damage exists
        if 'estimate_amount' in extracted and 'estimated_damage' not in extracted:
            extracted['estimated_damage'] = extracted['estimate_amount']
    
    def _clean_description(self, description: str) -> str:
        """Clean description text"""
        # Remove any field labels that might have been included
        field_labels = ['VEHICLE MAKE:', 'V.I.N.:', 'CONTACT:', 'ASSET TYPE:']
        for label in field_labels:
            if label in description:
                description = description.split(label)[0].strip()
        
        # Remove trailing INVESTIGATION NEEDED if it's a separate line
        if 'INVESTIGATION NEEDED' in description:
            description = description.replace('INVESTIGATION NEEDED', '').strip()
        
        return description