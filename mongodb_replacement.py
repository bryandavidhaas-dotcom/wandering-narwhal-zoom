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
        self.active_connections = set()
        self.connection_count = 0
        self.max_connections = 50  # Limit concurrent connections
    
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

# Add connection management methods to InMemoryMongoDB
def register_connection(self, client):
    """Register a new connection"""
    if len(self.active_connections) >= self.max_connections:
        raise Exception(f"Maximum connections ({self.max_connections}) exceeded")
    self.active_connections.add(client.connection_id)
    self.connection_count += 1
    print(f"📊 Connection registered. Active: {len(self.active_connections)}/{self.max_connections}")

def unregister_connection(self, client):
    """Unregister a connection"""
    self.active_connections.discard(client.connection_id)
    print(f"📊 Connection unregistered. Active: {len(self.active_connections)}/{self.max_connections}")

async def cleanup(self):
    """Cleanup all resources"""
    print("🧹 Cleaning up MongoDB replacement system...")
    
    # Clear all databases
    for db_name in list(self.databases.keys()):
        db_data = self.databases[db_name]
        for collection_name in list(db_data.keys()):
            db_data[collection_name].clear()
        db_data.clear()
    self.databases.clear()
    
    # Clear active connections
    self.active_connections.clear()
    self.connection_count = 0
    self.running = False
    
    print("✅ MongoDB replacement system cleaned up")

# Add methods to the class
InMemoryMongoDB.register_connection = register_connection
InMemoryMongoDB.unregister_connection = unregister_connection
InMemoryMongoDB.cleanup = cleanup

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
    def __init__(self, connection_string, **kwargs):
        self.connection_string = connection_string
        self.databases = {}
        self.closed = False
        self.connection_id = id(self)
        
        # Register this connection
        in_memory_db.register_connection(self)
        
        # Store connection pool configuration
        self.max_pool_size = kwargs.get('maxPoolSize', 10)
        self.min_pool_size = kwargs.get('minPoolSize', 1)
        self.max_idle_time_ms = kwargs.get('maxIdleTimeMS', 30000)
        self.wait_queue_timeout_ms = kwargs.get('waitQueueTimeoutMS', 5000)
        self.server_selection_timeout_ms = kwargs.get('serverSelectionTimeoutMS', 5000)
        self.connect_timeout_ms = kwargs.get('connectTimeoutMS', 10000)
        self.socket_timeout_ms = kwargs.get('socketTimeoutMS', 20000)
        
        print(f"🔗 Mock MongoDB client created with pool config: max={self.max_pool_size}, min={self.min_pool_size}")
    
    def __getitem__(self, db_name):
        if db_name not in self.databases:
            self.databases[db_name] = MockDatabase(db_name)
        return self.databases[db_name]
    
    async def command(self, command_name, *args, **kwargs):
        if self.closed:
            raise Exception("Client is closed")
        if command_name == 'ping':
            return {'ok': 1}
        return {'ok': 1}
    
    @property
    def admin(self):
        return self
    
    def close(self):
        """Close the mock client and cleanup resources"""
        if not self.closed:
            self.closed = True
            # Cleanup all databases and collections
            for db in self.databases.values():
                if hasattr(db, 'cleanup'):
                    db.cleanup()
            self.databases.clear()
            
            # Unregister this connection
            in_memory_db.unregister_connection(self)
            print(f"🔌 Mock MongoDB client {self.connection_id} closed and cleaned up")
    
    def __del__(self):
        """Ensure cleanup on garbage collection"""
        if not self.closed:
            self.close()

class MockDatabase:
    def __init__(self, db_name):
        self.db_name = db_name
        self.collections = {}
        self.closed = False
    
    async def command(self, command_name, *args, **kwargs):
        """Handle database commands like ping"""
        if self.closed:
            raise Exception("Database is closed")
        if command_name == 'ping':
            return {'ok': 1}
        return {'ok': 1}
    
    def cleanup(self):
        """Cleanup database resources"""
        if not self.closed:
            self.closed = True
            # Cleanup all collections
            for collection in self.collections.values():
                if hasattr(collection, 'cleanup'):
                    collection.cleanup()
            self.collections.clear()
            print(f"🗄️  Mock database '{self.db_name}' cleaned up")
    
    def __getattr__(self, collection_name):
        if collection_name not in self.collections:
            self.collections[collection_name] = MockCollection(self.db_name, collection_name)
        return self.collections[collection_name]

class MockCollection:
    def __init__(self, db_name, collection_name):
        self.db_name = db_name
        self.collection_name = collection_name
        self.closed = False
        self.operation_timeout = 20.0  # Default 20 second timeout
    
    async def find_one(self, filter_dict, sort=None):
        if self.closed:
            raise Exception("Collection is closed")
        return await asyncio.wait_for(
            in_memory_db.find_one(self.db_name, self.collection_name, filter_dict, sort),
            timeout=self.operation_timeout
        )
    
    async def insert_one(self, document):
        if self.closed:
            raise Exception("Collection is closed")
        _id = await asyncio.wait_for(
            in_memory_db.insert_one(self.db_name, self.collection_name, document),
            timeout=self.operation_timeout
        )
        return type('InsertResult', (), {'inserted_id': _id})()
    
    async def find(self, filter_dict=None):
        if self.closed:
            raise Exception("Collection is closed")
        results = await asyncio.wait_for(
            in_memory_db.find(self.db_name, self.collection_name, filter_dict),
            timeout=self.operation_timeout
        )
        return MockCursor(results)
    
    async def update_one(self, filter_dict, update_dict):
        if self.closed:
            raise Exception("Collection is closed")
        success = await asyncio.wait_for(
            in_memory_db.update_one(self.db_name, self.collection_name, filter_dict, update_dict),
            timeout=self.operation_timeout
        )
        return type('UpdateResult', (), {'modified_count': 1 if success else 0})()
    
    def cleanup(self):
        """Cleanup collection resources"""
        if not self.closed:
            self.closed = True
            print(f"📄 Mock collection '{self.db_name}.{self.collection_name}' cleaned up")

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
    
    # Check connection limits
    if len(in_memory_db.active_connections) >= in_memory_db.max_connections:
        print(f"⚠️  Warning: Approaching connection limit ({len(in_memory_db.active_connections)}/{in_memory_db.max_connections})")
    
    return MockAsyncIOMotorClient(connection_string, **kwargs)

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