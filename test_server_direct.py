#!/usr/bin/env python3

import requests
import json

def test_server_endpoints():
    """Test both server endpoints to see which one works"""
    
    # Test 1: Check if server is running
    try:
        response = requests.get("http://localhost:8001/", timeout=5)
        print(f"✅ Server is running on port 8001: {response.status_code}")
        print(f"Response: {response.json()}")
    except Exception as e:
        print(f"❌ Server not responding on port 8001: {e}")
        return
    
    # Test 2: Check health endpoint
    try:
        response = requests.get("http://localhost:8001/health", timeout=5)
        print(f"✅ Health check: {response.status_code}")
        print(f"Health: {response.json()}")
    except Exception as e:
        print(f"❌ Health check failed: {e}")
    
    # Test 3: Try the /api/recommendations endpoint (should work with DirectRecommendationRequest)
    bryan_profile_direct = {
        "age": "45",
        "location": "United States",
        "educationLevel": "Bachelor's Degree",
        "currentRole": "Executive/Senior Management",
        "experience": "26 years",
        "salaryExpectations": "$150,000 - $250,000",
        "explorationLevel": 3
    }
    
    print(f"\n🧪 Testing /api/recommendations endpoint...")
    try:
        response = requests.post("http://localhost:8001/api/recommendations", 
                               json=bryan_profile_direct, timeout=10)
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            recommendations = response.json()
            print(f"✅ SUCCESS! Got {len(recommendations)} recommendations")
            
            # Check for problematic careers
            problematic = []
            for career in recommendations:
                title = career.get('title', 'Unknown')
                if 'Medical Assistant' in title or 'Delivery Driver' in title:
                    problematic.append(title)
            
            if problematic:
                print(f"❌ FOUND PROBLEMATIC CAREERS: {problematic}")
            else:
                print("✅ No problematic careers found!")
                
            # Show top 3
            print("\nTop 3 recommendations:")
            for i, career in enumerate(recommendations[:3]):
                title = career.get('title', 'Unknown')
                salary_min = career.get('salaryMin', career.get('minSalary', 0))
                salary_max = career.get('salaryMax', career.get('maxSalary', 0))
                score = career.get('relevanceScore', career.get('score', 0))
                print(f"  {i+1}. {title}: ${salary_min:,}-${salary_max:,} (score: {score})")
        else:
            print(f"❌ Error: {response.status_code}")
            print(f"Response: {response.text[:500]}")
            
    except Exception as e:
        print(f"❌ /api/recommendations failed: {e}")
    
    # Test 4: Try the /recommendations endpoint (should work with RecommendationRequest)
    bryan_profile_wrapped = {
        "user_profile": bryan_profile_direct,
        "limit": 10
    }
    
    print(f"\n🧪 Testing /recommendations endpoint...")
    try:
        response = requests.post("http://localhost:8001/recommendations", 
                               json=bryan_profile_wrapped, timeout=10)
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            recommendations = result.get('recommendations', [])
            print(f"✅ SUCCESS! Got {len(recommendations)} recommendations")
            
            # Check for problematic careers
            problematic = []
            for career in recommendations:
                title = career.get('title', 'Unknown')
                if 'Medical Assistant' in title or 'Delivery Driver' in title:
                    problematic.append(title)
            
            if problematic:
                print(f"❌ FOUND PROBLEMATIC CAREERS: {problematic}")
            else:
                print("✅ No problematic careers found!")
                
        else:
            print(f"❌ Error: {response.status_code}")
            print(f"Response: {response.text[:500]}")
            
    except Exception as e:
        print(f"❌ /recommendations failed: {e}")

if __name__ == "__main__":
    test_server_endpoints()