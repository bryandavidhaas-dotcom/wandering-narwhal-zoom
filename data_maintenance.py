import json
import re

def extract_ts_array(ts_content):
    """
    Extracts and parses the TRADES_CAREER_TEMPLATES array from a TypeScript file.
    """
    # A more robust regex to find the array, ignoring comments
    match = re.search(r'export const TRADES_CAREER_TEMPLATES: CareerTemplate\[\] = (\[.*?\]);', ts_content, re.DOTALL)
    if not match:
        print("Error: Could not find TRADES_CAREER_TEMPLATES array in the TypeScript file.")
        return []
    
    array_str = match.group(1)

    # This is a simplified parser and may need to be more robust
    # Remove comments
    array_str = re.sub(r'//.*?\n', '', array_str)
    # Convert JS object keys to JSON strings
    array_str = re.sub(r'(\s*)(\w+):', r'\1"\2":', array_str)
    # Convert single quotes to double quotes
    array_str = array_str.replace("'", '"')
    # Remove trailing commas
    array_str = re.sub(r',\s*([\}\]])', r'\1', array_str)

    try:
        return json.loads(array_str)
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON from TypeScript file: {e}")
        return []

def consolidate_and_validate():
    """
    Consolidates career data from multiple sources and validates it for completeness.
    """
    try:
        with open('careers.json', 'r', encoding='utf-8') as f:
            main_careers = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Error reading careers.json: {e}")
        main_careers = []

    try:
        with open('trades_careers.json', 'r', encoding='utf-8') as f:
            trades_careers = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Error reading trades_careers.json: {e}")
        trades_careers = []

    all_careers_raw = main_careers + trades_careers
    
    seen_career_types = set()
    unique_careers = []
    for career in all_careers_raw:
        career_type = career.get('careerType')
        if career_type and career_type not in seen_career_types:
            unique_careers.append(career)
            seen_career_types.add(career_type)

    with open('all_careers.json', 'w', encoding='utf-8') as f:
        json.dump(unique_careers, f, indent=2)
    print(f"Successfully consolidated {len(unique_careers)} careers into all_careers.json")

    all_career_types = sorted([career.get('careerType') for career in unique_careers if career.get('careerType')])
    with open('all_career_types.json', 'w', encoding='utf-8') as f:
        json.dump(all_career_types, f, indent=2)
    print(f"Successfully updated all_career_types.json with {len(all_career_types)} unique career types.")

    # Validation
    essential_fields = [
        "title", "description", "requiredTechnicalSkills", "requiredSoftSkills", 
        "minSalary", "maxSalary", "experienceLevel", "minYearsExperience", 
        "maxYearsExperience", "workDataWeight", "workPeopleWeight", 
        "creativityWeight", "problemSolvingWeight", "leadershipWeight"
    ]
    
    incomplete_careers = []
    for i, career in enumerate(unique_careers):
        missing_fields = [field for field in essential_fields if field not in career or not career[field]]
        if missing_fields:
            incomplete_careers.append({
                "index": i,
                "title": career.get("title", "N/A"),
                "careerType": career.get("careerType", "N/A"),
                "missing_fields": missing_fields
            })

    if not incomplete_careers:
        print("\nValidation successful: All career profiles are complete.")
    else:
        print(f"\nFound {len(incomplete_careers)} incomplete career profiles:")
        for career in incomplete_careers:
            print(f"  - Index: {career['index']}, Title: {career['title']}, Missing: {', '.join(career['missing_fields'])}")

if __name__ == "__main__":
    consolidate_and_validate()