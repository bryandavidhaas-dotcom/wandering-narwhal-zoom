import json

def validate_career_data():
    """
    Validates the consolidated career data to ensure all profiles have the essential fields
    required by the recommendation engine.
    """
    essential_fields = [
        "career_id", "title", "description", "required_technical_skills",
        "required_soft_skills", "salary_min", "salary_max", "experience_level",
        "min_years_experience", "max_years_experience", "work_data_weight",
        "work_people_weight", "creativity_weight", "problem_solving_weight",
        "leadership_weight"
    ]

    try:
        with open('all_careers.json', 'r', encoding='utf-8') as f:
            all_careers = json.load(f)
    except FileNotFoundError:
        print("Error: all_careers.json not found. Please run the consolidation script first.")
        return
    except json.JSONDecodeError:
        print("Error: Could not decode all_careers.json.")
        return

    incomplete_careers = []
    for i, career in enumerate(all_careers):
        missing_fields = [field for field in essential_fields if field not in career or not career[field]]
        if missing_fields:
            incomplete_careers.append({
                "index": i,
                "title": career.get("title", "N/A"),
                "career_id": career.get("career_id", "N/A"),
                "missing_fields": missing_fields
            })

    if not incomplete_careers:
        print("Validation successful: All career profiles are complete and ready for the recommendation engine.")
    else:
        print(f"Found {len(incomplete_careers)} incomplete career profiles:")
        for career in incomplete_careers:
            print(f"  - Index: {career['index']}, Title: {career['title']}, Missing: {', '.join(career['missing_fields'])}")

if __name__ == "__main__":
    validate_career_data()