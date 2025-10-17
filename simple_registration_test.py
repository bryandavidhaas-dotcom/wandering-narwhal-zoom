#!/usr/bin/env python3
"""
Simple test to verify registration endpoint returns JWT tokens
"""

import requests
import json
import uuid

def test_registration():
    """Test registration endpoint"""
    print("🧪 Testing Registration Endpoint")
    print("=" * 40)
    
    # Generate unique test user
    test_email = f"test_{uuid.uuid4().hex[:8]}@example.com"
    test_password = "TestPassword123!"
    
    print(f"📧 Email: {test_email}")
    print(f"🔐 Password: {test_password}")
    
    # Test registration
    url = "http://localhost:8002/api/v1/auth/register"
    data = {
        "email": test_email,
        "password": test_password
    }
    
    try:
        response = requests.post(url, json=data)
        print(f"\n📡 Status Code: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"📄 Response: {json.dumps(result, indent=2)}")
            
            if "access_token" in result and "token_type" in result:
                print("✅ SUCCESS: Registration returns JWT tokens!")
                print(f"🔑 Token Type: {result['token_type']}")
                print(f"🎫 Token Length: {len(result['access_token'])} characters")
                return True
            else:
                print("❌ FAIL: No JWT tokens in response")
                return False
        else:
            print(f"❌ FAIL: HTTP {response.status_code}")
            print(f"Error: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ FAIL: {e}")
        return False

if __name__ == "__main__":
    success = test_registration()
    print("\n" + "=" * 40)
    if success:
        print("🎉 Registration flow is working correctly!")
    else:
        print("💥 Registration flow has issues!")