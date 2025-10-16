import json
from collections import defaultdict

def calculate_all_stats():
    """
    Calculates all statistics for the homepage from the career data and assessment structure.
    """
    # --- Career Data Analysis ---
    try:
        with open('production_career_data.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
            career_data = data.get('careers', [])
    except FileNotFoundError:
        print("Error: production_career_data.json not found.")
        return
    except json.JSONDecodeError:
        print("Error: Could not decode JSON from production_career_data.json.")
        return

    num_careers = len(career_data)
    
    # 1. Skill-Career Connections
    skill_career_connections = 0
    for career in career_data:
        skill_career_connections += len(career.get('requiredTechnicalSkills', []))
        skill_career_connections += len(career.get('requiredSoftSkills', []))

    # 2. Career Data Points
    career_data_points = 0
    if num_careers > 0:
        # CORRECTED LOGIC: Get keys from the first career object in the list
        career_data_points = num_careers * len(career_data.keys())

    # --- User Assessment Data Point Analysis ---
    # Based on the structure of frontend/src/pages/Assessment.tsx
    assessment_data_points = {
        "Basic Information": 10, # age, location, education, etc. + resume + linkedin
        "Certifications": 44,
        "Technical Skills": 32,
        "Soft Skills": 32,
        "Work Preferences": 8, # sliders
        "Interests": 18,
        "Industries": 18,
        "Goals & Expectations": 3 # careerGoals, workLifeBalance, salaryExpectations
    }
    total_assessment_points = sum(assessment_data_points.values())
    
    # 3. Total Data Points Analyzed
    total_data_points = career_data_points + total_assessment_points

    # 4. Career Categorization
    categories = {
        "Technology & Engineering": ["engineer", "developer", "architect", "technician", "scientist", "tech", "it"],
        "Healthcare & Medical": ["physician", "nurse", "therapist", "medical", "health", "practitioner", "surgeon"],
        "Skilled Trades & Construction": ["electrician", "plumber", "carpenter", "construction", "mechanic", "welder", "hvac"],
        "Education & Training": ["teacher", "professor", "educator", "trainer", "counselor", "school", "education"],
        "Business & Finance": ["analyst", "manager", "accountant", "consultant", "director", "finance", "business"],
        "Legal & Law": ["lawyer", "attorney", "legal", "paralegal"],
        "Creative & Arts": ["designer", "artist", "creative", "writer", "photographer", "art"],
        "Public Service & Government": ["government", "public service", "officer", "federal", "state", "municipal"],
        "Hospitality & Service": ["hotel", "restaurant", "hospitality", "service", "tourism"],
        "Manufacturing & Industrial": ["manufacturing", "industrial", "production", "plant", "operator"],
        "Agriculture & Environment": ["agriculture", "environmental", "farm", "conservation", "agronomist"]
    }
    
    category_counts = defaultdict(int)
    unassigned_careers = []

    for career in career_data:
        title = career.get('title', '').lower()
        career_type = career.get('careerType', '').lower()
        description = career.get('description', '').lower()
        
        assigned = False
        for category, keywords in categories.items():
            # Simple keyword matching
            search_text = f"{title} {career_type} {description}"
            if any(keyword in search_text for keyword in keywords):
                category_counts[category] += 1
                assigned = True
                break
        
        if not assigned:
            unassigned_careers.append(career['title'])
            category_counts["Other"] += 1

    # --- Print All Results ---
    print("--- Homepage Statistics ---")
    print(f"\n1. Total Careers in Database: {num_careers}")
    print(f"2. Skill-Career Connections: {skill_career_connections}")
    print(f"3. Total Data Points Analyzed: {total_data_points} (Careers: {career_data_points}, User Profile: {total_assessment_points})")
    
    print("\n4. Career Category Counts:")
    for category, count in sorted(category_counts.items()):
        print(f"- {category}: {count}")
        
    if unassigned_careers:
        print("\nUnassigned Careers:")
        for title in unassigned_careers:
            print(f"- {title}")

if __name__ == "__main__":
    calculate_all_stats()