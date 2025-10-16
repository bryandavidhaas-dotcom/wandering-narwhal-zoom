#!/usr/bin/env python3
"""
Test script to test the actual authentication flow and identify bcrypt issues
"""
import sys
import os
import asyncio
import requests
import json
from datetime import datetime

sys.path.append('./backend')

async def test_registration_endpoint():
    """Test the registration endpoint directly"""
    print("🔍 Testing registration endpoint...")
    
    # Test data
    test_user = {
        "email": "bryandavidhaas@gmail.com",
        "password": "testpassword123"
    }
    
    try:
        # Make request to registration endpoint
        response = requests.post(
            "http://localhost:8002/api/v1/auth/register",
            json=test_user,
            headers={"Content-Type": "application/json"}
        )
        
        print(f"📊 Registration response status: {response.status_code}")
        print(f"📊 Registration response: {response.text}")
        
        if response.status_code == 200:
            print("✅ Registration successful!")
            return True
        else:
            print(f"❌ Registration failed with status {response.status_code}")
            return False
            
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to backend server on port 8002")
        print("🔧 Make sure the backend server is running")
        return False
    except Exception as e:
        print(f"❌ Registration test failed: {e}")
        return False

async def test_login_endpoint():
    """Test the login endpoint"""
    print("🔍 Testing login endpoint...")
    
    # Test data - using form data as expected by OAuth2PasswordRequestForm
    login_data = {
        "username": "bryandavidhaas@gmail.com",  # OAuth2 uses 'username' field
        "password": "testpassword123"
    }
    
    try:
        # Make request to login endpoint
        response = requests.post(
            "http://localhost:8002/api/v1/auth/login",
            data=login_data,  # Use data instead of json for form data
            headers={"Content-Type": "application/x-www-form-urlencoded"}
        )
        
        print(f"📊 Login response status: {response.status_code}")
        print(f"📊 Login response: {response.text}")
        
        if response.status_code == 200:
            print("✅ Login successful!")
            return True
        else:
            print(f"❌ Login failed with status {response.status_code}")
            return False
            
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to backend server on port 8002")
        return False
    except Exception as e:
        print(f"❌ Login test failed: {e}")
        return False

async def test_direct_database_operations():
    """Test direct database operations to see if the issue is there"""
    print("🔍 Testing direct database operations...")
    
    try:
        from app.core.security import get_password_hash, verify_password
        from app.models.user import User
        from app.core.config import get_settings
        
        # Test password hashing
        password = "testpassword123"
        hashed = get_password_hash(password)
        print(f"✅ Password hashed: {hashed[:50]}...")
        
        # Test password verification
        is_valid = verify_password(password, hashed)
        print(f"✅ Password verification: {is_valid}")
        
        # Try to create a User model instance
        user_data = {
            "email": "bryandavidhaas@gmail.com",
            "hashed_password": hashed
        }
        
        user = User(**user_data)
        print(f"✅ User model created: {user.email}")
        
        return True
        
    except Exception as e:
        print(f"❌ Direct database operations failed: {e}")
        print(f"❌ Error type: {type(e)}")
        import traceback
        traceback.print_exc()
        return False

async def main():
    print("🚀 Starting authentication flow tests...")
    print("=" * 50)
    
    # Test 1: Direct database operations
    print("\n1️⃣ Testing direct database operations...")
    db_success = await test_direct_database_operations()
    
    # Test 2: Registration endpoint
    print("\n2️⃣ Testing registration endpoint...")
    reg_success = await test_registration_endpoint()
    
    # Test 3: Login endpoint (only if registration worked)
    if reg_success:
        print("\n3️⃣ Testing login endpoint...")
        login_success = await test_login_endpoint()
    else:
        print("\n3️⃣ Skipping login test (registration failed)")
        login_success = False
    
    print("\n" + "=" * 50)
    print("📊 Test Results Summary:")
    print(f"   Direct DB Operations: {'✅ PASS' if db_success else '❌ FAIL'}")
    print(f"   Registration Endpoint: {'✅ PASS' if reg_success else '❌ FAIL'}")
    print(f"   Login Endpoint: {'✅ PASS' if login_success else '❌ FAIL'}")
    
    if db_success and reg_success and login_success:
        print("🎉 All authentication tests passed!")
        return True
    else:
        print("💥 Some authentication tests failed!")
        return False

if __name__ == "__main__":
    success = asyncio.run(main())
    if not success:
        sys.exit(1)