#!/usr/bin/env python3
"""
Create user account script for bryandavidhaas@gmail.com
This script will create the user account with proper password hashing
"""
import asyncio
import os
import sys
from motor.motor_asyncio import AsyncIOMotorClient
from passlib.context import CryptContext
from dotenv import load_dotenv
from datetime import datetime

# Load environment variables
load_dotenv('backend/.env')

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

async def create_user_account():
    """Create user account for bryandavidhaas@gmail.com"""
    
    print("Creating User Account")
    print("=" * 50)
    
    # Get connection details
    mongodb_url = os.getenv('MONGODB_URL', 'mongodb://localhost:27017')
    mongodb_database = os.getenv('MONGODB_DATABASE', 'career_platform')
    
    print(f"MongoDB URL: {mongodb_url}")
    print(f"Database: {mongodb_database}")
    
    try:
        # Connect to MongoDB
        client = AsyncIOMotorClient(mongodb_url, serverSelectionTimeoutMS=5000)
        await client.admin.command('ping')
        print("✅ Connected to MongoDB")
        
        # Get database and users collection
        db = client[mongodb_database]
        users_collection = db.users
        
        # User details
        email = "bryandavidhaas@gmail.com"
        temporary_password = "TempPass123!"  # User should change this
        
        # Check if user already exists
        existing_user = await users_collection.find_one({"email": email})
        if existing_user:
            print(f"⚠️  User {email} already exists")
            print(f"   User ID: {existing_user['_id']}")
            print(f"   Created: {existing_user.get('created_at', 'Unknown')}")
            
            # Ask if we should update the password
            print(f"\n🔄 Updating password for existing user...")
            hashed_password = pwd_context.hash(temporary_password)
            
            await users_collection.update_one(
                {"email": email},
                {
                    "$set": {
                        "password": hashed_password,
                        "updated_at": datetime.utcnow(),
                        "password_reset_required": True
                    }
                }
            )
            print(f"✅ Password updated for {email}")
            
        else:
            # Create new user
            print(f"👤 Creating new user: {email}")
            
            # Hash the temporary password
            hashed_password = pwd_context.hash(temporary_password)
            
            # Create user document
            user_doc = {
                "email": email,
                "password": hashed_password,
                "first_name": "Bryan",
                "last_name": "Haas",
                "is_active": True,
                "is_verified": True,
                "password_reset_required": True,
                "created_at": datetime.utcnow(),
                "updated_at": datetime.utcnow(),
                "profile": {
                    "preferences": {},
                    "skills": [],
                    "experience_level": "experienced",
                    "career_interests": []
                }
            }
            
            # Insert user
            result = await users_collection.insert_one(user_doc)
            print(f"✅ User created with ID: {result.inserted_id}")
        
        # Verify user creation/update
        user = await users_collection.find_one({"email": email})
        if user:
            print(f"\n📋 User Details:")
            print(f"   Email: {user['email']}")
            print(f"   Name: {user.get('first_name', '')} {user.get('last_name', '')}")
            print(f"   Active: {user.get('is_active', False)}")
            print(f"   Verified: {user.get('is_verified', False)}")
            print(f"   Password Reset Required: {user.get('password_reset_required', False)}")
            print(f"   Created: {user.get('created_at', 'Unknown')}")
        
        print(f"\n🔑 Temporary Password: {temporary_password}")
        print("⚠️  User should change this password on first login")
        
        client.close()
        return True
        
    except Exception as e:
        print(f"❌ Error creating user account: {e}")
        return False

def verify_password_hash():
    """Test password hashing functionality"""
    print("\n🔐 Testing Password Hashing")
    print("=" * 50)
    
    test_password = "TempPass123!"
    hashed = pwd_context.hash(test_password)
    
    print(f"Original: {test_password}")
    print(f"Hashed: {hashed}")
    
    # Verify the hash
    is_valid = pwd_context.verify(test_password, hashed)
    print(f"Verification: {'✅ PASS' if is_valid else '❌ FAIL'}")
    
    return is_valid

async def main():
    print("User Account Creation Script")
    print("=" * 50)
    
    # Test password hashing first
    if not verify_password_hash():
        print("❌ Password hashing test failed")
        return 1
    
    # Create user account
    success = await create_user_account()
    
    if success:
        print("\n🎉 User account setup completed!")
        print("Next steps:")
        print("1. User can log in with bryandavidhaas@gmail.com")
        print("2. Use temporary password: TempPass123!")
        print("3. User should change password on first login")
        return 0
    else:
        print("\n❌ User account creation failed")
        return 1

if __name__ == "__main__":
    exit_code = asyncio.run(main())
    exit(exit_code)