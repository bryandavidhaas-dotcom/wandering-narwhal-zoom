#!/usr/bin/env python3
"""
Test script to verify the fixed registration flow that returns JWT tokens directly
"""

import requests
import json
import uuid
from datetime import datetime

# Configuration
BASE_URL = "http://localhost:8002"
REGISTER_URL = f"{BASE_URL}/api/v1/auth/register"
LOGIN_URL = f"{BASE_URL}/api/v1/auth/login"
ME_URL = f"{BASE_URL}/api/v1/auth/users/me"

def test_registration_flow():
    """Test the complete registration flow"""
    print("🧪 Testing Fixed Registration Flow")
    print("=" * 50)
    
    # Generate unique test user
    test_email = f"test_user_{uuid.uuid4().hex[:8]}@example.com"
    test_password = "TestPassword123!"
    
    print(f"📧 Test Email: {test_email}")
    print(f"🔐 Test Password: {test_password}")
    print()
    
    # Step 1: Test Registration (should return JWT tokens directly)
    print("1️⃣ Testing Registration Endpoint...")
    registration_data = {
        "email": test_email,
        "password": test_password
    }
    
    try:
        response = requests.post(
            REGISTER_URL,
            json=registration_data,
            headers={"Content-Type": "application/json"}
        )
        
        print(f"   Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"   Response: {json.dumps(data, indent=2)}")
            
            # Check if response contains JWT tokens
            if "access_token" in data and "token_type" in data:
                print("   ✅ Registration successful - JWT tokens returned!")
                access_token = data["access_token"]
                token_type = data["token_type"]
                
                # Step 2: Test that the token works for authenticated requests
                print("\n2️⃣ Testing Token Authentication...")
                headers = {"Authorization": f"{token_type} {access_token}"}
                
                me_response = requests.get(ME_URL, headers=headers)
                print(f"   Status Code: {me_response.status_code}")
                
                if me_response.status_code == 200:
                    user_data = me_response.json()
                    print(f"   User Data: {json.dumps(user_data, indent=2)}")
                    print("   ✅ Token authentication successful!")
                    
                    # Verify the user email matches
                    if user_data.get("email") == test_email:
                        print("   ✅ User email matches registration!")
                        return True
                    else:
                        print("   ❌ User email mismatch!")
                        return False
                else:
                    print(f"   ❌ Token authentication failed: {me_response.text}")
                    return False
            else:
                print("   ❌ Registration response missing JWT tokens!")
                print(f"   Expected: access_token, token_type")
                print(f"   Got: {list(data.keys())}")
                return False
        else:
            print(f"   ❌ Registration failed: {response.text}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"   ❌ Request failed: {e}")
        return False

def test_old_vs_new_flow():
    """Compare old flow (register + login) vs new flow (register with tokens)"""
    print("\n🔄 Comparing Old vs New Registration Flow")
    print("=" * 50)
    
    # Test the new flow
    test_email = f"new_flow_{uuid.uuid4().hex[:8]}@example.com"
    test_password = "TestPassword123!"
    
    print("🆕 New Flow: Register with direct JWT tokens")
    registration_data = {
        "email": test_email,
        "password": test_password
    }
    
    start_time = datetime.now()
    response = requests.post(REGISTER_URL, json=registration_data)
    end_time = datetime.now()
    
    new_flow_time = (end_time - start_time).total_seconds()
    
    if response.status_code == 200:
        data = response.json()
        if "access_token" in data:
            print(f"   ✅ New flow successful in {new_flow_time:.3f}s")
            print(f"   📊 Steps: 1 (register with tokens)")
        else:
            print("   ❌ New flow failed - no tokens returned")
    else:
        print(f"   ❌ New flow failed: {response.text}")
    
    print("\n📊 Flow Comparison:")
    print(f"   Old Flow: Register → Login (2 API calls)")
    print(f"   New Flow: Register with tokens (1 API call)")
    print(f"   Improvement: 50% fewer API calls, better UX")

if __name__ == "__main__":
    print("🚀 Starting Registration Flow Tests")
    print(f"⏰ Test started at: {datetime.now()}")
    print()
    
    # Test the main registration flow
    success = test_registration_flow()
    
    # Compare flows
    test_old_vs_new_flow()
    
    print("\n" + "=" * 50)
    if success:
        print("🎉 All tests passed! Registration flow is working correctly.")
        print("✅ Users can now register and proceed directly to assessment!")
    else:
        print("❌ Tests failed! Please check the implementation.")
    
    print(f"⏰ Test completed at: {datetime.now()}")