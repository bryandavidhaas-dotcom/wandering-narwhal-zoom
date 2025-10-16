#!/usr/bin/env python3
"""
Comprehensive AI Features Testing and Validation Script

This script tests all AI-related functionality to identify issues and validate fixes.
"""

import asyncio
import json
import sys
import os
from typing import Dict, Any, List
import httpx
from datetime import datetime

# Add backend to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

# Test data for realistic assessment
TEST_ASSESSMENT_DATA = {
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
    "salaryExpectations": "80000-120000",
    "resumeText": "Experienced junior developer with 3 years in full-stack development..."
}

class AITestResults:
    def __init__(self):
        self.results = {
            "timestamp": datetime.now().isoformat(),
            "ai_client_tests": {},
            "api_endpoint_tests": {},
            "configuration_tests": {},
            "integration_tests": {},
            "performance_tests": {},
            "error_handling_tests": {},
            "summary": {}
        }
    
    def add_result(self, category: str, test_name: str, status: str, details: Dict[str, Any]):
        if category not in self.results:
            self.results[category] = {}
        self.results[category][test_name] = {
            "status": status,
            "timestamp": datetime.now().isoformat(),
            "details": details
        }
    
    def save_results(self, filename: str = "ai_test_results.json"):
        with open(filename, 'w') as f:
            json.dump(self.results, f, indent=2)
        print(f"✅ Test results saved to {filename}")

async def test_ai_client_direct():
    """Test AI client functionality directly"""
    print("\n🧪 Testing AI Client Direct Functionality...")
    
    try:
        from app.ai.ai_client import AIClient
        from app.core.config import settings
        
        # Test 1: AI Client Initialization
        print("  📋 Test 1: AI Client Initialization")
        try:
            ai_client = AIClient(api_key=settings.AI_API_KEY)
            print(f"    ✅ AI Client initialized with API key: {settings.AI_API_KEY[:10]}...")
            return {
                "initialization": {
                    "status": "success",
                    "api_key_configured": settings.AI_API_KEY != "your_ai_model_api_key_here",
                    "api_key_preview": settings.AI_API_KEY[:10] + "..." if len(settings.AI_API_KEY) > 10 else settings.AI_API_KEY
                }
            }
        except Exception as e:
            print(f"    ❌ AI Client initialization failed: {e}")
            return {
                "initialization": {
                    "status": "failed",
                    "error": str(e),
                    "api_key_configured": False
                }
            }
            
    except ImportError as e:
        print(f"    ❌ Failed to import AI client: {e}")
        return {
            "initialization": {
                "status": "failed",
                "error": f"Import error: {e}",
                "api_key_configured": False
            }
        }

async def test_ai_recommendations():
    """Test AI recommendation generation"""
    print("\n🧪 Testing AI Recommendation Generation...")
    
    try:
        from app.ai.ai_client import AIClient
        from app.core.config import settings
        
        ai_client = AIClient(api_key=settings.AI_API_KEY)
        
        # Test 2: Get Recommendations
        print("  📋 Test 2: Generate Recommendations")
        try:
            recommendations = await ai_client.get_recommendations(TEST_ASSESSMENT_DATA)
            
            if recommendations:
                print(f"    ✅ Generated {len(recommendations)} recommendations")
                
                # Validate recommendation structure
                first_rec = recommendations[0]
                required_fields = ["job_id", "title", "company", "location", "description", "score"]
                missing_fields = [field for field in required_fields if field not in first_rec]
                
                if missing_fields:
                    print(f"    ⚠️  Missing fields in recommendations: {missing_fields}")
                else:
                    print("    ✅ Recommendation structure is valid")
                
                return {
                    "recommendation_generation": {
                        "status": "success",
                        "count": len(recommendations),
                        "structure_valid": len(missing_fields) == 0,
                        "missing_fields": missing_fields,
                        "sample_recommendation": first_rec,
                        "using_mock_data": first_rec.get("job_id") == "job_001"  # Check if using fallback
                    }
                }
            else:
                print("    ❌ No recommendations generated")
                return {
                    "recommendation_generation": {
                        "status": "failed",
                        "error": "No recommendations returned",
                        "count": 0
                    }
                }
                
        except Exception as e:
            print(f"    ❌ Recommendation generation failed: {e}")
            return {
                "recommendation_generation": {
                    "status": "failed",
                    "error": str(e)
                }
            }
            
    except Exception as e:
        print(f"    ❌ AI client setup failed: {e}")
        return {
            "recommendation_generation": {
                "status": "failed",
                "error": f"Setup error: {e}"
            }
        }

