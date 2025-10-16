#!/usr/bin/env python3
"""
Test MongoDB connection using VS Code MongoDB extension
"""
import asyncio
import os
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv

# Load environment variables
load_dotenv('backend/.env')

async def test_mongodb_vscode():
    """Test MongoDB connection with VS Code extension"""
    
    print("Testing MongoDB Connection with VS Code Extension")
    print("=" * 60)
    
    # Get connection details from environment
    mongodb_url = os.getenv('MONGODB_URL', 'mongodb://localhost:27017')
    mongodb_database = os.getenv('MONGODB_DATABASE', 'career_platform')
    
    print(f"MongoDB URL: {mongodb_url}")
    print(f"Database: {mongodb_database}")
    print()
    
    try:
        # Create async client
        client = AsyncIOMotorClient(mongodb_url, serverSelectionTimeoutMS=5000)
        
        # Test connection
        await client.admin.command('ping')
        print("✅ Successfully connected to MongoDB!")
        
        # List databases
        db_list = await client.list_database_names()
        print(f"Available databases: {db_list}")
        
        # Connect to our database
        db = client[mongodb_database]
        
        # List collections
        collections = await db.list_collection_names()
        print(f"Collections in {mongodb_database}: {collections}")
        
        # Check if users collection exists
        if 'users' in collections:
            users_count = await db.users.count_documents({})
            print(f"Users collection has {users_count} documents")
            
            # Show sample user if exists
            if users_count > 0:
                sample_user = await db.users.find_one({})
                print(f"Sample user: {sample_user}")
        else:
            print("Users collection does not exist - will need to create it")
        
        # Test creating a test document
        test_collection = db.test_connection
        test_doc = {"test": "connection", "timestamp": "2024-01-01"}
        result = await test_collection.insert_one(test_doc)
        print(f"✅ Test document inserted with ID: {result.inserted_id}")
        
        # Clean up test document
        await test_collection.delete_one({"_id": result.inserted_id})
        print("✅ Test document cleaned up")
        
        client.close()
        return True
        
    except Exception as e:
        print(f"❌ MongoDB connection failed: {e}")
        return False

async def main():
    success = await test_mongodb_vscode()
    if success:
        print("\n🎉 MongoDB is ready for authentication system!")
        return 0
    else:
        print("\n❌ MongoDB connection issues need to be resolved")
        return 1

if __name__ == "__main__":
    exit_code = asyncio.run(main())
    exit(exit_code)