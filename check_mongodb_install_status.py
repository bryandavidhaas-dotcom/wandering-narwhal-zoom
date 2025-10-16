#!/usr/bin/env python3
"""
MongoDB Installation Status Checker
===================================
Monitors the winget MongoDB installation and checks when it's complete
"""

import subprocess
import time
import sys

def check_installation_status():
    print("🔍 CHECKING MONGODB INSTALLATION STATUS")
    print("=" * 45)
    
    # Check if winget process is still running
    try:
        result = subprocess.run(['tasklist', '/FI', 'IMAGENAME eq winget.exe'], 
                              capture_output=True, text=True)
        
        if 'winget.exe' in result.stdout:
            print("⏳ MongoDB installation is STILL RUNNING")
            print("   winget.exe process is active")
            
            # Extract PID if possible
            lines = result.stdout.strip().split('\n')
            for line in lines:
                if 'winget.exe' in line:
                    parts = line.split()
                    if len(parts) >= 2:
                        pid = parts[1]
                        print(f"   Process ID: {pid}")
            
            print("\n💡 HOW TO KNOW WHEN IT'S COMPLETE:")
            print("   1. Terminal 3 will show completion message")
            print("   2. Command prompt will return (you'll see the prompt again)")
            print("   3. This script will show 'INSTALLATION COMPLETE'")
            print("   4. You can run: python mongodb_diagnostic.py")
            
            return False
            
        else:
            print("✅ MongoDB installation appears COMPLETE")
            print("   No winget.exe process found")
            
            # Double-check by trying to find MongoDB
            try:
                mongo_result = subprocess.run(['mongod', '--version'], 
                                            capture_output=True, text=True, timeout=5)
                if mongo_result.returncode == 0:
                    print("✅ MongoDB is now available in PATH")
                    version_line = mongo_result.stdout.split('\n')[0]
                    print(f"   {version_line}")
                    
                    print("\n🎉 INSTALLATION COMPLETE!")
                    print("   Next steps:")
                    print("   1. Run: python fix_auth_immediate.py")
                    print("   2. Or run: python mongodb_diagnostic.py")
                    
                    return True
                else:
                    print("⚠️  Installation may be complete but MongoDB not in PATH")
                    print("   Try restarting your terminal or computer")
                    return False
                    
            except (FileNotFoundError, subprocess.TimeoutExpired):
                print("⚠️  Installation complete but MongoDB not yet available")
                print("   You may need to:")
                print("   - Restart your terminal")
                print("   - Restart your computer")
                print("   - Check Windows Services for MongoDB")
                return False
                
    except Exception as e:
        print(f"❌ Error checking installation status: {e}")
        return False

def monitor_installation():
    """Continuously monitor until installation is complete"""
    print("🔄 MONITORING MONGODB INSTALLATION...")
    print("Press Ctrl+C to stop monitoring\n")
    
    try:
        while True:
            complete = check_installation_status()
            if complete:
                break
            
            print(f"\n⏰ Checking again in 30 seconds...")
            print("-" * 45)
            time.sleep(30)
            
    except KeyboardInterrupt:
        print("\n\n⏹️  Monitoring stopped by user")
        print("Run this script again anytime to check status")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--monitor":
        monitor_installation()
    else:
        check_installation_status()
        print("\n💡 TIP: Run 'python check_mongodb_install_status.py --monitor' to continuously monitor")