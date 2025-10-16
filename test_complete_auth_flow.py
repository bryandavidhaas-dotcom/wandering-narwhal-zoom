#!/usr/bin/env python3
"""
Test complete authentication flow with a fresh user account.
"""

import requests
import json
import uuid

def test_complete_auth_flow():
    """Test registration and login with a fresh user"""
    
    # Generate a unique email to avoid conflicts
    unique_id = str(uuid.uuid4())[:8]
    email = f"test-{unique_id}@example.com"
    password = "testpassword123"
    
    print(f"🔧 Testing complete auth flow with fresh user:")
    print(f"   Email: {email}")
    print(f"   Password: {password}")
    
    # Step 1: Register new user
    print(f"\n📝 Step 1: Registering new user...")
    try:
        reg_url = "http://localhost:8002/api/v1/auth/register"
        reg_data = {
            "email": email,
            "password": password
        }
        
        print(f"🔍 POST {reg_url}")
        print(f"🔍 Data: {reg_data}")
        
        reg_response = requests.post(reg_url, json=reg_data, timeout=10)
        print(f"🔍 Status Code: {reg_response.status_code}")
        
        try:
            reg_json = reg_response.json()
            print(f"🔍 Response JSON: {json.dumps(reg_json, indent=2)}")
        except:
            print(f"🔍 Response Text: {reg_response.text}")
        
        if reg_response.status_code != 200:
            print(f"❌ Registration failed with status {reg_response.status_code}")
            return False
        
        print("✅ Registration successful!")
        
    except Exception as e:
        print(f"❌ Registration failed: {e}")
        return False
    
    # Step 2: Login with new user
    print(f"\n🔐 Step 2: Logging in with new user...")
    try:
        login_url = "http://localhost:8002/api/v1/auth/login"
        login_data = {
            "username": email,
            "password": password
        }
        
        print(f"🔍 POST {login_url}")
        print(f"🔍 Data: {login_data}")
        
        login_response = requests.post(login_url, data=login_data, timeout=10)
        print(f"🔍 Status Code: {login_response.status_code}")
        
        try:
            login_json = login_response.json()
            print(f"🔍 Response JSON: {json.dumps(login_json, indent=2)}")
        except:
            print(f"🔍 Response Text: {login_response.text}")
        
        if login_response.status_code != 200:
            print(f"❌ Login failed with status {login_response.status_code}")
            return False
        
        print("✅ Login successful!")
        
        # Step 3: Test protected endpoint
        if 'access_token' in login_json:
            token = login_json['access_token']
            print(f"\n🛡️  Step 3: Testing protected endpoint...")
            
            headers = {"Authorization": f"Bearer {token}"}
            me_url = "http://localhost:8002/api/v1/auth/users/me"
            
            me_response = requests.get(me_url, headers=headers, timeout=10)
            print(f"🔍 GET {me_url}")
            print(f"🔍 Status Code: {me_response.status_code}")
            
            try:
                me_json = me_response.json()
                print(f"🔍 User Info: {json.dumps(me_json, indent=2)}")
            except:
                print(f"🔍 Response Text: {me_response.text}")
            
            if me_response.status_code == 200:
                print("✅ Protected endpoint access successful!")
                return True
            else:
                print("❌ Protected endpoint access failed")
                return False
        else:
            print("⚠️  No access token in login response")
            return False
            
    except Exception as e:
        print(f"❌ Login failed: {e}")
        return False

def test_existing_user_login():
    """Test login with the existing bryandavidhaas@gmail.com user"""
    print(f"\n🔧 Testing login with existing user: bryandavidhaas@gmail.com")
    
    try:
        login_url = "http://localhost:8002/api/v1/auth/login"
        login_data = {
            "username": "bryandavidhaas@gmail.com",
            "password": "testpassword123"
        }
        
        login_response = requests.post(login_url, data=login_data, timeout=10)
        print(f"🔍 Status Code: {login_response.status_code}")
        
        if login_response.status_code == 200:
            print("✅ Existing user login successful!")
            return True
        else:
            try:
                error_json = login_response.json()
                print(f"❌ Existing user login failed: {error_json.get('detail', 'Unknown error')}")
            except:
                print(f"❌ Existing user login failed: {login_response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Existing user login test failed: {e}")
        return False

def main():
    print("🚀 Testing Complete Authentication System...")
    print("=" * 60)
    
    # Test 1: Complete flow with fresh user
    fresh_user_success = test_complete_auth_flow()
    
    # Test 2: Existing user login
    existing_user_success = test_existing_user_login()
    
    print("\n" + "=" * 60)
    print("🏁 FINAL RESULTS:")
    print(f"  Fresh user flow: {'✅' if fresh_user_success else '❌'}")
    print(f"  Existing user login: {'✅' if existing_user_success else '❌'}")
    
    if fresh_user_success:
        print("\n🎉 Authentication system is fully functional!")
        print("✅ Users can register, login, and access protected endpoints")
        
        if not existing_user_success:
            print("⚠️  Note: Existing user may have password issues from old system")
        
        return True
    else:
        print("\n❌ Authentication system has issues")
        return False

if __name__ == "__main__":
    main()