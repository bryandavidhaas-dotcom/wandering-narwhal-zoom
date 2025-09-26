#!/usr/bin/env python3
"""
Simple MongoDB Atlas connection test
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

print(f"Testing connection to: {mongo_uri}")
print(f"Database: {database_name}")

try:
    # Create client
    client = MongoClient(mongo_uri, serverSelectionTimeoutMS=10000)
    
    # Test connection
    client.admin.command('ping')
    print("✅ Successfully connected to MongoDB Atlas!")
    
    # Get database
    db = client[database_name]
    
    # List collections
    collections = db.list_collection_names()
    print(f"📋 Collections in database: {collections}")
    
    # Test insert
    test_collection = db['test']
    result = test_collection.insert_one({"test": "connection", "status": "success"})
    print(f"✅ Test document inserted with ID: {result.inserted_id}")
    
    # Clean up test document
    test_collection.delete_one({"_id": result.inserted_id})
    print("🧹 Test document cleaned up")
    
    client.close()
    print("🔌 Connection closed successfully")
    
except Exception as e:
    print(f"❌ Connection failed: {e}")