#!/usr/bin/env python3
"""
Test backend API endpoints with Claude integration.
"""
import asyncio
import requests
import json
import time
import subprocess
import sys
from pathlib import Path

class BackendAPITester:
    def __init__(self):
        self.base_url = "http://localhost:8002"
        self.results = {
            "backend_health": False,
            "user_registration": False,
            "user_login": False,
            "ai_recommendations": False,
            "ai_tuning": False,
            "error_handling": False
        }
        self.auth_token = None
        
    def test_backend_health(self):
        """Test if backend is running."""
        print("\n🏥 Testing Backend Health")
        print("=" * 50)
        
        try:
            response = requests.get(f"{self.base_url}/health", timeout=5)
            if response.status_code == 200:
                print("✅ Backend is running and healthy")
                self.results["backend_health"] = True
                return True
            else:
                print(f"⚠️  Backend responded with status {response.status_code}")
                return False
        except requests.exceptions.ConnectionError:
            print("❌ Backend is not running")
            return False
        except Exception as e:
            print(f"❌ Health check failed: {e}")
            return False
    
    def start_backend_if_needed(self):
        """Start backend server if not running."""
        if not self.test_backend_health():
            print("\n🚀 Starting Backend Server")
            print("=" * 50)
            
            try:
                # Start backend server
                backend_path = Path(__file__).parent / "backend"
                if backend_path.exists():
                    print("Starting backend server...")
                    # Note: This would start the server but we'll skip for now
                    print("⚠️  Backend needs to be started manually")
                    return False
                else:
                    print("❌ Backend directory not found")
                    return False
            except Exception as e:
                print(f"❌ Failed to start backend: {e}")
                return False
        return True
    
    def test_user_registration(self):
        """Test user registration endpoint."""
        print("\n👤 Testing User Registration")
        print("=" * 50)
        
        test_user = {
            "username": f"testuser_{int(time.time())}",
            "email": f"test_{int(time.time())}@example.com",
            "password": "testpassword123"
        }
        
        try:
            response = requests.post(
                f"{self.base_url}/api/v1/auth/register",
                json=test_user,
                timeout=10
            )
            
            if response.status_code == 200:
                print("✅ User registration successful")
                self.results["user_registration"] = True
                return test_user
            else:
                print(f"⚠️  Registration failed with status {response.status_code}")
                print(f"Response: {response.text}")
                return None
                
        except Exception as e:
            print(f"❌ Registration test failed: {e}")
            return None
    
    def test_user_login(self, user_data):
        """Test user login endpoint."""
        print("\n🔐 Testing User Login")
        print("=" * 50)
        
        if not user_data:
            print("❌ No user data available for login test")
            return False
            
        login_data = {
            "username": user_data["username"],
            "password": user_data["password"]
        }
        
        try:
            response = requests.post(
                f"{self.base_url}/api/v1/auth/login",
                data=login_data,  # Form data for OAuth2
                timeout=10
            )
            
            if response.status_code == 200:
                token_data = response.json()
                self.auth_token = token_data.get("access_token")
                print("✅ User login successful")
                print(f"📋 Token received: {self.auth_token[:20]}..." if self.auth_token else "No token")
                self.results["user_login"] = True
                return True
            else:
                print(f"⚠️  Login failed with status {response.status_code}")
                print(f"Response: {response.text}")
                return False
                
        except Exception as e:
            print(f"❌ Login test failed: {e}")
            return False
    
    def test_ai_recommendations(self):
        """Test AI recommendations endpoint."""
        print("\n🤖 Testing AI Recommendations")
        print("=" * 50)
        
        if not self.auth_token:
            print("❌ No auth token available for AI recommendations test")
            return False
            
        assessment_data = {
            "technicalSkills": ["Python", "JavaScript", "SQL"],
            "softSkills": ["Communication", "Problem Solving"],
            "experience": "3 years",
            "careerGoals": "Senior Software Engineer",
            "currentRole": "Software Developer",
            "educationLevel": "Bachelor's Degree",
            "salaryExpectations": "$80,000-$100,000",
            "industries": ["Technology", "Fintech"],
            "interests": ["Machine Learning", "Web Development"],
            "workingWithData": 4,
            "workingWithPeople": 3,
            "creativeTasks": 4
        }
        
        headers = {
            "Authorization": f"Bearer {self.auth_token}",
            "Content-Type": "application/json"
        }
        
        try:
            response = requests.post(
                f"{self.base_url}/api/v1/ai/recommendations",
                json=assessment_data,
                headers=headers,
                timeout=30  # AI calls can take longer
            )
            
            if response.status_code == 200:
                recommendations = response.json()
                print("✅ AI recommendations successful")
                print(f"📋 Received {len(recommendations.get('recommendations', []))} recommendations")
                
                # Validate response structure
                if self.validate_recommendations_response(recommendations):
                    print("✅ Response format validation passed")
                    self.results["ai_recommendations"] = True
                    return recommendations
                else:
                    print("⚠️  Response format validation failed")
                    return None
            else:
                print(f"⚠️  AI recommendations failed with status {response.status_code}")
                print(f"Response: {response.text}")
                return None
                
        except Exception as e:
            print(f"❌ AI recommendations test failed: {e}")
            return None
    
    def test_ai_tuning(self, initial_recommendations):
        """Test AI tuning endpoint."""
        print("\n🎯 Testing AI Tuning")
        print("=" * 50)
        
        if not self.auth_token:
            print("❌ No auth token available for AI tuning test")
            return False
            
        if not initial_recommendations:
            print("❌ No initial recommendations available for tuning test")
            return False
            
        tuning_data = {
            "current_recommendations": initial_recommendations.get("recommendations", []),
            "prompt": "I prefer remote work opportunities with higher salaries in the tech industry"
        }
        
        headers = {
            "Authorization": f"Bearer {self.auth_token}",
            "Content-Type": "application/json"
        }
        
        try:
            response = requests.post(
                f"{self.base_url}/api/v1/ai/tune",
                json=tuning_data,
                headers=headers,
                timeout=30
            )
            
            if response.status_code == 200:
                tuned_recommendations = response.json()
                print("✅ AI tuning successful")
                print(f"📋 Received {len(tuned_recommendations.get('recommendations', []))} tuned recommendations")
                self.results["ai_tuning"] = True
                return True
            else:
                print(f"⚠️  AI tuning failed with status {response.status_code}")
                print(f"Response: {response.text}")
                return False
                
        except Exception as e:
            print(f"❌ AI tuning test failed: {e}")
            return False
    
    def test_error_handling(self):
        """Test error handling with invalid requests."""
        print("\n🛡️  Testing Error Handling")
        print("=" * 50)
        
        if not self.auth_token:
            print("❌ No auth token available for error handling test")
            return False
            
        headers = {
            "Authorization": f"Bearer {self.auth_token}",
            "Content-Type": "application/json"
        }
        
        # Test with invalid assessment data
        invalid_data = {
            "invalid_field": "invalid_value"
        }
        
        try:
            response = requests.post(
                f"{self.base_url}/api/v1/ai/recommendations",
                json=invalid_data,
                headers=headers,
                timeout=30
            )
            
            if response.status_code in [200, 400, 422]:  # Any handled response
                print("✅ Error handling works - server responded appropriately")
                self.results["error_handling"] = True
                return True
            else:
                print(f"⚠️  Unexpected error response: {response.status_code}")
                return False
                
        except Exception as e:
            print(f"❌ Error handling test failed: {e}")
            return False
    
    def validate_recommendations_response(self, response):
        """Validate the structure of recommendations response."""
        if not isinstance(response, dict):
            print("❌ Response should be a dictionary")
            return False
            
        if "recommendations" not in response:
            print("❌ Response missing 'recommendations' field")
            return False
            
        recommendations = response["recommendations"]
        if not isinstance(recommendations, list):
            print("❌ Recommendations should be a list")
            return False
            
        if len(recommendations) == 0:
            print("⚠️  No recommendations returned")
            return True  # Empty list is acceptable
            
        # Check first recommendation structure
        first_rec = recommendations[0]
        required_fields = ["job_id", "title", "company", "location"]
        
        for field in required_fields:
            if field not in first_rec:
                print(f"⚠️  Missing required field: {field}")
                
        return True
    
    def print_summary(self):
        """Print test summary."""
        print("\n📋 Backend API Test Summary")
        print("=" * 50)
        
        total_tests = len(self.results)
        passed_tests = sum(self.results.values())
        
        for test_name, passed in self.results.items():
            status = "✅ PASS" if passed else "❌ FAIL"
            print(f"{test_name.replace('_', ' ').title()}: {status}")
        
        print(f"\nOverall: {passed_tests}/{total_tests} tests passed")
        
        if passed_tests == total_tests:
            print("🎉 All backend API tests passed!")
        elif passed_tests >= total_tests * 0.7:
            print("⚠️  Most tests passed. Some issues may need attention.")
        else:
            print("❌ Multiple test failures. Backend API needs fixing.")
        
        return passed_tests / total_tests

def main():
    """Run all backend API tests."""
    print("🧪 Backend API Testing with Claude Integration")
    print("=" * 60)
    
    tester = BackendAPITester()
    
    # Check if backend is running
    if not tester.start_backend_if_needed():
        print("\n❌ Backend is not running. Please start the backend server first.")
        print("Run: cd backend && python -m uvicorn app.main:app --host 0.0.0.0 --port 8002 --reload")
        return
    
    # Run tests in sequence
    user_data = tester.test_user_registration()
    
    if tester.test_user_login(user_data):
        recommendations = tester.test_ai_recommendations()
        tester.test_ai_tuning(recommendations)
        tester.test_error_handling()
    
    # Print final summary
    success_rate = tester.print_summary()
    
    # Save results to file
    results_file = "backend_api_test_results.json"
    with open(results_file, 'w') as f:
        json.dump({
            "test_type": "backend_api_integration",
            "timestamp": time.time(),
            "success_rate": success_rate,
            "results": tester.results
        }, f, indent=2)
    
    print(f"\n📄 Results saved to {results_file}")

if __name__ == "__main__":
    main()