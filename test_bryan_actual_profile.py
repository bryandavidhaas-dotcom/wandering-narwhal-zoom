#!/usr/bin/env python3

import requests
import json

# Test the actual API endpoint with Bryan's profile
def test_bryan_profile():
    url = "http://localhost:8001/api/recommendations"
    
    # Bryan's actual profile - using the DirectRecommendationRequest format
    bryan_profile = {
        "age": "45",
        "location": "United States",
        "educationLevel": "Bachelor's Degree",
        "certifications": [],
        "currentSituation": "Employed",
        "currentRole": "Executive/Senior Management",
        "experience": "26 years",
        "resumeText": "Executive with 26 years of experience in technology, business, and finance. Leadership, strategy, and management expertise.",
        "linkedinProfile": "",
        "technicalSkills": ["Leadership", "Strategy", "Management", "Technology"],
        "softSkills": ["Leadership", "Communication", "Strategic Planning"],
        "workingWithData": 4,
        "workingWithPeople": 5,
        "creativeTasks": 3,
        "problemSolving": 5,
        "leadership": 5,
        "physicalHandsOnWork": 1,
        "outdoorWork": 1,
        "mechanicalAptitude": 2,
        "interests": ["Leadership", "Strategy", "Technology"],
        "industries": ["Technology", "Business", "Finance"],
        "workEnvironment": "Office",
        "careerGoals": "Executive Growth and Strategic Planning",
        "workLifeBalance": "Balanced",
        "salaryExpectations": "$150,000 - $250,000",
        "explorationLevel": 3
    }
    
    print("Testing Bryan's profile against enhanced server...")
    print(f"URL: {url}")
    print(f"Profile summary: {bryan_profile['experience']} experience, ${bryan_profile['salaryExpectations']} salary")
    
    try:
        response = requests.post(url, json=bryan_profile, timeout=10)
        print(f"\nResponse Status: {response.status_code}")
        
        if response.status_code == 200:
            recommendations = response.json()
            print(f"Number of recommendations: {len(recommendations)}")
            
            # Check for problematic careers
            problematic_careers = []
            for career in recommendations:
                career_title = career.get('title', 'Unknown')
                salary_range = career.get('salary_range', 'Unknown')
                
                if 'Medical Assistant' in career_title or 'Delivery Driver' in career_title:
                    problematic_careers.append({
                        'title': career_title,
                        'salary': salary_range,
                        'score': career.get('relevanceScore', 0)
                    })
            
            if problematic_careers:
                print(f"\n❌ PROBLEM: Found {len(problematic_careers)} inappropriate careers:")
                for career in problematic_careers:
                    print(f"  - {career['title']}: {career['salary']} (score: {career['score']})")
            else:
                print("\n✅ SUCCESS: No inappropriate careers found!")
            
            # Show top 5 recommendations
            print(f"\nTop 5 recommendations:")
            for i, career in enumerate(recommendations[:5]):
                title = career.get('title', 'Unknown')
                salary_min = career.get('salaryMin', career.get('minSalary', 0))
                salary_max = career.get('salaryMax', career.get('maxSalary', 0))
                score = career.get('relevanceScore', career.get('score', 0))
                zone = career.get('zone', 'unknown')
                
                print(f"  {i+1}. {title}: ${salary_min:,}-${salary_max:,} (score: {score}, zone: {zone})")
                
        else:
            print(f"Error: {response.status_code}")
            print(f"Response: {response.text}")
            
    except requests.exceptions.ConnectionError:
        print("❌ ERROR: Cannot connect to server on port 8001")
        print("Make sure the enhanced server is running!")
    except Exception as e:
        print(f"❌ ERROR: {e}")

if __name__ == "__main__":
    test_bryan_profile()