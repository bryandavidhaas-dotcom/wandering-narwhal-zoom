#!/usr/bin/env python3
"""
Comprehensive database connectivity and user account verification script.
Checks both MongoDB and SQLite databases for user bryandavidhaas@gmail.com.
"""

import asyncio
import os
import sqlite3
import sys
from datetime import datetime
from pathlib import Path

# Add backend to path for imports
sys.path.append(str(Path(__file__).resolve().parent / "backend"))

try:
    from motor.motor_asyncio import AsyncIOMotorClient
    from beanie import init_beanie
    from dotenv import load_dotenv
    MONGODB_AVAILABLE = True
except ImportError as e:
    print(f"⚠️ MongoDB dependencies not available: {e}")
    MONGODB_AVAILABLE = False

# Load environment variables
load_dotenv()

class DatabaseChecker:
    def __init__(self):
        self.target_email = "bryandavidhaas@gmail.com"
        self.results = {
            "mongodb": {"connected": False, "user_found": False, "collections": {}, "error": None},
            "sqlite": {"connected": False, "user_found": False, "tables": {}, "error": None},
            "summary": {}
        }
    
    async def check_mongodb_connection(self):
        """Check MongoDB connectivity and search for user"""
        print("🔍 Checking MongoDB connection...")
        
        if not MONGODB_AVAILABLE:
            self.results["mongodb"]["error"] = "MongoDB dependencies not installed"
            print("❌ MongoDB dependencies not available")
            return
        
        try:
            # Try different MongoDB URLs
            mongo_urls = [
                os.getenv("MONGODB_URL", "mongodb://localhost:27017"),
                "mongodb://localhost:27017",
                "mongodb://127.0.0.1:27017"
            ]
            
            client = None
            connected_url = None
            
            for url in mongo_urls:
                try:
                    print(f"   Trying: {url}")
                    client = AsyncIOMotorClient(url, serverSelectionTimeoutMS=5000)
                    # Test connection
                    await client.admin.command('ping')
                    connected_url = url
                    print(f"✅ Connected to MongoDB at: {url}")
                    break
                except Exception as e:
                    print(f"   Failed: {e}")
                    continue
            
            if not client or not connected_url:
                raise Exception("Could not connect to any MongoDB instance")
            
            self.results["mongodb"]["connected"] = True
            
            # Get database name
            db_name = os.getenv("MONGODB_DATABASE", "career_platform")
            db = client[db_name]
            
            # List collections
            collections = await db.list_collection_names()
            print(f"📋 Collections in {db_name}: {collections}")
            self.results["mongodb"]["collections"] = collections
            
            # Check for user-related collections
            user_collections = [col for col in collections if 'user' in col.lower()]
            
            if user_collections:
                for collection_name in user_collections:
                    collection = db[collection_name]
                    
                    # Count total documents
                    total_docs = await collection.count_documents({})
                    print(f"   {collection_name}: {total_docs} documents")
                    self.results["mongodb"]["collections"][collection_name] = total_docs
                    
                    # Search for the target email
                    user_query = {"email": self.target_email}
                    user_doc = await collection.find_one(user_query)
                    
                    if user_doc:
                        print(f"✅ Found user in {collection_name}: {user_doc}")
                        self.results["mongodb"]["user_found"] = True
                        self.results["mongodb"]["found_in"] = collection_name
                        self.results["mongodb"]["user_data"] = str(user_doc)
                    else:
                        print(f"❌ User not found in {collection_name}")
                    
                    # Show sample documents
                    sample_docs = await collection.find({}).limit(3).to_list(length=3)
                    if sample_docs:
                        print(f"   Sample documents from {collection_name}:")
                        for i, doc in enumerate(sample_docs, 1):
                            # Show only key fields to avoid clutter
                            key_fields = {}
                            for key in ['_id', 'email', 'user_id', 'created_at']:
                                if key in doc:
                                    key_fields[key] = doc[key]
                            print(f"     {i}. {key_fields}")
            else:
                print("❌ No user-related collections found")
                
                # Check all collections for email field
                for collection_name in collections:
                    collection = db[collection_name]
                    sample_doc = await collection.find_one({})
                    if sample_doc and 'email' in sample_doc:
                        print(f"   Found email field in {collection_name}")
                        user_doc = await collection.find_one({"email": self.target_email})
                        if user_doc:
                            print(f"✅ Found user in {collection_name}: {user_doc}")
                            self.results["mongodb"]["user_found"] = True
                            self.results["mongodb"]["found_in"] = collection_name
            
        except Exception as e:
            print(f"❌ MongoDB connection failed: {e}")
            self.results["mongodb"]["error"] = str(e)
    
    def check_sqlite_connection(self):
        """Check SQLite databases and search for user"""
        print("\n🔍 Checking SQLite databases...")
        
        sqlite_files = [
            "careers.db",
            "careers_corrupted_backup_20251006_163621.db",
            "backend/careers.db"
        ]
        
        for db_file in sqlite_files:
            if os.path.exists(db_file):
                print(f"📁 Checking {db_file}...")
                try:
                    conn = sqlite3.connect(db_file)
                    cursor = conn.cursor()
                    
                    # Get all tables
                    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
                    tables = cursor.fetchall()
                    table_names = [table[0] for table in tables]
                    
                    print(f"   Tables: {table_names}")
                    self.results["sqlite"]["tables"][db_file] = table_names
                    self.results["sqlite"]["connected"] = True
                    
                    # Check each table for user data
                    for table_name in table_names:
                        try:
                            # Get table schema
                            cursor.execute(f"PRAGMA table_info({table_name})")
                            columns = cursor.fetchall()
                            column_names = [col[1] for col in columns]
                            
                            print(f"   {table_name} columns: {column_names}")
                            
                            # Check if table has email column
                            if 'email' in column_names:
                                print(f"   🔍 Searching for user in {table_name}...")
                                cursor.execute(f"SELECT * FROM {table_name} WHERE email = ?", (self.target_email,))
                                user_data = cursor.fetchall()
                                
                                if user_data:
                                    print(f"✅ Found user in {table_name}: {user_data}")
                                    self.results["sqlite"]["user_found"] = True
                                    self.results["sqlite"]["found_in"] = f"{db_file}.{table_name}"
                                    self.results["sqlite"]["user_data"] = str(user_data)
                                else:
                                    print(f"❌ User not found in {table_name}")
                                
                                # Show sample data
                                cursor.execute(f"SELECT * FROM {table_name} LIMIT 3")
                                sample_data = cursor.fetchall()
                                if sample_data:
                                    print(f"   Sample data from {table_name}:")
                                    for i, row in enumerate(sample_data, 1):
                                        print(f"     {i}. {dict(zip(column_names, row))}")
                            
                            # Check for user-related tables
                            elif 'user' in table_name.lower():
                                print(f"   🔍 Found user-related table: {table_name}")
                                cursor.execute(f"SELECT * FROM {table_name} LIMIT 5")
                                sample_data = cursor.fetchall()
                                if sample_data:
                                    print(f"   Sample data: {sample_data}")
                        
                        except Exception as e:
                            print(f"   ⚠️ Error checking table {table_name}: {e}")
                    
                    conn.close()
                    
                except Exception as e:
                    print(f"❌ Error with {db_file}: {e}")
                    self.results["sqlite"]["error"] = str(e)
            else:
                print(f"❌ {db_file} not found")
    
    def check_user_creation_scripts(self):
        """Look for user creation and migration scripts"""
        print("\n🔍 Checking for user creation scripts...")
        
        script_patterns = [
            "**/migration*.py",
            "**/populate*.py", 
            "**/create_user*.py",
            "**/seed*.py",
            "**/init*.py"
        ]
        
        found_scripts = []
        for pattern in script_patterns:
            for script_file in Path(".").rglob(pattern):
                if script_file.is_file():
                    found_scripts.append(str(script_file))
        
        if found_scripts:
            print(f"📋 Found potential user creation scripts:")
            for script in found_scripts:
                print(f"   - {script}")
                
                # Quick scan for user creation patterns
                try:
                    with open(script, 'r', encoding='utf-8') as f:
                        content = f.read()
                        if any(keyword in content.lower() for keyword in ['user', 'email', 'bryandavidhaas']):
                            print(f"     ✅ Contains user-related code")
                        else:
                            print(f"     ❌ No obvious user-related code")
                except Exception as e:
                    print(f"     ⚠️ Could not read file: {e}")
        else:
            print("❌ No user creation scripts found")
    
    def check_test_files(self):
        """Check test files for user creation patterns"""
        print("\n🔍 Checking test files for user patterns...")
        
        test_files = list(Path(".").rglob("test*.py"))
        user_related_tests = []
        
        for test_file in test_files:
            try:
                with open(test_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                    if 'bryandavidhaas' in content.lower() or ('user' in content.lower() and 'email' in content.lower()):
                        user_related_tests.append(str(test_file))
                        print(f"📋 Found user-related test: {test_file}")
            except Exception as e:
                continue
        
        if not user_related_tests:
            print("❌ No user-related test files found")
    
    def generate_summary(self):
        """Generate summary of findings"""
        print("\n" + "="*60)
        print("📊 SUMMARY OF FINDINGS")
        print("="*60)
        
        # MongoDB Summary
        print(f"🍃 MongoDB Status:")
        if self.results["mongodb"]["connected"]:
            print(f"   ✅ Connected successfully")
            print(f"   📋 Collections: {list(self.results['mongodb']['collections'].keys())}")
            if self.results["mongodb"]["user_found"]:
                print(f"   ✅ User {self.target_email} FOUND in {self.results['mongodb'].get('found_in', 'unknown')}")
            else:
                print(f"   ❌ User {self.target_email} NOT FOUND")
        else:
            print(f"   ❌ Connection failed: {self.results['mongodb'].get('error', 'Unknown error')}")
        
        # SQLite Summary
        print(f"\n💾 SQLite Status:")
        if self.results["sqlite"]["connected"]:
            print(f"   ✅ Connected successfully")
            print(f"   📋 Databases checked: {list(self.results['sqlite']['tables'].keys())}")
            if self.results["sqlite"]["user_found"]:
                print(f"   ✅ User {self.target_email} FOUND in {self.results['sqlite'].get('found_in', 'unknown')}")
            else:
                print(f"   ❌ User {self.target_email} NOT FOUND")
        else:
            print(f"   ❌ Connection failed: {self.results['sqlite'].get('error', 'Unknown error')}")
        
        # Overall conclusion
        print(f"\n🎯 CONCLUSION:")
        user_found_anywhere = self.results["mongodb"]["user_found"] or self.results["sqlite"]["user_found"]
        
        if user_found_anywhere:
            print(f"   ✅ User account {self.target_email} EXISTS in the system")
            if self.results["mongodb"]["user_found"]:
                print(f"   📍 Location: MongoDB - {self.results['mongodb'].get('found_in')}")
            if self.results["sqlite"]["user_found"]:
                print(f"   📍 Location: SQLite - {self.results['sqlite'].get('found_in')}")
        else:
            print(f"   ❌ User account {self.target_email} DOES NOT EXIST in any database")
            print(f"   💡 Possible reasons:")
            print(f"      - User has not registered yet")
            print(f"      - User data is stored in a different database/collection")
            print(f"      - Database connection issues preventing access")
            print(f"      - User data was deleted or corrupted")
        
        # Database connectivity status
        print(f"\n🔌 Database Connectivity:")
        if self.results["mongodb"]["connected"]:
            print(f"   ✅ MongoDB: Accessible")
        else:
            print(f"   ❌ MongoDB: Not accessible - {self.results['mongodb'].get('error', 'Unknown error')}")
        
        if self.results["sqlite"]["connected"]:
            print(f"   ✅ SQLite: Accessible")
        else:
            print(f"   ❌ SQLite: Not accessible - {self.results['sqlite'].get('error', 'Unknown error')}")

async def main():
    """Main function to run all database checks"""
    print("🚀 Starting Comprehensive Database Check")
    print(f"🎯 Target user: bryandavidhaas@gmail.com")
    print(f"⏰ Started at: {datetime.now()}")
    print("-" * 60)
    
    checker = DatabaseChecker()
    
    # Run all checks
    await checker.check_mongodb_connection()
    checker.check_sqlite_connection()
    checker.check_user_creation_scripts()
    checker.check_test_files()
    
    # Generate summary
    checker.generate_summary()
    
    print(f"\n⏰ Completed at: {datetime.now()}")

if __name__ == "__main__":
    asyncio.run(main())