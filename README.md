# FNOL (First Notice of Loss) Processing Agent

A lightweight agent that extracts key fields from FNOL documents, identifies missing/inconsistent fields, classifies claims, and routes them to appropriate workflows using intelligent parsing and rule-based routing.

## ✨ Features

1. **Multi-Format Document Parsing**: Extract text from PDF and TXT FNOL documents
2. **Intelligent Field Extraction**: Identify key insurance claim fields using regex patterns and AI-like inference
3. **Automatic Validation**: Detect missing mandatory fields and data inconsistencies
4. **Rule-Based Routing**: Apply business logic to determine optimal workflow paths
5. **Structured JSON Output**: Generate standardized assessment-compliant results
6. **Batch Processing**: Handle multiple documents in a single run

## 🏗️ Tech Stack

### Core Application
- **Language**: Python 3.8+
- **Parsing Library**: pdfplumber (for PDF extraction)
- **Data Validation**: Custom regex-based field extraction
- **Configuration**: JSON-based routing rules
- **Output Format**: JSON (assessment-compliant)

### File Support
- **PDF Documents**: ACORD forms and other insurance PDFs
- **Text Files**: Structured FNOL text documents
- **Output**: JSON result files for each processed document

## 📁 Project Structure

fnol_agent/
├── run.py # Main command-line interface
├── requirements.txt # Python dependencies
├── README.md # This documentation
├── config/ # Configuration files
│ └── routing_rules.json # Business routing rules
├── data/ # Sample PDF documents
│ └── ACORD-Automobile-Loss-Notice-12.05.16.pdf
├── txt_files/ # Sample TXT documents
│ ├── fnoi_fraud_alert.txt
│ ├── fnoi_injury_claim.txt
│ ├── fnoi_small_claim.txt
│ └── fnoi_theft_claim.txt
├── src/ # Core application source
│ ├── init.py
│ ├── parser.py # Document parser (PDF/TXT)
│ ├── validator.py # Field validation engine
│ ├── router.py # Routing decision engine
│ ├── models.py # Data models (Pydantic)
│ └── processor.py # Main processing pipeline
└── *.json # Generated output files


## 🚀 Quick Start

### 1. Prerequisites
- Python 3.8 or higher
- pip (Python package manager)
- Basic command-line knowledge

### 2. Installation

```bash
# Navigate to your project directory
cd path/to/fnol_agent

# Create virtual environment (recommended)
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate

# Linux/Mac:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Show available commands
python run.py help

# Run complete demo (processes all 5 sample files)
python run.py demo

# Process a single file
python run.py process data/ACORD-Automobile-Loss-Notice-12.05.16.pdf
python run.py process txt_files/fnoi_theft_claim.txt

# Test specific components
python test_fixes.py


🔧 How It Works
1. Parsing Phase
PDF Processing: Uses pdfplumber to extract text from PDF documents

Text Processing: Regex patterns identify key-value pairs in TXT files

Field Extraction: Extracts 10+ key insurance fields including:

Policy Information (number, holder name)

Incident Details (date, time, location)

Claim Information (type, description, estimated damage)

Asset Details (type, VIN)

2. Validation Phase
Mandatory Field Check: Validates presence of required fields

Data Format Validation: Checks dates, amounts, and formats

Inference Logic: Infers missing fields (e.g., asset type from VIN)

3. Routing Phase (Business Rules)
Applies rules in priority order:

Priority	Rule	Route
1	Description contains fraud indicators ("fraudulent", "staged")	Investigation Flag
2	Claim type indicates injury	Specialist Queue
3	Any mandatory field missing	Manual Review
4	Estimated damage < $25,000	Fast-track
5	Estimated damage ≥ $25,000	Standard Processing
4. Output Phase
Generates JSON files with:

extractedFields: All successfully extracted data

missingFields: List of missing mandatory fields

recommendedRoute: Determined workflow route

reasoning: Explanation for routing decision

📝 Output Format Example
json
{
  "extractedFields": {
    "policy_number": "INS987654321",
    "policyholder_name": "Jane M. Doe",
    "incident_date": "01/20/2024",
    "incident_time": "02:15 PM",
    "location": "789 Park Avenue, Metropolis, NY 10001",
    "estimate_amount": "45000",
    "estimated_damage": "45000",
    "claim_type": "Theft",
    "asset_type": "Vehicle",
    "vin": "5XYZU3LB8EG123789",
    "description": "Vehicle stolen from parking garage overnight..."
  },
  "missingFields": ["claimant", "initial_estimate"],
  "recommendedRoute": "Standard Processing",
  "reasoning": "Estimated damage ($45,000) ≥ $25,000"
}

Verify Output
Check generated JSON files:

*_result.json: Individual document results

all_results.json: Combined results from demo run

🐛 Troubleshooting
Issue	Solution
"ModuleNotFoundError: No module named 'pdfplumber'"	Run pip install pdfplumber
"File not found" error	Ensure files exist in data/ or txt_files/
PDF parsing returns empty results	PDF may be scanned/image-based (requires OCR)
Field extraction misses data	Check regex patterns in src/parser.py
Wrong routing decisions	Verify business rules in src/router.py
⚡ Performance Notes
Processing Speed: TXT files process in <100ms, PDFs in 1-5 seconds

Memory Usage: Minimal (processes one document at a time)

Scalability: Handles batch processing via python run.py demo

Output: Generates separate JSON files for each processed document

