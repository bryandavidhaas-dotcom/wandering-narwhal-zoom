#!/usr/bin/env python3
"""
Verify the career data migration
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
database_name = os.getenv('MONGODB_DATABASE', 'career_recommendations')

print(f"Verifying migration in database: {database_name}")

try:
    # Create client
    client = MongoClient(mongo_uri, serverSelectionTimeoutMS=10000)
    
    # Get database
    db = client[database_name]
    
    # Check careers collection
    careers_collection = db['careers']
    career_count = careers_collection.count_documents({})
    
    print(f"✅ Found {career_count} career documents in the database")
    
    if career_count > 0:
        # Show a sample career
        sample_career = careers_collection.find_one()
        print(f"📋 Sample career: {sample_career.get('title', 'Unknown')}")
        print(f"🏢 Career type: {sample_career.get('careerType', 'Unknown')}")
        print(f"💰 Salary range: ${sample_career.get('salaryMin', 0):,} - ${sample_career.get('salaryMax', 0):,}")
        
        # List all career titles
        all_careers = list(careers_collection.find({}, {"title": 1, "careerType": 1}))
        print(f"\n📝 All migrated careers:")
        for i, career in enumerate(all_careers, 1):
            print(f"  {i}. {career.get('title', 'Unknown')} ({career.get('careerType', 'Unknown')})")
    
    client.close()
    print(f"\n🎉 Migration verification complete!")
    
except Exception as e:
    print(f"❌ Verification failed: {e}")