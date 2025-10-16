#!/usr/bin/env python3
"""
Comprehensive bcrypt debugging script to identify the password length issue.
"""

import sys
import os
import asyncio
import requests
import json

# Add the backend directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

def test_password_encoding():
    """Test password encoding and byte length"""
    password = "testpassword123"
    print(f"🔍 Testing password: '{password}'")
    print(f"🔍 Password length (characters): {len(password)}")
    
    # Test different encodings
    encodings = ['utf-8', 'ascii', 'latin-1']
    for encoding in encodings:
        try:
            encoded = password.encode(encoding)
            print(f"🔍 {encoding} encoding: {len(encoded)} bytes - {encoded}")
        except Exception as e:
            print(f"❌ {encoding} encoding failed: {e}")

def test_bcrypt_directly():
    """Test bcrypt hashing directly"""
    try:
        import bcrypt
        password = "testpassword123"
        print(f"\n🔧 Testing bcrypt directly with password: '{password}'")
        
        # Test encoding
        password_bytes = password.encode('utf-8')
        print(f"🔍 Password bytes: {password_bytes} (length: {len(password_bytes)})")
        
        if len(password_bytes) > 72:
            print(f"⚠️  Password exceeds 72 bytes, truncating...")
            password_bytes = password_bytes[:72]
            print(f"🔍 Truncated bytes: {password_bytes} (length: {len(password_bytes)})")
        
        # Generate salt and hash
        salt = bcrypt.gensalt()
        print(f"🔍 Generated salt: {salt}")
        
        hashed = bcrypt.hashpw(password_bytes, salt)
        print(f"✅ Hashed password: {hashed}")
        print(f"🔍 Hash length: {len(hashed)} bytes")
        
        # Test verification
        is_valid = bcrypt.checkpw(password_bytes, hashed)
        print(f"✅ Password verification: {is_valid}")
        
        return hashed.decode('utf-8')
        
    except Exception as e:
        print(f"❌ Direct bcrypt test failed: {e}")
        import traceback
        traceback.print_exc()
        return None

def test_security_module():
    """Test the security module functions"""
    try:
        from app.core.security import get_password_hash, verify_password
        password = "testpassword123"
        print(f"\n🔧 Testing security module with password: '{password}'")
        
        # Test hashing
        hashed = get_password_hash(password)
        print(f"✅ Security module hash: {hashed}")
        
        # Test verification
        is_valid = verify_password(password, hashed)
        print(f"✅ Security module verification: {is_valid}")
        
        return hashed
        
    except Exception as e:
        print(f"❌ Security module test failed: {e}")
        import traceback
        traceback.print_exc()
        return None

def test_user_model():
    """Test the User model creation"""
    try:
        from app.models.user import User
        print(f"\n🔧 Testing User model creation")
        
        user_data = {
            "email": "bryandavidhaas@gmail.com",
            "hashed_password": "test_hash_value"
        }
        
        user = User(**user_data)
        print(f"✅ User model created: {user}")
        print(f"🔍 User dict: {user.dict()}")
        
        return True
        
    except Exception as e:
        print(f"❌ User model test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_registration_endpoint():
    """Test the registration endpoint directly"""
    try:
        print(f"\n🔧 Testing registration endpoint")
        
        url = "http://localhost:8002/api/v1/auth/register"
        data = {
            "email": "bryandavidhaas@gmail.com",
            "password": "testpassword123"
        }
        
        print(f"🔍 POST {url}")
        print(f"🔍 Data: {data}")
        
        response = requests.post(url, json=data, timeout=10)
        print(f"🔍 Status Code: {response.status_code}")
        print(f"🔍 Response Headers: {dict(response.headers)}")
        
        try:
            response_json = response.json()
            print(f"🔍 Response JSON: {json.dumps(response_json, indent=2)}")
        except:
            print(f"🔍 Response Text: {response.text}")
        
        if response.status_code == 200:
            print("✅ Registration successful!")
            return True
        else:
            print(f"❌ Registration failed with status {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Registration endpoint test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_login_endpoint():
    """Test the login endpoint"""
    try:
        print(f"\n🔧 Testing login endpoint")
        
        url = "http://localhost:8002/api/v1/auth/login"
        data = {
            "username": "bryandavidhaas@gmail.com",
            "password": "testpassword123"
        }
        
        print(f"🔍 POST {url}")
        print(f"🔍 Data: {data}")
        
        response = requests.post(url, data=data, timeout=10)
        print(f"🔍 Status Code: {response.status_code}")
        
        try:
            response_json = response.json()
            print(f"🔍 Response JSON: {json.dumps(response_json, indent=2)}")
        except:
            print(f"🔍 Response Text: {response.text}")
        
        if response.status_code == 200:
            print("✅ Login successful!")
            return True
        else:
            print(f"❌ Login failed with status {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Login endpoint test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    print("🚀 Starting comprehensive bcrypt debugging...")
    print("=" * 60)
    
    # Test 1: Password encoding
    test_password_encoding()
    
    # Test 2: Direct bcrypt
    bcrypt_hash = test_bcrypt_directly()
    
    # Test 3: Security module
    security_hash = test_security_module()
    
    # Test 4: User model
    user_model_ok = test_user_model()
    
    # Test 5: Registration endpoint
    registration_ok = test_registration_endpoint()
    
    # Test 6: Login endpoint (only if registration succeeded)
    if registration_ok:
        login_ok = test_login_endpoint()
    else:
        print("\n⚠️  Skipping login test due to registration failure")
        login_ok = False
    
    print("\n" + "=" * 60)
    print("🏁 SUMMARY:")
    print(f"  Direct bcrypt: {'✅' if bcrypt_hash else '❌'}")
    print(f"  Security module: {'✅' if security_hash else '❌'}")
    print(f"  User model: {'✅' if user_model_ok else '❌'}")
    print(f"  Registration: {'✅' if registration_ok else '❌'}")
    print(f"  Login: {'✅' if login_ok else '❌'}")
    
    if registration_ok and login_ok:
        print("\n🎉 All tests passed! Authentication system is working!")
    else:
        print("\n❌ Some tests failed. Check the output above for details.")

if __name__ == "__main__":
    main()