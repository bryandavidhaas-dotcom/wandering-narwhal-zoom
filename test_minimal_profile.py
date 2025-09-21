#!/usr/bin/env python3
"""
Test script to verify that users with minimal profiles get appropriate recommendations
"""

import requests
import json

def test_minimal_profile_user():
    """Test that a user with minimal profile gets reasonable recommendations"""
    
    # Minimal user profile (similar to test11@example.com)
    payload = {
        "experience": "1-2",
        "technicalSkills": [],
        "softSkills": [],
        "workingWithData": 3,
        "workingWithPeople": 3,
        "creativeTasks": 3,
        "problemSolving": 3,
        "leadership": 3,
        "interests": [],
        "industries": [],
        "workEnvironment": "hybrid",
        "salaryExpectations": "50k-70k",
        "careerGoals": "",
        "age": "22-25",
        "location": "United States",
        "educationLevel": "bachelors",
        "certifications": [],
        "currentSituation": "employed",
        "currentRole": "",
        "resumeText": "",
        "linkedinProfile": "",
        "workLifeBalance": "important",
        "explorationLevel": 3  # Adventure Zone
    }
    
    try:
        print("🧪 Testing Minimal Profile User (Adventure Zone)...")
        print("📤 Sending request to backend...")
        
        response = requests.post(
            "http://localhost:8000/api/recommendations",
            json=payload,
            headers={"Content-Type": "application/json"},
            timeout=30
        )
        
        if response.status_code == 200:
            recommendations = response.json()
            print(f"✅ SUCCESS: Got {len(recommendations)} recommendations")
            
            # Analyze recommendations
            appropriate_careers = []
            questionable_careers = []
            
            for career in recommendations:
                title = career.get('title', '').lower()
                score = career.get('relevanceScore', 0)
                
                # Check for inappropriate recommendations
                if any(keyword in title for keyword in [
                    'medical equipment technician', 'clinical research', 'plumber', 
                    'electrician', 'welder', 'mechanic', 'hvac technician',
                    'carpenter', 'sheet metal', 'boilermaker'
                ]):
                    questionable_careers.append(f"{career['title']} (score: {score})")
                else:
                    appropriate_careers.append(f"{career['title']} (score: {score})")
            
            print(f"\n📊 ANALYSIS:")
            print(f"✅ Appropriate careers: {len(appropriate_careers)}")
            for career in appropriate_careers[:5]:  # Show top 5
                print(f"   ✅ {career}")
            
            if questionable_careers:
                print(f"\n⚠️ Questionable careers for minimal profile: {len(questionable_careers)}")
                for career in questionable_careers:
                    print(f"   ❓ {career}")
                return False
            else:
                print("✅ EXCELLENT: No questionable trades/technical careers for minimal profile")
                return True
                
        else:
            print(f"❌ API Error: {response.status_code} - {response.text}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Connection Error: {e}")
        return False

if __name__ == "__main__":
    print("🚀 MINIMAL PROFILE RECOMMENDATION TEST")
    print("=" * 50)
    
    success = test_minimal_profile_user()
    
    print("\n" + "=" * 50)
    if success:
        print("✅ MINIMAL PROFILE TEST PASSED!")
        print("✅ Users with minimal profiles get appropriate recommendations")
    else:
        print("❌ MINIMAL PROFILE TEST FAILED!")
        print("❌ Users with minimal profiles are still getting inappropriate recommendations")