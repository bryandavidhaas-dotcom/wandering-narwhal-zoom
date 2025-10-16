import json
import sys
from pathlib import Path

# Add the project root to the Python path to allow for absolute imports
sys.path.append(str(Path(__file__).resolve().parent.parent))

from backend.recommendation_engine.career_database import CareerDatabase, CareerData, CareerField, ExperienceLevel

def populate_from_json(db_path: str = "backend/careers.db", json_path: str = "backend/career_data.json"):
    """
    Populates the career database from a JSON file.

    Args:
        db_path: The path to the SQLite database file.
        json_path: The path to the source JSON file.
    """
    print(f"Initializing database at: {db_path}")
    db = CareerDatabase(db_path)
    
    print(f"Reading career data from: {json_path}")
    try:
        with open(json_path, 'r') as f:
            careers_json = json.load(f)
    except FileNotFoundError:
        print(f"ERROR: JSON file not found at '{json_path}'. Cannot populate database.")
        return
    except json.JSONDecodeError:
        print(f"ERROR: Could not decode JSON from '{json_path}'. Please check the file for syntax errors.")
        return

    print(f"Found {len(careers_json)} careers to process.")
    
    migrated_count = 0
    for i, career_dict in enumerate(careers_json):
        try:
            # Basic validation
            if not all(k in career_dict for k in ['careerType', 'title', 'experienceLevel']):
                print(f"Skipping career {i+1} due to missing required fields (careerType, title, experienceLevel).")
                continue

            career_data = CareerData(
                career_id=career_dict.get('careerType'),
                title=career_dict.get('title'),
                description=career_dict.get('description', ''),
                # Assign a default field; this can be enhanced later
                career_field=CareerField(career_dict.get('careerField', 'other')),
                experience_level=ExperienceLevel(career_dict.get('experienceLevel', 'mid')),
                salary_min=career_dict.get('salaryMin', 50000),
                salary_max=career_dict.get('salaryMax', 100000),
                required_technical_skills=career_dict.get('requiredTechnicalSkills', []),
                required_soft_skills=career_dict.get('requiredSoftSkills', []),
                preferred_skills=career_dict.get('preferredSkills', []),
                required_certifications=career_dict.get('requiredCertifications', []),
                valued_certifications=career_dict.get('valuedCertifications', []),
                required_education=career_dict.get('requiredEducation', 'bachelors'),
                preferred_education=career_dict.get('preferredEducation', 'bachelors'),
                min_years_experience=career_dict.get('minYearsExperience', 0),
                max_years_experience=career_dict.get('maxYearsExperience', 50),
                work_data_weight=career_dict.get('workDataWeight', 3),
                work_people_weight=career_dict.get('workPeopleWeight', 3),
                creativity_weight=career_dict.get('creativityWeight', 3),
                problem_solving_weight=career_dict.get('problemSolvingWeight', 3),
                leadership_weight=career_dict.get('leadershipWeight', 3),
                hands_on_work_weight=career_dict.get('handsOnWorkWeight', 3),
                physical_work_weight=career_dict.get('physicalWorkWeight', 3),
                outdoor_work_weight=career_dict.get('outdoorWorkWeight', 3),
                mechanical_aptitude_weight=career_dict.get('mechanicalAptitudeWeight', 3),
                preferred_industries=career_dict.get('preferredIndustries', []),
                preferred_interests=career_dict.get('preferredInterests', []),
                companies=career_dict.get('companies', []),
                work_environments=career_dict.get('workEnvironments', ['office']),
                remote_options=career_dict.get('remoteOptions', 'Available'),
                learning_path=career_dict.get('learningPath', ''),
                day_in_life=career_dict.get('dayInLife', ''),
                resume_keywords=career_dict.get('resumeKeywords', [])
            )
            
            if db.add_career(career_data):
                migrated_count += 1
                
        except (ValueError, KeyError) as e:
            print(f"Skipping career {i+1} ('{career_dict.get('title', 'N/A')}') due to a data error: {e}")
            continue
            
    print(f"\nDatabase population complete.")
    print(f"Successfully migrated {migrated_count} out of {len(careers_json)} careers.")

if __name__ == "__main__":
    populate_from_json()