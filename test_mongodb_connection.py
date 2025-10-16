#!/usr/bin/env python3
"""
Test MongoDB connection and service status
"""
import pymongo
import sys
from pymongo import MongoClient
from pymongo.errors import ServerSelectionTimeoutError, ConnectionFailure

def test_mongodb_connection():
    """Test MongoDB connection with various connection strings"""
    
    connection_strings = [
        "mongodb://localhost:27017/",
        "mongodb://127.0.0.1:27017/",
        "mongodb://localhost:27017/wandering_narwhal_zoom",
        "mongodb://127.0.0.1:27017/wandering_narwhal_zoom"
    ]
    
    print("Testing MongoDB connections...")
    print("=" * 50)
    
    for conn_str in connection_strings:
        print(f"\nTesting: {conn_str}")
        try:
            # Create client with short timeout
            client = MongoClient(conn_str, serverSelectionTimeoutMS=3000)
            
            # Test the connection
            client.admin.command('ping')
            print(f"✅ SUCCESS: Connected to {conn_str}")
            
            # List databases
            dbs = client.list_database_names()
            print(f"   Available databases: {dbs}")
            
            # Check if our database exists
            if 'wandering_narwhal_zoom' in dbs:
                db = client['wandering_narwhal_zoom']
                collections = db.list_collection_names()
                print(f"   Collections in wandering_narwhal_zoom: {collections}")
                
                # Check users collection
                if 'users' in collections:
                    users_count = db.users.count_documents({})
                    print(f"   Users collection has {users_count} documents")
            
            client.close()
            return True
            
        except ServerSelectionTimeoutError:
            print(f"❌ TIMEOUT: Cannot connect to {conn_str} (MongoDB may not be running)")
        except ConnectionFailure as e:
            print(f"❌ CONNECTION FAILED: {conn_str} - {e}")
        except Exception as e:
            print(f"❌ ERROR: {conn_str} - {e}")
    
    return False

def check_mongodb_service():
    """Check if MongoDB service is running using system commands"""
    import subprocess
    import os
    
    print("\nChecking MongoDB service status...")
    print("=" * 50)
    
    try:
        # Try to find MongoDB processes
        if os.name == 'nt':  # Windows
            result = subprocess.run(['tasklist', '/FI', 'IMAGENAME eq mongod.exe'], 
                                  capture_output=True, text=True, timeout=10)
            if 'mongod.exe' in result.stdout:
                print("✅ MongoDB process (mongod.exe) is running")
                return True
            else:
                print("❌ MongoDB process (mongod.exe) not found")
        else:  # Unix-like
            result = subprocess.run(['pgrep', 'mongod'], capture_output=True, text=True, timeout=10)
            if result.returncode == 0:
                print("✅ MongoDB process (mongod) is running")
                return True
            else:
                print("❌ MongoDB process (mongod) not found")
                
    except subprocess.TimeoutExpired:
        print("⚠️  Timeout checking MongoDB service")
    except Exception as e:
        print(f"⚠️  Error checking MongoDB service: {e}")
    
    return False

def start_mongodb_service():
    """Attempt to start MongoDB service"""
    import subprocess
    import os
    
    print("\nAttempting to start MongoDB service...")
    print("=" * 50)
    
    try:
        if os.name == 'nt':  # Windows
            # Try to start MongoDB service
            result = subprocess.run(['net', 'start', 'MongoDB'], 
                                  capture_output=True, text=True, timeout=30)
            if result.returncode == 0:
                print("✅ MongoDB service started successfully")
                return True
            else:
                print(f"❌ Failed to start MongoDB service: {result.stderr}")
                
                # Try alternative service name
                result = subprocess.run(['net', 'start', 'MongoDBCompass'], 
                                      capture_output=True, text=True, timeout=30)
                if result.returncode == 0:
                    print("✅ MongoDB service started successfully (MongoDBCompass)")
                    return True
                    
        else:  # Unix-like
            result = subprocess.run(['sudo', 'systemctl', 'start', 'mongod'], 
                                  capture_output=True, text=True, timeout=30)
            if result.returncode == 0:
                print("✅ MongoDB service started successfully")
                return True
            else:
                print(f"❌ Failed to start MongoDB service: {result.stderr}")
                
    except subprocess.TimeoutExpired:
        print("⚠️  Timeout starting MongoDB service")
    except Exception as e:
        print(f"⚠️  Error starting MongoDB service: {e}")
    
    return False

if __name__ == "__main__":
    print("MongoDB Connection and Service Test")
    print("=" * 50)
    
    # Check if MongoDB service is running
    service_running = check_mongodb_service()
    
    # Test connection
    connection_success = test_mongodb_connection()
    
    if not connection_success and not service_running:
        print("\n🔧 MongoDB appears to be not running. Attempting to start...")
        if start_mongodb_service():
            print("\n🔄 Retesting connection after starting service...")
            connection_success = test_mongodb_connection()
    
    print("\n" + "=" * 50)
    print("SUMMARY:")
    print(f"MongoDB Service Running: {'✅ YES' if service_running else '❌ NO'}")
    print(f"MongoDB Connection: {'✅ SUCCESS' if connection_success else '❌ FAILED'}")
    
    if connection_success:
        print("\n✅ MongoDB is ready for use!")
        sys.exit(0)
    else:
        print("\n❌ MongoDB is not accessible. Manual intervention may be required.")
        sys.exit(1)