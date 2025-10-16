#!/usr/bin/env python3
"""
MongoDB Readiness Checker
========================
Quick script to check if MongoDB is ready for login
"""

import asyncio
from motor.motor_asyncio import AsyncIOMotorClient

async def check_mongodb_ready():
    print("🔍 Checking MongoDB status...")
    
    try:
        client = AsyncIOMotorClient("mongodb://localhost:27017", serverSelectionTimeoutMS=3000)
        await client.admin.command("ping")
        
        # Check if your user exists
        db = client["recommender"]
        user = await db.users.find_one({"email": "bryandavidhaas@gmail.com"})
        
        await client.close()
        
        if user:
            print("✅ MongoDB is READY! Your user account exists.")
            print("🎉 You can now try logging in to your application!")
            return True
        else:
            print("⚠️  MongoDB is running but your user account is missing.")
            print("   Run: python fix_auth_immediate.py")
            return False
            
    except Exception as e:
        print("❌ MongoDB is NOT ready yet.")
        print(f"   Error: {str(e)[:100]}...")
        return False

if __name__ == "__main__":
    asyncio.run(check_mongodb_ready())