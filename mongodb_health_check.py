#!/usr/bin/env python3
"""
Quick MongoDB Health Check Script
Use this for regular verification of MongoDB status
"""

import pymongo
import subprocess
import socket
from datetime import datetime

def quick_health_check():
    """Perform a quick health check of MongoDB"""
    print("MongoDB Quick Health Check")
    print(f"Timestamp: {datetime.now().isoformat()}")
    print("-" * 40)
    
    checks_passed = 0
    total_checks = 4
    
    # 1. Service Status
    try:
        result = subprocess.run(['sc', 'query', 'MongoDB'], capture_output=True, text=True, shell=True)
        if "RUNNING" in result.stdout:
            print("✅ MongoDB service is running")
            checks_passed += 1
        else:
            print("❌ MongoDB service is not running")
    except:
        print("❌ Could not check MongoDB service status")
    
    # 2. Port Accessibility
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(3)
        result = sock.connect_ex(('localhost', 27017))
        sock.close()
        if result == 0:
            print("✅ Port 27017 is accessible")
            checks_passed += 1
        else:
            print("❌ Port 27017 is not accessible")
    except:
        print("❌ Could not test port accessibility")
    
    # 3. Database Connection
    try:
        client = pymongo.MongoClient("mongodb://localhost:27017/", serverSelectionTimeoutMS=3000)
        client.admin.command('ping')
        print("✅ Database connection successful")
        checks_passed += 1
        client.close()
    except:
        print("❌ Database connection failed")
    
    # 4. Recommender Database
    try:
        client = pymongo.MongoClient("mongodb://localhost:27017/", serverSelectionTimeoutMS=3000)
        databases = client.list_database_names()
        if "recommender" in databases:
            print("✅ 'recommender' database exists")
            checks_passed += 1
        else:
            print("⚠️  'recommender' database not found")
        client.close()
    except:
        print("❌ Could not check recommender database")
    
    # Summary
    print("-" * 40)
    if checks_passed == total_checks:
        print("🎉 All health checks passed!")
        print("   MongoDB is working correctly.")
    else:
        print(f"⚠️  {checks_passed}/{total_checks} health checks passed.")
        print("   Some issues detected - run full verification if needed.")
    
    return checks_passed == total_checks

if __name__ == "__main__":
    quick_health_check()