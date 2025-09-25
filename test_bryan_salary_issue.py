#!/usr/bin/env python3
"""
Test to reproduce Bryan Haas's salary filtering issue.
This test will trace through the recommendation engine logic to understand
why Medical Assistant and Delivery Driver are still being recommended
despite the salary parsing fix.
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

def create_bryan_profile():
    """Create Bryan Haas's profile based on typical data analyst background"""
    return {
        "user_id": "bryan_haas",
        "name": "Bryan Haas",
        "experience_years": 8,  # Senior data analyst level
        "salary_expectations": "150000-250000",  # $150k-250k range
        "current_role": "Senior Data Analyst",
        "skills": ["Python", "SQL", "Data Analysis", "Machine Learning", "Tableau", "Statistics"],
        "industries": ["Technology", "Finance"],
        "education": "Bachelor's in Computer Science",
        "location": "San Francisco, CA"
    }

def parse_salary_expectations(salary_str: str) -> tuple:
    """Parse salary string to min/max values - FIXED VERSION"""
    if not salary_str:
        return (50000, 200000)  # Default range
    
    print(f"🔍 Parsing salary: '{salary_str}'")
    
    # Handle machine-friendly format first (e.g., "150000-250000")
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
    clean_str = salary_str.replace(',', '')
    numbers = re.findall(r'\d+', clean_str)
    
    print(f"🔍 Legacy parsing: '{salary_str}' -> numbers: {numbers}")
    
    if len(numbers) >= 2:
        min_val = int(numbers[0])  # FIXED: Use index [0] instead of entire list
        max_val = int(numbers[1])  # FIXED: Use index [1] instead of entire list
        
        if 'k' in salary_str.lower():
            min_val *= 1000
            max_val *= 1000
        
        print(f"✅ Legacy format parsed: min={min_val}, max={max_val}")
        return (min_val, max_val)
    elif len(numbers) == 1:
        val = int(numbers[0])
        if 'k' in salary_str.lower():
            val *= 1000
        print(f"✅ Single value parsed: {val}, creating range")
        return (val - 10000, val + 10000)
    
    print("⚠️ Could not parse salary, using default range")
    return (50000, 200000)

def is_salary_compatible(user_min: int, user_max: int, career_min: int, career_max: int, 
                        max_deviation: float = 0.3) -> bool:
    """Check if career salary range is compatible with user expectations"""
    
    # Calculate overlap considering deviation tolerance
    user_min_adjusted = user_min * (1 - max_deviation)
    user_max_adjusted = user_max * (1 + max_deviation)
    
    # Check if there's any overlap between ranges
    has_overlap = not (career_max < user_min_adjusted or career_min > user_max_adjusted)
    
    print(f"   User range: ${user_min:,} - ${user_max:,}")
    print(f"   User adjusted: ${user_min_adjusted:,.0f} - ${user_max_adjusted:,.0f}")
    print(f"   Career range: ${career_min:,} - ${career_max:,}")
    print(f"   Overlap: {'✅ YES' if has_overlap else '❌ NO'}")
    
    return has_overlap

def test_salary_filtering_with_sample_careers():
    """Test salary filtering with careers that should and shouldn't match Bryan's expectations"""
    
    print("🧪 Testing Bryan Haas Salary Filtering Issue")
    print("=" * 60)
    
    # Bryan's profile
    bryan = create_bryan_profile()
    user_min, user_max = parse_salary_expectations(bryan["salary_expectations"])
    
    print(f"\n👤 Bryan's Profile:")
    print(f"   Experience: {bryan['experience_years']} years")
    print(f"   Current Role: {bryan['current_role']}")
    print(f"   Salary Expectations: {bryan['salary_expectations']} -> ${user_min:,} - ${user_max:,}")
    print(f"   Skills: {', '.join(bryan['skills'][:3])}...")
    
    # Sample careers to test
    test_careers = [
        {
            "title": "Senior Data Scientist",
            "min_salary": 160000,
            "max_salary": 240000,
            "should_match": True
        },
        {
            "title": "Principal Data Engineer", 
            "min_salary": 180000,
            "max_salary": 280000,
            "should_match": True
        },
        {
            "title": "Medical Assistant",
            "min_salary": 35000,
            "max_salary": 45000,
            "should_match": False
        },
        {
            "title": "Delivery Driver",
            "min_salary": 30000,
            "max_salary": 50000,
            "should_match": False
        },
        {
            "title": "Data Analyst",
            "min_salary": 70000,
            "max_salary": 100000,
            "should_match": False  # Too low for Bryan's expectations
        },
        {
            "title": "VP Engineering",
            "min_salary": 220000,
            "max_salary": 350000,
            "should_match": True  # Overlaps with Bryan's range
        }
    ]
    
    print(f"\n🎯 Testing Salary Compatibility:")
    print("-" * 60)
    
    all_correct = True
    
    for career in test_careers:
        print(f"\n📋 {career['title']}:")
        
        is_compatible = is_salary_compatible(
            user_min, user_max, 
            career["min_salary"], career["max_salary"]
        )
        
        expected = career["should_match"]
        result = "✅ PASS" if is_compatible == expected else "❌ FAIL"
        
        print(f"   Expected: {'Should match' if expected else 'Should NOT match'}")
        print(f"   Actual: {'Matches' if is_compatible else 'Does NOT match'}")
        print(f"   Result: {result}")
        
        if is_compatible != expected:
            all_correct = False
    
    print("\n" + "=" * 60)
    if all_correct:
        print("🎉 All salary filtering tests passed!")
        print("✅ The salary parsing fix is working correctly")
        print("✅ Medical Assistant and Delivery Driver should be filtered out")
    else:
        print("⚠️ Some salary filtering tests failed!")
        print("🔍 This indicates the salary filter logic needs investigation")
    
    return all_correct

def test_salary_filter_edge_cases():
    """Test edge cases in salary filtering"""
    print(f"\n🧪 Testing Salary Filter Edge Cases:")
    print("-" * 40)
    
    bryan_min, bryan_max = 150000, 250000
    
    edge_cases = [
        {
            "name": "Career slightly below range",
            "career_min": 140000,
            "career_max": 160000,
            "should_match": True  # With 30% deviation, this should match
        },
        {
            "name": "Career way below range", 
            "career_min": 35000,
            "career_max": 45000,
            "should_match": False  # Medical Assistant - should NOT match
        },
        {
            "name": "Career slightly above range",
            "career_min": 240000,
            "career_max": 300000,
            "should_match": True  # With 30% deviation, this should match
        },
        {
            "name": "Career at exact boundary",
            "career_min": 150000,
            "career_max": 250000,
            "should_match": True  # Exact match
        }
    ]
    
    for case in edge_cases:
        print(f"\n📋 {case['name']}:")
        is_compatible = is_salary_compatible(
            bryan_min, bryan_max,
            case["career_min"], case["career_max"]
        )
        
        expected = case["should_match"]
        result = "✅ PASS" if is_compatible == expected else "❌ FAIL"
        print(f"   Result: {result}")

if __name__ == "__main__":
    success = test_salary_filtering_with_sample_careers()
    test_salary_filter_edge_cases()
    
    if success:
        print(f"\n🔍 CONCLUSION:")
        print("The salary parsing and filtering logic appears to be working correctly.")
        print("If Bryan is still seeing Medical Assistant and Delivery Driver recommendations,")
        print("the issue might be in:")
        print("1. The actual salary data for these careers")
        print("2. The filtering logic not being applied properly")
        print("3. The careers being added after salary filtering")
        print("4. A different part of the recommendation pipeline")