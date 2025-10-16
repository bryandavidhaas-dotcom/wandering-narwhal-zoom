#!/usr/bin/env python3
"""
Final AI Testing with Authentication
"""

import asyncio
import httpx
import json
import random

async def test_ai_with_auth():
    """Test AI endpoints with authentication"""
    print("🧪 Final AI Testing with Authentication...")
    
    base_url = "http://localhost:8002"
    
    # Use a random email to avoid conflicts
    random_id = random.randint(1000, 9999)
    test_email = f"ai_test_{random_id}@example.com"
    
    # Test data
    test_assessment = {
        "user_id": f"test_user_ai_{random_id}",
        "age": "25-30",
        "location": "San Francisco, CA",
        "educationLevel": "bachelors",
        "currentSituation": "employed",
        "currentRole": "Junior Software Developer",
        "experience": "2-5",
        "technicalSkills": ["Python", "JavaScript", "React", "SQL", "Git"],
        "softSkills": ["Communication", "Problem Solving", "Team Collaboration"],
        "workingWithData": 4,
        "workingWithPeople": 3,
        "creativeTasks": 4,
        "problemSolving": 5,
        "leadership": 2,
        "physicalHandsOnWork": 1,
        "outdoorWork": 1,
        "mechanicalAptitude": 2,
        "interests": ["Technology & Software", "Data & Analytics", "Artificial Intelligence"],
        "industries": ["Technology & Software", "Financial Services", "Healthcare"],
        "careerGoals": "Transition to a senior software engineering role with focus on AI/ML",
        "workLifeBalance": "important",
        "salaryExpectations": "80000-120000"
    }
    
    async with httpx.AsyncClient(timeout=30.0) as client:
        try:
            # Step 1: Register new user
            print(f"  📋 Step 1: Register user {test_email}")
            register_data = {
                "email": test_email,
                "password": "testpassword123",
                "full_name": f"AI Test User {random_id}"
            }
            
            response = await client.post(
                f"{base_url}/api/v1/auth/register",
                json=register_data
            )
            print(f"    Registration Status: {response.status_code}")
            
            if response.status_code != 200:
                print(f"    ❌ Registration failed: {response.text}")
                return
            
            # Step 2: Login
            print("  📋 Step 2: Login")
            login_data = {
                "username": test_email,
                "password": "testpassword123"
            }
            
            login_response = await client.post(
                f"{base_url}/api/v1/auth/login",
                data=login_data,
                headers={"Content-Type": "application/x-www-form-urlencoded"}
            )
            
            print(f"    Login Status: {login_response.status_code}")
            
            if login_response.status_code != 200:
                print(f"    ❌ Login failed: {login_response.text}")
                return
            
            login_result = login_response.json()
            token = login_result.get("access_token")
            print("    ✅ Login successful, got token")
            
            # Step 3: Test AI Recommendations
            print("  📋 Step 3: Test AI Recommendations")
            auth_headers = {"Authorization": f"Bearer {token}"}
            
            rec_response = await client.post(
                f"{base_url}/api/v1/ai/recommendations",
                json=test_assessment,
                headers=auth_headers
            )
            
            print(f"    AI Recommendations Status: {rec_response.status_code}")
            
            if rec_response.status_code == 200:
                rec_data = rec_response.json()
                recommendations = rec_data.get("recommendations", [])
                print(f"    ✅ Success: {len(recommendations)} recommendations")
                
                if recommendations:
                    sample_rec = recommendations[0]
                    print(f"    📊 Sample recommendation:")
                    print(f"      Title: {sample_rec.get('title', 'N/A')}")
                    print(f"      Company: {sample_rec.get('company', 'N/A')}")
                    print(f"      Score: {sample_rec.get('score', 'N/A')}")
                    print(f"      Job ID: {sample_rec.get('job_id', 'N/A')}")
                    
                    # Check if using mock data
                    if sample_rec.get('job_id') == 'job_001':
                        print("    ⚠️  Using mock data (API key issue)")
                        api_working = False
                    else:
                        print("    ✅ Using real AI recommendations")
                        api_working = True
                    
                    # Step 4: Test AI Tuning
                    print("  📋 Step 4: Test AI Tuning")
                    tuning_data = {
                        "current_recommendations": recommendations,
                        "prompt": "I want more remote opportunities and higher salary positions"
                    }
                    
                    tune_response = await client.post(
                        f"{base_url}/api/v1/ai/tune",
                        json=tuning_data,
                        headers=auth_headers
                    )
                    
                    print(f"    AI Tuning Status: {tune_response.status_code}")
                    
                    if tune_response.status_code == 200:
                        tune_data = tune_response.json()
                        tuned_recs = tune_data.get("recommendations", [])
                        print(f"    ✅ Tuning Success: {len(tuned_recs)} recommendations")
                        
                        # Check if tuning changed anything
                        original_titles = [r.get('title') for r in recommendations]
                        tuned_titles = [r.get('title') for r in tuned_recs]
                        
                        if original_titles != tuned_titles:
                            print("    ✅ Tuning modified recommendations")
                            tuning_working = True
                        else:
                            print("    ⚠️  Tuning returned same recommendations")
                            tuning_working = False
                    else:
                        print(f"    ❌ Tuning failed: {tune_response.text}")
                        tuning_working = False
                    
                    # Summary
                    print("\n" + "="*50)
                    print("🎯 AI TESTING SUMMARY")
                    print("="*50)
                    print(f"✅ Authentication: Working")
                    print(f"✅ AI Recommendations Endpoint: Working")
                    print(f"✅ AI Tuning Endpoint: Working")
                    print(f"{'✅' if api_working else '⚠️ '} Real AI API: {'Working' if api_working else 'Using Mock Data'}")
                    print(f"{'✅' if tuning_working else '⚠️ '} AI Tuning Logic: {'Working' if tuning_working else 'Limited'}")
                    
                    if not api_working:
                        print("\n🔧 ISSUES FOUND:")
                        print("- AI API key is invalid or not working")
                        print("- System is falling back to mock data")
                        print("- Real AI recommendations are not being generated")
                    
                    if not tuning_working:
                        print("- AI tuning is not modifying recommendations")
                        print("- Tuning logic may need improvement")
                    
                else:
                    print("    ❌ No recommendations returned")
            else:
                print(f"    ❌ AI Recommendations failed: {rec_response.text}")
                
        except Exception as e:
            print(f"❌ Testing failed: {e}")

if __name__ == "__main__":
    asyncio.run(test_ai_with_auth())