#!/usr/bin/env python3
"""
Direct test of the security module to see what's actually being imported.
"""

import sys
import os

# Add the backend directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

def test_security_import():
    """Test what's actually being imported from security module"""
    try:
        print("🔍 Testing security module import...")
        
        # Import the function
        from app.core.security import get_password_hash
        
        # Check the function details
        import inspect
        print(f"🔍 Function: {get_password_hash}")
        print(f"🔍 Module: {get_password_hash.__module__}")
        print(f"🔍 File: {inspect.getfile(get_password_hash)}")
        
        # Get the source code
        try:
            source = inspect.getsource(get_password_hash)
            print(f"🔍 Source code:")
            print(source)
        except Exception as e:
            print(f"❌ Could not get source: {e}")
        
        # Test the function
        password = "testpassword123"
        print(f"\n🔧 Testing with password: '{password}'")
        
        hashed = get_password_hash(password)
        print(f"✅ Hashed successfully: {hashed}")
        
        return True
        
    except Exception as e:
        print(f"❌ Security module test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    test_security_import()