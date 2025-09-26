#!/usr/bin/env python3
"""
Test if the simple_server.py is actually running and responding
"""

import requests
import json

def test_simple_server():
    """Test the simple_server endpoints directly"""
    
    print("🔍 Testing simple_server.py endpoints")
    print("=" * 50)
    
    # Test root endpoint
    try:
        response = requests.get("http://localhost:8000/", timeout=5)
        print(f"GET /: {response.status_code}")
        if response.status_code == 200:
            print(f"Response: {response.json()}")
        else:
            print(f"Error: {response.text}")
    except Exception as e:
        print(f"GET /: Error - {e}")
    
    # Test health endpoint
    try:
        response = requests.get("http://localhost:8000/health", timeout=5)
        print(f"GET /health: {response.status_code}")
        if response.status_code == 200:
            print(f"Response: {response.json()}")
        else:
            print(f"Error: {response.text}")
    except Exception as e:
        print(f"GET /health: Error - {e}")
    
    # Test the enhanced API endpoint with minimal data
    test_data = {
        "salaryExpectations": "150000-250000",
        "experience": "20+ years",
        "explorationLevel": 3,
        "currentRole": "SVP Product Management"
    }
    
    try:
        response = requests.post(
            "http://localhost:8000/api/recommendations",
            json=test_data,
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        print(f"POST /api/recommendations: {response.status_code}")
        if response.status_code == 200:
            recommendations = response.json()
            print(f"✅ SUCCESS: Got {len(recommendations)} recommendations")
            
            # Check for Medical Assistant specifically
            medical_assistant_found = False
            for rec in recommendations:
                title = rec.get("title", "").lower()
                if "medical assistant" in title:
                    medical_assistant_found = True
                    salary_min = rec.get("salaryMin", rec.get("minSalary", 0))
                    salary_max = rec.get("salaryMax", rec.get("maxSalary", 0))
                    print(f"🚨 FOUND MEDICAL ASSISTANT: ${salary_min:,}-${salary_max:,}")
                    break
            
            if not medical_assistant_found:
                print("✅ Medical Assistant NOT found - filtering is working!")
            
            return True
        else:
            print(f"Error: {response.text}")
            return False
    except Exception as e:
        print(f"POST /api/recommendations: Error - {e}")
        return False

if __name__ == "__main__":
    success = test_simple_server()
    if success:
        print("\n🎉 simple_server.py is running and responding!")
    else:
        print("\n❌ simple_server.py is not working properly")