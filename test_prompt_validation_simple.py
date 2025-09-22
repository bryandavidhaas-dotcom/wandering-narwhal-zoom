"""
Simple test script to verify the prompt validation functionality works correctly.
This bypasses the complex import issues in the test framework.
"""

import sys
import os
import json
from datetime import datetime, timedelta

# Add the recommendation-engine directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'recommendation-engine'))

# Now import the modules directly
from models import (
    UserProfile, Career, Skill, UserSkill, RequiredSkill, SalaryRange,
    PersonalInfo, AssessmentResults, ProfessionalData, Experience,
    SkillLevel, InterestLevel, Demand
)
from config import RecommendationConfig
from engine import RecommendationEngine


def create_test_user_profile():
    """Create a test user profile."""
    return UserProfile(
        user_id="test_user",
        personal_info=PersonalInfo(
            age=28,
            location="San Francisco, CA",
            salary_expectations=SalaryRange(min=80000, max=120000, currency="USD"),
            willing_to_relocate=False,
            preferred_work_style="hybrid"
        ),
        assessment_results=AssessmentResults(
            personality_traits=["Analytical", "Detail-Oriented"],
            work_values=["Autonomy", "Innovation"],
            interests={
                "Technology": InterestLevel.VERY_HIGH,
                "Data Analysis": InterestLevel.HIGH
            }
        ),
        professional_data=ProfessionalData(
            resume_skills=["Python", "Data Analysis"],
            linkedin_skills=["Python", "Machine Learning"],
            experience=[
                Experience(
                    title="Data Analyst",
                    company="Tech Corp",
                    duration_years=2.0,
                    description="Analyzed data using Python",
                    skills_used=["Python", "Data Analysis"]
                )
            ],
            education="Bachelor's in Computer Science",
            certifications=[]
        ),
        skills=[
            UserSkill(
                skill_id="skill_1",
                name="Python",
                level=SkillLevel.ADVANCED,
                years_experience=3.0,
                is_certified=False,
                last_used=datetime.utcnow() - timedelta(days=1)
            )
        ],
        user_interests=["AI Ethics", "Data Privacy"]
    )


def create_test_career(career_id: str, title: str, description_length: int = 100):
    """Create a test career with specified description length."""
    description = "A" * description_length  # Create description of specified length
    
    return Career(
        career_id=career_id,
        title=title,
        description=description,
        required_skills=[
            RequiredSkill(
                skill_id="skill_1",
                name="Python",
                proficiency=SkillLevel.INTERMEDIATE,
                is_mandatory=True,
                weight=1.0
            )
        ],
        salary_range=SalaryRange(min=80000, max=120000, currency="USD"),
        demand=Demand.MEDIUM,
        related_careers=[],
        growth_potential="Good",
        work_environment="Tech",
        education_requirements="Bachelor's degree",
        career_field="technology"
    )


def test_prefilter_limit_configuration():
    """Test that the prefilter limit has been reduced."""
    print("Testing prefilter limit configuration...")
    
    config = RecommendationConfig()
    print(f"Current prefilter_limit: {config.prefilter_limit}")
    
    # Should be 100 (reduced from original 200)
    assert config.prefilter_limit == 100, f"Expected prefilter_limit to be 100, got {config.prefilter_limit}"
    print("✅ Prefilter limit correctly set to 100")


def test_prompt_size_validation_within_limit():
    """Test prompt size validation when careers fit within limit."""
    print("\nTesting prompt size validation within limit...")
    
    engine = RecommendationEngine()
    user_profile = create_test_user_profile()
    
    # Create a small number of careers that should fit within the limit
    careers = [
        create_test_career(f"career_{i}", f"Test Career {i}", 100)
        for i in range(5)
    ]
    
    validated_careers, was_truncated = engine._validate_prompt_size(
        user_profile, careers, max_size=50000
    )
    
    assert not was_truncated, "Careers should not be truncated with small list"
    assert len(validated_careers) == len(careers), "All careers should be retained"
    print("✅ Small career list passes validation without truncation")


def test_prompt_size_validation_exceeds_limit():
    """Test prompt size validation when careers exceed limit."""
    print("\nTesting prompt size validation exceeding limit...")
    
    engine = RecommendationEngine()
    user_profile = create_test_user_profile()
    
    # Create many careers with long descriptions to exceed the limit
    careers = [
        create_test_career(f"career_{i}", f"Test Career {i}", 1000)
        for i in range(100)
    ]
    
    validated_careers, was_truncated = engine._validate_prompt_size(
        user_profile, careers, max_size=10000  # Small limit to force truncation
    )
    
    assert was_truncated, "Large career list should be truncated"
    assert len(validated_careers) < len(careers), "Career list should be reduced"
    assert len(validated_careers) > 0, "Should still have some careers"
    print(f"✅ Large career list truncated from {len(careers)} to {len(validated_careers)}")


