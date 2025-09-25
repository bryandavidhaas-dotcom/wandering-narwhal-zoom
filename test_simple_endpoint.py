#!/usr/bin/env python3

import requests
import json

def test_simple_endpoint():
    """Test the /api/recommendations endpoint with a simple request"""
    
    url = "http://localhost:8001/api/recommendations"
    
    # Simple test data
    test_data = {
        "age": "45",
        "currentRole": "Executive",
        "experience": "26 years",
        "salaryExpectations": "$150,000 - $250,000",
        "explorationLevel": 3
    }
    
    print(f"Testing {url}")
    print(f"Data: {json.dumps(test_data, indent=2)}")
    
    try:
        response = requests.post(url, json=test_data, timeout=10)
        print(f"\nResponse Status: {response.status_code}")
        
        if response.status_code == 200:
            recommendations = response.json()
            print(f"✅ SUCCESS! Got {len(recommendations)} recommendations")
            
            # Check for problematic careers
            for i, career in enumerate(recommendations[:3]):
                title = career.get('title', 'Unknown')
                salary_min = career.get('salaryMin', career.get('minSalary', 0))
                salary_max = career.get('salaryMax', career.get('maxSalary', 0))
                print(f"  {i+1}. {title}: ${salary_min:,}-${salary_max:,}")
                
                if 'Medical Assistant' in title or 'Delivery Driver' in title:
                    print(f"    ❌ PROBLEM: Found inappropriate career!")
                    
        else:
            print(f"❌ Error: {response.status_code}")
            print(f"Response: {response.text}")
            
    except requests.exceptions.ConnectionError:
        print("❌ ERROR: Cannot connect to server")
    except Exception as e:
        print(f"❌ ERROR: {e}")

if __name__ == "__main__":
    test_simple_endpoint()