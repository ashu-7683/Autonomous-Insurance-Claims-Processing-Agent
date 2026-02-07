# test_fixes.py
from src.processor import FNOLProcessor

def test_fraud_alert():
    print("Testing Fraud Alert TXT...")
    processor = FNOLProcessor()
    result = processor.process_document("txt_files/fnol_fraud_alert.txt")
    
    print("\nExpected:")
    print("- Location should be extracted")
    print("- Claim type should be 'Fire Damage' (not 'Fire Damage\\nDESCRIPTION')")
    print("- Should route to 'Investigation Flag' (contains 'suspicious')")
    
    print("\nActual Result:")
    print(f"Location: {result['extractedFields'].get('location', 'MISSING')}")
    print(f"Claim Type: {result['extractedFields'].get('claim_type', 'MISSING')}")
    print(f"Route: {result['recommendedRoute']}")
    print(f"Reasoning: {result['reasoning']}")
    
    return result

def test_injury_claim():
    print("\n" + "="*50)
    print("Testing Injury Claim TXT...")
    processor = FNOLProcessor()
    result = processor.process_document("txt_files/fnol_injury_claim.txt")
    
    print("\nExpected:")
    print("- Location should be extracted")
    print("- Claim type should be 'Injury' (not 'Injury\\nDESCRIPTION')")
    print("- Should route to 'Specialist Queue'")
    
    print("\nActual Result:")
    print(f"Location: {result['extractedFields'].get('location', 'MISSING')}")
    print(f"Claim Type: {result['extractedFields'].get('claim_type', 'MISSING')}")
    print(f"Route: {result['recommendedRoute']}")
    print(f"Reasoning: {result['reasoning']}")
    
    return result

def test_all_files():
    print("\n" + "="*50)
    print("Testing All Files...")
    
    files = [
        "txt_files/fnol_fraud_alert.txt",
        "txt_files/fnol_injury_claim.txt",
        "txt_files/fnol_small_claim.txt",
        "txt_files/fnol_theft_claim.txt",
        "data/ACORD-Automobile-Loss-Notice-12.05.16.pdf"
    ]
    
    processor = FNOLProcessor()
    
    for file in files:
        print(f"\n{'='*40}")
        print(f"File: {file}")
        try:
            result = processor.process_document(file)
            print(f"Route: {result['recommendedRoute']}")
            print(f"Missing: {len(result['missingFields'])} fields")
            
            # Show problematic fields
            for field in ['claim_type', 'asset_type']:
                if field in result['extractedFields']:
                    value = result['extractedFields'][field]
                    if '\\n' in str(value) or 'DESCRIPTION' in str(value):
                        print(f"⚠ {field} needs cleaning: {value}")
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    test_fraud_alert()
    test_injury_claim()
    test_all_files()