def test_prefilter_effectiveness():
    """Test that pre-filtering effectively reduces the number of careers."""
    print("\nTesting pre-filtering effectiveness...")
    
    engine = RecommendationEngine()
    user_profile = create_test_user_profile()
    
    # Create highly relevant careers (should be kept)
    relevant_careers = []
    for i in range(20):
        career = Career(
            career_id=f"relevant_{i}",
            title=f"Python Developer {i}",
            description="Develops software using Python and machine learning",
            required_skills=[
                RequiredSkill(
                    skill_id="skill_1",
                    name="Python",
                    proficiency=SkillLevel.INTERMEDIATE,
                    is_mandatory=True,
                    weight=1.0
                )
            ],
            salary_range=SalaryRange(min=80000, max=120000, currency="USD"),
            demand=Demand.HIGH,
            related_careers=[],
            growth_potential="Excellent",
            work_environment="Tech companies",
            education_requirements="Bachelor's degree",
            career_field="technology"
        )
        relevant_careers.append(career)
    
    # Create less relevant careers (should be filtered out)
    irrelevant_careers = []
    for i in range(80):
        career = Career(
            career_id=f"irrelevant_{i}",
            title=f"Unrelated Job {i}",
            description="Job that has nothing to do with user's skills or interests",
            required_skills=[
                RequiredSkill(
                    skill_id="skill_unrelated",
                    name="Unrelated Skill",
                    proficiency=SkillLevel.EXPERT,
                    is_mandatory=True,
                    weight=1.0
                )
            ],
            salary_range=SalaryRange(min=30000, max=50000, currency="USD"),
            demand=Demand.LOW,
            related_careers=[],
            growth_potential="Limited",
            work_environment="Various",
            education_requirements="High school",
            career_field="other"
        )
        irrelevant_careers.append(career)
    
    all_careers = relevant_careers + irrelevant_careers
    
    # Create summarized profile
    summarized_profile = engine._preprocess_user_profile(user_profile)
    
    # Apply pre-filtering
    filtered_careers = engine._prefilter_careers(summarized_profile, all_careers)
    
    print(f"Original careers: {len(all_careers)}")
    print(f"Filtered careers: {len(filtered_careers)}")
    print(f"Reduction: {len(all_careers) - len(filtered_careers)} careers")
    
    # Should significantly reduce the number of careers
    assert len(filtered_careers) <= engine.config.prefilter_limit, "Should respect prefilter limit"
    assert len(filtered_careers) < len(all_careers), "Should reduce career count"
    
    # Should prioritize relevant careers
    filtered_ids = [career.career_id for career in filtered_careers]
    relevant_in_filtered = sum(1 for career_id in filtered_ids if career_id.startswith("relevant_"))
    irrelevant_in_filtered = sum(1 for career_id in filtered_ids if career_id.startswith("irrelevant_"))
    
    print(f"Relevant careers in filtered: {relevant_in_filtered}")
    print(f"Irrelevant careers in filtered: {irrelevant_in_filtered}")
    
    # Should have more relevant than irrelevant careers
    assert relevant_in_filtered > irrelevant_in_filtered, "Should prioritize relevant careers"
    print("✅ Pre-filtering effectively prioritizes relevant careers")


def test_integration_with_get_recommendations():
    """Test that the prompt validation integrates properly with the main recommendation flow."""
    print("\nTesting integration with get_recommendations...")
    
    engine = RecommendationEngine()
    user_profile = create_test_user_profile()
    
    # Create a moderate number of careers
    careers = [
        create_test_career(f"career_{i}", f"Test Career {i}", 200)
        for i in range(30)
    ]
    
    try:
        # Get recommendations (this should use the new validation internally)
        recommendations = engine.get_recommendations(
            user_profile, careers, limit=5, exploration_level=3
        )
        
        assert isinstance(recommendations, list), "Should return a list"
        assert len(recommendations) <= 5, "Should respect limit"
        print(f"✅ Successfully generated {len(recommendations)} recommendations")
        
    except Exception as e:
        print(f"❌ Error in get_recommendations: {e}")
        raise


def main():
    """Run all tests."""
    print("Running Prompt Validation Tests")
    print("=" * 50)
    
    try:
        test_prefilter_limit_configuration()
        test_prompt_size_validation_within_limit()
        test_prompt_size_validation_exceeds_limit()
        test_prefilter_effectiveness()
        test_integration_with_get_recommendations()
        
        print("\n" + "=" * 50)
        print("✅ ALL TESTS PASSED!")
        print("The prompt validation implementation is working correctly.")
        print("Key improvements:")
        print("- Prefilter limit reduced from 200 to 100 careers")
        print("- Prompt size validation prevents overflow errors")
        print("- Automatic truncation with warning logging")
        print("- Pre-filtering prioritizes relevant careers")
        
    except Exception as e:
        print(f"\n❌ TEST FAILED: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    return True


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)