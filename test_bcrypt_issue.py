#!/usr/bin/env python3
"""
Test script to reproduce and fix bcrypt compatibility issues
"""
import sys
import os
sys.path.append('./backend')

def test_bcrypt_compatibility():
    print("🔍 Testing bcrypt compatibility...")
    
    try:
        from app.core.security import get_password_hash, verify_password
        print("✅ Successfully imported security functions")
        
        # Test with the password that will be used
        test_password = "testpassword123"
        print(f"🔍 Testing password hashing with: '{test_password}' (length: {len(test_password)})")
        
        # Try to hash the password
        hashed = get_password_hash(test_password)
        print(f"✅ Password hashed successfully: {hashed[:50]}...")
        
        # Try to verify the password
        is_valid = verify_password(test_password, hashed)
        print(f"✅ Password verification: {is_valid}")
        
        # Test with a longer password to trigger the 72-byte limit
        long_password = "a" * 80  # 80 characters, definitely over 72 bytes
        print(f"🔍 Testing with long password (length: {len(long_password)})")
        
        try:
            long_hashed = get_password_hash(long_password)
            print(f"✅ Long password hashed successfully")
        except Exception as e:
            print(f"❌ Long password hashing failed: {e}")
            print(f"❌ Error type: {type(e)}")
            return False
            
    except Exception as e:
        print(f"❌ Import or basic functionality failed: {e}")
        print(f"❌ Error type: {type(e)}")
        return False
    
    return True

if __name__ == "__main__":
    success = test_bcrypt_compatibility()
    if success:
        print("🎉 All bcrypt tests passed!")
    else:
        print("💥 Bcrypt compatibility issues detected!")
        sys.exit(1)