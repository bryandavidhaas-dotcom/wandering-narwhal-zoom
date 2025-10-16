#!/usr/bin/env python3
"""
Register a user via the API
"""

import requests
import json

def register_user():
    url = "http://localhost:8002/api/v1/auth/register"
    data = {
        "email": "bryandavidhaas@gmail.com",
        "password": "testpassword123"
    }
    
    headers = {
        "Content-Type": "application/json"
    }
    
    try:
        print("🔧 Registering user via API...")
        response = requests.post(url, json=data, headers=headers)
        
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 200:
            print("✅ User registered successfully!")
        else:
            print("❌ Registration failed")
            
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    register_user()