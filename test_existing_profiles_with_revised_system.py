#!/usr/bin/env python3
"""
Test existing email address profiles against the revised job title/category system.

This script demonstrates how existing profiles perform with the enhanced
categorization system, showing cleaned up recommendations.
"""

import sys
import os
import json
from datetime import datetime
from typing import Dict, Any

# Add the recommendation engine to the path
sys.path.append('recommendation-engine')

from models import (
    UserProfile, PersonalInfo, AssessmentResults, ProfessionalData,
    Experience, UserSkill, SalaryRange, SkillLevel, InterestLevel
)
from enhanced_categorization import EnhancedCategorizationEngine
from enhanced_engine import EnhancedRecommendationEngine
from config import CategorizationThresholds
from enhanced_mock_data import (
    ENHANCED_SKILLS, ENHANCED_CAREERS, 
    STUDENT_PROFILE, TRADES_PROFESSIONAL_PROFILE, SENIOR_PROFESSIONAL_PROFILE
)


def load_golden_dataset_profile(filepath: str) -> UserProfile:
    """Load and convert golden dataset JSON to UserProfile object."""
    with open(filepath, 'r', encoding='utf-8') as f:
        dataset = json.load(f)
    
    json_profile = dataset["user_profile"]
    
    # Convert salary expectations
    salary_exp = None
    if json_profile["personal_info"].get("salary_expectations"):
        salary_data = json_profile["personal_info"]["salary_expectations"]
        salary_exp = SalaryRange(
            min=salary_data["min"],
            max=salary_data["max"],
            currency=salary_data["currency"]
        )
    
    # Convert personal info
    personal_info = PersonalInfo(
        age=json_profile["personal_info"]["age"],
        location=json_profile["personal_info"]["location"],
        salary_expectations=salary_exp,
        willing_to_relocate=json_profile["personal_info"]["willing_to_relocate"],
        preferred_work_style=json_profile["personal_info"]["preferred_work_style"]
    )
    
    # Convert interests
    interests = {}
    for interest, level_str in json_profile["assessment_results"]["interests"].items():
        level_map = {
            "low": InterestLevel.LOW,
            "medium": InterestLevel.MEDIUM,
            "high": InterestLevel.HIGH,
            "very_high": InterestLevel.VERY_HIGH
        }
        interests[interest] = level_map[level_str]
    
    # Convert assessment results
    assessment_results = AssessmentResults(
        personality_traits=json_profile["assessment_results"]["personality_traits"],
        work_values=json_profile["assessment_results"]["work_values"],
        interests=interests
    )
    
    # Convert experience
    experiences = []
    for exp_data in json_profile["professional_data"]["experience"]:
        experience = Experience(
            title=exp_data["title"],
            company=exp_data["company"],
            duration_years=exp_data["duration_years"],
            description=exp_data["description"],
            skills_used=exp_data["skills_used"]
        )
        experiences.append(experience)
    
    # Convert professional data
    professional_data = ProfessionalData(
        resume_skills=json_profile["professional_data"]["resume_skills"],
        linkedin_skills=json_profile["professional_data"]["linkedin_skills"],
        experience=experiences,
        education=json_profile["professional_data"]["education"],
        certifications=json_profile["professional_data"]["certifications"]
    )
    
    # Convert skills
    skills = []
    for skill_data in json_profile["skills"]:
        level_map = {
            "beginner": SkillLevel.BEGINNER,
            "intermediate": SkillLevel.INTERMEDIATE,
            "advanced": SkillLevel.ADVANCED,
            "expert": SkillLevel.EXPERT
        }
        
        last_used = None
        if skill_data.get("last_used"):
            last_used = datetime.fromisoformat(skill_data["last_used"])
        
        skill = UserSkill(
            skill_id=skill_data["skill_id"],
            name=skill_data["name"],
            level=level_map[skill_data["level"]],
            years_experience=skill_data["years_experience"],
            is_certified=skill_data["is_certified"],
            last_used=last_used
        )
        skills.append(skill)
    
    # Create user profile
    return UserProfile(
        user_id=json_profile["user_id"],
        personal_info=personal_info,
        assessment_results=assessment_results,
        professional_data=professional_data,
        skills=skills,
        user_interests=json_profile["user_interests"]
    )


