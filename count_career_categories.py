import json
from collections import defaultdict

def categorize_careers():
    """
    Categorizes and counts careers from the production data.
    """
    try:
        with open('production_career_data.json', 'r') as f:
            data = json.load(f)
            careers = data.get('careers', [])
    except FileNotFoundError:
        print("Error: production_career_data.json not found.")
        return
    except json.JSONDecodeError:
        print("Error: Could not decode JSON from production_career_data.json.")
        return

    # This is a sample categorization based on keywords.
    # It might need refinement based on the actual data.
    categories = {
        "Technology & Engineering": ["engineer", "developer", "architect", "technician", "scientist"],
        "Healthcare & Medical": ["physician", "nurse", "therapist", "medical", "health"],
        "Skilled Trades & Construction": ["electrician", "plumber", "carpenter", "construction", "mechanic"],
        "Education & Training": ["teacher", "professor", "educator", "trainer", "counselor"],
        "Business & Finance": ["analyst", "manager", "accountant", "consultant", "director"],
        "Legal & Law": ["lawyer", "attorney", "legal", "paralegal"],
        "Creative & Arts": ["designer", "artist", "creative", "writer", "photographer"],
        "Public Service & Government": ["government", "public service", "officer", "federal"],
        "Hospitality & Service": ["hotel", "restaurant", "hospitality", "service"],
        "Manufacturing & Industrial": ["manufacturing", "industrial", "production", "plant"],
        "Agriculture & Environment": ["agriculture", "environmental", "farm", "conservation"]
    }

    category_counts = defaultdict(int)
    
    for career in careers:
        title = career.get('title', '').lower()
        career_type = career.get('careerType', '').lower()
        description = career.get('description', '').lower()
        
        assigned = False
        for category, keywords in categories.items():
            # Check against title, careerType, and description for better matching
            if any(keyword in title for keyword in keywords) or \
               any(keyword in career_type for keyword in keywords) or \
               any(keyword in description for keyword in keywords):
                category_counts[category] += 1
                assigned = True
                break # Assign to the first matching category
        
        if not assigned:
            category_counts["Other"] += 1

    print("Career Category Counts:")
    for category, count in category_counts.items():
        print(f"- {category}: {count}")
        
    print(f"\nTotal Careers: {len(careers)}")

if __name__ == "__main__":
    categorize_careers()