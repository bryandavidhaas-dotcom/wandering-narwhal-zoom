import json
import os
import importlib.util
from pathlib import Path
import inspect

# Define the paths
backend_path = Path(__file__).resolve().parent
json_output_path = backend_path / "career_data.json"

# The only module we need to process is the comprehensive one
career_modules = [
    "comprehensive_careers",
]

def load_careers_from_module(module_name: str):
    """Dynamically loads a Python module and extracts the 'COMPREHENSIVE_CAREERS' list."""
    module_path = backend_path / f"{module_name}.py"
    
    if not module_path.exists():
        print(f"Warning: Module file not found at {module_path}")
        return []

    # Dynamically import the module
    spec = importlib.util.spec_from_file_location(module_name, module_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    
    # Directly look for the 'COMPREHENSIVE_CAREERS' variable
    careers_list = getattr(module, "COMPREHENSIVE_CAREERS", [])
    if careers_list:
        print(f"  Found career list: 'COMPREHENSIVE_CAREERS'")
        return careers_list
    
    return []

def consolidate_careers():
    """
    Consolidates careers from the comprehensive career file into a single JSON file.
    """
    all_careers = []
    print("Starting career consolidation process...")

    for module_name in career_modules:
        print(f"Processing module: {module_name}")
        careers = load_careers_from_module(module_name)
        if careers:
            print(f"    -> Found {len(careers)} careers.")
            all_careers.extend(careers)
        else:
            print(f"    -> 'COMPREHENSIVE_CAREERS' list not found in {module_name}.")

    print(f"\nTotal careers consolidated: {len(all_careers)}")

    # Write the consolidated data to the JSON file
    try:
        with open(json_output_path, 'w') as f:
            json.dump(all_careers, f, indent=2)
        print(f"Successfully wrote {len(all_careers)} careers to {json_output_path}")
    except IOError as e:
        print(f"ERROR: Could not write to JSON file at {json_output_path}: {e}")

if __name__ == "__main__":
    consolidate_careers()