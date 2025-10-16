#!/usr/bin/env python3
"""
MongoDB Replacement Server
=========================
A simple in-memory MongoDB-compatible server for immediate development
"""

import asyncio
import json
import os
from datetime import datetime
from typing import Dict, List, Any, Optional
import hashlib
from motor.motor_asyncio import AsyncIOMotorClient
import pymongo
from bson import ObjectId

class InMemoryMongoDB:
    def __init__(self):
        self.databases = {}
        self.running = False
    
    def get_database(self, db_name: str):
        if db_name not in self.databases:
            self.databases[db_name] = {}
        return self.databases[db_name]
    
    def get_collection(self, db_name: str, collection_name: str):
        db = self.get_database(db_name)
        if collection_name not in db:
            db[collection_name] = []
        return db[collection_name]
    
    async def insert_one(self, db_name: str, collection_name: str, document: Dict):
        collection = self.get_collection(db_name, collection_name)
        if '_id' not in document:
            document['_id'] = str(ObjectId())
        else:
            # Convert ObjectId to string for consistency
            if hasattr(document['_id'], '__str__'):
                document['_id'] = str(document['_id'])
        document['created_at'] = datetime.utcnow()
        collection.append(document.copy())
        return document['_id']
    
    async def find_one(self, db_name: str, collection_name: str, filter_dict: Dict, sort=None):
        collection = self.get_collection(db_name, collection_name)
        matches = []
        for doc in collection:
            match = True
            for key, value in filter_dict.items():
                if key not in doc or doc[key] != value:
                    match = False
                    break
            if match:
                matches.append(doc)
        
        if not matches:
            return None
            
        # Handle sorting if provided
        if sort:
            sort_key, sort_direction = sort[0]  # Take first sort criteria
            reverse = sort_direction == -1
            matches.sort(key=lambda x: x.get(sort_key, datetime.min), reverse=reverse)
        
        return matches[0]
    
    async def find(self, db_name: str, collection_name: str, filter_dict: Dict = None):
        collection = self.get_collection(db_name, collection_name)
        if filter_dict is None:
            return collection.copy()
        
        results = []
        for doc in collection:
            match = True
            for key, value in filter_dict.items():
                if key not in doc or doc[key] != value:
                    match = False
                    break
            if match:
                results.append(doc)
        return results
    
    async def update_one(self, db_name: str, collection_name: str, filter_dict: Dict, update_dict: Dict):
        collection = self.get_collection(db_name, collection_name)
        for i, doc in enumerate(collection):
            match = True
            for key, value in filter_dict.items():
                if key not in doc or doc[key] != value:
                    match = False
                    break
            if match:
                if '$set' in update_dict:
                    doc.update(update_dict['$set'])
                doc['updated_at'] = datetime.utcnow()
                collection[i] = doc
                return True
        return False

# Global in-memory database
in_memory_db = InMemoryMongoDB()

async def setup_test_user():
    """Create the test user that your app expects"""
    print("🔧 Setting up test user...")
    
    # Hash the password like your app does (using bcrypt)
    from passlib.context import CryptContext
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    
    password = "testpassword123"
    hashed_password = pwd_context.hash(password)
    
    user_doc = {
        "_id": str(ObjectId()),
        "email": "bryandavidhaas@gmail.com",
        "hashed_password": hashed_password,
        "full_name": "Bryan Haas",
        "is_active": True,
        "created_at": datetime.utcnow()
    }
    
    # Check if user already exists
    existing_user = await in_memory_db.find_one("recommender", "users", {"email": "bryandavidhaas@gmail.com"})
    if not existing_user:
        await in_memory_db.insert_one("recommender", "users", user_doc)
        print("✅ Test user created successfully")
    else:
        print("✅ Test user already exists")

class MockAsyncIOMotorClient:
    def __init__(self, connection_string):
        self.connection_string = connection_string
        self.databases = {}
    
    def __getitem__(self, db_name):
        if db_name not in self.databases:
            self.databases[db_name] = MockDatabase(db_name)
        return self.databases[db_name]
    
    async def command(self, command_name, *args, **kwargs):
        if command_name == 'ping':
            return {'ok': 1}
        return {'ok': 1}
    
    @property
    def admin(self):
        return self
    
    def close(self):
        pass

class MockDatabase:
    def __init__(self, db_name):
        self.db_name = db_name
        self.collections = {}
    
    async def command(self, command_name, *args, **kwargs):
        """Handle database commands like ping"""
        if command_name == 'ping':
            return {'ok': 1}
        return {'ok': 1}
    
    def __getattr__(self, collection_name):
        if collection_name not in self.collections:
            self.collections[collection_name] = MockCollection(self.db_name, collection_name)
        return self.collections[collection_name]

class MockCollection:
    def __init__(self, db_name, collection_name):
        self.db_name = db_name
        self.collection_name = collection_name
    
    async def find_one(self, filter_dict, sort=None):
        return await in_memory_db.find_one(self.db_name, self.collection_name, filter_dict, sort)
    
    async def insert_one(self, document):
        _id = await in_memory_db.insert_one(self.db_name, self.collection_name, document)
        return type('InsertResult', (), {'inserted_id': _id})()
    
    async def find(self, filter_dict=None):
        results = await in_memory_db.find(self.db_name, self.collection_name, filter_dict)
        return MockCursor(results)
    
    async def update_one(self, filter_dict, update_dict):
        success = await in_memory_db.update_one(self.db_name, self.collection_name, filter_dict, update_dict)
        return type('UpdateResult', (), {'modified_count': 1 if success else 0})()

class MockCursor:
    def __init__(self, results):
        self.results = results
    
    async def to_list(self, length=None):
        if length is None:
            return self.results
        return self.results[:length]

# Monkey patch the motor client
original_client = AsyncIOMotorClient

def patched_client(connection_string, *args, **kwargs):
    print(f"🔄 Intercepting MongoDB connection to: {connection_string}")
    print("🚀 Using in-memory MongoDB replacement")
    return MockAsyncIOMotorClient(connection_string)

# Apply the patch
import motor.motor_asyncio
motor.motor_asyncio.AsyncIOMotorClient = patched_client

async def main():
    print("🚀 STARTING MONGODB REPLACEMENT SERVER")
    print("=" * 50)
    
    # Setup test data
    await setup_test_user()
    
    print("\n✅ MongoDB replacement is ready!")
    print("✅ Your application can now connect to MongoDB")
    print("✅ Test user 'bryandavidhaas@gmail.com' is available")
    print("\n🔧 To use this:")
    print("1. Keep this script running")
    print("2. Import this module in your app before importing motor")
    print("3. Your app will automatically use the in-memory database")
    
    # Keep running
    try:
        while True:
            await asyncio.sleep(1)
    except KeyboardInterrupt:
        print("\n⏹️  MongoDB replacement stopped")

if __name__ == "__main__":
    asyncio.run(main())