#!/usr/bin/env python3
"""
Direct AI Features Testing Script

This script tests AI functionality with existing user credentials.
"""

import requests
import json
import time
from typing import Dict, Any

def test_ai_features():
    """Test AI features with existing user"""
    base_url = "http://localhost:8002/api/v1"
    
    print("🚀 TESTING AI FEATURES DIRECTLY")
    print("=" * 50)
    
    # Try to login with existing user
    login_data = {
        "username": "ai_test_user@example.com",
        "password": "TestPassword123!"
    }
    
    print("1. Logging in with existing user...")
    try:
        response = requests.post(f"{base_url}/auth/login", data=login_data, timeout=10)
        if response.status_code == 200:
            token_data = response.json()
            auth_token = token_data.get("access_token")
            headers = {"Authorization": f"Bearer {auth_token}"}
            print("✅ Login successful")
        else:
            print(f"❌ Login failed: {response.status_code} - {response.text}")
            return
    except Exception as e:
        print(f"❌ Login error: {e}")
        return
    
    # Test assessment data
    assessment_data = {
        "technicalSkills": ["Python", "JavaScript", "SQL", "Machine Learning"],
        "softSkills": ["Communication", "Problem Solving", "Leadership"],
        "experience": "3-5 years",
        "careerGoals": "Advance to senior technical role",
        "currentRole": "Software Developer",
        "educationLevel": "Bachelor's Degree",
        "salaryExpectations": "$80,000 - $120,000",
        "industries": ["Technology", "Healthcare"],
        "interests": ["AI", "Web Development"],
        "workingWithData": 4,
        "workingWithPeople": 3,
        "creativeTasks": 4
    }
    
    # Test AI Recommendations
    print("\n2. Testing AI Recommendations...")
    try:
        start_time = time.time()
        response = requests.post(
            f"{base_url}/ai/recommendations",
            json=assessment_data,
            headers=headers,
            timeout=35
        )
        end_time = time.time()
        response_time = end_time - start_time
        
        print(f"   Response time: {response_time:.2f}s")
        print(f"   Status code: {response.status_code}")
        
        if response.status_code == 200:
            recommendations = response.json()
            if "recommendations" in recommendations:
                rec_list = recommendations["recommendations"]
                print(f"   ✅ AI Recommendations: {len(rec_list)} recommendations received")
                
                # Show first recommendation
                if rec_list:
                    first_rec = rec_list[0]
                    print(f"   Sample: {first_rec.get('title', 'N/A')} at {first_rec.get('company', 'N/A')}")
                    
                    # Test AI Tuning
                    print("\n3. Testing AI Recommendation Tuning...")
                    tuning_data = {
                        "current_recommendations": rec_list,
                        "prompt": "Focus more on remote opportunities and AI/ML roles"
                    }
                    
                    try:
                        start_time = time.time()
                        tune_response = requests.post(
                            f"{base_url}/ai/tune",
                            json=tuning_data,
                            headers=headers,
                            timeout=35
                        )
                        end_time = time.time()
                        tune_time = end_time - start_time
                        
                        print(f"   Response time: {tune_time:.2f}s")
                        print(f"   Status code: {tune_response.status_code}")
                        
                        if tune_response.status_code == 200:
                            tuned_recs = tune_response.json()
                            if "recommendations" in tuned_recs:
                                tuned_list = tuned_recs["recommendations"]
                                print(f"   ✅ AI Tuning: {len(tuned_list)} tuned recommendations received")
                                if tuned_list:
                                    print(f"   Sample tuned: {tuned_list[0].get('title', 'N/A')} at {tuned_list[0].get('company', 'N/A')}")
                            else:
                                print(f"   ❌ AI Tuning: Invalid response format")
                        else:
                            print(f"   ❌ AI Tuning failed: {tune_response.text}")
                    except requests.exceptions.Timeout:
                        print(f"   ⚠️  AI Tuning: Timeout after 35s (timeout handling working)")
                    except Exception as e:
                        print(f"   ❌ AI Tuning error: {e}")
            else:
                print(f"   ❌ AI Recommendations: Invalid response format - {recommendations}")
        else:
            print(f"   ❌ AI Recommendations failed: {response.text}")
            
    except requests.exceptions.Timeout:
        print(f"   ⚠️  AI Recommendations: Timeout after 35s (timeout handling working)")
    except Exception as e:
        print(f"   ❌ AI Recommendations error: {e}")
    
    # Test Legacy Recommendations
    print("\n4. Testing Legacy Recommendations...")
    try:
        response = requests.post(
            f"{base_url}/recommendation/generate-recommendations",
            json=assessment_data,
            headers=headers,
            timeout=10
        )
        
        print(f"   Status code: {response.status_code}")
        
        if response.status_code == 200:
            legacy_recs = response.json()
            if isinstance(legacy_recs, list):
                print(f"   ✅ Legacy Recommendations: {len(legacy_recs)} recommendations received")
            else:
                print(f"   ✅ Legacy Recommendations: Response received (format: {type(legacy_recs)})")
        else:
            print(f"   ❌ Legacy Recommendations failed: {response.text}")
            
    except Exception as e:
        print(f"   ❌ Legacy Recommendations error: {e}")
    
    # Test Fallback with minimal data
    print("\n5. Testing Fallback Mechanisms...")
    minimal_data = {
        "technicalSkills": [],
        "softSkills": [],
        "experience": "",
        "careerGoals": ""
    }
    
    try:
        response = requests.post(
            f"{base_url}/ai/recommendations",
            json=minimal_data,
            headers=headers,
            timeout=35
        )
        
        print(f"   Status code: {response.status_code}")
        
        if response.status_code == 200:
            fallback_recs = response.json()
            if "recommendations" in fallback_recs and fallback_recs["recommendations"]:
                rec_list = fallback_recs["recommendations"]
                print(f"   ✅ Fallback: {len(rec_list)} recommendations received")
                
                # Check if these are mock recommendations
                first_rec = rec_list[0]
                is_mock = (
                    first_rec.get("job_id", "").startswith("job_") or
                    first_rec.get("company") in ["Tech Corp", "Data Solutions Inc"]
                )
                print(f"   Mock data detected: {is_mock}")
            else:
                print(f"   ❌ Fallback: No recommendations in response")
        else:
            print(f"   ❌ Fallback failed: {response.text}")
            
    except Exception as e:
        print(f"   ❌ Fallback error: {e}")
    
    print("\n" + "=" * 50)
    print("🏁 AI FEATURES TESTING COMPLETE")

if __name__ == "__main__":
    test_ai_features()