#!/usr/bin/env python3
"""
Test to trace through the entire recommendation pipeline and identify
where Medical Assistant and Delivery Driver recommendations are coming from
despite proper salary filtering.
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

from backend.comprehensive_careers import COMPREHENSIVE_CAREERS, parse_salary_expectations
from backend.healthcare_careers import HEALTHCARE_CAREERS

def create_bryan_profile():
    """Create Bryan's profile similar to what the frontend would send"""
    return {
        "user_id": "bryan_haas",
        "name": "Bryan Haas",
        "experience_years": 8,
        "salary_expectations": "150000-250000",  # $150k-250k
        "current_role": "Senior Data Analyst", 
        "skills": ["Python", "SQL", "Data Analysis", "Machine Learning", "Tableau"],
        "industries": ["Technology", "Finance"],
        "education": "Bachelor's in Computer Science",
        "location": "San Francisco, CA"
    }

def apply_salary_filter(careers, user_min_salary, user_max_salary, max_deviation=0.3):
    """Apply salary filtering logic"""
    filtered_careers = []
    
    # Calculate user's adjusted range with deviation tolerance
    user_min_adjusted = user_min_salary * (1 - max_deviation)
    user_max_adjusted = user_max_salary * (1 + max_deviation)
    
    print(f"🔍 Salary Filter Applied:")
    print(f"   User expectations: ${user_min_salary:,} - ${user_max_salary:,}")
    print(f"   User adjusted range: ${user_min_adjusted:,.0f} - ${user_max_adjusted:,.0f}")
    print(f"   Deviation tolerance: {max_deviation*100}%")
    
    rejected_careers = []
    
    for career in careers:
        career_min = career.get("minSalary", 0)
        career_max = career.get("maxSalary", 999999)
        
        # Check if there's overlap between user range and career range
        has_overlap = not (career_max < user_min_adjusted or career_min > user_max_adjusted)
        
        if has_overlap:
            filtered_careers.append(career)
        else:
            rejected_careers.append({
                "title": career["title"],
                "salary_range": f"${career_min:,} - ${career_max:,}",
                "reason": "Salary mismatch"
            })
    
    print(f"   ✅ Careers passed filter: {len(filtered_careers)}")
    print(f"   ❌ Careers rejected: {len(rejected_careers)}")
    
    # Show some rejected careers for debugging
    if rejected_careers:
        print(f"   📋 Sample rejected careers:")
        for career in rejected_careers[:5]:
            print(f"      - {career['title']}: {career['salary_range']}")
    
    return filtered_careers, rejected_careers

def apply_experience_filter(careers, user_experience_years):
    """Apply experience level filtering"""
    filtered_careers = []
    rejected_careers = []
    
    print(f"\n🔍 Experience Filter Applied:")
    print(f"   User experience: {user_experience_years} years")
    
    for career in careers:
        min_exp = career.get("minExperienceYears", 0)
        max_exp = career.get("maxExperienceYears", 50)
        
        # Allow some flexibility in experience matching
        exp_buffer = 2  # Allow 2 years flexibility
        
        if (user_experience_years >= (min_exp - exp_buffer) and 
            user_experience_years <= (max_exp + exp_buffer)):
            filtered_careers.append(career)
        else:
            rejected_careers.append({
                "title": career["title"],
                "exp_range": f"{min_exp}-{max_exp} years",
                "reason": "Experience mismatch"
            })
    
    print(f"   ✅ Careers passed filter: {len(filtered_careers)}")
    print(f"   ❌ Careers rejected: {len(rejected_careers)}")
    
    return filtered_careers, rejected_careers

def find_problematic_careers(all_careers):
    """Find Medical Assistant and Delivery Driver in the career database"""
    problematic_careers = []
    
    for career in all_careers:
        title = career["title"].lower()
        if "medical assistant" in title or "delivery driver" in title:
            problematic_careers.append(career)
    
    return problematic_careers

