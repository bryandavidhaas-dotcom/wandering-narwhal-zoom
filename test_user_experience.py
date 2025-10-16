#!/usr/bin/env python3
"""
Test the complete user experience for both returning and new users
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

async def test_returning_user_experience():
    """Test the complete experience for bryandavidhaas@gmail.com as a returning user"""
    print("🔄 TESTING RETURNING USER EXPERIENCE")
    print("=" * 60)
    
    import mongodb_replacement
    
    # Setup returning user with existing data
    mongodb_replacement.in_memory_db.databases = {}
    await mongodb_replacement.setup_test_user()
    
    # Get user and add assessment + recommendations
    user = await mongodb_replacement.in_memory_db.find_one('recommender', 'users', {'email': 'bryandavidhaas@gmail.com'})
    user_id = user['_id']
    
    # Add existing assessment
    assessment_data = {
        '_id': str(ObjectId()),
        'user_id': user_id,
        'skills': ['Python', 'JavaScript', 'Data Analysis', 'Problem Solving'],
        'experience': '5 years in software development',
        'career_goals': 'Transition to data science and AI',
        'preferences': {'location': 'Remote', 'salary_range': '80000-120000'},
        'created_at': datetime.utcnow()
    }
    await mongodb_replacement.in_memory_db.insert_one('recommender', 'assessments', assessment_data)
    
    # Add existing recommendations
    recommendations_data = {
        '_id': str(ObjectId()),
        'user_id': user_id,
        'recommendations': [
            {
                'job_title': 'Senior Data Scientist',
                'company': 'Tech Innovations Inc',
                'location': 'Remote',
                'description': 'Lead data science initiatives and mentor junior analysts',
                'requirements': ['Python', 'Machine Learning', 'Leadership']
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
    
    print("✅ Returning user setup complete with existing assessment and recommendations")
    
    # Test returning user flow
    try:
        # 1. Login
        print("\n1. 🔐 Testing login...")
        login_response = requests.post(
            'http://localhost:8000/api/v1/auth/login',
            data={'username': 'bryandavidhaas@gmail.com', 'password': 'testpassword123'},
            headers={'Content-Type': 'application/x-www-form-urlencoded'},
            timeout=10
        )
        
        if login_response.status_code == 200:
            token = login_response.json().get('access_token')
            print("   ✅ Login successful - returning user authenticated")
            headers = {'Authorization': f'Bearer {token}'}
            
            # 2. Get latest recommendations
            print("2. 📋 Testing get latest recommendations...")
            rec_response = requests.get(
                'http://localhost:8000/api/v1/recommendation/get-latest-recommendations',
                headers=headers, timeout=10
            )
            
            if rec_response.status_code == 200:
                rec_data = rec_response.json()
                recommendations = rec_data.get('recommendations', [])
                print(f"   ✅ Found {len(recommendations)} existing recommendations")
                if recommendations:
                    print(f"   📋 Sample: {recommendations[0].get('job_title')} at {recommendations[0].get('company')}")
                return True, "Returning user can login and access existing recommendations"
            else:
                print(f"   ❌ Recommendations failed: {rec_response.status_code}")
                return False, f"Recommendations endpoint failed: {rec_response.text}"
        else:
            print(f"   ❌ Login failed: {login_response.status_code}")
            return False, f"Login failed: {login_response.text}"
            
    except Exception as e:
        return False, f"Error in returning user flow: {e}"

async def test_new_user_experience():
    """Test the complete experience for a new user"""
    print("\n🆕 TESTING NEW USER EXPERIENCE")
    print("=" * 60)
    
    new_email = "newuser@example.com"
    new_password = "newpassword123"
    
    try:
        # 1. Register new user
        print("1. 📝 Testing user registration...")
        register_response = requests.post(
            'http://localhost:8000/api/v1/auth/register',
            json={'email': new_email, 'password': new_password},
            timeout=10
        )
        
        if register_response.status_code == 200:
            print("   ✅ Registration successful")
            
            # 2. Login as new user
            print("2. 🔐 Testing login...")
            login_response = requests.post(
                'http://localhost:8000/api/v1/auth/login',
                data={'username': new_email, 'password': new_password},
                headers={'Content-Type': 'application/x-www-form-urlencoded'},
                timeout=10
            )
            
            if login_response.status_code == 200:
                token = login_response.json().get('access_token')
                print("   ✅ Login successful")
                headers = {'Authorization': f'Bearer {token}'}
                
                # 3. Submit assessment
                print("3. 📊 Testing assessment submission...")
                assessment_data = {
                    'skills': ['Python', 'SQL', 'Data Visualization'],
                    'experience': '3 years in data analysis',
                    'career_goals': 'Become a data scientist',
                    'preferences': {
                        'location': 'New York',
                        'salary_range': '70000-100000',
                        'work_type': 'Full-time'
                    }
                }
                
                assessment_response = requests.post(
                    'http://localhost:8000/api/v1/assessment/submit-assessment',
                    json=assessment_data,
                    headers=headers,
                    timeout=10
                )
                
                if assessment_response.status_code == 200:
                    print("   ✅ Assessment submitted successfully")
                    
                    # 4. Generate recommendations
                    print("4. 🎯 Testing recommendation generation...")
                    gen_rec_response = requests.post(
                        'http://localhost:8000/api/v1/recommendation/generate-recommendations',
                        headers=headers,
                        timeout=15
                    )
                    
                    if gen_rec_response.status_code == 200:
                        rec_data = gen_rec_response.json()
                        recommendations = rec_data.get('recommendations', [])
                        print(f"   ✅ Generated {len(recommendations)} recommendations")
                        if recommendations:
                            print(f"   📋 Sample: {recommendations[0].get('job_title')} at {recommendations[0].get('company')}")
                        
                        # 5. Get latest recommendations
                        print("5. 📋 Testing get latest recommendations...")
                        latest_rec_response = requests.get(
                            'http://localhost:8000/api/v1/recommendation/get-latest-recommendations',
                            headers=headers,
                            timeout=10
                        )
                        
                        if latest_rec_response.status_code == 200:
                            print("   ✅ Can retrieve latest recommendations")
                            return True, "New user can complete full flow: register → login → assess → get recommendations"
                        else:
                            return False, f"Cannot retrieve recommendations: {latest_rec_response.text}"
                    else:
                        return False, f"Recommendation generation failed: {gen_rec_response.text}"
                else:
                    return False, f"Assessment submission failed: {assessment_response.text}"
            else:
                return False, f"Login failed: {login_response.text}"
        else:
            return False, f"Registration failed: {register_response.text}"
            
    except Exception as e:
        return False, f"Error in new user flow: {e}"

async def main():
    print("🚀 COMPLETE USER EXPERIENCE TEST")
    print("=" * 80)
    
    # Test returning user
    returning_success, returning_message = await test_returning_user_experience()
    
    # Wait a moment
    await asyncio.sleep(1)
    
    # Test new user
    new_success, new_message = await test_new_user_experience()
    
    print("\n" + "=" * 80)
    print("📊 USER EXPERIENCE SUMMARY")
    print("=" * 80)
    
    print(f"\n🔄 RETURNING USER (bryandavidhaas@gmail.com):")
    if returning_success:
        print(f"   ✅ {returning_message}")
    else:
        print(f"   ❌ {returning_message}")
    
    print(f"\n🆕 NEW USER EXPERIENCE:")
    if new_success:
        print(f"   ✅ {new_message}")
    else:
        print(f"   ❌ {new_message}")
    
    print(f"\n🎯 OVERALL STATUS:")
    if returning_success and new_success:
        print("   ✅ Both returning and new user experiences are working!")
    elif returning_success:
        print("   ⚠️  Returning user works, but new user experience has issues")
    elif new_success:
        print("   ⚠️  New user works, but returning user experience has issues")
    else:
        print("   ❌ Both user experiences need fixes")
    
    return returning_success and new_success

if __name__ == "__main__":
    result = asyncio.run(main())
    sys.exit(0 if result else 1)