#!/usr/bin/env python3
"""
Test script to verify the login flow handles users with and without assessments properly.
"""

import asyncio
import aiohttp
import json
from datetime import datetime
import uuid

# Configuration
BASE_URL = "http://localhost:8002/api/v1"
TEST_EMAIL_WITH_ASSESSMENT = "test_with_assessment@example.com"
TEST_EMAIL_WITHOUT_ASSESSMENT = "test_without_assessment@example.com"
TEST_PASSWORD = "testpassword123"

async def make_request(session, method, url, **kwargs):
    """Make HTTP request with error handling"""
    try:
        async with session.request(method, url, **kwargs) as response:
            text = await response.text()
            try:
                data = json.loads(text) if text else {}
            except json.JSONDecodeError:
                data = {"raw_response": text}
            
            return {
                "status": response.status,
                "data": data,
                "success": 200 <= response.status < 300
            }
    except Exception as e:
        return {
            "status": 0,
            "data": {"error": str(e)},
            "success": False
        }

async def register_user(session, email, password):
    """Register a new user"""
    print(f"\n🔄 Registering user: {email}")
    
    response = await make_request(
        session, 
        "POST", 
        f"{BASE_URL}/auth/register",
        json={"email": email, "password": password}
    )
    
    if response["success"]:
        print(f"✅ User registered successfully")
        print(f"   Assessment completed: {response['data'].get('assessment_completed', 'N/A')}")
        return response["data"].get("access_token")
    else:
        print(f"❌ Registration failed: {response['data']}")
        return None

async def login_user(session, email, password):
    """Login user and check assessment status"""
    print(f"\n🔄 Logging in user: {email}")
    
    # Use form data for OAuth2PasswordRequestForm
    form_data = aiohttp.FormData()
    form_data.add_field('username', email)
    form_data.add_field('password', password)
    
    response = await make_request(
        session,
        "POST",
        f"{BASE_URL}/auth/login",
        data=form_data
    )
    
    if response["success"]:
        assessment_completed = response["data"].get("assessment_completed", False)
        print(f"✅ Login successful")
        print(f"   Access token: {response['data'].get('access_token', 'N/A')[:20]}...")
        print(f"   Assessment completed: {assessment_completed}")
        return response["data"].get("access_token"), assessment_completed
    else:
        print(f"❌ Login failed: {response['data']}")
        return None, False

async def submit_assessment(session, token):
    """Submit a test assessment for the user"""
    print(f"\n🔄 Submitting assessment")
    
    assessment_data = {
        "age": "25-30",
        "location": "San Francisco, CA",
        "educationLevel": "bachelors",
        "currentSituation": "employed",
        "currentRole": "Software Engineer",
        "experience": "3-5",
        "technicalSkills": ["Python", "JavaScript"],
        "softSkills": ["Communication", "Problem Solving"],
        "workingWithData": 4,
        "workingWithPeople": 3,
        "creativeTasks": 4,
        "problemSolving": 5,
        "leadership": 3,
        "physicalHandsOnWork": 2,
        "outdoorWork": 2,
        "mechanicalAptitude": 3,
        "interests": ["Technology & Software"],
        "industries": ["Technology & Software"],
        "careerGoals": "Advance to senior role",
        "workLifeBalance": "important",
        "salaryExpectations": "80000-120000"
    }
    
    headers = {"Authorization": f"Bearer {token}"}
    response = await make_request(
        session,
        "POST",
        f"{BASE_URL}/assessment/submit-assessment",
        json=assessment_data,
        headers=headers
    )
    
    if response["success"]:
        print(f"✅ Assessment submitted successfully")
        return True
    else:
        print(f"❌ Assessment submission failed: {response['data']}")
        return False

async def cleanup_user(session, email):
    """Clean up test user (if cleanup endpoint exists)"""
    print(f"\n🧹 Attempting to cleanup user: {email}")
    # Note: This would require a cleanup endpoint in the actual API
    # For now, we'll just log the attempt
    print(f"   (Cleanup endpoint not implemented - user {email} may remain in database)")

async def test_login_flow():
    """Test the complete login flow for users with and without assessments"""
    print("🚀 Starting Login Assessment Flow Test")
    print("=" * 60)
    
    async with aiohttp.ClientSession() as session:
        # Test 1: User without assessment
        print("\n📋 TEST 1: User WITHOUT Assessment")
        print("-" * 40)
        
        # Register user without assessment
        token_without = await register_user(session, TEST_EMAIL_WITHOUT_ASSESSMENT, TEST_PASSWORD)
        if not token_without:
            print("❌ Failed to register user without assessment")
            return
        
        # Login and verify assessment_completed is False
        login_token, assessment_completed = await login_user(session, TEST_EMAIL_WITHOUT_ASSESSMENT, TEST_PASSWORD)
        if login_token and not assessment_completed:
            print("✅ TEST 1 PASSED: User without assessment correctly identified")
        else:
            print("❌ TEST 1 FAILED: Assessment status incorrect")
        
        # Test 2: User with assessment
        print("\n📋 TEST 2: User WITH Assessment")
        print("-" * 40)
        
        # Register user who will complete assessment
        token_with = await register_user(session, TEST_EMAIL_WITH_ASSESSMENT, TEST_PASSWORD)
        if not token_with:
            print("❌ Failed to register user with assessment")
            return
        
        # Submit assessment for this user
        assessment_submitted = await submit_assessment(session, token_with)
        if not assessment_submitted:
            print("❌ Failed to submit assessment")
            return
        
        # Login and verify assessment_completed is True
        login_token, assessment_completed = await login_user(session, TEST_EMAIL_WITH_ASSESSMENT, TEST_PASSWORD)
        if login_token and assessment_completed:
            print("✅ TEST 2 PASSED: User with assessment correctly identified")
        else:
            print("❌ TEST 2 FAILED: Assessment status incorrect")
        
        # Test 3: Re-login user without assessment to ensure consistency
        print("\n📋 TEST 3: Re-login User WITHOUT Assessment")
        print("-" * 40)
        
        login_token, assessment_completed = await login_user(session, TEST_EMAIL_WITHOUT_ASSESSMENT, TEST_PASSWORD)
        if login_token and not assessment_completed:
            print("✅ TEST 3 PASSED: User without assessment still correctly identified")
        else:
            print("❌ TEST 3 FAILED: Assessment status changed unexpectedly")
        
        # Cleanup (optional)
        await cleanup_user(session, TEST_EMAIL_WITHOUT_ASSESSMENT)
        await cleanup_user(session, TEST_EMAIL_WITH_ASSESSMENT)
    
    print("\n" + "=" * 60)
    print("🏁 Login Assessment Flow Test Complete")

async def main():
    """Main test function"""
    try:
        await test_login_flow()
    except Exception as e:
        print(f"❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    print("🧪 Login Assessment Flow Test")
    print("This script tests the login flow for users with and without assessments")
    print("Make sure the backend server is running on http://localhost:8002")
    print()
    
    # Run the test
    asyncio.run(main())