#!/usr/bin/env python3
"""
Test script to test the new server on a different port
"""
import sys
import os
import asyncio
import requests
import json

sys.path.append('./backend')

async def test_new_server():
    """Test the new server directly"""
    print("🔍 Testing new server on port 8003...")
    
    # Test data
    test_user = {
        "email": "bryandavidhaas@gmail.com",
        "password": "testpassword123"
    }
    
    try:
        # Make request to registration endpoint on port 8003
        response = requests.post(
            "http://localhost:8003/api/v1/auth/register",
            json=test_user,
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        
        print(f"📊 Registration response status: {response.status_code}")
        print(f"📊 Registration response: {response.text}")
        
        if response.status_code == 200:
            print("✅ Registration successful!")
            return True
        else:
            print(f"❌ Registration failed with status {response.status_code}")
            return False
            
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to backend server on port 8003")
        print("🔧 Server not running on port 8003")
        return False
    except Exception as e:
        print(f"❌ Registration test failed: {e}")
        return False

if __name__ == "__main__":
    success = asyncio.run(test_new_server())
    if success:
        print("🎉 New server test passed!")
    else:
        print("💥 New server test failed!")