def test_full_recommendation_pipeline():
    """Test the complete recommendation pipeline"""
    print("🧪 Testing Full Recommendation Pipeline")
    print("=" * 60)
    
    # Step 1: Get Bryan's profile
    bryan = create_bryan_profile()
    user_min, user_max = parse_salary_expectations(bryan["salary_expectations"])
    
    print(f"👤 Bryan's Profile:")
    print(f"   Experience: {bryan['experience_years']} years")
    print(f"   Salary Expectations: ${user_min:,} - ${user_max:,}")
    print(f"   Current Role: {bryan['current_role']}")
    
    # Step 2: Get all available careers
    all_careers = COMPREHENSIVE_CAREERS.copy()
    print(f"\n📊 Career Database:")
    print(f"   Total careers available: {len(all_careers)}")
    
    # Step 3: Look for problematic careers in the database
    problematic = find_problematic_careers(all_careers)
    print(f"\n🔍 Searching for problematic careers:")
    if problematic:
        print(f"   Found {len(problematic)} problematic careers:")
        for career in problematic:
            print(f"   - {career['title']}: ${career.get('minSalary', 'N/A'):,} - ${career.get('maxSalary', 'N/A'):,}")
    else:
        print("   ✅ No 'Medical Assistant' or 'Delivery Driver' found in main database")
    
    # Step 4: Check healthcare careers specifically
    print(f"\n🏥 Checking Healthcare Careers Database:")
    healthcare_problematic = find_problematic_careers(HEALTHCARE_CAREERS)
    if healthcare_problematic:
        print(f"   Found {len(healthcare_problematic)} problematic careers in healthcare:")
        for career in healthcare_problematic:
            min_sal = career.get('minSalary', 0)
            max_sal = career.get('maxSalary', 0)
            print(f"   - {career['title']}: ${min_sal:,} - ${max_sal:,}")
            print(f"     Experience Level: {career.get('experienceLevel', 'N/A')}")
            print(f"     Experience Years: {career.get('minExperienceYears', 'N/A')}-{career.get('maxExperienceYears', 'N/A')}")
    else:
        print("   ✅ No problematic careers found in healthcare database")
    
    # Step 5: Apply salary filtering to all careers
    print(f"\n" + "="*60)
    salary_filtered, salary_rejected = apply_salary_filter(all_careers, user_min, user_max)
    
    # Step 6: Apply experience filtering
    exp_filtered, exp_rejected = apply_experience_filter(salary_filtered, bryan["experience_years"])
    
    # Step 7: Check if problematic careers made it through
    final_problematic = find_problematic_careers(exp_filtered)
    
    print(f"\n🎯 Final Results:")
    print(f"   Careers after all filtering: {len(exp_filtered)}")
    
    if final_problematic:
        print(f"   ❌ PROBLEM: {len(final_problematic)} problematic careers made it through:")
        for career in final_problematic:
            print(f"      - {career['title']}")
    else:
        print(f"   ✅ SUCCESS: No problematic careers in final results")
    
    # Step 8: Show some sample final recommendations
    print(f"\n📋 Sample Final Recommendations:")
    for i, career in enumerate(exp_filtered[:10]):
        min_sal = career.get('minSalary', 0)
        max_sal = career.get('maxSalary', 0)
        exp_level = career.get('experienceLevel', 'N/A')
        print(f"   {i+1}. {career['title']} (${min_sal:,}-${max_sal:,}, {exp_level})")
    
    return len(final_problematic) == 0

def test_salary_parsing_edge_cases():
    """Test various salary parsing scenarios"""
    print(f"\n🧪 Testing Salary Parsing Edge Cases:")
    print("-" * 40)
    
    test_cases = [
        "150000-250000",  # Machine format
        "150,000-250,000",  # With commas
        "$150,000 - $250,000",  # With dollar signs and spaces
        "150k-250k",  # With k notation
        "flexible",  # Flexible salary
        "",  # Empty string
        "invalid-format"  # Invalid format
    ]
    
    for salary_str in test_cases:
        try:
            min_sal, max_sal = parse_salary_expectations(salary_str)
            print(f"   '{salary_str}' -> ${min_sal:,} - ${max_sal:,}")
        except Exception as e:
            print(f"   '{salary_str}' -> ERROR: {e}")

if __name__ == "__main__":
    success = test_full_recommendation_pipeline()
    test_salary_parsing_edge_cases()
    
    print(f"\n" + "="*60)
    if success:
        print("🎉 PIPELINE TEST PASSED")
        print("✅ No problematic careers found in final recommendations")
        print("✅ Salary filtering is working correctly")
        print("\n🔍 If Bryan is still seeing these recommendations, the issue might be:")
        print("1. Different salary data being used in production")
        print("2. A different recommendation engine being called")
        print("3. Recommendations being added from a different source")
        print("4. Frontend displaying cached or different data")
    else:
        print("❌ PIPELINE TEST FAILED")
        print("🚨 Problematic careers are making it through the filters")
        print("🔧 The recommendation pipeline needs debugging")