async def test_ai_tuning():
    """Test AI recommendation tuning"""
    print("\n🧪 Testing AI Recommendation Tuning...")
    
    try:
        from app.ai.ai_client import AIClient
        from app.core.config import settings
        
        ai_client = AIClient(api_key=settings.AI_API_KEY)
        
        # First get some recommendations to tune
        initial_recommendations = await ai_client.get_recommendations(TEST_ASSESSMENT_DATA)
        
        if not initial_recommendations:
            return {
                "tuning": {
                    "status": "failed",
                    "error": "No initial recommendations to tune"
                }
            }
        
        # Test 3: Tune Recommendations
        print("  📋 Test 3: Tune Recommendations")
        try:
            tuning_prompt = "I want more remote opportunities and higher salary positions"
            tuned_recommendations = await ai_client.tune_recommendations(initial_recommendations, tuning_prompt)
            
            if tuned_recommendations:
                print(f"    ✅ Tuned recommendations: {len(tuned_recommendations)} results")
                
                # Check if tuning actually changed anything
                initial_titles = [rec.get("title", "") for rec in initial_recommendations]
                tuned_titles = [rec.get("title", "") for rec in tuned_recommendations]
                
                changes_detected = initial_titles != tuned_titles
                
                return {
                    "tuning": {
                        "status": "success",
                        "initial_count": len(initial_recommendations),
                        "tuned_count": len(tuned_recommendations),
                        "changes_detected": changes_detected,
                        "tuning_prompt": tuning_prompt
                    }
                }
            else:
                print("    ❌ Tuning returned no results")
                return {
                    "tuning": {
                        "status": "failed",
                        "error": "No tuned recommendations returned"
                    }
                }
                
        except Exception as e:
            print(f"    ❌ Recommendation tuning failed: {e}")
            return {
                "tuning": {
                    "status": "failed",
                    "error": str(e)
                }
            }
            
    except Exception as e:
        print(f"    ❌ AI tuning setup failed: {e}")
        return {
            "tuning": {
                "status": "failed",
                "error": f"Setup error: {e}"
            }
        }

async def test_api_endpoints():
    """Test AI API endpoints"""
    print("\n🧪 Testing AI API Endpoints...")
    
    base_url = "http://localhost:8000"
    
    # First, we need to authenticate to get a token
    async with httpx.AsyncClient() as client:
        try:
            # Test 4: AI Recommendations Endpoint
            print("  📋 Test 4: AI Recommendations API Endpoint")
            
            # Try to call the endpoint without authentication first
            try:
                response = await client.post(
                    f"{base_url}/api/v1/ai/recommendations",
                    json=TEST_ASSESSMENT_DATA,
                    timeout=30.0
                )
                
                if response.status_code == 401:
                    print("    ⚠️  Authentication required (expected)")
                    return {
                        "api_endpoints": {
                            "status": "authentication_required",
                            "recommendations_endpoint": "requires_auth",
                            "status_code": 401
                        }
                    }
                elif response.status_code == 200:
                    data = response.json()
                    print(f"    ✅ API endpoint working: {len(data.get('recommendations', []))} recommendations")
                    return {
                        "api_endpoints": {
                            "status": "success",
                            "recommendations_endpoint": "working",
                            "status_code": 200,
                            "recommendation_count": len(data.get('recommendations', []))
                        }
                    }
                else:
                    print(f"    ❌ Unexpected status code: {response.status_code}")
                    return {
                        "api_endpoints": {
                            "status": "failed",
                            "recommendations_endpoint": "error",
                            "status_code": response.status_code,
                            "response": response.text
                        }
                    }
                    
            except httpx.TimeoutException:
                print("    ❌ API endpoint timeout")
                return {
                    "api_endpoints": {
                        "status": "failed",
                        "error": "timeout",
                        "recommendations_endpoint": "timeout"
                    }
                }
            except httpx.ConnectError:
                print("    ❌ Cannot connect to API server")
                return {
                    "api_endpoints": {
                        "status": "failed",
                        "error": "connection_error",
                        "recommendations_endpoint": "unreachable"
                    }
                }
                
        except Exception as e:
            print(f"    ❌ API endpoint test failed: {e}")
            return {
                "api_endpoints": {
                    "status": "failed",
                    "error": str(e)
                }
            }

async def test_configuration():
    """Test AI configuration"""
    print("\n🧪 Testing AI Configuration...")
    
    try:
        from app.core.config import settings
        
        # Test 5: Configuration Validation
        print("  📋 Test 5: Configuration Validation")
        
        config_results = {
            "ai_api_key_set": settings.AI_API_KEY != "your_ai_model_api_key_here",
            "ai_api_key_length": len(settings.AI_API_KEY),
            "ai_api_key_preview": settings.AI_API_KEY[:10] + "..." if len(settings.AI_API_KEY) > 10 else settings.AI_API_KEY,
            "debug_mode": settings.DEBUG,
            "cors_origins": settings.CORS_ORIGINS
        }
        
        if config_results["ai_api_key_set"]:
            print("    ✅ AI API key is configured")
        else:
            print("    ❌ AI API key is using default placeholder")
        
        print(f"    📊 API key length: {config_results['ai_api_key_length']} characters")
        print(f"    📊 Debug mode: {config_results['debug_mode']}")
        
        return {
            "configuration": {
                "status": "success" if config_results["ai_api_key_set"] else "warning",
                **config_results
            }
        }
        
    except Exception as e:
        print(f"    ❌ Configuration test failed: {e}")
        return {
            "configuration": {
                "status": "failed",
                "error": str(e)
            }
        }

