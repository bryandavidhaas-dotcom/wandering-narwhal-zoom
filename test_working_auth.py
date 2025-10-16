#!/usr/bin/env python3
"""
Test script to test the working authentication system
"""
import sys
import os
import asyncio
import requests
import json
from datetime import datetime

sys.path.append('./backend')

async def test_working_auth():
    """Test the working authentication system"""
    print("🚀 Testing working authentication system on port 8003...")
    print("=" * 60)
    
    # Use a unique email for this test
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    test_user = {
        "email": f"test_user_{timestamp}@example.com",
        "password": "testpassword123"
    }
    
    # Test 1: Registration
    print("\n1️⃣ Testing user registration...")
    try:
        response = requests.post(
            "http://localhost:8003/api/v1/auth/register",
            json=test_user,
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        
        print(f"📊 Registration status: {response.status_code}")
        if response.status_code == 200:
            print("✅ Registration successful!")
            user_data = response.json()
            print(f"📧 User created: {user_data.get('email', 'N/A')}")
        else:
            print(f"❌ Registration failed: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Registration test failed: {e}")
        return False
    
    # Test 2: Login
    print("\n2️⃣ Testing user login...")
    try:
        login_data = {
            "username": test_user["email"],  # OAuth2 uses 'username' field
            "password": test_user["password"]
        }
        
        response = requests.post(
            "http://localhost:8003/api/v1/auth/login",
            data=login_data,  # Use data instead of json for form data
            headers={"Content-Type": "application/x-www-form-urlencoded"},
            timeout=10
        )
        
        print(f"📊 Login status: {response.status_code}")
        if response.status_code == 200:
            print("✅ Login successful!")
            token_data = response.json()
            access_token = token_data.get('access_token')
            print(f"🔑 Access token received: {access_token[:50]}..." if access_token else "❌ No token received")
            return True
        else:
            print(f"❌ Login failed: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Login test failed: {e}")
        return False

async def test_bryan_credentials():
    """Test with the specific credentials requested"""
    print("\n" + "=" * 60)
    print("3️⃣ Testing with requested credentials...")
    
    bryan_user = {
        "email": "bryandavidhaas@gmail.com",
        "password": "testpassword123"
    }
    
    # Test login (user should already exist)
    try:
        login_data = {
            "username": bryan_user["email"],
            "password": bryan_user["password"]
        }
        
        response = requests.post(
            "http://localhost:8003/api/v1/auth/login",
            data=login_data,
            headers={"Content-Type": "application/x-www-form-urlencoded"},
            timeout=10
        )
        
        print(f"📊 Bryan login status: {response.status_code}")
        if response.status_code == 200:
            print("✅ Bryan can login successfully!")
            token_data = response.json()
            access_token = token_data.get('access_token')
            print(f"🔑 Bryan's access token: {access_token[:50]}..." if access_token else "❌ No token received")
            return True
        else:
            print(f"❌ Bryan login failed: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Bryan login test failed: {e}")
        return False

async def main():
    print("🎯 AUTHENTICATION SYSTEM TEST")
    print("Testing the fixed bcrypt implementation...")
    
    # Test with new user
    new_user_success = await test_working_auth()
    
    # Test with Bryan's credentials
    bryan_success = await test_bryan_credentials()
    
    print("\n" + "=" * 60)
    print("📊 FINAL RESULTS:")
    print(f"   New User Registration & Login: {'✅ PASS' if new_user_success else '❌ FAIL'}")
    print(f"   Bryan's Login: {'✅ PASS' if bryan_success else '❌ FAIL'}")
    
    if new_user_success and bryan_success:
        print("\n🎉 ALL AUTHENTICATION TESTS PASSED!")
        print("🔐 The bcrypt compatibility issue has been FIXED!")
        print("✅ Users can now register and login successfully!")
        return True
    else:
        print("\n💥 Some tests failed!")
        return False

if __name__ == "__main__":
    success = asyncio.run(main())
    if not success:
        sys.exit(1)