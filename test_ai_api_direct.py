#!/usr/bin/env python3
"""
Direct API Testing for AI Endpoints
"""

import asyncio
import httpx
import json

async def test_ai_api_endpoints():
    """Test AI API endpoints directly"""
    print("🧪 Testing AI API Endpoints Directly...")
    
    base_url = "http://localhost:8002"
    
    # Test data
    test_assessment = {
        "user_id": "test_user_ai",
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
            # Test 1: Health Check
            print("  📋 Test 1: Health Check")
            try:
                response = await client.get(f"{base_url}/api/v1/health")
                print(f"    Status: {response.status_code}")
                if response.status_code == 200:
                    health_data = response.json()
                    print(f"    Health: {health_data}")
                else:
                    print(f"    Error: {response.text}")
            except Exception as e:
                print(f"    ❌ Health check failed: {e}")
            
            # Test 2: AI Recommendations Endpoint (without auth)
            print("  📋 Test 2: AI Recommendations Endpoint (no auth)")
            try:
                response = await client.post(
                    f"{base_url}/api/v1/ai/recommendations",
                    json=test_assessment
                )
                print(f"    Status: {response.status_code}")
                if response.status_code == 401:
                    print("    ✅ Authentication required (expected)")
                elif response.status_code == 200:
                    data = response.json()
                    print(f"    ✅ Success: {len(data.get('recommendations', []))} recommendations")
                    print(f"    Sample: {data.get('recommendations', [{}])[0] if data.get('recommendations') else 'None'}")
                else:
                    print(f"    ❌ Unexpected status: {response.text}")
            except Exception as e:
                print(f"    ❌ AI recommendations test failed: {e}")
            
            # Test 3: Try to register a test user and get token
            print("  📋 Test 3: Register Test User for Authentication")
            try:
                register_data = {
                    "email": "ai_test@example.com",
                    "password": "testpassword123",
                    "full_name": "AI Test User"
                }
                
                response = await client.post(
                    f"{base_url}/api/v1/auth/register",
                    json=register_data
                )
                print(f"    Registration Status: {response.status_code}")
                
                if response.status_code == 200:
                    reg_data = response.json()
                    print("    ✅ User registered successfully")
                    
                    # Now try to login
                    login_data = {
                        "username": "ai_test@example.com",
                        "password": "testpassword123"
                    }
                    
                    login_response = await client.post(
                        f"{base_url}/api/v1/auth/login",
                        data=login_data,
                        headers={"Content-Type": "application/x-www-form-urlencoded"}
                    )
                    
                    print(f"    Login Status: {login_response.status_code}")
                    
                    if login_response.status_code == 200:
                        login_result = login_response.json()
                        token = login_result.get("access_token")
                        print("    ✅ Login successful, got token")
                        
                        # Test 4: AI Recommendations with Authentication
                        print("  📋 Test 4: AI Recommendations with Authentication")
                        try:
                            auth_headers = {"Authorization": f"Bearer {token}"}
                            auth_response = await client.post(
                                f"{base_url}/api/v1/ai/recommendations",
                                json=test_assessment,
                                headers=auth_headers
                            )
                            
                            print(f"    Authenticated Status: {auth_response.status_code}")
                            
                            if auth_response.status_code == 200:
                                auth_data = auth_response.json()
                                recommendations = auth_data.get("recommendations", [])
                                print(f"    ✅ Success: {len(recommendations)} recommendations")
                                
                                if recommendations:
                                    sample_rec = recommendations[0]
                                    print(f"    Sample recommendation:")
                                    print(f"      Title: {sample_rec.get('title', 'N/A')}")
                                    print(f"      Company: {sample_rec.get('company', 'N/A')}")
                                    print(f"      Score: {sample_rec.get('score', 'N/A')}")
                                    print(f"      Job ID: {sample_rec.get('job_id', 'N/A')}")
                                    
                                    # Check if using mock data
                                    if sample_rec.get('job_id') == 'job_001':
                                        print("    ⚠️  Using mock data (API key issue)")
                                    else:
                                        print("    ✅ Using real AI recommendations")
                                
                                # Test 5: AI Tuning with Authentication
                                print("  📋 Test 5: AI Tuning with Authentication")
                                try:
                                    tuning_data = {
                                        "current_recommendations": recommendations,
                                        "prompt": "I want more remote opportunities and higher salary positions"
                                    }
                                    
                                    tune_response = await client.post(
                                        f"{base_url}/api/v1/ai/tune",
                                        json=tuning_data,
                                        headers=auth_headers
                                    )
                                    
                                    print(f"    Tuning Status: {tune_response.status_code}")
                                    
                                    if tune_response.status_code == 200:
                                        tune_data = tune_response.json()
                                        tuned_recs = tune_data.get("recommendations", [])
                                        print(f"    ✅ Tuning Success: {len(tuned_recs)} recommendations")
                                        
                                        # Check if tuning changed anything
                                        original_titles = [r.get('title') for r in recommendations]
                                        tuned_titles = [r.get('title') for r in tuned_recs]
                                        
                                        if original_titles != tuned_titles:
                                            print("    ✅ Tuning modified recommendations")
                                        else:
                                            print("    ⚠️  Tuning returned same recommendations")
                                    else:
                                        print(f"    ❌ Tuning failed: {tune_response.text}")
                                        
                                except Exception as e:
                                    print(f"    ❌ Tuning test failed: {e}")
                            else:
                                print(f"    ❌ Authenticated request failed: {auth_response.text}")
                                
                        except Exception as e:
                            print(f"    ❌ Authenticated AI test failed: {e}")
                    else:
                        print(f"    ❌ Login failed: {login_response.text}")
                else:
                    print(f"    ❌ Registration failed: {response.text}")
                    
            except Exception as e:
                print(f"    ❌ Authentication test failed: {e}")
                
        except Exception as e:
            print(f"❌ API testing failed: {e}")

if __name__ == "__main__":
    asyncio.run(test_ai_api_endpoints())