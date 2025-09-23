import json
import re

def extract_ts_array(ts_content):
    """Extracts the array content from the TypeScript file."""
    # Use a regular expression to find the array assignment
    match = re.search(r'export const TRADES_CAREER_TEMPLATES: CareerTemplate\[\] = (\[.*?\]);', ts_content, re.DOTALL)
    if not match:
        print("Error: Could not find TRADES_CAREER_TEMPLATES array in the TypeScript file.")
        return []
    
    array_str = match.group(1)
    
    # Basic conversion from TS object keys to JSON strings
    array_str = re.sub(r'(\w+):', r'"\1":', array_str)
    
    try:
        return json.loads(array_str)
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON from TypeScript file: {e}")
        # Attempt to fix common issues like trailing commas
        array_str = re.sub(r',\s*([\}\]])', r'\1', array_str)
        try:
            return json.loads(array_str)
        except json.JSONDecodeError as e2:
            print(f"Secondary decoding attempt failed: {e2}")
            return []

def consolidate_career_data():
    """
    Merges career data from careers.json and a TypeScript file into a new all_careers.json file,
    and updates all_career_types.json with all unique career types.
    """
    try:
        with open('careers.json', 'r', encoding='utf-8') as f:
            main_careers = json.load(f)
    except FileNotFoundError:
        print("Error: careers.json not found.")
        main_careers = []
    except json.JSONDecodeError:
        print("Error: Could not decode careers.json.")
        main_careers = []

    try:
        with open('frontend/src/utils/tradesCareerTemplates.ts', 'r', encoding='utf-8') as f:
            ts_content = f.read()
        trades_careers = extract_ts_array(ts_content)
    except FileNotFoundError:
        print("Error: frontend/src/utils/tradesCareerTemplates.ts not found.")
        trades_careers = []

    # Combine the lists of careers
    all_careers_raw = main_careers + trades_careers
    
    # Standardize and remove duplicates
    seen_career_types = set()
    unique_careers = []
    for career in all_careers_raw:
        career_type = career.get('careerType')
        if career_type and career_type not in seen_career_types:
            standardized_career = {
                "career_id": career_type,
                "title": career.get("title"),
                "description": career.get("description"),
                "required_technical_skills": career.get("requiredTechnicalSkills"),
                "required_soft_skills": career.get("requiredSoftSkills"),
                "salary_min": career.get("minSalary"),
                "salary_max": career.get("maxSalary"),
                "experience_level": career.get("experienceLevel"),
                "min_years_experience": career.get("minExperienceYears"),
                "max_years_experience": career.get("maxExperienceYears"),
                "work_data_weight": career.get("workDataWeight"),
                "work_people_weight": career.get("workPeopleWeight"),
                "creativity_weight": career.get("creativityWeight"),
                "problem_solving_weight": career.get("problemSolvingWeight"),
                "leadership_weight": career.get("leadershipWeight"),
            }
            unique_careers.append(standardized_career)
            seen_career_types.add(career_type)

    # Write the consolidated list to all_careers.json
    try:
        with open('all_careers.json', 'w', encoding='utf-8') as f:
            json.dump(unique_careers, f, indent=2)
        print(f"Successfully consolidated {len(unique_careers)} careers into all_careers.json")
    except IOError as e:
        print(f"Error writing to all_careers.json: {e}")

    # Generate the new all_career_types.json from the consolidated data
    all_career_types = sorted([career.get('career_id') for career in unique_careers if career.get('career_id')])
    
    try:
        with open('all_career_types.json', 'w', encoding='utf-8') as f:
            json.dump(all_career_types, f, indent=2)
        print(f"Successfully updated all_career_types.json with {len(all_career_types)} unique career types.")
    except IOError as e:
        print(f"Error writing to all_career_types.json: {e}")

if __name__ == "__main__":
    consolidate_career_data()