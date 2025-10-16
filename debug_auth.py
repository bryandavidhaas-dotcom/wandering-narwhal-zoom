#!/usr/bin/env python3
"""
Authentication Debug Script
Diagnoses login issues for bryandavidhaas@gmail.com
"""

import asyncio
import os
import sys
from pathlib import Path

# Add backend to path
backend_path = Path(__file__).parent / "backend"
sys.path.insert(0, str(backend_path))

from dotenv import load_dotenv
from motor.motor_asyncio import AsyncIOMotorClient

# Load environment variables
load_dotenv(backend_path / ".env")

async def diagnose_auth_issue():
    print("🔍 AUTHENTICATION DIAGNOSIS")
    print("=" * 50)
    
    # 1. Check environment configuration
    print("\n1. ENVIRONMENT CONFIGURATION:")
    database_url = os.getenv("DATABASE_URL")
    mongodb_url = os.getenv("MONGODB_URL") 
    jwt_secret = os.getenv("JWT_SECRET_KEY")
    
    print(f"   DATABASE_URL: {database_url}")
    print(f"   MONGODB_URL: {mongodb_url}")
    print(f"   JWT_SECRET_KEY: {'✅ Set' if jwt_secret else '❌ Missing'}")
    
    # 2. Test database connectivity
    print("\n2. DATABASE CONNECTIVITY:")
    try:
        # Use the correct connection string
        conn_str = database_url or mongodb_url or "mongodb://localhost:27017"
        print(f"   Connecting to: {conn_str}")
        
        client = AsyncIOMotorClient(conn_str)
        
        # Test connection
        await client.admin.command("ping")
        print("   ✅ MongoDB connection successful")
        
        # Check database and collection
        db = client["recommender"]  # This matches main.py
        collections = await db.list_collection_names()
        print(f"   Collections: {collections}")
        
        # 3. Check user account
        print("\n3. USER ACCOUNT STATUS:")
        user = await db.users.find_one({"email": "bryandavidhaas@gmail.com"})
        
        if user:
            print("   ✅ User account found")
            print(f"   Email: {user.get('email')}")
            print(f"   Created: {user.get('created_at')}")
            print(f"   Fields: {list(user.keys())}")
            
            # Check password field inconsistency
            has_password = "password" in user
            has_hashed_password = "hashed_password" in user
            print(f"   Has 'password' field: {has_password}")
            print(f"   Has 'hashed_password' field: {has_hashed_password}")
            
            if has_password and has_hashed_password:
                print("   ⚠️  ISSUE: User has both 'password' and 'hashed_password' fields")
            elif not has_password and not has_hashed_password:
                print("   ❌ CRITICAL: User has no password field at all")
            elif has_password:
                print("   ✅ User has 'password' field")
            elif has_hashed_password:
                print("   ✅ User has 'hashed_password' field")
                
        else:
            print("   ❌ User account NOT FOUND")
            
            # List all users to see what exists
            all_users = await db.users.find({}).to_list(length=20)
            print(f"   Total users in database: {len(all_users)}")
            if all_users:
                print("   Existing users:")
                for u in all_users[:5]:  # Show first 5
                    print(f"     - {u.get('email', 'no email')}")
        
        # 4. Test password verification
        print("\n4. PASSWORD VERIFICATION TEST:")
        if user:
            try:
                # Import password verification
                from app.core.security import verify_password
                
                password_field = user.get("password") or user.get("hashed_password")
                if password_field:
                    print("   Password field found, ready for verification test")
                    print("   (Actual password verification would happen during login)")
                else:
                    print("   ❌ No password field to verify against")
                    
            except ImportError as e:
                print(f"   ❌ Cannot import security module: {e}")
        
        await client.close()
        
    except Exception as e:
        print(f"   ❌ Database connection failed: {e}")
        return
    
    # 5. Check authentication endpoint
    print("\n5. AUTHENTICATION ENDPOINT CHECK:")
    try:
        from app.api.v1.endpoints.auth import router
        print("   ✅ Auth router imported successfully")
        
        # Check if the login endpoint exists
        routes = [route.path for route in router.routes]
        print(f"   Available auth routes: {routes}")
        
    except ImportError as e:
        print(f"   ❌ Cannot import auth router: {e}")
    
    print("\n" + "=" * 50)
    print("DIAGNOSIS COMPLETE")

if __name__ == "__main__":
    asyncio.run(diagnose_auth_issue())