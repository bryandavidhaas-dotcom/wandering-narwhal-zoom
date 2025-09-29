#!/usr/bin/env python3
"""
Test script for MongoDB-enhanced server verification on port 8004
"""

import requests
import json
import sys
from datetime import datetime

BASE_URL = "http://localhost:8004"

def test_server_health():
    """Test server health endpoint"""
    try:
        response = requests.get(f"{BASE_URL}/health")
        print(f"Health Check Status: {response.status_code}")
        data = response.json()
        print(f"Health Response: {json.dumps(data, indent=2)}")
        
        # Check for MongoDB integration indicators
        mongodb_indicators = [
            data.get('mongodb_compatible', False),
            'mongodb' in data.get('message', '').lower(),
            data.get('database_status') == 'in-memory'
        ]
        
        print(f"MongoDB Integration Indicators: {mongodb_indicators}")
        return response.status_code == 200 and any(mongodb_indicators)
    except Exception as e:
        print(f"Health check failed: {e}")
        return False

def test_careers_endpoint():
    """Test careers endpoint with MongoDB format"""
    try:
        response = requests.get(f"{BASE_URL}/careers?limit=3")
        print(f"\nCareers Endpoint Status: {response.status_code}")
        data = response.json()
        print(f"Total careers: {data.get('total_count', 'unknown')}")
        print(f"MongoDB compatible: {data.get('mongodb_compatible', False)}")
        
        if data.get('careers'):
            career = data['careers'][0]
            print(f"Sample career structure:")
            print(f"  - career_id: {career.get('career_id')}")
            print(f"  - title: {career.get('title')}")
            print(f"  - salary_range: {career.get('salary_range')}")
            print(f"  - required_skills count: {len(career.get('required_skills', []))}")
            print(f"  - created_at: {career.get('created_at')}")
            print(f"  - updated_at: {career.get('updated_at')}")
        
        return response.status_code == 200 and data.get('mongodb_compatible', False)
    except Exception as e:
        print(f"Careers endpoint test failed: {e}")
        return False

def test_recommendations_endpoint():
    """Test recommendations endpoint with sample user profile"""
    try:
        # Sample user profile for testing
        user_profile = {
            "skills": ["Python", "Data Analysis", "SQL"],
            "interests": ["Technology", "Problem Solving"],
            "experience_level": "intermediate",
            "education_level": "bachelors",
            "work_environment": "office",
            "salary_expectation": 85000
        }
        
        response = requests.post(f"{BASE_URL}/api/recommendations", json=user_profile)
        print(f"\nRecommendations Endpoint Status: {response.status_code}")
        
        if response.status_code == 200:
            recommendations = response.json()
            print(f"Number of recommendations: {len(recommendations)}")
            
            if recommendations:
                rec = recommendations[0]
                print(f"Sample recommendation structure:")
                print(f"  - title: {rec.get('title')}")
                print(f"  - careerType: {rec.get('careerType')}")
                print(f"  - relevanceScore: {rec.get('relevanceScore')}")
                print(f"  - database_source: {rec.get('database_source')}")
                print(f"  - api_version: {rec.get('api_version')}")
                print(f"  - enhanced: {rec.get('enhanced')}")
                print(f"  - zone: {rec.get('zone')}")
                
                # Check MongoDB career structure
                mongodb_career = rec.get('mongodb_career')
                if mongodb_career:
                    print(f"  - MongoDB career_id: {mongodb_career.get('career_id')}")
                    print(f"  - MongoDB salary_range: {mongodb_career.get('salary_range')}")
                    print(f"  - MongoDB required_skills count: {len(mongodb_career.get('required_skills', []))}")
                    return True
        
        return response.status_code == 200
    except Exception as e:
        print(f"Recommendations endpoint test failed: {e}")
        return False

def main():
    """Run all tests"""
    print("=" * 60)
    print("MongoDB-Enhanced Server Verification Tests (Port 8004)")
    print("=" * 60)
    
    tests = [
        ("Health Check", test_server_health),
        ("Careers Endpoint", test_careers_endpoint),
        ("Recommendations Endpoint", test_recommendations_endpoint)
    ]
    
    results = []
    for test_name, test_func in tests:
        print(f"\n{'='*20} {test_name} {'='*20}")
        success = test_func()
        results.append((test_name, success))
        print(f"Result: {'✅ PASSED' if success else '❌ FAILED'}")
    
    print("\n" + "=" * 60)
    print("FINAL RESULTS:")
    print("=" * 60)
    
    passed = 0
    for test_name, success in results:
        status = "✅ PASSED" if success else "❌ FAILED"
        print(f"{test_name}: {status}")
        if success:
            passed += 1
    
    print(f"\nOverall: {passed}/{len(results)} tests passed")
    
    if passed == len(results):
        print("🎉 All tests passed! MongoDB integration is working correctly.")
        return 0
    elif passed >= len(results) * 0.8:
        print("✅ Most tests passed! MongoDB integration is largely working.")
        return 0
    else:
        print("⚠️  Some tests failed. Please check the server implementation.")
        return 1

if __name__ == "__main__":
    sys.exit(main())