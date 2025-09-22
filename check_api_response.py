#!/usr/bin/env python3
"""
Quick script to check the API response format.
"""

import requests
import json

def check_api_response():
    """Check what the API actually returns."""
    
    # Simple test profile
    test_profile = {
        "user_id": "test_user",
        "personal_info": {
            "age": 26,
            "location": "Seattle, WA",
            "salary_expectations": {
                "min": 70000,
                "max": 100000,
                "currency": "USD"
            }
        },
        "skills": [
            {
                "name": "Python",
                "level": "intermediate",
                "years_experience": 2.0
            }
        ],
        "user_interests": ["Technology", "Data Analysis"]
    }
    
    try:
        response = requests.post(
            "http://localhost:8000/recommendations",
            json=test_profile,
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        
        print(f"Status Code: {response.status_code}")
        print(f"Response Type: {type(response.json())}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"Response Keys: {list(data.keys()) if isinstance(data, dict) else 'Not a dict'}")
            print(f"Response Structure:")
            print(json.dumps(data, indent=2)[:1000] + "..." if len(str(data)) > 1000 else json.dumps(data, indent=2))
        else:
            print(f"Error Response: {response.text}")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    check_api_response()