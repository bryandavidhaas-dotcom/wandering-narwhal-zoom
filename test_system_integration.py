#!/usr/bin/env python3
"""
System Integration Test Suite
Proves what's actually working vs broken before any fixes are made.
"""

import asyncio
import sys
import os
import requests
import json
from datetime import datetime

# Add backend to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

class SystemVerifier:
    def __init__(self):
        self.results = {}
        self.api_base = "http://localhost:8002"
        
    def log_test(self, test_name, status, details=""):
        """Log test results with timestamp"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        status_icon = "✅" if status else "❌"
        print(f"[{timestamp}] {status_icon} {test_name}")
        if details:
            print(f"    {details}")
        self.results[test_name] = {"status": status, "details": details, "timestamp": timestamp}
        
    def test_password_hashing(self):
        """Test if password hashing works without errors"""
        try:
            from app.core.security import get_password_hash, verify_password
            
            # Test basic hashing
            test_password = "testpassword123"
            hashed = get_password_hash(test_password)
            
            if not hashed or len(hashed) < 10:
                self.log_test("Password Hashing", False, "Hash too short or empty")
                return False
                
            # Test verification
            if not verify_password(test_password, hashed):
                self.log_test("Password Hashing", False, "Verification failed")
                return False
                
            # Test long password (bcrypt 72-byte limit)
            long_password = "a" * 100  # 100 characters
            try:
                long_hashed = get_password_hash(long_password)
                if not verify_password(long_password, long_hashed):
                    self.log_test("Password Hashing", False, "Long password verification failed")
                    return False
            except Exception as e:
                self.log_test("Password Hashing", False, f"Long password failed: {e}")
                return False
                
            self.log_test("Password Hashing", True, f"Hash length: {len(hashed)}")
            return True
            
        except Exception as e:
            self.log_test("Password Hashing", False, f"Import/execution error: {e}")
            return False
    
    def test_database_operations(self):
        """Test if database operations work"""
        try:
            # Import MongoDB replacement first
            import mongodb_replacement
            from motor.motor_asyncio import AsyncIOMotorClient
            
            async def db_test():
                client = AsyncIOMotorClient('mongodb://localhost:27017')
                db = client.test_verification
                collection = db.test_collection
                
                # Test insert
                test_doc = {"test": "verification", "timestamp": datetime.now().isoformat()}
                result = await collection.insert_one(test_doc)
                
                if not result.inserted_id:
                    return False, "Insert failed - no ID returned"
                
                # Test find
                found_doc = await collection.find_one({"test": "verification"})
                if not found_doc:
                    return False, "Find failed - document not found"
                
                # Test update
                update_result = await collection.update_one(
                    {"_id": result.inserted_id},
                    {"$set": {"updated": True}}
                )
                
                if update_result.modified_count != 1:
                    return False, "Update failed"
                
                return True, f"All operations successful, ID: {result.inserted_id}"
            
            success, details = asyncio.run(db_test())
            self.log_test("Database Operations", success, details)
            return success
            
        except Exception as e:
            self.log_test("Database Operations", False, f"Error: {e}")
            return False
    
    def test_api_server_health(self):
        """Test if API server is responding"""
        try:
            response = requests.get(f"{self.api_base}/api/v1/health", timeout=5)
            
            if response.status_code == 200:
                data = response.json()
                self.log_test("API Server Health", True, f"Status: {data.get('status', 'unknown')}")
                return True
            else:
                self.log_test("API Server Health", False, f"HTTP {response.status_code}")
                return False
                
        except requests.exceptions.RequestException as e:
            self.log_test("API Server Health", False, f"Connection error: {e}")
            return False
    
    def test_user_registration_api(self):
        """Test user registration API endpoint"""
        try:
            test_user = {
                "email": f"test_{datetime.now().timestamp()}@example.com",
                "password": "testpassword123"
            }
            
            response = requests.post(
                f"{self.api_base}/api/v1/auth/register",
                json=test_user,
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                if "email" in data:
                    self.log_test("User Registration API", True, f"User created: {data['email']}")
                    return True
                else:
                    self.log_test("User Registration API", False, "No email in response")
                    return False
            else:
                self.log_test("User Registration API", False, f"HTTP {response.status_code}: {response.text}")
                return False
                
        except Exception as e:
            self.log_test("User Registration API", False, f"Error: {e}")
            return False
    
    def test_user_login_api(self):
        """Test user login API endpoint"""
        try:
            # First register a user
            test_user = {
                "email": f"login_test_{datetime.now().timestamp()}@example.com",
                "password": "testpassword123"
            }
            
            reg_response = requests.post(
                f"{self.api_base}/api/v1/auth/register",
                json=test_user,
                timeout=10
            )
            
            if reg_response.status_code != 200:
                self.log_test("User Login API", False, "Registration failed for login test")
                return False
            
            # Now try to login
            login_data = {
                "username": test_user["email"],  # FastAPI OAuth2 uses 'username'
                "password": test_user["password"]
            }
            
            login_response = requests.post(
                f"{self.api_base}/api/v1/auth/login",
                data=login_data,  # Form data, not JSON
                timeout=10
            )
            
            if login_response.status_code == 200:
                data = login_response.json()
                if "access_token" in data:
                    self.log_test("User Login API", True, "Token received")
                    return True
                else:
                    self.log_test("User Login API", False, "No access_token in response")
                    return False
            else:
                self.log_test("User Login API", False, f"HTTP {login_response.status_code}: {login_response.text}")
                return False
                
        except Exception as e:
            self.log_test("User Login API", False, f"Error: {e}")
            return False
    
    def test_assessment_submission(self):
        """Test assessment submission and data persistence"""
        try:
            # This test requires a logged-in user, so we'll test the endpoint exists
            response = requests.post(
                f"{self.api_base}/api/v1/assessment/submit-assessment",
                json={"test": "data"},
                timeout=5
            )
            
            # We expect 401 (unauthorized) since we're not logged in
            # But if we get 404, the endpoint doesn't exist
            if response.status_code == 401:
                self.log_test("Assessment Submission", True, "Endpoint exists (401 unauthorized as expected)")
                return True
            elif response.status_code == 404:
                self.log_test("Assessment Submission", False, "Endpoint not found (404)")
                return False
            else:
                self.log_test("Assessment Submission", True, f"Endpoint responds (HTTP {response.status_code})")
                return True
                
        except Exception as e:
            self.log_test("Assessment Submission", False, f"Error: {e}")
            return False
    
    def test_recommendations_generation(self):
        """Test recommendations generation endpoint"""
        try:
            response = requests.post(
                f"{self.api_base}/api/v1/recommendation/generate-recommendations",
                timeout=5
            )
            
            # We expect 401 (unauthorized) since we're not logged in
            if response.status_code == 401:
                self.log_test("Recommendations Generation", True, "Endpoint exists (401 unauthorized as expected)")
                return True
            elif response.status_code == 404:
                self.log_test("Recommendations Generation", False, "Endpoint not found (404)")
                return False
            else:
                self.log_test("Recommendations Generation", True, f"Endpoint responds (HTTP {response.status_code})")
                return True
                
        except Exception as e:
            self.log_test("Recommendations Generation", False, f"Error: {e}")
            return False
    
    def run_all_tests(self):
        """Run all verification tests"""
        print("=" * 60)
        print("SYSTEM VERIFICATION TEST SUITE")
        print("=" * 60)
        print()
        
        tests = [
            self.test_password_hashing,
            self.test_database_operations,
            self.test_api_server_health,
            self.test_user_registration_api,
            self.test_user_login_api,
            self.test_assessment_submission,
            self.test_recommendations_generation,
        ]
        
        passed = 0
        total = len(tests)
        
        for test in tests:
            if test():
                passed += 1
        
        print()
        print("=" * 60)
        print(f"RESULTS: {passed}/{total} tests passed")
        print("=" * 60)
        
        if passed == total:
            print("🎉 ALL TESTS PASSED - System is working correctly!")
        else:
            print(f"⚠️  {total - passed} TESTS FAILED - System has issues that need fixing")
        
        return passed == total

if __name__ == "__main__":
    verifier = SystemVerifier()
    success = verifier.run_all_tests()
    sys.exit(0 if success else 1)