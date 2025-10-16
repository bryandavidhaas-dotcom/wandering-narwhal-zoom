#!/usr/bin/env python3
"""
Complete test of login and recommendation flow
"""
import asyncio
import sys
import os
import requests
import json
from datetime import datetime
from bson import ObjectId

# Add backend to path
sys.path.insert(0, './backend')
sys.path.insert(0, '.')

async def setup_complete_test_data():
    """Setup user, assessment, and recommendation data"""
    print("🔧 Setting up complete test data...")
    
    import mongodb_replacement
    
    # Clear existing data
    mongodb_replacement.in_memory_db.databases = {}
    
    # Setup test user
    await mongodb_replacement.setup_test_user()
    
    # Get the user
    user = await mongodb_replacement.in_memory_db.find_one('recommender', 'users', {'email': 'bryandavidhaas@gmail.com'})
    if not user:
        print('❌ User not found after setup')
        return None
    
    user_id = user['_id']
    print(f'✅ User setup complete with ID: {user_id}')
    
    # Create test assessment
    assessment_data = {
        '_id': ObjectId(),
        'user_id': user_id,
        'skills': ['Python', 'JavaScript', 'Data Analysis', 'Problem Solving'],
        'experience': '5 years in software development',
        'career_goals': 'Transition to data science and AI',
        'preferences': {
            'location': 'Remote',
            'salary_range': '80000-120000',
            'work_type': 'Full-time'
        },
        'created_at': datetime.utcnow()
    }
    
    await mongodb_replacement.in_memory_db.insert_one('recommender', 'assessments', assessment_data)
    print('✅ Test assessment created')
    
    # Create test recommendations
    recommendations_data = {
        '_id': ObjectId(),
        'user_id': user_id,
        'recommendations': [
            {
                'job_title': 'Data Scientist',
                'company': 'Tech Innovations Inc',
                'location': 'Remote',
                'description': 'Analyze complex datasets to drive business decisions',
                'requirements': ['Python', 'Machine Learning', 'Statistics']
            },
            {
                'job_title': 'Full Stack Developer',
                'company': 'StartupCorp',
                'location': 'San Francisco, CA',
                'description': 'Build end-to-end web applications',
                'requirements': ['JavaScript', 'React', 'Node.js']
            }
        ],
        'created_at': datetime.utcnow()
    }
    
    await mongodb_replacement.in_memory_db.insert_one('recommender', 'recommendations', recommendations_data)
    print('✅ Test recommendations created')
    
    return user_id

def test_complete_api_flow():
    """Test the complete API flow"""
    print("\n🧪 Testing Complete API Flow...")
    
    try:
        # Test 1: Login
        print("1. Testing login...")
        login_response = requests.post(
            'http://localhost:8000/api/v1/auth/login',
            data={'username': 'bryandavidhaas@gmail.com', 'password': 'testpassword123'},
            headers={'Content-Type': 'application/x-www-form-urlencoded'},
            timeout=10
        )
        
        print(f"   Login Status: {login_response.status_code}")
        
        if login_response.status_code != 200:
            print(f"   ❌ Login failed: {login_response.text}")
            return False
        
        token_data = login_response.json()
        token = token_data.get('access_token')
        print("   ✅ Login successful")
        
        # Test 2: Get user info
        print("2. Testing user info...")
        headers = {'Authorization': f'Bearer {token}'}
        user_response = requests.get('http://localhost:8000/api/v1/auth/users/me', headers=headers, timeout=10)
        print(f"   User info Status: {user_response.status_code}")
        
        if user_response.status_code == 200:
            print("   ✅ User info retrieved")
        else:
            print(f"   ❌ User info failed: {user_response.text}")
        
        # Test 3: Get recommendations
        print("3. Testing recommendations...")
        rec_response = requests.get(
            'http://localhost:8000/api/v1/recommendation/get-latest-recommendations',
            headers=headers,
            timeout=10
        )
        
        print(f"   Recommendations Status: {rec_response.status_code}")
        
        if rec_response.status_code == 200:
            rec_data = rec_response.json()
            recommendations = rec_data.get('recommendations', [])
            print(f"   ✅ Found {len(recommendations)} recommendations")
            
            # Show first recommendation
            if recommendations:
                first_rec = recommendations[0]
                print(f"   📋 Sample: {first_rec.get('job_title')} at {first_rec.get('company')}")
            
            return True
        else:
            print(f"   ❌ Recommendations failed: {rec_response.text}")
            return False
            
    except Exception as e:
        print(f"❌ API test error: {e}")
        return False

async def main():
    print("🚀 COMPLETE FLOW TEST")
    print("=" * 50)
    
    # Setup data
    user_id = await setup_complete_test_data()
    
    if not user_id:
        print("❌ Failed to setup test data")
        return
    
    # Wait a moment for server to be ready
    await asyncio.sleep(1)
    
    # Test API flow
    success = test_complete_api_flow()
    
    print("\n" + "=" * 50)
    if success:
        print("✅ ALL TESTS PASSED - Login and Recommendations working!")
    else:
        print("❌ Some tests failed")
    
    return success

if __name__ == "__main__":
    result = asyncio.run(main())
    sys.exit(0 if result else 1)