#!/usr/bin/env python3
"""
Test script to make an API call to the backend and check if CRNA is still recommended.
"""

import requests
import json

def test_bryan_recommendations():
    """Test that Bryan (Product Manager) no longer gets CRNA recommendations"""
    
    # Bryan's profile data
    bryan_data = {
        "experience": "20+",
        "salaryExpectations": "150k-250k",
        "explorationLevel": 3,
        "resumeText": "Senior Product Manager with 20+ years experience in product strategy, roadmap development, and team leadership. Led multiple product launches and managed cross-functional teams.",
        "technicalSkills": ["Product Management", "Analytics", "Roadmapping"],
        "currentRole": "Senior Product Manager",
        "educationLevel": "Bachelor's in Business",
        "certifications": ["PMP", "Agile Certified"]
    }
    
    print("🧪 Testing API Call for Bryan (Product Manager)")
    print("=" * 50)
    
    try:
        # Make API call
        response = requests.post(
            "http://localhost:8000/api/recommendations",
            headers={"Content-Type": "application/json"},
            json=bryan_data,
            timeout=30
        )
        
        if response.status_code == 200:
            recommendations = response.json()
            print(f"✅ API call successful - received {len(recommendations)} recommendations")
            
            # Check if CRNA is in the recommendations
            crna_found = False
            for rec in recommendations:
                title = rec.get("title", "").lower()
                if "nurse anesthetist" in title or "crna" in title:
                    crna_found = True
                    print(f"🚫 PROBLEM: Found CRNA recommendation: {rec.get('title', '')}")
                    break
            
            if not crna_found:
                print("✅ SUCCESS: No CRNA recommendation found for Product Manager!")
                print("🛡️  Safety guardrails are working correctly!")
            
            # Show first few recommendations
            print(f"\n📋 First 5 recommendations for Bryan:")
            for i, rec in enumerate(recommendations[:5]):
                title = rec.get("title", "Unknown")
                zone = rec.get("zone", "unknown")
                score = rec.get("relevanceScore", 0)
                print(f"  {i+1}. {title} ({zone} zone, score: {score})")
                
        else:
            print(f"❌ API call failed with status {response.status_code}")
            print(f"Response: {response.text}")
            
    except requests.exceptions.RequestException as e:
        print(f"❌ API call failed with error: {e}")
        print("Make sure the backend server is running on http://localhost:8000")

if __name__ == "__main__":
    test_bryan_recommendations()