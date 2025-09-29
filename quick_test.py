#!/usr/bin/env python3
"""Quick test to verify backend endpoints are working."""

import requests
import json

def test_endpoint(url, method="GET", data=None):
    try:
        if method == "GET":
            response = requests.get(url, timeout=5)
        else:
            response = requests.post(url, json=data, timeout=5)
        
        print(f"{method} {url}: {response.status_code}")
        if response.status_code == 200:
            result = response.json()
            if isinstance(result, dict):
                print(f"  Keys: {list(result.keys())}")
                if 'total_count' in result:
                    print(f"  Total count: {result['total_count']}")
            print("  ✅ SUCCESS")
        else:
            print(f"  ❌ ERROR: {response.text}")
        return response.status_code == 200
    except Exception as e:
        print(f"{method} {url}: ❌ FAILED - {e}")
        return False

if __name__ == "__main__":
    base_url = "http://localhost:8000"
    
    print("Quick Backend API Test")
    print("=" * 30)
    
    # Test endpoints
    tests = [
        ("GET", f"{base_url}/health"),
        ("GET", f"{base_url}/"),
        ("GET", f"{base_url}/careers"),
        ("GET", f"{base_url}/skills"),
        ("POST", f"{base_url}/recommendations", {"user_profile": {}, "limit": 3})
    ]
    
    results = []
    for method, url, *data in tests:
        test_data = data[0] if data else None
        success = test_endpoint(url, method, test_data)
        results.append(success)
        print()
    
    passed = sum(results)
    total = len(results)
    print(f"Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 ALL TESTS PASSED - Backend is working!")
    else:
        print("⚠️  Some tests failed - Backend needs fixes")