import json
from pathlib import Path

# Define the path to the career data
backend_path = Path(__file__).resolve().parent
json_path = backend_path / "career_data.json"

# Define the mapping for inconsistent experience levels
experience_level_map = {
    "Senior-Level": "senior",
    "Mid-Level": "mid",
    "Entry-Level": "entry",
    # Add any other variations if found
}

def clean_experience_levels():
    """
    Cleans the 'experienceLevel' field in the career_data.json file.
    """
    print(f"Reading career data from: {json_path}")
    try:
        with open(json_path, 'r') as f:
            careers = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"ERROR: Could not read or decode JSON file: {e}")
        return

    cleaned_count = 0
    print("Starting data cleaning process for 'experienceLevel'...")

    for career in careers:
        original_level = career.get("experienceLevel")
        if original_level in experience_level_map:
            new_level = experience_level_map[original_level]
            career["experienceLevel"] = new_level
            cleaned_count += 1
            print(f"  - Cleaned '{career.get('title')}': Changed '{original_level}' to '{new_level}'")

    if cleaned_count == 0:
        print("No inconsistencies found. Data is already clean.")
    else:
        print(f"\nCleaned {cleaned_count} career entries.")

    # Write the cleaned data back to the file
    try:
        with open(json_path, 'w') as f:
            json.dump(careers, f, indent=2)
        print(f"Successfully wrote cleaned data back to {json_path}")
    except IOError as e:
        print(f"ERROR: Could not write cleaned data to file: {e}")

if __name__ == "__main__":
    clean_experience_levels()