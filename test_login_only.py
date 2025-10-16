#!/usr/bin/env python3
"""
Test login functionality with existing user credentials.
"""

import requests
import json

def test_login():
    """Test login with existing credentials"""
    try:
        print("🔧 Testing login endpoint with existing user...")
        
        url = "http://localhost:8002/api/v1/auth/login"
        data = {
            "username": "bryandavidhaas@gmail.com",
            "password": "testpassword123"
        }
        
        print(f"🔍 POST {url}")
        print(f"🔍 Data: {data}")
        
        response = requests.post(url, data=data, timeout=10)
        print(f"🔍 Status Code: {response.status_code}")
        print(f"🔍 Response Headers: {dict(response.headers)}")
        
        try:
            response_json = response.json()
            print(f"🔍 Response JSON: {json.dumps(response_json, indent=2)}")
        except:
            print(f"🔍 Response Text: {response.text}")
        
        if response.status_code == 200:
            print("✅ Login successful!")
            
            # Test accessing protected endpoint
            if 'access_token' in response_json:
                token = response_json['access_token']
                print(f"\n🔧 Testing protected endpoint with token...")
                
                headers = {"Authorization": f"Bearer {token}"}
                me_url = "http://localhost:8002/api/v1/auth/users/me"
                
                me_response = requests.get(me_url, headers=headers, timeout=10)
                print(f"🔍 GET {me_url}")
                print(f"🔍 Status Code: {me_response.status_code}")
                
                try:
                    me_json = me_response.json()
                    print(f"🔍 User Info: {json.dumps(me_json, indent=2)}")
                except:
                    print(f"🔍 Response Text: {me_response.text}")
                
                if me_response.status_code == 200:
                    print("✅ Protected endpoint access successful!")
                    return True
                else:
                    print("❌ Protected endpoint access failed")
                    return False
            else:
                print("⚠️  No access token in response")
                return False
        else:
            print(f"❌ Login failed with status {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Login test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    print("🚀 Testing login functionality...")
    print("=" * 50)
    
    success = test_login()
    
    print("\n" + "=" * 50)
    if success:
        print("🎉 Authentication system is fully functional!")
        print("✅ User can login and access protected endpoints")
    else:
        print("❌ Authentication system has issues")

if __name__ == "__main__":
    main()