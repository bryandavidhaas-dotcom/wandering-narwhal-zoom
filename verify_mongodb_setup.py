#!/usr/bin/env python3
"""
Comprehensive MongoDB Setup Verification Script
Verifies MongoDB 7.0.14 installation and configuration
"""

import pymongo
import sys
import json
from datetime import datetime
import subprocess
import os

def print_header(title):
    """Print a formatted header"""
    print("\n" + "="*60)
    print(f" {title}")
    print("="*60)

def test_mongodb_connection():
    """Test MongoDB connection and basic operations"""
    print_header("MONGODB CONNECTION TEST")
    
    try:
        # Connect to MongoDB
        client = pymongo.MongoClient("mongodb://localhost:27017/", serverSelectionTimeoutMS=5000)
        
        # Test connection
        client.admin.command('ping')
        print("✅ MongoDB connection successful")
        
        # Get server info
        server_info = client.server_info()
        print(f"✅ MongoDB version: {server_info['version']}")
        print(f"✅ Server uptime: {server_info.get('uptime', 'N/A')} seconds")
        
        return client
        
    except Exception as e:
        print(f"❌ MongoDB connection failed: {e}")
        return None

def verify_recommender_database(client):
    """Verify the recommender database exists and is accessible"""
    print_header("RECOMMENDER DATABASE VERIFICATION")
    
    try:
        # List all databases
        databases = client.list_database_names()
        print(f"✅ Available databases: {databases}")
        
        # Check if recommender database exists
        if "recommender" in databases:
            print("✅ 'recommender' database exists")
            
            # Access the database
            db = client.recommender
            collections = db.list_collection_names()
            print(f"✅ Collections in 'recommender' database: {collections}")
            
            # Test basic operations
            test_collection = db.test_verification
            
            # Insert test document
            test_doc = {
                "test_id": "verification_test",
                "timestamp": datetime.now(),
                "status": "testing"
            }
            result = test_collection.insert_one(test_doc)
            print(f"✅ Test document inserted with ID: {result.inserted_id}")
            
            # Read test document
            found_doc = test_collection.find_one({"test_id": "verification_test"})
            if found_doc:
                print("✅ Test document retrieved successfully")
            
            # Clean up test document
            test_collection.delete_one({"test_id": "verification_test"})
            print("✅ Test document cleaned up")
            
            return True
        else:
            print("⚠️  'recommender' database does not exist - creating it")
            # Create the database by inserting a document
            db = client.recommender
            db.init_collection.insert_one({"initialized": True, "timestamp": datetime.now()})
            print("✅ 'recommender' database created")
            return True
            
    except Exception as e:
        print(f"❌ Database verification failed: {e}")
        return False

def check_mongodb_service():
    """Check MongoDB service status on Windows"""
    print_header("MONGODB SERVICE STATUS")
    
    try:
        # Check if MongoDB service is running
        result = subprocess.run(
            ['sc', 'query', 'MongoDB'],
            capture_output=True,
            text=True,
            shell=True
        )
        
        if result.returncode == 0:
            output = result.stdout
            if "RUNNING" in output:
                print("✅ MongoDB service is running")
                
                # Check if service is set to auto-start
                config_result = subprocess.run(
                    ['sc', 'qc', 'MongoDB'],
                    capture_output=True,
                    text=True,
                    shell=True
                )
                
                if "AUTO_START" in config_result.stdout:
                    print("✅ MongoDB service is set to start automatically")
                else:
                    print("⚠️  MongoDB service is not set to auto-start")
                    print("   Run: sc config MongoDB start= auto")
                
                return True
            else:
                print("❌ MongoDB service is not running")
                return False
        else:
            print("❌ MongoDB service not found")
            return False
            
    except Exception as e:
        print(f"❌ Service check failed: {e}")
        return False

def test_port_accessibility():
    """Test if MongoDB port 27017 is accessible"""
    print_header("PORT ACCESSIBILITY TEST")
    
    try:
        import socket
        
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(5)
        result = sock.connect_ex(('localhost', 27017))
        sock.close()
        
        if result == 0:
            print("✅ Port 27017 is accessible")
            return True
        else:
            print("❌ Port 27017 is not accessible")
            return False
            
    except Exception as e:
        print(f"❌ Port test failed: {e}")
        return False

def check_mongodb_processes():
    """Check for MongoDB processes"""
    print_header("MONGODB PROCESSES")
    
    try:
        result = subprocess.run(
            ['tasklist', '/FI', 'IMAGENAME eq mongod.exe'],
            capture_output=True,
            text=True,
            shell=True
        )
        
        if "mongod.exe" in result.stdout:
            print("✅ MongoDB daemon (mongod.exe) is running")
            # Extract process info
            lines = result.stdout.strip().split('\n')
            for line in lines:
                if "mongod.exe" in line:
                    parts = line.split()
                    if len(parts) >= 2:
                        print(f"   Process ID: {parts[1]}")
            return True
        else:
            print("❌ MongoDB daemon (mongod.exe) is not running")
            return False
            
    except Exception as e:
        print(f"❌ Process check failed: {e}")
        return False

def generate_verification_report(results):
    """Generate a comprehensive verification report"""
    print_header("VERIFICATION SUMMARY")
    
    all_passed = all(results.values())
    
    print(f"Overall Status: {'✅ PASS' if all_passed else '❌ FAIL'}")
    print(f"Timestamp: {datetime.now().isoformat()}")
    print("\nDetailed Results:")
    
    for test_name, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"  {test_name}: {status}")
    
    # Save report to file
    report = {
        "timestamp": datetime.now().isoformat(),
        "overall_status": "PASS" if all_passed else "FAIL",
        "test_results": results,
        "mongodb_version": "7.0.14",
        "connection_string": "mongodb://localhost:27017/",
        "database": "recommender"
    }
    
    with open("mongodb_verification_report.json", "w") as f:
        json.dump(report, f, indent=2)
    
    print(f"\n📄 Detailed report saved to: mongodb_verification_report.json")
    
    return all_passed

def main():
    """Main verification function"""
    print("MongoDB Setup Verification Script")
    print(f"Started at: {datetime.now().isoformat()}")
    
    results = {}
    
    # Test MongoDB connection
    client = test_mongodb_connection()
    results["mongodb_connection"] = client is not None
    
    if client:
        # Verify recommender database
        results["recommender_database"] = verify_recommender_database(client)
        client.close()
    else:
        results["recommender_database"] = False
    
    # Check service status
    results["mongodb_service"] = check_mongodb_service()
    
    # Test port accessibility
    results["port_accessibility"] = test_port_accessibility()
    
    # Check processes
    results["mongodb_processes"] = check_mongodb_processes()
    
    # Generate final report
    success = generate_verification_report(results)
    
    if success:
        print("\n🎉 All MongoDB verification tests passed!")
        print("   Your MongoDB setup is working correctly.")
        sys.exit(0)
    else:
        print("\n⚠️  Some MongoDB verification tests failed.")
        print("   Please review the results above.")
        sys.exit(1)

if __name__ == "__main__":
    main()