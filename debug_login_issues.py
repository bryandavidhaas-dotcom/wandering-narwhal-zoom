#!/usr/bin/env python3
"""
Debug script to identify login and recommendation issues
"""
import asyncio
import sys
import os
import requests
import json
from datetime import datetime

# Add backend to path
sys.path.insert(0, './backend')
sys.path.insert(0, '.')

async def test_database_connection():
    """Test database connection and user data"""
    print("🔍 Testing Database Connection...")
    try:
        import mongodb_replacement
        
        # Check if user exists
        user = await mongodb_replacement.in_memory_db.find_one("recommender", "users", {"email": "bryandavidhaas@gmail.com"})
        if user:
            print(f"✅ User found: {user.get('email')}")
            print(f"   - Has hashed_password: {'hashed_password' in user}")
            print(f"   - Has password: {'password' in user}")
            print(f"   - User ID: {user.get('_id')}")
            print(f"   - Created at: {user.get('created_at')}")
            return user
        else:
            print("❌ User not found in database")
            return None
    except Exception as e:
        print(f"❌ Database connection error: {e}")
        return None

def test_password_verification():
    """Test password hashing and verification"""
    print("\n🔍 Testing Password Verification...")
    try:
        from passlib.context import CryptContext
        pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        
        # Test password hashing
        test_password = "testpassword123"
        hashed = pwd_context.hash(test_password)
        print(f"✅ Password hashing works")
        
        # Test verification
        is_valid = pwd_context.verify(test_password, hashed)
        print(f"✅ Password verification works: {is_valid}")
        
        return True
    except Exception as e:
        print(f"❌ Password verification error: {e}")
        return False

def test_api_endpoints():
    """Test API endpoints"""
    print("\n🔍 Testing API Endpoints...")
    
    try:
        # Test health endpoint
        health_response = requests.get('http://localhost:8000/api/v1/health', timeout=5)
        print(f"Health endpoint: {health_response.status_code} - {health_response.text}")
        
        # Test login endpoint
        login_data = {
            'username': 'bryandavidhaas@gmail.com',
            'password': 'testpassword123'
        }
        
        login_response = requests.post(
            'http://localhost:8000/api/v1/auth/login',
            data=login_data,
            headers={'Content-Type': 'application/x-www-form-urlencoded'},
            timeout=10
        )
        
        print(f"Login endpoint: {login_response.status_code}")
        print(f"Login response: {login_response.text}")
        
        if login_response.status_code == 200:
            token_data = login_response.json()
            token = token_data.get('access_token')
            print(f"✅ Login successful, token received")
            
            # Test recommendations endpoint
            headers = {'Authorization': f'Bearer {token}'}
            rec_response = requests.get(
                'http://localhost:8000/api/v1/recommendation/get-latest-recommendations',
                headers=headers,
                timeout=10
            )
            print(f"Recommendations endpoint: {rec_response.status_code}")
            print(f"Recommendations response: {rec_response.text}")
            
            return token
        else:
            print("❌ Login failed")
            return None
            
    except requests.exceptions.RequestException as e:
        print(f"❌ API request error: {e}")
        return None
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return None

async def test_ai_client():
    """Test AI client functionality"""
    print("\n🔍 Testing AI Client...")
    try:
        from backend.app.ai.ai_client import AIClient
        from backend.app.core.config import settings
        
        print(f"AI API Key configured: {settings.AI_API_KEY != 'your_ai_model_api_key_here'}")
        
        # Test AI client initialization
        ai_client = AIClient(api_key="test-key")
        print("✅ AI Client initialized")
        
        # Check if methods are async
        import inspect
        get_rec_method = getattr(ai_client, 'get_recommendations')
        is_async = inspect.iscoroutinefunction(get_rec_method)
        print(f"get_recommendations is async: {is_async}")
        
        return True
    except Exception as e:
        print(f"❌ AI Client error: {e}")
        return False

async def main():
    print("🚀 DEBUGGING LOGIN AND RECOMMENDATION ISSUES")
    print("=" * 60)
    print(f"Timestamp: {datetime.now()}")
    print()
    
    # Test 1: Database connection and user data
    user = await test_database_connection()
    
    # Test 2: Password verification
    pwd_ok = test_password_verification()
    
    # Test 3: API endpoints
    token = test_api_endpoints()
    
    # Test 4: AI client
    ai_ok = await test_ai_client()
    
    print("\n" + "=" * 60)
    print("🔍 DIAGNOSIS SUMMARY:")
    print("=" * 60)
    
    issues_found = []
    
    if not user:
        issues_found.append("❌ User not found in database")
    
    if not pwd_ok:
        issues_found.append("❌ Password verification system broken")
    
    if not token:
        issues_found.append("❌ Login endpoint failing")
    
    if not ai_ok:
        issues_found.append("❌ AI client has issues")
    
    if issues_found:
        print("ISSUES IDENTIFIED:")
        for issue in issues_found:
            print(f"  {issue}")
    else:
        print("✅ All systems appear to be working")
    
    print("\n🔍 MOST LIKELY ROOT CAUSES:")
    print("1. AI Client async/await mismatch - methods are sync but called with await")
    print("2. Missing AI API key configuration")
    print("3. User ID field handling inconsistencies")
    
    return issues_found

if __name__ == "__main__":
    asyncio.run(main())