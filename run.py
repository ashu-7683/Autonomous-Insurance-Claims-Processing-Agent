# run.py - Updated for assessment
import sys
from pathlib import Path
from src.processor import FNOLProcessor
import json


def process_single_file(file_path: str, output_file: str = None):
    """Process a single FNOL document"""
    processor = FNOLProcessor()
    
    # Check if file exists
    if not Path(file_path).exists():
        print(f"Error: File not found - {file_path}")
        return
    
    print(f"Processing: {file_path}")
    print("-" * 50)
    
    # Process the document
    result = processor.process_document(file_path)
    
    # Display results
    print(f"Extracted Fields: {len(result['extractedFields'])}")
    print(f"Missing Fields: {result['missingFields']}")
    print(f"Recommended Route: {result['recommendedRoute']}")
    print(f"Reasoning: {result['reasoning']}")
    print()
    
    # Show extracted fields
    if result['extractedFields']:
        print("Extracted Data:")
        for key, value in result['extractedFields'].items():
            print(f"  {key}: {value}")
    
    # Save to JSON file
    if output_file:
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(result, f, indent=2, ensure_ascii=False)
        print(f"\nResult saved to: {output_file}")
    else:
        # Save with default name
        default_name = f"{Path(file_path).stem}_result.json"
        with open(default_name, 'w', encoding='utf-8') as f:
            json.dump(result, f, indent=2, ensure_ascii=False)
        print(f"\nResult saved to: {default_name}")
    
    return result


def process_demo():
    """Process all demo files from assessment"""
    processor = FNOLProcessor()
    
    demo_files = [
        "data/ACORD-Automobile-Loss-Notice-12.05.16.pdf",
        "txt_files/fnol_theft_claim.txt",
        "txt_files/fnol_injury_claim.txt",
        "txt_files/fnol_small_claim.txt",
        "txt_files/fnol_fraud_alert.txt"
    ]
    
    all_results = []
    
    for file_path in demo_files:
        print(f"\n{'='*60}")
        print(f"PROCESSING: {file_path}")
        print('='*60)
        
        if Path(file_path).exists():
            result = processor.process_document(file_path)
            all_results.append(result)
            
            # Display summary
            print(f"Extracted Fields: {len(result['extractedFields'])}")
            print(f"Missing Fields: {len(result['missingFields'])}")
            print(f"Recommended Route: {result['recommendedRoute']}")
            print(f"Reasoning: {result['reasoning']}")
            
            # Save individual result
            output_file = f"{Path(file_path).stem}_result.json"
            processor.save_result(result, output_file)
        else:
            print(f"File not found: {file_path}")
    
    # Save all results to a single file
    if all_results:
        with open("all_results.json", 'w', encoding='utf-8') as f:
            json.dump(all_results, f, indent=2, ensure_ascii=False)
        print(f"\n✅ All results saved to: all_results.json")


def show_help():
    """Show help message"""
    print("FNOL Processing Agent - Assessment Solution")
    print("=" * 50)
    print("\nCommands:")
    print("  python run.py demo              - Process all demo files")
    print("  python run.py process <file>    - Process a single file")
    print("  python run.py help              - Show this help")
    print("\nExamples:")
    print("  python run.py demo")
    print("  python run.py process data/ACORD-Automobile-Loss-Notice-12.05.16.pdf")
    print("  python run.py process txt_files/fnol_injury_claim.txt")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        show_help()
    elif sys.argv[1] == "demo":
        process_demo()
    elif sys.argv[1] == "process" and len(sys.argv) > 2:
        process_single_file(sys.argv[2])
    elif sys.argv[1] == "help":
        show_help()
    else:
        print(f"Unknown command: {sys.argv[1]}")
        show_help()