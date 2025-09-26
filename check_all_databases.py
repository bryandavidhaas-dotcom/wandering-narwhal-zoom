#!/usr/bin/env python3
"""
Check all databases and collections to find the migrated data
"""
import os
from pathlib import Path
from pymongo import MongoClient
from dotenv import load_dotenv

# Load environment variables from backend/.env
backend_env_path = Path(__file__).parent / "backend" / ".env"
load_dotenv(backend_env_path)

# Get connection details
mongo_uri = os.getenv('MONGODB_URL')

print("Checking all databases for migrated career data...")

try:
    # Create client
    client = MongoClient(mongo_uri, serverSelectionTimeoutMS=10000)
    
    # List all databases
    databases = client.list_database_names()
    print(f"📋 Available databases: {databases}")
    
    # Check each database for careers collection
    for db_name in databases:
        if db_name not in ['admin', 'local', 'config']:  # Skip system databases
            db = client[db_name]
            collections = db.list_collection_names()
            print(f"\n🗂️  Database '{db_name}' collections: {collections}")
            
            if 'careers' in collections:
                careers_collection = db['careers']
                career_count = careers_collection.count_documents({})
                print(f"   ✅ Found {career_count} career documents in '{db_name}.careers'")
                
                if career_count > 0:
                    # Show sample career
                    sample_career = careers_collection.find_one()
                    print(f"   📋 Sample career: {sample_career.get('title', 'Unknown')}")
                    
                    # List all career titles
                    all_careers = list(careers_collection.find({}, {"title": 1, "careerType": 1}))
                    print(f"   📝 All careers in this database:")
                    for i, career in enumerate(all_careers[:5], 1):  # Show first 5
                        print(f"     {i}. {career.get('title', 'Unknown')} ({career.get('careerType', 'Unknown')})")
                    if len(all_careers) > 5:
                        print(f"     ... and {len(all_careers) - 5} more")
    
    client.close()
    print(f"\n🎉 Database search complete!")
    
except Exception as e:
    print(f"❌ Search failed: {e}")