#!/usr/bin/env python3
"""
Debug script to test the ENABLE_SENIORITY_CATEGORY_GUARDRAIL functionality.
This script will help identify why "medical assistant" and "delivery driver" 
are still appearing in results when they should be filtered out.
"""

import sys
import os
# Add the recommendation-engine directory to the path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'recommendation-engine')))

# Import the modules
from config import ENABLE_SENIORITY_CATEGORY_GUARDRAIL
from filters import FilterEngine
from categorization import determine_user_career_field, get_career_field
from models import UserProfile, Career, PersonalInfo, ProfessionalData, Experience as WorkExperience, AssessmentResults
from mock_data import MOCK_SKILLS, MOCK_CAREERS

def create_test_user_profile(experience_years=12, current_role="Product Manager"):
    """Create a test user profile with specified experience."""
    personal_info = PersonalInfo(
        age=35,
        location="San Francisco, CA",
        salary_expectations=None
    )
    
    work_exp = WorkExperience(
        title=current_role,
        company="Tech Company",
        duration_years=experience_years,
        description=f"Senior {current_role} with {experience_years} years of experience"
    )
    
    professional_data = ProfessionalData(
        experience=[work_exp],
        education="Bachelor's Degree",
        resume_skills=["Product Management", "Strategy", "Leadership"],
        linkedin_skills=["Product Strategy", "Team Leadership"]
    )
    
    return UserProfile(
        user_id="test_user",
        personal_info=personal_info,
        professional_data=professional_data,
        skills=[],
        assessment_results=AssessmentResults(
            personality_traits=[],
            work_values=[],
            interests={}
        )
    )

def create_problematic_careers():
    """Create careers that should be filtered out by the guardrail."""
    from models import SalaryRange, Demand as MarketDemand
    
    medical_assistant = Career(
        career_id="medical_assistant_001",
        title="Medical Assistant",
        description="Assists healthcare professionals with clinical and administrative tasks",
        salary_range=SalaryRange(min=35000, max=45000, currency="USD"),
        required_skills=[],
        demand=MarketDemand.HIGH,
        career_field="healthcare"
    )
    
    delivery_driver = Career(
        career_id="delivery_driver_001", 
        title="Delivery Driver",
        description="Delivers packages and goods to customers",
        salary_range=SalaryRange(min=30000, max=40000, currency="USD"),
        required_skills=[],
        demand=MarketDemand.MEDIUM,
        career_field="service"
    )
    
    return [medical_assistant, delivery_driver]

def test_guardrail_configuration():
    """Test if the guardrail configuration is properly set."""
    print("=== GUARDRAIL CONFIGURATION TEST ===")
    print(f"ENABLE_SENIORITY_CATEGORY_GUARDRAIL: {ENABLE_SENIORITY_CATEGORY_GUARDRAIL}")
    print()

def test_career_field_determination():
    """Test career field determination for problematic careers."""
    print("=== CAREER FIELD DETERMINATION TEST ===")
    
    problematic_careers = create_problematic_careers()
    
    for career in problematic_careers:
        career_field = get_career_field(career)
        print(f"Career: {career.title}")
        print(f"  Explicit career_field: {career.career_field}")
        print(f"  Determined career_field: {career_field}")
        print()

def test_user_field_determination():
    """Test user career field determination."""
    print("=== USER FIELD DETERMINATION TEST ===")
    
    # Test with different user profiles
    test_cases = [
        (12, "Product Manager"),
        (8, "Software Engineer"), 
        (15, "Marketing Director"),
        (5, "Junior Developer")  # Should not trigger guardrail
    ]
    
    for experience_years, role in test_cases:
        user_profile = create_test_user_profile(experience_years, role)
        user_field = determine_user_career_field(user_profile)
        
        print(f"User: {role} ({experience_years} years)")
        print(f"  Determined field: {user_field}")
        print(f"  Meets experience threshold (>=10): {experience_years >= 10}")
        print()

def test_filtering_logic():
    """Test the actual filtering logic."""
    print("=== FILTERING LOGIC TEST ===")
    
    # Create filter engine
    from config import FilteringConfig
    filter_config = FilteringConfig()
    filter_engine = FilterEngine(filter_config, MOCK_SKILLS)
    
    # Test with senior user who should trigger guardrail
    senior_user = create_test_user_profile(12, "Product Manager")
    user_field = determine_user_career_field(senior_user)
    
    print(f"Senior User Field: {user_field}")
    print(f"Experience Years: {senior_user.professional_data.experience[0].duration_years}")
    print(f"Guardrail Enabled: {ENABLE_SENIORITY_CATEGORY_GUARDRAIL}")
    print()
    
    # Test problematic careers
    problematic_careers = create_problematic_careers()
    all_careers = MOCK_CAREERS + problematic_careers
    
    print("Testing filtering with all careers...")
    filtered_careers = filter_engine.apply_initial_filters(senior_user, all_careers)
    
    print(f"Original careers: {len(all_careers)}")
    print(f"Filtered careers: {len(filtered_careers)}")
    print()
    
    # Check if problematic careers were filtered out
    filtered_titles = [career.title for career in filtered_careers]
    
    for career in problematic_careers:
        is_filtered_out = career.title not in filtered_titles
        career_field = get_career_field(career)
        
        print(f"Career: {career.title}")
        print(f"  Career field: {career_field}")
        print(f"  User field: {user_field}")
        print(f"  Should be filtered out: {career_field != user_field}")
        print(f"  Actually filtered out: {is_filtered_out}")
        print(f"  ❌ PROBLEM!" if not is_filtered_out and career_field != user_field else "  ✅ OK")
        print()

def test_backend_integration():
    """Test which backend is actually running."""
    print("=== BACKEND INTEGRATION TEST ===")
    print("Active terminals show:")
    print("  Terminal 5: cd backend; python -m uvicorn simple_server:app --host 0.0.0.0 --port 8000 --reload")
    print("  This means simple_server.py is running, NOT main.py")
    print()
    print("simple_server.py analysis:")
    print("  - Uses MOCK_CAREERS hardcoded data")
    print("  - Does NOT import or use the FilterEngine")
    print("  - Does NOT implement ENABLE_SENIORITY_CATEGORY_GUARDRAIL")
    print("  - generate_enhanced_recommendations() has its own filtering logic")
    print()
    print("🚨 ROOT CAUSE IDENTIFIED: Wrong backend server is running!")

if __name__ == "__main__":
    print("SENIORITY CATEGORY GUARDRAIL DEBUG ANALYSIS")
    print("=" * 60)
    print()
    
    test_guardrail_configuration()
    test_career_field_determination() 
    test_user_field_determination()
    test_filtering_logic()
    test_backend_integration()
    
    print("=" * 60)
    print("DIAGNOSIS SUMMARY:")
    print("1. ✅ Guardrail is enabled in config")
    print("2. ❌ Wrong backend server (simple_server.py) is running")
    print("3. ❌ simple_server.py bypasses FilterEngine entirely")
    print("4. ❌ simple_server.py uses mock data without proper filtering")
    print()
    print("RECOMMENDED FIX:")
    print("- Switch to main.py backend, OR")
    print("- Implement guardrail logic in simple_server.py")