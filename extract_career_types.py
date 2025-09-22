#!/usr/bin/env python3
"""
Extract careerType values from all *_careers.py files in the backend directory.
This script scans all career files and compiles a list of unique careerType values.
"""

import os
import re
import json
from pathlib import Path

def extract_career_types_from_file(file_path):
    """
    Extract careerType values from a single Python career file.
    
    Args:
        file_path (str): Path to the career file
        
    Returns:
        list: List of careerType values found in the file
    """
    career_types = []
    
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
            
        # Use regex to find all careerType values
        # This pattern looks for "careerType": "value" with proper string handling
        pattern = r'"careerType":\s*"([^"]+)"'
        matches = re.findall(pattern, content)
        
        career_types.extend(matches)
        
        print(f"Found {len(matches)} careerType values in {os.path.basename(file_path)}")
        
    except Exception as e:
        print(f"Error processing {file_path}: {e}")
    
    return career_types

def main():
    """
    Main function to extract all careerType values from backend career files.
    """
    # Define the backend directory path
    backend_dir = Path("backend")
    
    if not backend_dir.exists():
        print("Error: backend directory not found!")
        return
    
    # Find all *_careers.py files
    career_files = list(backend_dir.glob("*_careers.py"))
    
    if not career_files:
        print("No *_careers.py files found in the backend directory!")
        return
    
    print(f"Found {len(career_files)} career files:")
    for file in career_files:
        print(f"  - {file.name}")
    
    print("\nExtracting careerType values...")
    
    # Extract careerType values from all files
    all_career_types = []
    
    for career_file in career_files:
        career_types = extract_career_types_from_file(career_file)
        all_career_types.extend(career_types)
    
    # Remove duplicates and sort
    unique_career_types = sorted(list(set(all_career_types)))
    
    print(f"\nTotal careerType values found: {len(all_career_types)}")
    print(f"Unique careerType values: {len(unique_career_types)}")
    
    # Write to JSON file
    output_file = "all_career_types.json"
    
    try:
        with open(output_file, 'w', encoding='utf-8') as file:
            json.dump(unique_career_types, file, indent=2, ensure_ascii=False)
        
        print(f"\nSuccessfully wrote {len(unique_career_types)} unique career types to {output_file}")
        
        # Display first 10 career types as a sample
        print("\nSample career types:")
        for i, career_type in enumerate(unique_career_types[:10]):
            print(f"  {i+1}. {career_type}")
        
        if len(unique_career_types) > 10:
            print(f"  ... and {len(unique_career_types) - 10} more")
            
    except Exception as e:
        print(f"Error writing to {output_file}: {e}")

if __name__ == "__main__":
    main()