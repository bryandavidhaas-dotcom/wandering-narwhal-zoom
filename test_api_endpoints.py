#!/usr/bin/env python3
"""
Test script to verify API endpoints are working correctly
Tests the complete flow: Authentication -> Assessment -> Recommendations
"""

import requests
import json

BASE_URL = "http://localhost:8002/api/v1"

def test_authentication():
    """Test authentication with existing user"""
    print("🔐 Testing Authentication...")
    
    login_data = {
        "username": "bryandavidhaas@gmail.com",
        "password": "testpassword123"
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/auth/login",
            data=login_data,
            headers={"Content-Type": "application/x-www-form-urlencoded"},
            timeout=10
        )
        
        if response.status_code == 200:
            data = response.json()
            token = data.get("access_token")
            print(f"✅ Authentication successful! Token: {token[:20]}...")
            return token
        else:
            print(f"❌ Authentication failed: {response.status_code} - {response.text}")
            return None
            
    except Exception as e:
        print(f"❌ Authentication error: {e}")
        return None

def test_assessment_submission(token):
    """Test assessment submission"""
    print("\n📝 Testing Assessment Submission...")
    
    assessment_data = {
        "age": "45",
        "location": "Petaluma, CA",
        "educationLevel": "bachelors",
        "currentSituation": "employed",
        "currentRole": "Senior Product Manager",
        "experience": "20+",
        "certifications": ["PMP (Project Management)", "Google Analytics"],
        "technicalSkills": ["Microsoft Office Suite", "Data Analysis", "Project Management"],
        "softSkills": ["Leadership", "Communication", "Problem Solving"],
        "workingWithData": 5,
        "workingWithPeople": 5,
        "creativeTasks": 4,
        "problemSolving": 5,
        "leadership": 5,
        "physicalHandsOnWork": 2,
        "outdoorWork": 2,
        "mechanicalAptitude": 3,
        "interests": ["Technology & Software", "Business & Entrepreneurship", "Data & Analytics"],
        "industries": ["Technology & Software", "Financial Services", "Consulting & Professional Services"],
        "careerGoals": "Looking to transition into a more strategic role with focus on data-driven decision making",
        "workLifeBalance": "important",
        "salaryExpectations": "150000-250000"
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/assessment/submit-assessment",
            json=assessment_data,
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {token}"
            },
            timeout=10
        )
        
        if response.status_code == 200:
            print("✅ Assessment submitted successfully!")
            return True
        else:
            print(f"❌ Assessment submission failed: {response.status_code} - {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Assessment submission error: {e}")
        return False

def test_recommendation_generation(token):
    """Test recommendation generation"""
    print("\n🎯 Testing Recommendation Generation...")
    
    try:
        response = requests.post(
            f"{BASE_URL}/recommendation/generate-recommendations",
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {token}"
            },
            timeout=15
        )
        
        if response.status_code == 200:
            data = response.json()
            recommendations = data.get("recommendations", [])
            print(f"✅ Recommendations generated successfully! Count: {len(recommendations)}")
            if recommendations:
                print(f"   First recommendation: {recommendations[0].get('job_title', 'N/A')}")
            return True
        else:
            print(f"❌ Recommendation generation failed: {response.status_code} - {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Recommendation generation error: {e}")
        return False

def test_recommendation_retrieval(token):
    """Test recommendation retrieval"""
    print("\n📊 Testing Recommendation Retrieval...")
    
    try:
        response = requests.get(
            f"{BASE_URL}/recommendation/get-latest-recommendations",
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {token}"
            },
            timeout=10
        )
        
        if response.status_code == 200:
            data = response.json()
            recommendations = data.get("recommendations", [])
            print(f"✅ Recommendations retrieved successfully! Count: {len(recommendations)}")
            return True
        else:
            print(f"❌ Recommendation retrieval failed: {response.status_code} - {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Recommendation retrieval error: {e}")
        return False

def main():
    """Run all API endpoint tests"""
    print("🚀 API ENDPOINT TESTING")
    print("=" * 50)
    
    # Test 1: Authentication
    token = test_authentication()
    if not token:
        print("\n❌ Cannot proceed without authentication")
        return
    
    # Test 2: Assessment Submission
    assessment_success = test_assessment_submission(token)
    
    # Test 3: Recommendation Generation
    recommendation_success = test_recommendation_generation(token)
    
    # Test 4: Recommendation Retrieval
    retrieval_success = test_recommendation_retrieval(token)
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 TEST SUMMARY")
    print("=" * 50)
    print(f"Authentication: {'✅ PASS' if token else '❌ FAIL'}")
    print(f"Assessment Submission: {'✅ PASS' if assessment_success else '❌ FAIL'}")
    print(f"Recommendation Generation: {'✅ PASS' if recommendation_success else '❌ FAIL'}")
    print(f"Recommendation Retrieval: {'✅ PASS' if retrieval_success else '❌ FAIL'}")
    
    all_passed = token and assessment_success and recommendation_success and retrieval_success
    print(f"\n🎯 OVERALL RESULT: {'✅ ALL TESTS PASSED' if all_passed else '❌ SOME TESTS FAILED'}")
    
    if all_passed:
        print("\n🎉 All 404 API endpoint issues have been fixed!")
        print("The complete flow works: Authentication → Assessment → Recommendations → Retrieval")

if __name__ == "__main__":
    main()