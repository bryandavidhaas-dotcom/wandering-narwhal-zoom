import json
from backend.comprehensive_careers import COMPREHENSIVE_CAREERS

def consolidate_data():
    """
    Consolidates career data from comprehensive_careers.py into all_careers.json.
    """
    output_filename = 'all_careers.json'
    print(f"Consolidating {len(COMPREHENSIVE_CAREERS)} career profiles into {output_filename}...")

    with open(output_filename, 'w', encoding='utf-8') as f:
        json.dump(COMPREHENSIVE_CAREERS, f, indent=4)

    print(f"Successfully created {output_filename}")

if __name__ == "__main__":
    consolidate_data()