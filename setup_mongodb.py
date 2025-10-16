#!/usr/bin/env python3
"""
MongoDB Setup and Installation Script
=====================================
This script sets up MongoDB for the career platform, with multiple fallback options:
1. Check if MongoDB is already running
2. Try to start local MongoDB service
3. Install MongoDB if not present
4. Use MongoDB Atlas cloud option
5. Use embedded alternative (TinyDB) as fallback

Author: Phase 2 Setup System
Date: 2025-01-07
"""

import os
import sys
import subprocess
import asyncio
import platform
from pathlib import Path
from motor.motor_asyncio import AsyncIOMotorClient

class MongoDBSetup:
    def __init__(self):
        self.system = platform.system().lower()
        self.mongo_url = "mongodb://localhost:27017"
        self.db_name = "career_platform"
        
    def log(self, message: str, level: str = "INFO"):
        """Log setup progress"""
        print(f"[{level}] {message}")
    
    async def test_mongodb_connection(self, url: str = None) -> bool:
        """Test MongoDB connection"""
        test_url = url or self.mongo_url
        try:
            client = AsyncIOMotorClient(test_url, serverSelectionTimeoutMS=5000)
            await client.admin.command('ping')
            client.close()
            self.log(f"✅ MongoDB connection successful: {test_url}")
            return True
        except Exception as e:
            self.log(f"❌ MongoDB connection failed: {e}")
            return False
    
    def check_mongodb_installed(self) -> bool:
        """Check if MongoDB is installed"""
        try:
            result = subprocess.run(['mongod', '--version'], 
                                  capture_output=True, text=True, timeout=10)
            if result.returncode == 0:
                self.log("✅ MongoDB is installed")
                return True
        except (subprocess.TimeoutExpired, FileNotFoundError):
            pass
        
        self.log("❌ MongoDB is not installed")
        return False
    
    def install_mongodb_windows(self) -> bool:
        """Install MongoDB on Windows using chocolatey"""
        self.log("🔧 Installing MongoDB on Windows...")
        try:
            # Check if chocolatey is available
            subprocess.run(['choco', '--version'], check=True, capture_output=True)
            
            # Install MongoDB
            result = subprocess.run(['choco', 'install', 'mongodb', '-y'], 
                                  capture_output=True, text=True)
            
            if result.returncode == 0:
                self.log("✅ MongoDB installed successfully")
                return True
            else:
                self.log(f"❌ MongoDB installation failed: {result.stderr}")
                return False
                
        except subprocess.CalledProcessError:
            self.log("❌ Chocolatey not available. Please install MongoDB manually.")
            return False
        except FileNotFoundError:
            self.log("❌ Chocolatey not found. Please install MongoDB manually.")
            return False
    
    def install_mongodb_linux(self) -> bool:
        """Install MongoDB on Linux"""
        self.log("🔧 Installing MongoDB on Linux...")
        try:
            # Try apt-get first (Ubuntu/Debian)
            result = subprocess.run(['sudo', 'apt-get', 'update'], 
                                  capture_output=True, text=True)
            if result.returncode == 0:
                subprocess.run(['sudo', 'apt-get', 'install', '-y', 'mongodb'], 
                             check=True)
                self.log("✅ MongoDB installed successfully")
                return True
        except subprocess.CalledProcessError:
            pass
        
        try:
            # Try yum (CentOS/RHEL)
            subprocess.run(['sudo', 'yum', 'install', '-y', 'mongodb-server'], 
                         check=True)
            self.log("✅ MongoDB installed successfully")
            return True
        except subprocess.CalledProcessError:
            pass
        
        self.log("❌ Could not install MongoDB automatically")
        return False
    
    def install_mongodb_mac(self) -> bool:
        """Install MongoDB on macOS using homebrew"""
        self.log("🔧 Installing MongoDB on macOS...")
        try:
            # Check if homebrew is available
            subprocess.run(['brew', '--version'], check=True, capture_output=True)
            
            # Install MongoDB
            subprocess.run(['brew', 'tap', 'mongodb/brew'], check=True)
            subprocess.run(['brew', 'install', 'mongodb-community'], check=True)
            
            self.log("✅ MongoDB installed successfully")
            return True
            
        except subprocess.CalledProcessError:
            self.log("❌ Homebrew not available or installation failed")
            return False
        except FileNotFoundError:
            self.log("❌ Homebrew not found. Please install MongoDB manually.")
            return False
    
    def start_mongodb_service(self) -> bool:
        """Start MongoDB service"""
        self.log("🚀 Starting MongoDB service...")
        
        try:
            if self.system == "windows":
                # Try to start MongoDB service on Windows
                result = subprocess.run(['net', 'start', 'MongoDB'], 
                                      capture_output=True, text=True)
                if result.returncode == 0:
                    self.log("✅ MongoDB service started")
                    return True
                else:
                    # Try alternative service name
                    result = subprocess.run(['sc', 'start', 'MongoDB'], 
                                          capture_output=True, text=True)
                    if result.returncode == 0:
                        self.log("✅ MongoDB service started")
                        return True
            
            elif self.system == "linux":
                # Try systemctl first
                result = subprocess.run(['sudo', 'systemctl', 'start', 'mongod'], 
                                      capture_output=True, text=True)
                if result.returncode == 0:
                    self.log("✅ MongoDB service started")
                    return True
                
                # Try service command
                result = subprocess.run(['sudo', 'service', 'mongod', 'start'], 
                                      capture_output=True, text=True)
                if result.returncode == 0:
                    self.log("✅ MongoDB service started")
                    return True
            
            elif self.system == "darwin":  # macOS
                result = subprocess.run(['brew', 'services', 'start', 'mongodb-community'], 
                                      capture_output=True, text=True)
                if result.returncode == 0:
                    self.log("✅ MongoDB service started")
                    return True
            
            self.log("❌ Could not start MongoDB service")
            return False
            
        except Exception as e:
            self.log(f"❌ Error starting MongoDB service: {e}")
            return False
    
    def create_mongodb_data_directory(self) -> bool:
        """Create MongoDB data directory"""
        try:
            data_dir = Path("./mongodb_data")
            data_dir.mkdir(exist_ok=True)
            self.log(f"✅ MongoDB data directory created: {data_dir.absolute()}")
            return True
        except Exception as e:
            self.log(f"❌ Could not create data directory: {e}")
            return False
    
    def start_mongodb_manually(self) -> bool:
        """Start MongoDB manually with custom data directory"""
        self.log("🔧 Starting MongoDB manually...")
        
        try:
            if not self.create_mongodb_data_directory():
                return False
            
            # Start MongoDB with custom data directory
            data_dir = Path("./mongodb_data").absolute()
            
            if self.system == "windows":
                cmd = ['mongod', '--dbpath', str(data_dir), '--port', '27017']
            else:
                cmd = ['mongod', '--dbpath', str(data_dir), '--port', '27017', '--fork', '--logpath', './mongodb.log']
            
            process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            
            # Give MongoDB time to start
            import time
            time.sleep(3)
            
            if process.poll() is None:  # Process is still running
                self.log("✅ MongoDB started manually")
                return True
            else:
                self.log("❌ MongoDB failed to start manually")
                return False
                
        except Exception as e:
            self.log(f"❌ Error starting MongoDB manually: {e}")
            return False
    
    def setup_embedded_alternative(self) -> bool:
        """Setup TinyDB as embedded alternative"""
        self.log("🔄 Setting up embedded database alternative...")
        
        try:
            # Install TinyDB if not present
            subprocess.run([sys.executable, '-m', 'pip', 'install', 'tinydb'], 
                         check=True, capture_output=True)
            
            # Create embedded database adapter
            self.create_embedded_adapter()
            
            self.log("✅ Embedded database alternative ready")
            return True
            
        except Exception as e:
            self.log(f"❌ Could not setup embedded alternative: {e}")
            return False
    
    def create_embedded_adapter(self):
        """Create an adapter for embedded database"""
        adapter_code = '''#!/usr/bin/env python3
"""
Embedded Database Adapter
========================
Provides MongoDB-like interface using TinyDB for development/testing
"""

from tinydb import TinyDB, Query
from typing import List, Dict, Any
import uuid
from datetime import datetime

class EmbeddedCareerDB:
    def __init__(self, db_path: str = "embedded_careers.json"):
        self.db = TinyDB(db_path)
        self.careers = self.db.table('careers')
    
    def insert_career(self, career_data: Dict[str, Any]) -> str:
        """Insert a career record"""
        if 'career_id' not in career_data:
            career_data['career_id'] = str(uuid.uuid4())
        
        career_data['created_at'] = datetime.utcnow().isoformat()
        career_data['updated_at'] = datetime.utcnow().isoformat()
        
        self.careers.insert(career_data)
        return career_data['career_id']
    
    def find_careers(self, query: Dict[str, Any] = None) -> List[Dict[str, Any]]:
        """Find careers matching query"""
        if not query:
            return self.careers.all()
        
        Career = Query()
        results = []
        
        for key, value in query.items():
            if hasattr(Career, key):
                results = self.careers.search(getattr(Career, key) == value)
                break
        
        return results
    
    def count_careers(self) -> int:
        """Count total careers"""
        return len(self.careers)
    
    def clear_careers(self):
        """Clear all careers"""
        self.careers.truncate()

# Global instance
embedded_db = EmbeddedCareerDB()
'''
        
        with open('embedded_db_adapter.py', 'w') as f:
            f.write(adapter_code)
    
    async def run_setup(self) -> bool:
        """Run complete MongoDB setup process"""
        self.log("🚀 Starting MongoDB Setup Process")
        self.log("=" * 50)
        
        # Step 1: Test if MongoDB is already running
        if await self.test_mongodb_connection():
            self.log("✅ MongoDB is already running and accessible")
            return True
        
        # Step 2: Check if MongoDB is installed
        if not self.check_mongodb_installed():
            self.log("📦 MongoDB not found. Attempting installation...")
            
            # Try to install MongoDB
            if self.system == "windows":
                if not self.install_mongodb_windows():
                    self.log("⚠️ Automatic installation failed. Using embedded alternative.")
                    return self.setup_embedded_alternative()
            elif self.system == "linux":
                if not self.install_mongodb_linux():
                    self.log("⚠️ Automatic installation failed. Using embedded alternative.")
                    return self.setup_embedded_alternative()
            elif self.system == "darwin":
                if not self.install_mongodb_mac():
                    self.log("⚠️ Automatic installation failed. Using embedded alternative.")
                    return self.setup_embedded_alternative()
        
        # Step 3: Try to start MongoDB service
        if not self.start_mongodb_service():
            self.log("⚠️ Service start failed. Trying manual start...")
            
            # Step 4: Try manual start
            if not self.start_mongodb_manually():
                self.log("⚠️ Manual start failed. Using embedded alternative.")
                return self.setup_embedded_alternative()
        
        # Step 5: Test connection again
        import time
        time.sleep(2)  # Give MongoDB time to fully start
        
        if await self.test_mongodb_connection():
            self.log("✅ MongoDB setup completed successfully")
            return True
        else:
            self.log("⚠️ MongoDB setup failed. Using embedded alternative.")
            return self.setup_embedded_alternative()

async def main():
    """Main setup function"""
    setup = MongoDBSetup()
    success = await setup.run_setup()
    
    if success:
        print("\n🎉 DATABASE SETUP SUCCESSFUL!")
        print("Ready to proceed with Phase 2 migration.")
    else:
        print("\n❌ DATABASE SETUP FAILED!")
        print("Please install MongoDB manually or use the embedded alternative.")
    
    return success

if __name__ == "__main__":
    asyncio.run(main())