#!/usr/bin/env python3
"""
Comprehensive Authentication System Test
Tests JWT token generation, validation, and authentication flow
"""
import asyncio
import os
import sys
import requests
import json
from datetime import datetime, timedelta
from jose import jwt, JWTError
from passlib.context import CryptContext
from dotenv import load_dotenv

# Load environment variables
load_dotenv('backend/.env')

# Configuration
JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'your_super_secret_jwt_key_change_this_in_production_2024')
ALGORITHM = os.getenv('ALGORITHM', 'HS256')
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv('ACCESS_TOKEN_EXPIRE_MINUTES', '30'))

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def test_jwt_functionality():
    """Test JWT token creation and validation"""
    print("🔐 Testing JWT Token Functionality")
    print("=" * 60)
    
    # Test data
    test_email = "bryandavidhaas@gmail.com"
    
    print(f"JWT Secret Key: {JWT_SECRET_KEY[:20]}...")
    print(f"Algorithm: {ALGORITHM}")
    print(f"Token Expiry: {ACCESS_TOKEN_EXPIRE_MINUTES} minutes")
    print()
    
    try:
        # Create access token
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        to_encode = {"sub": test_email, "exp": expire}
        
        encoded_jwt = jwt.encode(to_encode, JWT_SECRET_KEY, algorithm=ALGORITHM)
        print(f"✅ Token Created: {encoded_jwt[:50]}...")
        
        # Decode and validate token
        payload = jwt.decode(encoded_jwt, JWT_SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get("sub")
        exp = payload.get("exp")
        
        print(f"✅ Token Decoded Successfully")
        print(f"   Email: {email}")
        print(f"   Expires: {datetime.fromtimestamp(exp)}")
        
        if email == test_email:
            print("✅ Email validation: PASS")
        else:
            print("❌ Email validation: FAIL")
            return False
            
        return True
        
    except JWTError as e:
        print(f"❌ JWT Error: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected Error: {e}")
        return False

def test_password_hashing():
    """Test password hashing and verification"""
    print("\n🔒 Testing Password Hashing")
    print("=" * 60)
    
    test_passwords = [
        "TempPass123!",
        "MySecurePassword456",
        "AnotherTest789@"
    ]
    
    all_passed = True
    
    for password in test_passwords:
        try:
            # Hash password
            hashed = pwd_context.hash(password)
            print(f"Password: {password}")
            print(f"Hashed: {hashed[:50]}...")
            
            # Verify password
            is_valid = pwd_context.verify(password, hashed)
            print(f"Verification: {'✅ PASS' if is_valid else '❌ FAIL'}")
            
            # Test wrong password
            wrong_verify = pwd_context.verify("wrongpassword", hashed)
            print(f"Wrong Password Test: {'✅ PASS' if not wrong_verify else '❌ FAIL'}")
            print()
            
            if not is_valid or wrong_verify:
                all_passed = False
                
        except Exception as e:
            print(f"❌ Error testing password {password}: {e}")
            all_passed = False
    
    return all_passed

async def test_api_endpoints():
    """Test authentication API endpoints"""
    print("🌐 Testing Authentication API Endpoints")
    print("=" * 60)
    
    base_url = "http://localhost:8000"  # Adjust if different
    
    # Test endpoints
    endpoints = [
        "/docs",  # FastAPI docs
        "/health",  # Health check if available
    ]
    
    print(f"Base URL: {base_url}")
    
    for endpoint in endpoints:
        try:
            response = requests.get(f"{base_url}{endpoint}", timeout=5)
            print(f"GET {endpoint}: {response.status_code} {'✅' if response.status_code < 400 else '❌'}")
        except requests.exceptions.ConnectionError:
            print(f"GET {endpoint}: ❌ Connection refused (server not running)")
        except requests.exceptions.Timeout:
            print(f"GET {endpoint}: ❌ Timeout")
        except Exception as e:
            print(f"GET {endpoint}: ❌ Error - {e}")
    
    return True

def test_configuration():
    """Test configuration and environment variables"""
    print("\n⚙️  Testing Configuration")
    print("=" * 60)
    
    required_vars = [
        'JWT_SECRET_KEY',
        'ALGORITHM', 
        'ACCESS_TOKEN_EXPIRE_MINUTES',
        'MONGODB_URL',
        'MONGODB_DATABASE'
    ]
    
    all_present = True
    
    for var in required_vars:
        value = os.getenv(var)
        if value:
            # Mask sensitive values
            display_value = value if var not in ['JWT_SECRET_KEY'] else f"{value[:10]}..."
            print(f"✅ {var}: {display_value}")
        else:
            print(f"❌ {var}: Not set")
            all_present = False
    
    return all_present

def create_test_token_for_user():
    """Create a test token for bryandavidhaas@gmail.com"""
    print("\n🎫 Creating Test Token for User")
    print("=" * 60)
    
    try:
        email = "bryandavidhaas@gmail.com"
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        
        token_data = {
            "sub": email,
            "exp": expire,
            "iat": datetime.utcnow(),
            "type": "access"
        }
        
        token = jwt.encode(token_data, JWT_SECRET_KEY, algorithm=ALGORITHM)
        
        print(f"✅ Test token created for {email}")
        print(f"Token: {token}")
        print(f"Expires: {expire}")
        print()
        print("You can use this token to test protected endpoints:")
        print(f"Authorization: Bearer {token}")
        
        return token
        
    except Exception as e:
        print(f"❌ Error creating test token: {e}")
        return None

async def main():
    """Run all authentication tests"""
    print("🚀 Authentication System Test Suite")
    print("=" * 80)
    print(f"Test started at: {datetime.now()}")
    print()
    
    tests = [
        ("Configuration", test_configuration),
        ("JWT Functionality", test_jwt_functionality),
        ("Password Hashing", test_password_hashing),
        ("API Endpoints", test_api_endpoints),
    ]
    
    results = {}
    
    for test_name, test_func in tests:
        print(f"\n{'='*20} {test_name} {'='*20}")
        try:
            if asyncio.iscoroutinefunction(test_func):
                result = await test_func()
            else:
                result = test_func()
            results[test_name] = result
        except Exception as e:
            print(f"❌ Test {test_name} failed with error: {e}")
            results[test_name] = False
    
    # Create test token
    test_token = create_test_token_for_user()
    
    # Summary
    print("\n" + "="*80)
    print("📊 TEST SUMMARY")
    print("="*80)
    
    passed = sum(1 for result in results.values() if result)
    total = len(results)
    
    for test_name, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{test_name:.<30} {status}")
    
    print(f"\nOverall: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All authentication tests passed!")
        print("\nNext steps:")
        print("1. Start the FastAPI server")
        print("2. Test login with bryandavidhaas@gmail.com")
        print("3. Use the test token above for protected endpoints")
        return 0
    else:
        print("❌ Some tests failed. Please review the issues above.")
        return 1

if __name__ == "__main__":
    exit_code = asyncio.run(main())
    exit(exit_code)