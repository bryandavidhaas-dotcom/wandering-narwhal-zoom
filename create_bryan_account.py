#!/usr/bin/env python3
"""
Create or update the bryandavidhaas@gmail.com account with the correct password.
"""

import sys
import os
import asyncio

# Add the backend directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

async def create_bryan_account():
    """Create or update Bryan's account with the correct password"""
    try:
        from app.core.security import get_password_hash
        from motor.motor_asyncio import AsyncIOMotorClient
        from datetime import datetime
        import uuid
        
        print("🔧 Creating/updating Bryan's account...")
        
        email = "bryandavidhaas@gmail.com"
        password = "testpassword123"
        
        # Hash the password using our fixed bcrypt implementation
        hashed_password = get_password_hash(password)
        print(f"✅ Password hashed successfully: {hashed_password[:20]}...")
        
        # Connect to database
        database_url = "mongodb://localhost:27017"
        client = AsyncIOMotorClient(database_url)
        db = client["recommender"]
        users_collection = db.users
        
        # Check if user exists
        existing_user = await users_collection.find_one({"email": email})
        
        if existing_user:
            print(f"👤 User {email} already exists, updating password...")
            
            # Update the existing user's password
            result = await users_collection.update_one(
                {"email": email},
                {
                    "$set": {
                        "hashed_password": hashed_password,
                        "updated_at": datetime.utcnow()
                    }
                }
            )
            
            if result.modified_count > 0:
                print("✅ User password updated successfully!")
            else:
                print("⚠️  No changes made to user")
        else:
            print(f"👤 Creating new user {email}...")
            
            # Create new user
            user_data = {
                "_id": str(uuid.uuid4()),
                "email": email,
                "hashed_password": hashed_password,
                "created_at": datetime.utcnow()
            }
            
            result = await users_collection.insert_one(user_data)
            
            if result.inserted_id:
                print("✅ User created successfully!")
            else:
                print("❌ Failed to create user")
                return False
        
        # Close the connection
        client.close()
        
        print(f"\n🎉 Bryan's account is ready!")
        print(f"   Email: {email}")
        print(f"   Password: {password}")
        
        return True
        
    except Exception as e:
        print(f"❌ Failed to create/update Bryan's account: {e}")
        import traceback
        traceback.print_exc()
        return False

async def test_bryan_login():
    """Test login with Bryan's account"""
    try:
        import requests
        import json
        
        print(f"\n🔐 Testing login with Bryan's account...")
        
        url = "http://localhost:8002/api/v1/auth/login"
        data = {
            "username": "bryandavidhaas@gmail.com",
            "password": "testpassword123"
        }
        
        response = requests.post(url, data=data, timeout=10)
        print(f"🔍 Status Code: {response.status_code}")
        
        if response.status_code == 200:
            response_json = response.json()
            print("✅ Bryan's login successful!")
            print(f"🔑 Access token received: {response_json.get('access_token', 'N/A')[:20]}...")
            return True
        else:
            try:
                error_json = response.json()
                print(f"❌ Login failed: {error_json.get('detail', 'Unknown error')}")
            except:
                print(f"❌ Login failed: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Login test failed: {e}")
        return False

async def main():
    print("🚀 Setting up Bryan's account...")
    print("=" * 50)
    
    # Step 1: Create/update account
    account_success = await create_bryan_account()
    
    if not account_success:
        print("❌ Failed to set up account")
        return
    
    # Step 2: Test login
    login_success = await test_bryan_login()
    
    print("\n" + "=" * 50)
    print("🏁 FINAL RESULT:")
    
    if account_success and login_success:
        print("🎉 SUCCESS! Bryan's account is fully functional!")
        print("✅ Account created/updated with correct password")
        print("✅ Login works perfectly")
        print(f"\n📧 Email: bryandavidhaas@gmail.com")
        print(f"🔑 Password: testpassword123")
    else:
        print("❌ There were issues setting up the account")

if __name__ == "__main__":
    asyncio.run(main())