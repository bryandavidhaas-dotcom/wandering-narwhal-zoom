#!/usr/bin/env python3
"""
Authentication Debug Script
Test the authentication system directly
"""

import asyncio
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

# Import MongoDB replacement BEFORE motor
try:
    import mongodb_replacement
    print("🔧 MongoDB replacement loaded successfully")
except ImportError as e:
    print(f"⚠️  MongoDB replacement not found: {e}")

from motor.motor_asyncio import AsyncIOMotorClient
from passlib.context import CryptContext
from app.core.security import verify_password

async def test_auth():
    print("🔍 AUTHENTICATION DEBUG")
    print("=" * 50)
    
    # Connect to database
    database_url = "mongodb://localhost:27017"
    client = AsyncIOMotorClient(database_url)
    db = client["recommender"]
    
    print(f"📊 Connected to database: {database_url}")
    
    # Check all users
    users = await db.users.find({}).to_list(length=None)
    print(f"\n👥 Found {len(users)} users in database:")
    
    for i, user in enumerate(users, 1):
        print(f"\n--- User {i} ---")
        print(f"Email: {user.get('email', 'N/A')}")
        print(f"ID: {user.get('_id', 'N/A')}")
        print(f"Full Name: {user.get('full_name', 'N/A')}")
        print(f"Is Active: {user.get('is_active', 'N/A')}")
        print(f"Has 'password' field: {'password' in user}")
        print(f"Has 'hashed_password' field: {'hashed_password' in user}")
        
        # Test password verification
        if user.get('email') == 'bryandavidhaas@gmail.com':
            print(f"\n🔐 Testing password verification for {user['email']}:")
            
            # Get the password field
            password_field = user.get("password") or user.get("hashed_password")
            if password_field:
                print(f"Password field found: {password_field[:20]}...")
                
                # Test with both possible passwords
                test_passwords = ["testpassword123", "TempPass123!"]
                for test_pwd in test_passwords:
                    try:
                        is_valid = verify_password(test_pwd, password_field)
                        print(f"Password '{test_pwd}': {'✅ VALID' if is_valid else '❌ INVALID'}")
                    except Exception as e:
                        print(f"Password '{test_pwd}': ❌ ERROR - {e}")
            else:
                print("❌ No password field found!")
    
    # Test creating a new user with correct password
    print(f"\n🔧 Creating test user with correct password...")
    
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    hashed_password = pwd_context.hash("testpassword123")
    
    # Check if user already exists
    existing_user = await db.users.find_one({"email": "test@example.com"})
    if existing_user:
        await db.users.delete_one({"email": "test@example.com"})
        print("🗑️ Removed existing test user")
    
    test_user = {
        "email": "test@example.com",
        "hashed_password": hashed_password,
        "full_name": "Test User",
        "is_active": True
    }
    
    await db.users.insert_one(test_user)
    print("✅ Test user created")
    
    # Verify the test user
    created_user = await db.users.find_one({"email": "test@example.com"})
    if created_user:
        password_field = created_user.get("hashed_password")
        is_valid = verify_password("testpassword123", password_field)
        print(f"Test user password verification: {'✅ VALID' if is_valid else '❌ INVALID'}")
    
    client.close()

if __name__ == "__main__":
    asyncio.run(test_auth())