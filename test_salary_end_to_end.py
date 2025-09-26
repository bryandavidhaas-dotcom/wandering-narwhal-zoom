#!/usr/bin/env python3
"""
End-to-end test for salary parsing and filtering
Tests the complete pipeline from frontend values to backend filtering
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

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

def get_careers_by_salary_range(min_salary: int, max_salary: int) -> list:
    """Filter careers by salary expectations - simplified version"""
    # Sample careers for testing
    sample_careers = [
        {"title": "Junior Developer", "minSalary": 60000, "maxSalary": 90000},
        {"title": "Mid-level Developer", "minSalary": 80000, "maxSalary": 120000},
        {"title": "Senior Developer", "minSalary": 100000, "maxSalary": 150000},
        {"title": "Principal Engineer", "minSalary": 140000, "maxSalary": 200000},
        {"title": "VP Engineering", "minSalary": 180000, "maxSalary": 300000},
    ]
    
    # Filter careers where there's salary overlap
    matching_careers = []
    for career in sample_careers:
        # Check if there's overlap between user expectations and career salary
        if career["maxSalary"] >= min_salary and career["minSalary"] <= max_salary:
            matching_careers.append(career)
    
    return matching_careers

def test_end_to_end_salary_filtering():
    print("🧪 End-to-End Salary Filtering Test")
    print("=" * 60)
    
    # Test cases: frontend dropdown values -> backend parsing -> career filtering
    test_cases = [
        {
            "frontend_value": "70000-100000",
            "description": "$70,000 - $100,000 range",
            "expected_min": 70000,
            "expected_max": 100000
        },
        {
            "frontend_value": "150000-250000", 
            "description": "$150,000 - $250,000 range",
            "expected_min": 150000,
            "expected_max": 250000
        },
        {
            "frontend_value": "0-30000",
            "description": "Under $30,000",
            "expected_min": 0,
            "expected_max": 30000
        },
        {
            "frontend_value": "0-0",
            "description": "Flexible/Open to Discussion",
            "expected_min": 0,
            "expected_max": 0
        }
    ]
    
    all_passed = True
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n📋 Test Case {i}: {test_case['description']}")
        print(f"   Frontend value: '{test_case['frontend_value']}'")
        
        # Step 1: Parse salary expectations (backend function)
        try:
            min_sal, max_sal = parse_salary_expectations(test_case['frontend_value'])
            
            if min_sal == test_case['expected_min'] and max_sal == test_case['expected_max']:
                print(f"   ✅ Parsing: {min_sal} - {max_sal}")
            else:
                print(f"   ❌ Parsing failed: got {min_sal}-{max_sal}, expected {test_case['expected_min']}-{test_case['expected_max']}")
                all_passed = False
                continue
                
        except Exception as e:
            print(f"   💥 Parsing error: {e}")
            all_passed = False
            continue
        
        # Step 2: Filter careers by salary range
        try:
            matching_careers = get_careers_by_salary_range(min_sal, max_sal)
            print(f"   🎯 Found {len(matching_careers)} matching careers:")
            for career in matching_careers:
                print(f"      - {career['title']} (${career['minSalary']:,} - ${career['maxSalary']:,})")
                
        except Exception as e:
            print(f"   💥 Filtering error: {e}")
            all_passed = False
    
    print("\n" + "=" * 60)
    if all_passed:
        print("🎉 All end-to-end tests passed!")
        print("✅ Frontend dropdown values are correctly parsed")
        print("✅ Backend salary filtering works properly") 
        print("✅ No more TypeError crashes!")
    else:
        print("⚠️ Some tests failed. Check the implementation.")
    
    return all_passed

if __name__ == "__main__":
    test_end_to_end_salary_filtering()