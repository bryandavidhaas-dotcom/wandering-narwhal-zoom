#!/usr/bin/env python3

import requests
import json

def test_port_8002():
    """Test the enhanced server on port 8002"""
    
    url = "http://localhost:8002/api/recommendations"
    
    # Bryan's profile
    bryan_profile = {
        "age": "45",
        "currentRole": "Executive/Senior Management",
        "experience": "26 years",
        "resumeText": "Executive with 26 years of experience in technology, business, and finance. Leadership, strategy, and management expertise.",
        "technicalSkills": ["Leadership", "Strategy", "Management", "Technology"],
        "salaryExpectations": "$150,000 - $250,000",
        "explorationLevel": 3
    }
    
    print(f"Testing enhanced server on port 8002...")
    print(f"URL: {url}")
    print(f"Profile: Executive, 26 years, ${bryan_profile['salaryExpectations']}")
    
    try:
        response = requests.post(url, json=bryan_profile, timeout=10)
        print(f"\nResponse Status: {response.status_code}")
        
        if response.status_code == 200:
            recommendations = response.json()
            print(f"✅ SUCCESS! Got {len(recommendations)} recommendations")
            
            # Check for problematic careers
            problematic_careers = []
            for career in recommendations:
                title = career.get('title', 'Unknown')
                if 'Medical Assistant' in title or 'Delivery Driver' in title:
                    problematic_careers.append(title)
            
            if problematic_careers:
                print(f"\n❌ PROBLEM: Found {len(problematic_careers)} inappropriate careers:")
                for title in problematic_careers:
                    print(f"  - {title}")
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
            print(f"❌ Error: {response.status_code}")
            print(f"Response: {response.text}")
            
    except Exception as e:
        print(f"❌ ERROR: {e}")

if __name__ == "__main__":
    test_port_8002()