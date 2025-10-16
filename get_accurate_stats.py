import json

def get_accurate_stats():
    """
    Calculates accurate statistics based on the career data.
    """
    try:
        with open('production_career_data.json', 'r') as f:
            data = json.load(f)
            career_data = data.get('careers', [])
    except FileNotFoundError:
        print("Error: production_career_data.json not found.")
        return
    except json.JSONDecodeError:
        print("Error: Could not decode JSON from production_career_data.json.")
        return

    num_careers = len(career_data)
    
    # Calculate data points analyzed
    # This will be the number of careers multiplied by the number of keys in each career object
    if num_careers > 0:
        # Get the number of keys from the first career object
        data_points_per_career = len(career_data.keys())
        num_data_points = num_careers * data_points_per_career
    else:
        num_data_points = 0

    # Calculate skill-career connections
    skill_career_connections = 0
    for career in career_data:
        skill_career_connections += len(career.get('requiredTechnicalSkills', []))
        skill_career_connections += len(career.get('requiredSoftSkills', []))

    print(f"Careers in Database: {num_careers}")
    print(f"Data Points Analyzed: {num_data_points}")
    print(f"Skill-Career Connections: {skill_career_connections}")

if __name__ == "__main__":
    get_accurate_stats()