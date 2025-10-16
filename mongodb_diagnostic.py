#!/usr/bin/env python3
"""
MongoDB Comprehensive Diagnostic Tool
=====================================
Systematically diagnoses MongoDB connection and configuration issues
"""

import asyncio
import subprocess
import sys
import os
import platform
from pathlib import Path
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv

async def diagnose_mongodb():
    print("🔍 MONGODB COMPREHENSIVE DIAGNOSTIC")
    print("=" * 50)
    
    # Step 1: Check MongoDB Installation
    print("\n1. CHECKING MONGODB INSTALLATION")
    print("-" * 30)
    
    mongodb_installed = False
    try:
        result = subprocess.run(['mongod', '--version'], capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            print("✅ MongoDB is installed")
            print(f"   Version: {result.stdout.split()[2] if len(result.stdout.split()) > 2 else 'Unknown'}")
            mongodb_installed = True
        else:
            print("❌ MongoDB installation issue")
            print(f"   Error: {result.stderr}")
    except FileNotFoundError:
        print("❌ MongoDB not found in PATH")
        print("   MongoDB may not be installed or not in system PATH")
    except subprocess.TimeoutExpired:
        print("⚠️  MongoDB version check timed out")
    except Exception as e:
        print(f"❌ Error checking MongoDB: {e}")
    
    # Step 2: Check MongoDB Service Status
    print("\n2. CHECKING MONGODB SERVICE STATUS")
    print("-" * 35)
    
    service_running = False
    if platform.system() == "Windows":
        try:
            result = subprocess.run(['sc', 'query', 'MongoDB'], capture_output=True, text=True)
            if "RUNNING" in result.stdout:
                print("✅ MongoDB Windows service is running")
                service_running = True
            elif "STOPPED" in result.stdout:
                print("⚠️  MongoDB Windows service is stopped")
                print("   Try: sc start MongoDB")
            else:
                print("❌ MongoDB Windows service not found")
        except Exception as e:
            print(f"❌ Error checking Windows service: {e}")
    
    # Step 3: Test Direct Connection
    print("\n3. TESTING DIRECT CONNECTION")
    print("-" * 30)
    
    connection_working = False
    try:
        client = AsyncIOMotorClient("mongodb://localhost:27017", serverSelectionTimeoutMS=5000)
        await client.admin.command("ping")
        print("✅ Direct connection to localhost:27017 successful")
        connection_working = True
        await client.close()
    except Exception as e:
        print(f"❌ Direct connection failed: {e}")
        print("   This suggests MongoDB is not running on localhost:27017")
    
    # Step 4: Check Environment Configuration
    print("\n4. CHECKING ENVIRONMENT CONFIGURATION")
    print("-" * 40)
    
    # Load environment variables
    load_dotenv()
    
    # Check if .env file exists
    env_file = Path("backend/.env")
    if env_file.exists():
        print("✅ backend/.env file exists")
        with open(env_file, 'r') as f:
            env_content = f.read()
            if "DATABASE_URL" in env_content:
                print("✅ DATABASE_URL found in .env file")
            else:
                print("⚠️  DATABASE_URL not found in .env file")
    else:
        print("❌ backend/.env file missing")
        print("   Copy backend/.env.example to backend/.env and configure it")
    
    # Check environment variables
    database_url = os.getenv('DATABASE_URL')
    mongodb_url = os.getenv('MONGODB_URL')
    
    print(f"   DATABASE_URL: {database_url or 'Not set'}")
    print(f"   MONGODB_URL: {mongodb_url or 'Not set'}")
    
    # Check config.py default
    sys.path.insert(0, str(Path(__file__).parent / "backend"))
    try:
        from app.core.config import settings
        print(f"   Config DATABASE_URL: {settings.DATABASE_URL}")
        
        if settings.DATABASE_URL == "your_mongodb_connection_string_here":
            print("⚠️  DATABASE_URL still has placeholder value")
    except Exception as e:
        print(f"❌ Error loading config: {e}")
    
    # Step 5: Check Database and User
    print("\n5. CHECKING DATABASE AND USER")
    print("-" * 30)
    
    if connection_working:
        try:
            client = AsyncIOMotorClient("mongodb://localhost:27017")
            db = client["recommender"]
            
            # List databases
            db_list = await client.list_database_names()
            print(f"   Available databases: {db_list}")
            
            if "recommender" in db_list:
                print("✅ 'recommender' database exists")
                
                # Check collections
                collections = await db.list_collection_names()
                print(f"   Collections in 'recommender': {collections}")
                
                if "users" in collections:
                    print("✅ 'users' collection exists")
                    
                    # Check for specific user
                    user = await db.users.find_one({"email": "bryandavidhaas@gmail.com"})
                    if user:
                        print("✅ User bryandavidhaas@gmail.com found")
                        print(f"   User fields: {list(user.keys())}")
                    else:
                        print("❌ User bryandavidhaas@gmail.com not found")
                        
                        # List all users
                        users = await db.users.find({}).to_list(length=10)
                        print(f"   Total users: {len(users)}")
                        for u in users:
                            print(f"     - {u.get('email', 'no email')}")
                else:
                    print("❌ 'users' collection not found")
            else:
                print("❌ 'recommender' database not found")
            
            await client.close()
        except Exception as e:
            print(f"❌ Database check failed: {e}")
    
    # Step 6: Provide Diagnosis Summary
    print("\n6. DIAGNOSIS SUMMARY")
    print("-" * 20)
    
    if not mongodb_installed:
        print("🚨 PRIMARY ISSUE: MongoDB is not properly installed")
        print("   SOLUTION: Wait for 'winget install MongoDB.Server' to complete")
        print("   THEN: Start MongoDB service or run 'python fix_auth_immediate.py'")
    elif not connection_working:
        print("🚨 PRIMARY ISSUE: MongoDB is installed but not running")
        print("   SOLUTION: Start MongoDB service or run 'python fix_auth_immediate.py'")
    elif not env_file.exists() or database_url == "your_mongodb_connection_string_here":
        print("🚨 PRIMARY ISSUE: Environment configuration not set up")
        print("   SOLUTION: Create backend/.env with proper DATABASE_URL")
    else:
        print("🚨 PRIMARY ISSUE: User account missing or database not populated")
        print("   SOLUTION: Run 'python fix_auth_immediate.py' to create user account")
    
    print("\n" + "=" * 50)
    return {
        'mongodb_installed': mongodb_installed,
        'service_running': service_running,
        'connection_working': connection_working,
        'env_configured': env_file.exists() and database_url != "your_mongodb_connection_string_here"
    }

if __name__ == "__main__":
    asyncio.run(diagnose_mongodb())