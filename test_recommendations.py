import requests
import json

# Test the recommendation API with a product manager profile
# This simulates the profile we configured in the browser

payload = {
    "profile": {
        "currentRole": "Product Manager",
        "experience": "3-5",
        "location": "San Francisco, CA",
        "education": "Bachelor's Degree",
        "workSituation": "Currently Employed"
    },
    "skills": [
        "Excel/Spreadsheets",
        "PowerPoint", 
        "Communication",
        "Problem Solving",
        "Critical Thinking",
        "Leadership",
        "Project Management"
    ],
    "interests": [
        "Technology & Software",
        "Business & Entrepreneurship", 
        "Sales & Marketing"
    ],
    "industries": [
        "Technology & Software",
        "Financial Services"
    ],
    "workPreferences": {
        "dataAnalytics": 4,
        "peopleTeams": 4,
        "creative": 4,
        "problemSolving": 4,
        "leadership": 5,
        "physicalHandsOnWork": 2,  # Prefer desk work
        "outdoorWork": 2,          # Indoor only
        "mechanicalAptitude": 2    # Not technical
    },
    "careerGoals": "I want to lead product strategy and development, working with cross-functional teams to build innovative solutions that solve customer problems and drive business growth. I'm interested in product management roles where I can combine strategic thinking with hands-on execution.",
    "salaryExpectations": "150k-250k",
    "workLifeBalance": "important"
}

try:
    print("🚀 Testing recommendation API with Product Manager profile...")
    print("📊 Key profile details:")
    print(f"   - Current Role: {payload['profile']['currentRole']}")
    print(f"   - Experience: {payload['profile']['experience']} years")
    print(f"   - Physical Work Preference: {payload['workPreferences']['physicalHandsOnWork']} (Prefer desk work)")
    print(f"   - Outdoor Work Preference: {payload['workPreferences']['outdoorWork']} (Indoor only)")
    print(f"   - Mechanical Aptitude: {payload['workPreferences']['mechanicalAptitude']} (Not technical)")
    print(f"   - Salary Range: {payload['salaryExpectations']}")
    print()
    
    response = requests.post(
        "http://localhost:8000/api/recommendations",
        json=payload,
        headers={"Content-Type": "application/json"}
    )
    
    print(f"📡 Response Status: {response.status_code}")
    
    if response.status_code == 200:
        recommendations = response.json()
        print(f"✅ Successfully received {len(recommendations)} recommendations!")
        print()
        
        # Look for Head of Product specifically
        head_of_product_found = False
        product_roles = []
        
        for i, rec in enumerate(recommendations, 1):
            career_title = rec.get('title', 'Unknown')
            career_type = rec.get('careerType', 'unknown')
            
            print(f"{i}. {career_title} (careerType: {career_type})")
            
            if 'head-of-product' in career_type.lower() or 'head of product' in career_title.lower():
                head_of_product_found = True
                print(f"   🎯 FOUND: Head of Product recommendation!")
                
            if 'product' in career_title.lower():
                product_roles.append(career_title)
        
        print()
        if head_of_product_found:
            print("🎉 SUCCESS: Head of Product is now being recommended!")
            print("✅ The frontend template fix and backend classification fix are working!")
        else:
            print("⚠️  Head of Product not found in recommendations")
            if product_roles:
                print(f"📋 Other product roles found: {', '.join(product_roles)}")
            else:
                print("❌ No product management roles found at all")
                
    else:
        print(f"❌ API Error: {response.status_code}")
        print(f"Response: {response.text}")
        
except requests.exceptions.ConnectionError:
    print("❌ Connection Error: Could not connect to the backend server")
    print("Make sure the backend is running on http://localhost:8000")
except Exception as e:
    print(f"❌ Error: {e}")