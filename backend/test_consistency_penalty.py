#!/usr/bin/env python3
"""
Test script for career path consistency penalty system
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from simple_server import (
    get_career_field_categories, 
    get_field_adjacency_map,
    identify_career_field,
    identify_user_field,
    calculate_consistency_penalty
)

def test_career_field_identification():
    """Test career field identification"""
    print("🧪 Testing Career Field Identification")
    print("=" * 50)
    
    # Test healthcare career
    healthcare_career = {
        "title": "Family Medicine Physician",
        "description": "Provide comprehensive primary care for patients of all ages, manage chronic conditions, preventive care."
    }
    field = identify_career_field(healthcare_career)
    print(f"Family Medicine Physician -> {field}")
    assert field == "healthcare", f"Expected 'healthcare', got '{field}'"
    
    # Test product management career
    pm_career = {
        "title": "Senior Product Manager",
        "description": "Own product strategy and roadmap, lead cross-functional teams, drive product success through data-driven decisions."
    }
    field = identify_career_field(pm_career)
    print(f"Senior Product Manager -> {field}")
    assert field == "product_management", f"Expected 'product_management', got '{field}'"
    
    # Test technology career
    tech_career = {
        "title": "Data Scientist",
        "description": "Build machine learning models, analyze complex datasets, provide data-driven insights for business decisions."
    }
    field = identify_career_field(tech_career)
    print(f"Data Scientist -> {field}")
    assert field == "technology", f"Expected 'technology', got '{field}'"
    
    print("✅ Career field identification tests passed!\n")

def test_user_field_identification():
    """Test user field identification"""
    print("🧪 Testing User Field Identification")
    print("=" * 50)
    
    # Test product management user
    pm_resume_insights = {
        "keyword_frequencies": {"product": 18, "engineering": 2, "data_science": 1, "management": 8},
        "dominant_theme": "product",
        "current_role": "Product Management"
    }
    pm_user_data = {
        "technical_skills": ["Product Management", "User Research", "Data Analysis", "Agile"]
    }
    field = identify_user_field(pm_resume_insights, pm_user_data)
    print(f"Product Management User -> {field}")
    assert field == "product_management", f"Expected 'product_management', got '{field}'"
    
    # Test technology user
    tech_resume_insights = {
        "keyword_frequencies": {"product": 1, "engineering": 12, "data_science": 8, "management": 3},
        "dominant_theme": "engineering",
        "current_role": "Software Engineering"
    }
    tech_user_data = {
        "technical_skills": ["Python", "JavaScript", "AWS", "Machine Learning"]
    }
    field = identify_user_field(tech_resume_insights, tech_user_data)
    print(f"Software Engineering User -> {field}")
    assert field == "technology", f"Expected 'technology', got '{field}'"
    
    print("✅ User field identification tests passed!\n")

def test_consistency_penalties():
    """Test consistency penalty calculations"""
    print("🧪 Testing Consistency Penalty Calculations")
    print("=" * 50)
    
    field_adjacency_map = get_field_adjacency_map()
    
    # Test 1: Product Management user looking at Healthcare career (should be heavily penalized)
    penalty = calculate_consistency_penalty(
        career_field="healthcare",
        user_field="product_management", 
        field_adjacency_map=field_adjacency_map,
        dominant_theme="product",
        keyword_frequencies={"product": 18, "engineering": 2}
    )
    print(f"Healthcare career for Product Management user with strong product theme: {penalty}")
    assert penalty <= -45, f"Expected penalty <= -45, got {penalty}"
    
    # Test 2: Product Management user looking at Technology career (should be no penalty)
    penalty = calculate_consistency_penalty(
        career_field="technology",
        user_field="product_management",
        field_adjacency_map=field_adjacency_map,
        dominant_theme="product",
        keyword_frequencies={"product": 18, "engineering": 2}
    )
    print(f"Technology career for Product Management user: {penalty}")
    assert penalty == 0, f"Expected penalty = 0, got {penalty}"
    
    # Test 3: Product Management user looking at Business Finance career (should be small penalty)
    penalty = calculate_consistency_penalty(
        career_field="business_finance",
        user_field="product_management",
        field_adjacency_map=field_adjacency_map,
        dominant_theme="product",
        keyword_frequencies={"product": 18, "engineering": 2}
    )
    print(f"Business Finance career for Product Management user: {penalty}")
    assert penalty == 0, f"Expected penalty = 0 (closely related), got {penalty}"
    
    # Test 4: Technology user looking at Healthcare career (should be heavily penalized)
    penalty = calculate_consistency_penalty(
        career_field="healthcare",
        user_field="technology",
        field_adjacency_map=field_adjacency_map,
        dominant_theme="engineering",
        keyword_frequencies={"engineering": 15, "product": 2}
    )
    print(f"Healthcare career for Technology user with strong engineering theme: {penalty}")
    assert penalty <= -45, f"Expected penalty <= -45, got {penalty}"
    
    print("✅ Consistency penalty tests passed!\n")

def test_full_scenario():
    """Test full scenario: Product Management user vs various careers"""
    print("🧪 Testing Full Scenario: Product Management User")
    print("=" * 50)
    
    # Product management user profile
    pm_resume_insights = {
        "keyword_frequencies": {"product": 18, "engineering": 2, "data_science": 1, "management": 8},
        "dominant_theme": "product",
        "current_role": "Product Management"
    }
    pm_user_data = {
        "technical_skills": ["Product Management", "User Research", "Data Analysis", "Agile"]
    }
    
    user_field = identify_user_field(pm_resume_insights, pm_user_data)
    field_adjacency_map = get_field_adjacency_map()
    
    # Test various careers
    test_careers = [
        {
            "title": "Family Medicine Physician",
            "description": "Provide comprehensive primary care for patients of all ages, manage chronic conditions, preventive care.",
            "expected_penalty_range": (-60, -30)
        },
        {
            "title": "Senior Product Manager", 
            "description": "Own product strategy and roadmap, lead cross-functional teams, drive product success through data-driven decisions.",
            "expected_penalty_range": (0, 0)
        },
        {
            "title": "Data Scientist",
            "description": "Build machine learning models, analyze complex datasets, provide data-driven insights for business decisions.",
            "expected_penalty_range": (0, 0)
        },
        {
            "title": "Electrician",
            "description": "Install and maintain electrical systems in residential and commercial buildings.",
            "expected_penalty_range": (-60, -30)
        }
    ]
    
    for career in test_careers:
        career_field = identify_career_field(career)
        penalty = calculate_consistency_penalty(
            career_field=career_field,
            user_field=user_field,
            field_adjacency_map=field_adjacency_map,
            dominant_theme=pm_resume_insights["dominant_theme"],
            keyword_frequencies=pm_resume_insights["keyword_frequencies"]
        )
        
        min_expected, max_expected = career["expected_penalty_range"]
        print(f"{career['title']} ({career_field}): penalty = {penalty} (expected: {min_expected} to {max_expected})")
        
        assert min_expected <= penalty <= max_expected, f"Penalty {penalty} not in expected range {min_expected} to {max_expected}"
    
    print("✅ Full scenario tests passed!\n")

if __name__ == "__main__":
    print("🚀 Starting Career Path Consistency Penalty Tests")
    print("=" * 60)
    
    try:
        test_career_field_identification()
        test_user_field_identification()
        test_consistency_penalties()
        test_full_scenario()
        
        print("🎉 ALL TESTS PASSED!")
        print("Career path consistency penalty system is working correctly.")
        print("Healthcare careers will now be heavily penalized for non-healthcare users.")
        
    except AssertionError as e:
        print(f"❌ TEST FAILED: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"💥 UNEXPECTED ERROR: {e}")
        sys.exit(1)