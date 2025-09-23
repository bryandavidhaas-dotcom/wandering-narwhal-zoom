#!/usr/bin/env python3
"""
Simple test to check if ENABLE_SENIORITY_CATEGORY_GUARDRAIL flag exists in config.
"""

import sys
import os

# Add the recommendation-engine directory to Python path
sys.path.insert(0, os.path.join(os.getcwd(), 'recommendation-engine'))

def test_config_flag():
    """Test if the ENABLE_SENIORITY_CATEGORY_GUARDRAIL flag exists."""
    print("🔍 Testing ENABLE_SENIORITY_CATEGORY_GUARDRAIL flag...")
    
    try:
        # Try to import the config module
        import config
        print("✅ Config module imported successfully")
        
        # Check if the flag exists
        if hasattr(config, 'ENABLE_SENIORITY_CATEGORY_GUARDRAIL'):
            flag_value = getattr(config, 'ENABLE_SENIORITY_CATEGORY_GUARDRAIL')
            print(f"✅ ENABLE_SENIORITY_CATEGORY_GUARDRAIL found: {flag_value}")
            return True, flag_value
        else:
            print("❌ ENABLE_SENIORITY_CATEGORY_GUARDRAIL NOT FOUND in config module")
            print("   This is the ROOT CAUSE of the issue!")
            
            # List all attributes in config to see what's available
            print("\n📋 Available config attributes:")
            config_attrs = [attr for attr in dir(config) if not attr.startswith('_')]
            for attr in config_attrs:
                print(f"   - {attr}")
            
            return False, None
            
    except ImportError as e:
        print(f"❌ Failed to import config module: {e}")
        return False, None
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False, None

def test_filters_import():
    """Test if we can import the filters module and see the problematic line."""
    print("\n🔍 Testing filters module import...")
    
    try:
        import filters
        print("✅ Filters module imported successfully")
        
        # Try to access the problematic line
        print("📋 Checking filters.py line 73 logic...")
        
        # Read the filters.py file to show the problematic line
        with open('recommendation-engine/filters.py', 'r') as f:
            lines = f.readlines()
            if len(lines) > 72:  # Line 73 is index 72
                problematic_line = lines[72].strip()
                print(f"   Line 73: {problematic_line}")
                
                if 'config.ENABLE_SENIORITY_CATEGORY_GUARDRAIL' in problematic_line:
                    print("   ⚠️  This line will fail if the config flag doesn't exist!")
                    return True
        
        return True
        
    except Exception as e:
        print(f"❌ Error testing filters: {e}")
        return False

def main():
    """Run the diagnostic tests."""
    print("🚨 SENIORITY GUARDRAIL ROOT CAUSE ANALYSIS")
    print("=" * 50)
    
    # Test 1: Check config flag
    flag_exists, flag_value = test_config_flag()
    
    # Test 2: Check filters import
    filters_ok = test_filters_import()
    
    print("\n" + "=" * 50)
    print("🎯 DIAGNOSIS RESULTS")
    print("=" * 50)
    
    if not flag_exists:
        print("🚨 ROOT CAUSE CONFIRMED:")
        print("   The ENABLE_SENIORITY_CATEGORY_GUARDRAIL flag is MISSING from config.py")
        print("   This causes the seniority guardrail logic to never execute!")
        print("\n💡 SOLUTION:")
        print("   Add the following line to recommendation-engine/config.py:")
        print("   ENABLE_SENIORITY_CATEGORY_GUARDRAIL = True")
        print("\n🔧 IMPACT:")
        print("   - Senior users (10+ years experience) get junior role recommendations")
        print("   - Medical Assistant, Delivery Driver, etc. are not filtered out")
        print("   - The categorization engine is never instantiated for field filtering")
    else:
        print(f"✅ Config flag exists with value: {flag_value}")
        if not flag_value:
            print("⚠️  However, the flag is set to False, so guardrail is disabled")
        else:
            print("🤔 Flag exists and is True - need to investigate further")

if __name__ == "__main__":
    main()