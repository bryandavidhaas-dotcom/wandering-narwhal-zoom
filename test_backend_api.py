#!/usr/bin/env python3
"""
Simple test script to verify the backend API is working correctly.
"""

import requests
import json
import time

# Wait for server to be ready
time.sleep(2)

BASE_URL = "http://localhost:8000"

def test_health_endpoint():
    """Test the health check endpoint."""
    try:
        response = requests.get(f"{BASE_URL}/health")
        print(f"Health check: {response.status_code}")
        if response.status_code == 200:
            print(f"Response: {response.json()}")
            return True
        else:
            print(f"Error: {response.text}")
            return False
    except Exception as e:
        print(f"Health check failed: {e}")
        return False

def test_root_endpoint():
    """Test the root endpoint."""
    try:
        response = requests.get(f"{BASE_URL}/")
        print(f"Root endpoint: {response.status_code}")
        if response.status_code == 200:
            print(f"Response: {response.json()}")
            return True
        else:
            print(f"Error: {response.text}")
            return False
    except Exception as e:
        print(f"Root endpoint failed: {e}")
        return False

def test_careers_endpoint():
    """Test the careers endpoint."""
    try:
        response = requests.get(f"{BASE_URL}/careers")
        print(f"Careers endpoint: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"Found {data.get('total_count', 0)} careers")
            return True
        else:
            print(f"Error: {response.text}")
            return False
    except Exception as e:
        print(f"Careers endpoint failed: {e}")
        return False

def test_recommendations_endpoint():
    """Test the recommendations endpoint."""
    try:
        test_request = {
            "user_profile": {
                "skills": ["Python", "Data Analysis"],
                "interests": ["Technology", "Problem Solving"]
            },
            "limit": 5
        }
        
        response = requests.post(f"{BASE_URL}/recommendations", json=test_request)
        print(f"Recommendations endpoint: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"Generated {data.get('total_count', 0)} recommendations")
            return True
        else:
            print(f"Error: {response.text}")
            return False
    except Exception as e:
        print(f"Recommendations endpoint failed: {e}")
        return False

if __name__ == "__main__":
    print("Testing Backend API Endpoints...")
    print("=" * 50)
    
    tests = [
        ("Health Check", test_health_endpoint),
        ("Root Endpoint", test_root_endpoint),
        ("Careers Endpoint", test_careers_endpoint),
        ("Recommendations Endpoint", test_recommendations_endpoint)
    ]
    
    results = []
    for test_name, test_func in tests:
        print(f"\n{test_name}:")
        print("-" * 30)
        success = test_func()
        results.append((test_name, success))
    
    print("\n" + "=" * 50)
    print("TEST RESULTS:")
    for test_name, success in results:
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{test_name}: {status}")
    
    all_passed = all(success for _, success in results)
    print(f"\nOverall: {'✅ ALL TESTS PASSED' if all_passed else '❌ SOME TESTS FAILED'}")