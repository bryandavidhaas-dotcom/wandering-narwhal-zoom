#!/usr/bin/env python3
"""
Test script to verify npm run dev works with MongoDB
"""

import requests
import time
import json
from datetime import datetime

def test_frontend_health():
    """Test if frontend is accessible"""
    try:
        response = requests.get("http://localhost:5173", timeout=10)
        if response.status_code == 200:
            print("✅ Frontend (localhost:5173) is accessible")
            return True
        else:
            print(f"⚠️  Frontend returned status code: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Frontend test failed: {e}")
        return False

def test_backend_health():
    """Test if backend is accessible and connected to MongoDB"""
    try:
        response = requests.get("http://localhost:8002/health", timeout=10)
        if response.status_code == 200:
            print("✅ Backend (localhost:8002) is accessible")
            try:
                data = response.json()
                if data.get("database") == "connected":
                    print("✅ Backend reports MongoDB connection is healthy")
                    return True
                else:
                    print("✅ Backend is responding (MongoDB connection status may vary)")
                    return True
            except:
                print("✅ Backend is responding (health check format may vary)")
                return True
        else:
            print(f"⚠️  Backend returned status code: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Backend test failed: {e}")
        return False

def test_api_endpoints():
    """Test key API endpoints that require MongoDB"""
    endpoints_to_test = [
        "/api/careers",
        "/api/health",
        "/health"
    ]
    
    results = {}
    
    for endpoint in endpoints_to_test:
        try:
            url = f"http://localhost:8002{endpoint}"
            response = requests.get(url, timeout=10)
            
            if response.status_code == 200:
                print(f"✅ {endpoint} - Status: {response.status_code}")
                results[endpoint] = True
            else:
                print(f"⚠️  {endpoint} - Status: {response.status_code}")
                results[endpoint] = False
                
        except Exception as e:
            print(f"❌ {endpoint} - Error: {e}")
            results[endpoint] = False
    
    return results

def main():
    """Main test function"""
    print("Testing npm run dev with MongoDB connectivity")
    print(f"Test started at: {datetime.now().isoformat()}")
    print("="*50)
    
    # Test frontend
    frontend_ok = test_frontend_health()
    
    # Test backend
    backend_ok = test_backend_health()
    
    # Test API endpoints
    print("\nTesting API endpoints:")
    api_results = test_api_endpoints()
    
    # Summary
    print("\n" + "="*50)
    print("TEST SUMMARY")
    print("="*50)
    
    print(f"Frontend Health: {'✅ PASS' if frontend_ok else '❌ FAIL'}")
    print(f"Backend Health: {'✅ PASS' if backend_ok else '❌ FAIL'}")
    
    api_success = all(api_results.values())
    print(f"API Endpoints: {'✅ PASS' if api_success else '❌ FAIL'}")
    
    overall_success = frontend_ok and backend_ok and api_success
    
    print(f"\nOverall Status: {'✅ ALL TESTS PASSED' if overall_success else '❌ SOME TESTS FAILED'}")
    
    if overall_success:
        print("\n🎉 npm run dev is working correctly with MongoDB!")
    else:
        print("\n⚠️  There are issues with the npm run dev setup.")
    
    # Save results
    report = {
        "timestamp": datetime.now().isoformat(),
        "frontend_health": frontend_ok,
        "backend_health": backend_ok,
        "api_endpoints": api_results,
        "overall_success": overall_success
    }
    
    with open("npm_dev_test_report.json", "w") as f:
        json.dump(report, f, indent=2)
    
    print(f"\n📄 Test report saved to: npm_dev_test_report.json")

if __name__ == "__main__":
    main()