async def test_error_handling():
    """Test AI error handling scenarios"""
    print("\n🧪 Testing AI Error Handling...")
    
    try:
        from app.ai.ai_client import AIClient
        
        # Test 6: Invalid API Key Handling
        print("  📋 Test 6: Invalid API Key Handling")
        
        try:
            # Test with invalid API key
            invalid_client = AIClient(api_key="invalid_key_12345")
            recommendations = await invalid_client.get_recommendations(TEST_ASSESSMENT_DATA)
            
            # Should fall back to mock data
            if recommendations and len(recommendations) > 0:
                print("    ✅ Graceful fallback to mock data on API failure")
                fallback_working = True
            else:
                print("    ❌ No fallback data provided on API failure")
                fallback_working = False
                
            return {
                "error_handling": {
                    "status": "success" if fallback_working else "failed",
                    "invalid_api_key_fallback": fallback_working,
                    "mock_data_count": len(recommendations) if recommendations else 0
                }
            }
            
        except Exception as e:
            print(f"    ❌ Error handling test failed: {e}")
            return {
                "error_handling": {
                    "status": "failed",
                    "error": str(e)
                }
            }
            
    except Exception as e:
        print(f"    ❌ Error handling setup failed: {e}")
        return {
            "error_handling": {
                "status": "failed",
                "error": f"Setup error: {e}"
            }
        }

async def main():
    """Run comprehensive AI testing"""
    print("🚀 Starting Comprehensive AI Features Testing...")
    print("=" * 60)
    
    results = AITestResults()
    
    # Run all tests
    test_functions = [
        ("ai_client_tests", test_ai_client_direct),
        ("ai_client_tests", test_ai_recommendations),
        ("ai_client_tests", test_ai_tuning),
        ("api_endpoint_tests", test_api_endpoints),
        ("configuration_tests", test_configuration),
        ("error_handling_tests", test_error_handling)
    ]
    
    for category, test_func in test_functions:
        try:
            test_result = await test_func()
            for test_name, details in test_result.items():
                results.add_result(category, test_name, details.get("status", "unknown"), details)
        except Exception as e:
            results.add_result(category, test_func.__name__, "failed", {"error": str(e)})
    
    # Generate summary
    total_tests = sum(len(category_results) for category_results in results.results.values() if isinstance(category_results, dict))
    passed_tests = 0
    failed_tests = 0
    warning_tests = 0
    
    for category_name, category_results in results.results.items():
        if isinstance(category_results, dict):
            for test_name, test_data in category_results.items():
                if isinstance(test_data, dict) and "status" in test_data:
                    status = test_data["status"]
                    if status == "success":
                        passed_tests += 1
                    elif status == "failed":
                        failed_tests += 1
                    elif status == "warning":
                        warning_tests += 1
    
    results.results["summary"] = {
        "total_tests": total_tests,
        "passed": passed_tests,
        "failed": failed_tests,
        "warnings": warning_tests,
        "success_rate": f"{(passed_tests / max(total_tests, 1)) * 100:.1f}%"
    }
    
    # Print summary
    print("\n" + "=" * 60)
    print("📊 AI TESTING SUMMARY")
    print("=" * 60)
    print(f"Total Tests: {total_tests}")
    print(f"✅ Passed: {passed_tests}")
    print(f"❌ Failed: {failed_tests}")
    print(f"⚠️  Warnings: {warning_tests}")
    print(f"Success Rate: {results.results['summary']['success_rate']}")
    
    # Save results
    results.save_results()
    
    print("\n🎯 KEY FINDINGS:")
    
    # Check critical issues
    config_test = results.results.get("configuration_tests", {}).get("configuration", {})
    if config_test.get("details", {}).get("ai_api_key_set") == False:
        print("❌ CRITICAL: AI API key is not configured - using placeholder value")
    
    ai_tests = results.results.get("ai_client_tests", {})
    if ai_tests.get("recommendation_generation", {}).get("details", {}).get("using_mock_data"):
        print("⚠️  WARNING: AI client is falling back to mock data")
    
    api_tests = results.results.get("api_endpoint_tests", {})
    if api_tests.get("api_endpoints", {}).get("details", {}).get("status") == "authentication_required":
        print("ℹ️  INFO: API endpoints require authentication (expected)")
    
    print("\n✅ AI testing completed. Check ai_test_results.json for detailed results.")

if __name__ == "__main__":
    asyncio.run(main())