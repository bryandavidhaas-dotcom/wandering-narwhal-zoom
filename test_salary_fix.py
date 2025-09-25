#!/usr/bin/env python3
"""
Quick test to verify the salary parsing fix
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

from comprehensive_careers import parse_salary_expectations

def test_salary_parsing():
    print("🧪 Testing Salary Parsing Fix")
    print("=" * 50)
    
    # Test cases that should work now
    test_cases = [
        # Machine-friendly format (new)
        ("70000-100000", (70000, 100000)),
        ("150000-250000", (150000, 250000)),
        ("0-30000", (0, 30000)),
        ("0-0", (0, 0)),
        
        # Legacy formats (should still work)
        ("80k-120k", (80000, 120000)),
        ("150,000-250,000", (150000, 250000)),
        ("$70,000 - $100,000", (70000, 100000)),
        
        # Special cases
        ("flexible", (0, 999999)),
        ("open to discussion", (0, 999999)),
        ("", (50000, 200000)),  # Default
    ]
    
    all_passed = True
    
    for input_str, expected in test_cases:
        try:
            result = parse_salary_expectations(input_str)
            if result == expected:
                print(f"✅ PASS: '{input_str}' -> {result}")
            else:
                print(f"❌ FAIL: '{input_str}' -> {result}, expected {expected}")
                all_passed = False
        except Exception as e:
            print(f"💥 ERROR: '{input_str}' -> {str(e)}")
            all_passed = False
    
    print("=" * 50)
    if all_passed:
        print("🎉 All tests passed! Salary parsing is fixed.")
    else:
        print("⚠️ Some tests failed. Check the implementation.")
    
    return all_passed

if __name__ == "__main__":
    test_salary_parsing()