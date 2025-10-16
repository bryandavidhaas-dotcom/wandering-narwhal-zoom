#!/usr/bin/env python3
"""
Comprehensive Authentication Test Suite
Tests all authentication use cases with exact credentials and provides proof
"""

import requests
import json
import sys
from datetime import datetime

# Test configuration
BASE_URL = "http://localhost:8000/api/v1"
TEST_USERS = [
    {
        "email": "test1@example.com",
        "password": "TestPassword123!",
        "name": "Test User 1"
    },
    {
        "email": "test2@example.com", 
        "password": "SecurePass456!",
        "name": "Test User 2"
    }
]

def print_header(title):
    print(f"\n{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}")

def print_test_result(test_name, success, details=""):
    status = "✅ PASS" if success else "❌ FAIL"
    print(f"{status} {test_name}")
    if details:
        print(f"    {details}")

def test_user_registration():
    """Test user registration functionality"""
    print_header("TESTING USER REGISTRATION")
    
    for i, user in enumerate(TEST_USERS, 1):
        print(f"\n--- Test {i}: Registering {user['email']} ---")
        
        try:
            response = requests.post(
                f"{BASE_URL}/auth/register",
                json={
                    "email": user["email"],
                    "password": user["password"]
                },
                headers={"Content-Type": "application/json"}
            )
            
            print(f"Request URL: {response.url}")
            print(f"Request Data: {json.dumps({'email': user['email'], 'password': '***'})}")
            print(f"Response Status: {response.status_code}")
            print(f"Response Headers: {dict(response.headers)}")
            
            if response.status_code == 200:
                data = response.json()
                print(f"Response Data: {json.dumps(data, indent=2)}")
                print_test_result(f"Register {user['email']}", True, f"User created successfully")
                user['registered'] = True
            else:
                print(f"Response Text: {response.text}")
                print_test_result(f"Register {user['email']}", False, f"Status {response.status_code}: {response.text}")
                user['registered'] = False
                
        except Exception as e:
            print_test_result(f"Register {user['email']}", False, f"Exception: {str(e)}")
            user['registered'] = False

def test_user_login():
    """Test user login functionality"""
    print_header("TESTING USER LOGIN")
    
    for i, user in enumerate(TEST_USERS, 1):
        if not user.get('registered', False):
            print(f"--- Test {i}: Skipping login for {user['email']} (not registered) ---")
            continue
            
        print(f"\n--- Test {i}: Logging in {user['email']} ---")
        
        try:
            # FastAPI OAuth2PasswordRequestForm expects form data, not JSON
            response = requests.post(
                f"{BASE_URL}/auth/login",
                data={
                    "username": user["email"],  # OAuth2 uses 'username' field
                    "password": user["password"]
                },
                headers={"Content-Type": "application/x-www-form-urlencoded"}
            )
            
            print(f"Request URL: {response.url}")
            print(f"Request Data: username={user['email']}, password=***")
            print(f"Response Status: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                print(f"Response Data: {json.dumps(data, indent=2)}")
                user['access_token'] = data.get('access_token')
                print_test_result(f"Login {user['email']}", True, f"Token received: {user['access_token'][:20]}...")
            else:
                print(f"Response Text: {response.text}")
                print_test_result(f"Login {user['email']}", False, f"Status {response.status_code}: {response.text}")
                
        except Exception as e:
            print_test_result(f"Login {user['email']}", False, f"Exception: {str(e)}")

def test_password_reset():
    """Test password reset functionality"""
    print_header("TESTING PASSWORD RESET")
    
    # Test with first registered user
    test_user = None
    for user in TEST_USERS:
        if user.get('registered', False):
            test_user = user
            break
    
    if not test_user:
        print_test_result("Password Reset", False, "No registered users available for testing")
        return
    
    print(f"\n--- Testing password reset for {test_user['email']} ---")
    
    # Step 1: Request password reset
    try:
        response = requests.post(
            f"{BASE_URL}/auth/forgot-password",
            json={"email": test_user["email"]},
            headers={"Content-Type": "application/json"}
        )
        
        print(f"Reset Request URL: {response.url}")
        print(f"Reset Request Data: {json.dumps({'email': test_user['email']})}")
        print(f"Reset Response Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"Reset Response Data: {json.dumps(data, indent=2)}")
            reset_token = data.get('reset_token')
            
            if reset_token:
                print_test_result("Password Reset Request", True, f"Reset token received: {reset_token[:20]}...")
                
                # Step 2: Use reset token to change password
                new_password = "NewPassword789!"
                reset_response = requests.post(
                    f"{BASE_URL}/auth/reset-password",
                    json={
                        "token": reset_token,
                        "new_password": new_password
                    },
                    headers={"Content-Type": "application/json"}
                )
                
                print(f"Password Change Status: {reset_response.status_code}")
                print(f"Password Change Response: {reset_response.text}")
                
                if reset_response.status_code == 200:
                    print_test_result("Password Reset Complete", True, "Password changed successfully")
                    
                    # Step 3: Test login with new password
                    login_response = requests.post(
                        f"{BASE_URL}/auth/login",
                        data={
                            "username": test_user["email"],
                            "password": new_password
                        },
                        headers={"Content-Type": "application/x-www-form-urlencoded"}
                    )
                    
                    if login_response.status_code == 200:
                        print_test_result("Login with New Password", True, "Login successful with new password")
                    else:
                        print_test_result("Login with New Password", False, f"Status {login_response.status_code}")
                else:
                    print_test_result("Password Reset Complete", False, f"Status {reset_response.status_code}")
            else:
                print_test_result("Password Reset Request", False, "No reset token in response")
        else:
            print(f"Reset Response Text: {response.text}")
            print_test_result("Password Reset Request", False, f"Status {response.status_code}")
            
    except Exception as e:
        print_test_result("Password Reset", False, f"Exception: {str(e)}")

def main():
    print_header("COMPREHENSIVE AUTHENTICATION TEST SUITE")
    print(f"Testing against: {BASE_URL}")
    print(f"Test started at: {datetime.now().isoformat()}")
    
    # Test all authentication use cases
    test_user_registration()
    test_user_login()
    test_password_reset()
    
    # Summary
    print_header("TEST SUMMARY")
    print("Exact credentials tested:")
    for user in TEST_USERS:
        status = "✅ Registered" if user.get('registered', False) else "❌ Failed"
        print(f"  Email: {user['email']}")
        print(f"  Password: {user['password']}")
        print(f"  Status: {status}")
        if user.get('access_token'):
            print(f"  Token: {user['access_token'][:30]}...")
        print()

if __name__ == "__main__":
    main()