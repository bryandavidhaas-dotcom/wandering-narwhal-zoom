#!/usr/bin/env python3
"""
Extract career dictionaries from all *_careers.py files in the backend directory.
This script scans all career files and compiles a single careers.json file.
"""

import os
import re
import json
from pathlib import Path
import ast

def extract_careers_from_file(file_path):
    """
    Extracts career dictionary objects from a single Python career file.
    
    Args:
        file_path (str): Path to the career file.
        
    Returns:
        list: A list of career dictionary objects found in the file.
    """
    careers = []
    
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
            
        # Find the start of the list
        # Find the start of the list
        list_start_index = content.find('[')
        if list_start_index == -1:
            print(f"No list found in {os.path.basename(file_path)}")
            return careers

        # Extract the list content
        list_content = content[list_start_index:]

        try:
            # Safely evaluate the string as a Python literal
            evaluated_careers = ast.literal_eval(list_content)
            if isinstance(evaluated_careers, list):
                careers.extend(evaluated_careers)
                print(f"Found {len(careers)} careers in {os.path.basename(file_path)}")
        except (ValueError, SyntaxError) as e:
            print(f"Error parsing list in {os.path.basename(file_path)}: {e}")
            
    except Exception as e:
        print(f"Error processing {file_path}: {e}")
    
    return careers

def main():
    """
    Main function to extract all career objects and save them to careers.json.
    """
    backend_dir = Path("backend")
    
    if not backend_dir.exists():
        print("Error: backend directory not found!")
        return
    
    career_files = list(backend_dir.glob("*_careers.py"))
    
    if not career_files:
        print("No *_careers.py files found in the backend directory!")
        return
    
    print(f"Found {len(career_files)} career files:")
    for file in career_files:
        print(f"  - {file.name}")
    
    print("\nExtracting career objects...")
    
    all_careers = []
    
    for career_file in career_files:
        careers = extract_careers_from_file(career_file)
        all_careers.extend(careers)
    
    print(f"\nTotal careers extracted: {len(all_careers)}")
    
    output_file = "careers.json"
    
    try:
        with open(output_file, 'w', encoding='utf-8') as file:
            json.dump(all_careers, file, indent=2, ensure_ascii=False)
        
        print(f"\nSuccessfully wrote {len(all_careers)} careers to {output_file}")
        
        # Display a sample of the first career object for verification
        if all_careers:
            print("\nSample career object:")
            print(json.dumps(all_careers, indent=2))
            
    except Exception as e:
        print(f"Error writing to {output_file}: {e}")

if __name__ == "__main__":
    main()