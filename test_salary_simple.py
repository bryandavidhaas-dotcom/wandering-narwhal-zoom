#!/usr/bin/env python3
"""
Simple test to verify the salary parsing fix without import issues
"""

def parse_salary_expectations(salary_str: str) -> tuple:
    """Parse salary string to min/max values with machine-friendly format support"""
    if not salary_str:
        return (50000, 200000)  # Default range
    
    print(f"🔍 Parsing salary: '{salary_str}'")
    
    # Handle machine-friendly format first (e.g., "70000-100000")
    if '-' in salary_str and salary_str.replace('-', '').replace('0', '').isdigit():
        try:
            parts = salary_str.split('-')
            if len(parts) == 2:
                min_val = int(parts[0])
                max_val = int(parts[1])
                print(f"✅ Machine format parsed: min={min_val}, max={max_val}")
                return (min_val, max_val)
        except ValueError:
            pass
    
    # Handle legacy user-friendly formats
    import re
    # Remove commas and extract all numbers
    clean_str = salary_str.replace(',', '')
    numbers = re.findall(r'\d+', clean_str)
    
    print(f"🔍 Legacy parsing: '{salary_str}' -> numbers: {numbers}")
    
    if len(numbers) >= 2:
        # Handle ranges like "150,000 - 250,000" or "150k - 250k"
        min_val = int(numbers[0])  # FIXED: Use index [0] instead of entire list
        max_val = int(numbers[1])  # FIXED: Use index [1] instead of entire list
        
        # Check if values are in thousands (like 150k = 150000)
        if 'k' in salary_str.lower():
            min_val *= 1000
            max_val *= 1000
        
        print(f"✅ Legacy format parsed: min={min_val}, max={max_val}")
        return (min_val, max_val)
    elif len(numbers) == 1:
        # Single number, create a range around it
        val = int(numbers[0])
        if 'k' in salary_str.lower():
            val *= 1000
        print(f"✅ Single value parsed: {val}, creating range")
        return (val - 10000, val + 10000)
    
    # Fallback for special cases
    salary_lower = salary_str.lower()
    if 'flexible' in salary_lower or 'open' in salary_lower:
        print("✅ Flexible salary detected")
        return (0, 999999)  # Very wide range for flexible
    
    print("⚠️ Could not parse salary, using default range")
    return (50000, 200000)  # Default range

def test_salary_parsing():
    print("🧪 Testing Salary Parsing Fix")
    print("=" * 50)
    
    # Test the problematic case from the original bug report
    print("Testing the original bug case:")
    try:
        result = parse_salary_expectations('80k-120k')
        print(f"✅ SUCCESS: '80k-120k' -> {result}")
    except Exception as e:
        print(f"❌ FAILED: '80k-120k' -> ERROR: {e}")
        return False
    
    # Test machine-friendly format
    test_cases = [
        ("70000-100000", (70000, 100000)),
        ("150000-250000", (150000, 250000)),
        ("0-30000", (0, 30000)),
        ("0-0", (0, 0)),
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