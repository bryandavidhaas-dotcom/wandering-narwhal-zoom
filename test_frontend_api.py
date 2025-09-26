#!/usr/bin/env python3
"""
Test what API the frontend is actually calling
"""

import requests
import json

def test_frontend_api():
    """Test different possible API endpoints"""
    
    print("🔍 Testing Frontend API Endpoints")
    print("=" * 50)
    
    # Test different possible ports and endpoints
    test_configs = [
        ("http://localhost:8000", "/api/recommendations"),
        ("http://localhost:3000", "/api/recommendations"),
        ("http://localhost:5173", "/api/recommendations"),
        ("http://localhost:8000", "/recommendations"),
        ("http://localhost:3000", "/recommendations"),
    ]
    
    bryan_profile = {
        "salaryExpectations": "150000-250000",
        "experience": "20+ years",
        "explorationLevel": 3,
        "currentRole": "SVP, Product Management"
    }
    
    for base_url, endpoint in test_configs:
        try:
            full_url = f"{base_url}{endpoint}"
            print(f"\n🧪 Testing: {full_url}")
            
            response = requests.post(
                full_url,
                json=bryan_profile,
                headers={"Content-Type": "application/json"},
                timeout=5
            )
            
            print(f"Status: {response.status_code}")
            
            if response.status_code == 200:
                recommendations = response.json()
                if isinstance(recommendations, list):
                    print(f"✅ SUCCESS: Got {len(recommendations)} recommendations")
                    
                    # Check for problematic careers
                    problematic = []
                    for rec in recommendations:
                        title = rec.get("title", "").lower()
                        if ("medical assistant" in title or 
                            "delivery driver" in title):
                            problematic.append(rec)
                    
                    if problematic:
                        print(f"🚨 FOUND PROBLEMATIC CAREERS:")
                        for rec in problematic:
                            salary_min = rec.get("salaryMin", rec.get("minSalary", 0))
                            salary_max = rec.get("salaryMax", rec.get("maxSalary", 0))
                            print(f"   - {rec['title']}: ${salary_min:,}-${salary_max:,}")
                    else:
                        print("✅ No problematic careers found")
                    
                    # Show first few recommendations
                    print("📋 First 3 recommendations:")
                    for i, rec in enumerate(recommendations[:3], 1):
                        title = rec.get("title", "")
                        salary_min = rec.get("salaryMin", rec.get("minSalary", 0))
                        salary_max = rec.get("salaryMax", rec.get("maxSalary", 0))
                        print(f"   {i}. {title}: ${salary_min:,}-${salary_max:,}")
                    
                    return full_url, recommendations
                else:
                    print(f"Response: {recommendations}")
            else:
                print(f"Error: {response.text}")
                
        except requests.exceptions.ConnectionError:
            print(f"❌ Connection refused")
        except requests.exceptions.Timeout:
            print(f"❌ Timeout")
        except Exception as e:
            print(f"❌ Error: {e}")
    
    return None, None

if __name__ == "__main__":
    working_url, recommendations = test_frontend_api()
    
    if working_url:
        print(f"\n🎉 FOUND WORKING API: {working_url}")
    else:
        print(f"\n❌ NO WORKING API FOUND")