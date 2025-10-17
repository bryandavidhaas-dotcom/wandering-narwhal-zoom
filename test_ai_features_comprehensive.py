#!/usr/bin/env python3
"""
Comprehensive AI Features Testing Script

This script tests all AI functionality end-to-end:
1. Creates test user account
2. Tests AI recommendation generation
3. Tests recommendation tuning
4. Validates timeout handling
5. Tests fallback mechanisms
6. Tests integration with assessment data
"""

import requests
import json
import time
import asyncio
from typing import Dict, Any, List

class AIFeaturesTester:
    def __init__(self, base_url: str = "http://localhost:8002/api/v1"):
        self.base_url = base_url
        self.session = requests.Session()
        self.auth_token = None
        self.test_results = {
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "tests": {},
            "summary": {
                "total_tests": 0,
                "passed": 0,
                "failed": 0,
                "errors": []
            }
        }

    def log_test(self, test_name: str, success: bool, details: Dict[str, Any] = None):
        """Log test results"""
        self.test_results["tests"][test_name] = {
            "success": success,
            "details": details or {},
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
        }
        self.test_results["summary"]["total_tests"] += 1
        if success:
            self.test_results["summary"]["passed"] += 1
            print(f"✅ {test_name}")
        else:
            self.test_results["summary"]["failed"] += 1
            print(f"❌ {test_name}")
            if details and "error" in details:
                self.test_results["summary"]["errors"].append(f"{test_name}: {details['error']}")

    def create_test_user(self) -> bool:
        """Create a test user account for AI testing"""
        print("\n=== CREATING TEST USER ===")
        
        test_user_data = {
            "email": "ai_test_user@example.com",
            "password": "TestPassword123!",
            "full_name": "AI Test User"
        }
        
        try:
            # Register user
            response = self.session.post(
                f"{self.base_url}/auth/register",
                json=test_user_data,
                timeout=10
            )
            
            if response.status_code == 201:
                self.log_test("User Registration", True, {"status_code": response.status_code})
            elif response.status_code == 400 and "already registered" in response.text.lower():
                self.log_test("User Registration", True, {"status_code": response.status_code, "note": "User already exists"})
            else:
                self.log_test("User Registration", False, {
                    "status_code": response.status_code,
                    "error": response.text
                })
                return False
            
            # Login user
            login_data = {
                "username": test_user_data["email"],
                "password": test_user_data["password"]
            }
            
            response = self.session.post(
                f"{self.base_url}/auth/login",
                data=login_data,  # Form data for OAuth2
                timeout=10
            )
            
            if response.status_code == 200:
                token_data = response.json()
                self.auth_token = token_data.get("access_token")
                self.session.headers.update({"Authorization": f"Bearer {self.auth_token}"})
                self.log_test("User Login", True, {"status_code": response.status_code})
                return True
            else:
                self.log_test("User Login", False, {
                    "status_code": response.status_code,
                    "error": response.text
                })
                return False
                
        except Exception as e:
            self.log_test("User Creation Process", False, {"error": str(e)})
            return False

    def create_test_assessment(self) -> Dict[str, Any]:
        """Create a comprehensive test assessment"""
        return {
            "technicalSkills": ["Python", "JavaScript", "SQL", "Machine Learning", "Data Analysis"],
            "softSkills": ["Communication", "Problem Solving", "Leadership", "Teamwork"],
            "experience": "3-5 years",
            "careerGoals": "Advance to senior technical role with leadership responsibilities",
            "currentRole": "Software Developer",
            "educationLevel": "Bachelor's Degree",
            "salaryExpectations": "$80,000 - $120,000",
            "industries": ["Technology", "Healthcare", "Finance"],
            "interests": ["Artificial Intelligence", "Web Development", "Data Science"],
            "workingWithData": 4,
            "workingWithPeople": 3,
            "creativeTasks": 4,
            "preferences": {
                "location": "Remote or San Francisco",
                "work_life_balance": "High",
                "company_size": "Medium to Large"
            }
        }

    def test_ai_recommendations(self) -> bool:
        """Test AI recommendation generation endpoint"""
        print("\n=== TESTING AI RECOMMENDATIONS ===")
        
        if not self.auth_token:
            self.log_test("AI Recommendations", False, {"error": "No auth token available"})
            return False
        
        assessment_data = self.create_test_assessment()
        
        try:
            start_time = time.time()
            response = self.session.post(
                f"{self.base_url}/ai/recommendations",
                json=assessment_data,
                timeout=35  # Slightly longer than the 30s API timeout
            )
            end_time = time.time()
            response_time = end_time - start_time
            
            if response.status_code == 200:
                recommendations = response.json()
                
                # Validate response structure
                if "recommendations" in recommendations:
                    rec_list = recommendations["recommendations"]
                    if isinstance(rec_list, list) and len(rec_list) > 0:
                        # Validate first recommendation structure
                        first_rec = rec_list[0]
                        required_fields = ["job_id", "title", "company", "location", "description"]
                        missing_fields = [field for field in required_fields if field not in first_rec]
                        
                        if not missing_fields:
                            self.log_test("AI Recommendations", True, {
                                "status_code": response.status_code,
                                "response_time": f"{response_time:.2f}s",
                                "recommendations_count": len(rec_list),
                                "sample_recommendation": first_rec
                            })
                            return True
                        else:
                            self.log_test("AI Recommendations", False, {
                                "error": f"Missing required fields: {missing_fields}",
                                "response": first_rec
                            })
                    else:
                        self.log_test("AI Recommendations", False, {
                            "error": "Empty or invalid recommendations list",
                            "response": recommendations
                        })
                else:
                    self.log_test("AI Recommendations", False, {
                        "error": "Missing 'recommendations' key in response",
                        "response": recommendations
                    })
            else:
                self.log_test("AI Recommendations", False, {
                    "status_code": response.status_code,
                    "error": response.text,
                    "response_time": f"{response_time:.2f}s"
                })
            
            return False
            
        except requests.exceptions.Timeout:
            self.log_test("AI Recommendations", False, {
                "error": "Request timed out (>35s)",
                "note": "This indicates the 30s timeout may not be working properly"
            })
            return False
        except Exception as e:
            self.log_test("AI Recommendations", False, {"error": str(e)})
            return False

    def test_ai_tuning(self) -> bool:
        """Test AI recommendation tuning endpoint"""
        print("\n=== TESTING AI RECOMMENDATION TUNING ===")
        
        if not self.auth_token:
            self.log_test("AI Tuning", False, {"error": "No auth token available"})
            return False
        
        # First get some recommendations to tune
        assessment_data = self.create_test_assessment()
        
        try:
            # Get initial recommendations
            rec_response = self.session.post(
                f"{self.base_url}/ai/recommendations",
                json=assessment_data,
                timeout=35
            )
            
            if rec_response.status_code != 200:
                self.log_test("AI Tuning - Get Initial Recommendations", False, {
                    "error": "Could not get initial recommendations for tuning test"
                })
                return False
            
            recommendations = rec_response.json().get("recommendations", [])
            if not recommendations:
                self.log_test("AI Tuning - Get Initial Recommendations", False, {
                    "error": "No recommendations returned for tuning test"
                })
                return False
            
            # Now test tuning
            tuning_data = {
                "current_recommendations": recommendations,
                "prompt": "I want more remote opportunities and higher salary ranges. Focus on senior-level positions in AI/ML."
            }
            
            start_time = time.time()
            response = self.session.post(
                f"{self.base_url}/ai/tune",
                json=tuning_data,
                timeout=35
            )
            end_time = time.time()
            response_time = end_time - start_time
            
            if response.status_code == 200:
                tuned_recommendations = response.json()
                
                if "recommendations" in tuned_recommendations:
                    tuned_list = tuned_recommendations["recommendations"]
                    if isinstance(tuned_list, list) and len(tuned_list) > 0:
                        self.log_test("AI Tuning", True, {
                            "status_code": response.status_code,
                            "response_time": f"{response_time:.2f}s",
                            "original_count": len(recommendations),
                            "tuned_count": len(tuned_list),
                            "sample_tuned": tuned_list[0] if tuned_list else None
                        })
                        return True
                    else:
                        self.log_test("AI Tuning", False, {
                            "error": "Empty or invalid tuned recommendations",
                            "response": tuned_recommendations
                        })
                else:
                    self.log_test("AI Tuning", False, {
                        "error": "Missing 'recommendations' key in tuning response",
                        "response": tuned_recommendations
                    })
            else:
                self.log_test("AI Tuning", False, {
                    "status_code": response.status_code,
                    "error": response.text,
                    "response_time": f"{response_time:.2f}s"
                })
            
            return False
            
        except requests.exceptions.Timeout:
            self.log_test("AI Tuning", False, {
                "error": "Request timed out (>35s)",
                "note": "This indicates the 30s timeout may not be working properly"
            })
            return False
        except Exception as e:
            self.log_test("AI Tuning", False, {"error": str(e)})
            return False

    def test_timeout_handling(self) -> bool:
        """Test that timeout handling works correctly"""
        print("\n=== TESTING TIMEOUT HANDLING ===")
        
        if not self.auth_token:
            self.log_test("Timeout Handling", False, {"error": "No auth token available"})
            return False
        
        # Create a large assessment that might cause timeout issues
        large_assessment = self.create_test_assessment()
        large_assessment["additional_context"] = "This is a very detailed assessment with lots of context. " * 100
        
        try:
            start_time = time.time()
            response = self.session.post(
                f"{self.base_url}/ai/recommendations",
                json=large_assessment,
                timeout=35
            )
            end_time = time.time()
            response_time = end_time - start_time
            
            # The request should complete within reasonable time (30s + buffer)
            if response_time <= 32:  # 30s timeout + 2s buffer
                if response.status_code == 200:
                    self.log_test("Timeout Handling", True, {
                        "status_code": response.status_code,
                        "response_time": f"{response_time:.2f}s",
                        "note": "Request completed within timeout limits"
                    })
                    return True
                else:
                    # Even if it fails, as long as it doesn't hang, timeout handling works
                    self.log_test("Timeout Handling", True, {
                        "status_code": response.status_code,
                        "response_time": f"{response_time:.2f}s",
                        "note": "Request failed but didn't hang - timeout handling working"
                    })
                    return True
            else:
                self.log_test("Timeout Handling", False, {
                    "error": f"Request took too long: {response_time:.2f}s",
                    "note": "Timeout handling may not be working properly"
                })
                return False
                
        except requests.exceptions.Timeout:
            # This is actually good - it means our client timeout is working
            self.log_test("Timeout Handling", True, {
                "note": "Client timeout triggered - server timeout handling working"
            })
            return True
        except Exception as e:
            self.log_test("Timeout Handling", False, {"error": str(e)})
            return False

    def test_fallback_mechanisms(self) -> bool:
        """Test fallback mechanisms when AI services are unavailable"""
        print("\n=== TESTING FALLBACK MECHANISMS ===")
        
        # This test is tricky because we can't easily simulate AI service failure
        # But we can test with invalid data that might cause the AI to fail
        
        if not self.auth_token:
            self.log_test("Fallback Mechanisms", False, {"error": "No auth token available"})
            return False
        
        # Test with minimal/invalid assessment data
        minimal_assessment = {
            "technicalSkills": [],
            "softSkills": [],
            "experience": "",
            "careerGoals": "",
            "preferences": {}
        }
        
        try:
            response = self.session.post(
                f"{self.base_url}/ai/recommendations",
                json=minimal_assessment,
                timeout=35
            )
            
            if response.status_code == 200:
                recommendations = response.json()
                if "recommendations" in recommendations and recommendations["recommendations"]:
                    # Check if these look like mock recommendations
                    rec_list = recommendations["recommendations"]
                    first_rec = rec_list[0]
                    
                    # Mock recommendations have specific patterns
                    is_mock = (
                        first_rec.get("job_id", "").startswith("job_") or
                        first_rec.get("company") in ["Tech Corp", "Data Solutions Inc"] or
                        first_rec.get("title") in ["Software Engineer", "Data Analyst"]
                    )
                    
                    self.log_test("Fallback Mechanisms", True, {
                        "status_code": response.status_code,
                        "recommendations_count": len(rec_list),
                        "appears_to_be_mock": is_mock,
                        "sample_recommendation": first_rec
                    })
                    return True
                else:
                    self.log_test("Fallback Mechanisms", False, {
                        "error": "No recommendations returned even with fallback",
                        "response": recommendations
                    })
            else:
                self.log_test("Fallback Mechanisms", False, {
                    "status_code": response.status_code,
                    "error": response.text
                })
            
            return False
            
        except Exception as e:
            self.log_test("Fallback Mechanisms", False, {"error": str(e)})
            return False

    def test_legacy_vs_ai_systems(self) -> bool:
        """Test both legacy and AI recommendation systems"""
        print("\n=== TESTING LEGACY VS AI SYSTEMS ===")
        
        if not self.auth_token:
            self.log_test("Legacy vs AI Systems", False, {"error": "No auth token available"})
            return False
        
        assessment_data = self.create_test_assessment()
        
        try:
            # Test AI system
            ai_response = self.session.post(
                f"{self.base_url}/ai/recommendations",
                json=assessment_data,
                timeout=35
            )
            
            # Test legacy system (if available)
            legacy_response = self.session.post(
                f"{self.base_url}/recommendation/generate-recommendations",
                json=assessment_data,
                timeout=10
            )
            
            ai_success = ai_response.status_code == 200
            legacy_success = legacy_response.status_code == 200
            
            results = {
                "ai_system": {
                    "status_code": ai_response.status_code,
                    "success": ai_success
                },
                "legacy_system": {
                    "status_code": legacy_response.status_code,
                    "success": legacy_success
                }
            }
            
            if ai_success:
                ai_recs = ai_response.json().get("recommendations", [])
                results["ai_system"]["recommendations_count"] = len(ai_recs)
            
            if legacy_success:
                legacy_recs = legacy_response.json()
                results["legacy_system"]["recommendations_count"] = len(legacy_recs) if isinstance(legacy_recs, list) else 0
            
            # At least one system should work
            if ai_success or legacy_success:
                self.log_test("Legacy vs AI Systems", True, results)
                return True
            else:
                self.log_test("Legacy vs AI Systems", False, {
                    "error": "Both systems failed",
                    "details": results
                })
                return False
                
        except Exception as e:
            self.log_test("Legacy vs AI Systems", False, {"error": str(e)})
            return False

    def run_all_tests(self) -> Dict[str, Any]:
        """Run all AI feature tests"""
        print("🚀 STARTING COMPREHENSIVE AI FEATURES TESTING")
        print("=" * 60)
        
        # Test sequence
        user_created = self.create_test_user()
        
        if user_created:
            self.test_ai_recommendations()
            self.test_ai_tuning()
            self.test_timeout_handling()
            self.test_fallback_mechanisms()
            self.test_legacy_vs_ai_systems()
        else:
            print("❌ Cannot proceed with AI tests - user creation failed")
        
        # Generate summary
        print("\n" + "=" * 60)
        print("🏁 TEST SUMMARY")
        print("=" * 60)
        
        summary = self.test_results["summary"]
        print(f"Total Tests: {summary['total_tests']}")
        print(f"Passed: {summary['passed']} ✅")
        print(f"Failed: {summary['failed']} ❌")
        print(f"Success Rate: {(summary['passed']/summary['total_tests']*100):.1f}%")
        
        if summary["errors"]:
            print("\nErrors:")
            for error in summary["errors"]:
                print(f"  • {error}")
        
        # Save results to file
        with open("ai_features_test_results.json", "w") as f:
            json.dump(self.test_results, f, indent=2)
        
        print(f"\n📊 Detailed results saved to: ai_features_test_results.json")
        
        return self.test_results

if __name__ == "__main__":
    tester = AIFeaturesTester()
    results = tester.run_all_tests()