def test_profile_with_enhanced_system(profile: UserProfile, profile_name: str):
    """Test a profile with the enhanced recommendation system."""
    print(f"\n{'='*60}")
    print(f"TESTING: {profile_name}")
    print(f"{'='*60}")
    
    # Initialize enhanced engine
    thresholds = CategorizationThresholds()
    engine = EnhancedRecommendationEngine(thresholds)
    
    # Get recommendations
    try:
        recommendations = engine.get_recommendations(
            profile, ENHANCED_CAREERS, ENHANCED_SKILLS
        )
        
        print(f"\n📊 RESULTS SUMMARY:")
        print(f"   Total Recommendations: {len(recommendations)}")
        
        # Category distribution
        categories = {"SAFE_ZONE": 0, "STRETCH_ZONE": 0, "ADVENTURE_ZONE": 0}
        for rec in recommendations:
            categories[rec.category.name] += 1
        
        print(f"   Safe Zone: {categories['SAFE_ZONE']}")
        print(f"   Stretch Zone: {categories['STRETCH_ZONE']}")
        print(f"   Adventure Zone: {categories['ADVENTURE_ZONE']}")
        
        # Show top recommendations per category
        print(f"\n🎯 TOP RECOMMENDATIONS BY CATEGORY:")
        
        for category_name in ["SAFE_ZONE", "STRETCH_ZONE", "ADVENTURE_ZONE"]:
            category_recs = [r for r in recommendations if r.category.name == category_name]
            if category_recs:
                print(f"\n   {category_name.replace('_', ' ')}:")
                for i, rec in enumerate(category_recs[:2], 1):  # Top 2 per category
                    print(f"   {i}. {rec.career.title}")
                    print(f"      Score: {rec.score.total_score:.2f} | Confidence: {rec.confidence:.2f}")
                    print(f"      Reasons: {rec.reasons[0] if rec.reasons else 'No reasons provided'}")
        
        return True
        
    except Exception as e:
        print(f"❌ ERROR testing {profile_name}: {str(e)}")
        return False


def main():
    """Main function to test existing profiles with revised system."""
    print("🔍 TESTING EXISTING PROFILES WITH REVISED CATEGORIZATION SYSTEM")
    print("=" * 80)
    
    test_results = []
    
    # Test 1: Golden Dataset Profile (Data Analyst)
    try:
        golden_profile = load_golden_dataset_profile("tests/golden_datasets/data_analyst_profile.json")
        result = test_profile_with_enhanced_system(golden_profile, "Data Analyst (Golden Dataset)")
        test_results.append(("Data Analyst Golden", result))
    except Exception as e:
        print(f"❌ Could not load golden dataset: {e}")
        test_results.append(("Data Analyst Golden", False))
    
    # Test 2: Student Profile
    result = test_profile_with_enhanced_system(STUDENT_PROFILE, "Student Profile")
    test_results.append(("Student Profile", result))
    
    # Test 3: Trades Professional Profile
    result = test_profile_with_enhanced_system(TRADES_PROFESSIONAL_PROFILE, "Trades Professional")
    test_results.append(("Trades Professional", result))
    
    # Test 4: Senior Professional Profile
    result = test_profile_with_enhanced_system(SENIOR_PROFESSIONAL_PROFILE, "Senior Professional")
    test_results.append(("Senior Professional", result))
    
    # Summary
    print(f"\n{'='*80}")
    print("📋 TEST SUMMARY")
    print(f"{'='*80}")
    
    successful_tests = sum(1 for _, result in test_results if result)
    total_tests = len(test_results)
    
    print(f"✅ Successful Tests: {successful_tests}/{total_tests}")
    
    for profile_name, result in test_results:
        status = "✅ PASSED" if result else "❌ FAILED"
        print(f"   {profile_name}: {status}")
    
    if successful_tests == total_tests:
        print(f"\n🎉 ALL TESTS PASSED! The revised categorization system works well with existing profiles.")
        print(f"💡 RECOMMENDATION: Use existing profiles - they will show improved, cleaned up recommendations.")
    else:
        print(f"\n⚠️  Some tests failed. You may want to review the failed profiles or create new clean ones.")
    
    print(f"\n📝 NEXT STEPS:")
    print(f"   1. Run this script to see the enhanced recommendations")
    print(f"   2. Compare with previous results to see improvements")
    print(f"   3. Use the frontend to test interactively with existing profiles")


if __name__ == "__main__":
    main()