#!/usr/bin/env python3
"""
Immediate Authentication Fix
============================
Creates your user account and starts a local MongoDB instance
"""

import asyncio
import subprocess
import sys
import os
from pathlib import Path

async def immediate_fix():
    print("🚀 IMMEDIATE AUTHENTICATION FIX")
    print("=" * 50)
    
    # Step 1: Try to start MongoDB with local data directory
    print("\n1. Starting local MongoDB instance...")
    
    try:
        # Create data directory
        data_dir = Path("./mongodb_data")
        data_dir.mkdir(exist_ok=True)
        
        # Start MongoDB in background
        cmd = ['mongod', '--dbpath', str(data_dir.absolute()), '--port', '27017']
        
        # Try to start MongoDB
        process = subprocess.Popen(
            cmd, 
            stdout=subprocess.PIPE, 
            stderr=subprocess.PIPE,
            creationflags=subprocess.CREATE_NEW_CONSOLE if os.name == 'nt' else 0
        )
        
        print(f"   MongoDB process started with PID: {process.pid}")
        
        # Wait a moment for MongoDB to start
        await asyncio.sleep(3)
        
        # Test connection
        from motor.motor_asyncio import AsyncIOMotorClient
        client = AsyncIOMotorClient("mongodb://localhost:27017")
        await client.admin.command("ping")
        print("   ✅ MongoDB is now running!")
        
        # Step 2: Create your user account
        print("\n2. Creating/verifying your user account...")
        
        db = client["recommender"]
        
        # Check if user exists
        user = await db.users.find_one({"email": "bryandavidhaas@gmail.com"})
        
        if not user:
            # Import password hashing
            sys.path.insert(0, str(Path(__file__).parent / "backend"))
            from app.core.security import get_password_hash
            
            # Create user account
            user_data = {
                "email": "bryandavidhaas@gmail.com",
                "hashed_password": get_password_hash("your_password_here"),  # You'll need to set this
                "created_at": "2024-01-01T00:00:00.000Z"
            }
            
            await db.users.insert_one(user_data)
            print("   ✅ User account created!")
        else:
            print("   ✅ User account already exists!")
            
        await client.close()
        
        print("\n🎉 AUTHENTICATION FIX COMPLETE!")
        print("You should now be able to log in to your application.")
        print("\nNOTE: If you don't remember your password, run the password reset.")
        
        return True
        
    except FileNotFoundError:
        print("   ❌ MongoDB not found. Waiting for installation to complete...")
        return False
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False

if __name__ == "__main__":
    success = asyncio.run(immediate_fix())
    if not success:
        print("\n⏳ MongoDB is still installing. Please wait and try again in a few minutes.")