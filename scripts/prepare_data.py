import json
import re

def prepare_career_data():
    """
    Reads the career data from the frontend TypeScript file and converts it to a JSON file.
    """
    try:
        with open('frontend/src/utils/careerMatching.ts', 'r', encoding='utf-8') as f:
            content = f.read()
    except FileNotFoundError:
        print("Error: careerMatching.ts not found. Make sure the frontend directory is in the correct location.")
        return

    # Extract the COMPREHENSIVE_CAREER_TEMPLATES array
    start = content.find('const COMPREHENSIVE_CAREER_TEMPLATES: CareerTemplate[] = [')
    end = content.find('];', start)
    
    if start == -1 or end == -1:
        print("Error: Could not find the COMPREHENSIVE_CAREER_TEMPLATES array in the file.")
        return

    career_data_str = content[start + len('const COMPREHENSIVE_CAREER_TEMPLATES: CareerTemplate[] = '):end+1]
    
    # A more robust way to handle the conversion from TS to JSON
    # This is still not a perfect solution, but it's better than the previous one
    # Add quotes around keys that are not already quoted
    json_str = re.sub(r'([{,]\s*)(\w+):', r'\1"\2":', career_data_str)
    # Replace single quotes with double quotes
    json_str = json_str.replace("'", '"')
    # Remove trailing commas
    json_str = re.sub(r',\s*([}\]])', r'\1', json_str)
    
    try:
        careers = json.loads(json_str)
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")
        return

    # Write the data to a new JSON file
    with open('backend/career_data.json', 'w', encoding='utf-8') as f:
        json.dump(careers, f, indent=2)

    print(f"Successfully created backend/career_data.json with {len(careers)} careers.")

if __name__ == "__main__":
    prepare_career_data()