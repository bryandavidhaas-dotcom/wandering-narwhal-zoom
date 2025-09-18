"""
Examples demonstrating how to use the recommendation engine.

This module provides practical examples of using the recommendation engine
with different configurations and scenarios.
"""

from datetime import datetime, timedelta
from typing import List

# Import the recommendation engine components
from . import RecommendationEngine
from .models import (
    UserProfile, Career, Skill, UserSkill, RequiredSkill, SalaryRange,
    PersonalInfo, AssessmentResults, ProfessionalData, Experience,
    SkillLevel, InterestLevel, Demand
)
from .config import (
    RecommendationConfig, ScoringWeights, CategorizationThresholds,
    FilteringConfig, ScoringConfig
)
from .mock_data import MOCK_SKILLS, MOCK_CAREERS, MOCK_USER_PROFILE, ALTERNATIVE_USER_PROFILE


def basic_example():
    """
    Basic example of using the recommendation engine.
    """
    print("=== Basic Recommendation Engine Example ===\n")
    
    # Initialize the engine with mock data
    engine = RecommendationEngine(skills_db=MOCK_SKILLS)
    
    # Get recommendations for the mock user
    recommendations = engine.get_recommendations(
        user_profile=MOCK_USER_PROFILE,
        available_careers=MOCK_CAREERS,
        limit=5
    )
    
    print(f"Generated {len(recommendations)} recommendations for user {MOCK_USER_PROFILE.user_id}:\n")
    
    for i, rec in enumerate(recommendations, 1):
        print(f"{i}. {rec.career.title}")
        print(f"   Category: {rec.category.value.replace('_', ' ').title()}")
        print(f"   Score: {rec.score.total_score:.3f}")
        print(f"   Confidence: {rec.confidence:.3f}")
        print(f"   Salary: ${rec.career.salary_range.min:,} - ${rec.career.salary_range.max:,}")
        print(f"   Top Reasons:")
        for reason in rec.reasons[:3]:
            print(f"     • {reason}")
        print()


def categorized_recommendations_example():
    """
    Example of getting recommendations organized by category.
    """
    print("=== Categorized Recommendations Example ===\n")
    
    engine = RecommendationEngine(skills_db=MOCK_SKILLS)
    
    # Get recommendations organized by category
    categorized = engine.get_recommendations_by_category(
        user_profile=MOCK_USER_PROFILE,
        available_careers=MOCK_CAREERS,
        limit_per_category=3
    )
    
    categories = {
        "safe_zone": "Safe Zone (Low Risk)",
        "stretch_zone": "Stretch Zone (Moderate Risk)",
        "adventure_zone": "Adventure Zone (High Risk)"
    }
    
    for category_key, category_name in categories.items():
        recommendations = categorized[category_key]
        print(f"{category_name}: {len(recommendations)} recommendations")
        
        for rec in recommendations:
            print(f"  • {rec.career.title} (Score: {rec.score.total_score:.3f})")
        print()


def custom_configuration_example():
    """
    Example of using custom configuration for different user types.
    """
    print("=== Custom Configuration Example ===\n")
    
    # Configuration for junior professionals (emphasize interests and growth)
    junior_config = RecommendationConfig(
        scoring_weights=ScoringWeights(
            skill_match=0.3,
            interest_match=0.4,  # Higher weight on interests
            salary_compatibility=0.1,
            experience_match=0.2
        ),
        categorization_thresholds=CategorizationThresholds(
            safe_zone_min=0.6,   # Lower threshold for safe zone
            stretch_zone_min=0.4,
            adventure_zone_min=0.2
        )
    )
    
    # Configuration for senior professionals (emphasize skills and salary)
    senior_config = RecommendationConfig(
        scoring_weights=ScoringWeights(
            skill_match=0.5,     # Higher weight on skills
            interest_match=0.2,
            salary_compatibility=0.2,  # Higher weight on salary
            experience_match=0.1
        ),
        categorization_thresholds=CategorizationThresholds(
            safe_zone_min=0.8,   # Higher threshold for safe zone
            stretch_zone_min=0.6,
            adventure_zone_min=0.4
        )
    )
    
    # Test both configurations
    junior_engine = RecommendationEngine(config=junior_config, skills_db=MOCK_SKILLS)
    senior_engine = RecommendationEngine(config=senior_config, skills_db=MOCK_SKILLS)
    
    junior_recs = junior_engine.get_recommendations(MOCK_USER_PROFILE, MOCK_CAREERS, limit=3)
    senior_recs = senior_engine.get_recommendations(MOCK_USER_PROFILE, MOCK_CAREERS, limit=3)
    
    print("Junior-focused recommendations:")
    for rec in junior_recs:
        print(f"  • {rec.career.title} - {rec.category.value} (Score: {rec.score.total_score:.3f})")
    
    print("\nSenior-focused recommendations:")
    for rec in senior_recs:
        print(f"  • {rec.career.title} - {rec.category.value} (Score: {rec.score.total_score:.3f})")
    print()


def detailed_explanation_example():
    """
    Example of getting detailed explanations for recommendations.
    """
    print("=== Detailed Explanation Example ===\n")
    
    engine = RecommendationEngine(skills_db=MOCK_SKILLS)
    
    # Get a recommendation and explain it
    recommendations = engine.get_recommendations(MOCK_USER_PROFILE, MOCK_CAREERS, limit=1)
    
    if recommendations:
        career = recommendations[0].career
        explanation = engine.explain_recommendation(MOCK_USER_PROFILE, career)
        
        print(f"Detailed explanation for: {explanation['career_title']}")
        print(f"Overall Score: {explanation['total_score']:.3f}")
        print(f"Category: {explanation['category'].replace('_', ' ').title()}")
        print(f"Confidence: {explanation['confidence']:.3f}")
        
        print("\nScore Breakdown:")
        breakdown = explanation['score_breakdown']
        print(f"  • Skill Match: {breakdown['skill_match']:.3f}")
        print(f"  • Interest Match: {breakdown['interest_match']:.3f}")
        print(f"  • Salary Compatibility: {breakdown['salary_compatibility']:.3f}")
        print(f"  • Experience Match: {breakdown['experience_match']:.3f}")
        
        print("\nReasons for Recommendation:")
        for i, reason in enumerate(explanation['reasons'], 1):
            print(f"  {i}. {reason}")
        
        print("\nDetailed Skill Analysis:")
        skill_details = explanation['detailed_breakdown']['skill_details']
        
        if skill_details['matched_skills']:
            print("  Matched Skills:")
            for skill in skill_details['matched_skills']:
                print(f"    • {skill['name']}: {skill['user_level']} (required: {skill['required_level']})")
        
        if skill_details['missing_mandatory']:
            print("  Missing Mandatory Skills:")
            for skill in skill_details['missing_mandatory']:
                print(f"    • {skill}")
        print()


def comparison_example():
    """
    Example comparing recommendations for different user profiles.
    """
    print("=== User Profile Comparison Example ===\n")
    
    engine = RecommendationEngine(skills_db=MOCK_SKILLS)
    
    # Get recommendations for both user profiles
    user1_recs = engine.get_recommendations(MOCK_USER_PROFILE, MOCK_CAREERS, limit=5)
    user2_recs = engine.get_recommendations(ALTERNATIVE_USER_PROFILE, MOCK_CAREERS, limit=5)
    
    print("User 1 (Data-focused professional):")
    print(f"Skills: {[skill.name for skill in MOCK_USER_PROFILE.skills[:4]]}")
    print("Top recommendations:")
    for rec in user1_recs[:3]:
        print(f"  • {rec.career.title} (Score: {rec.score.total_score:.3f})")
    
    print("\nUser 2 (Leadership-focused professional):")
    print(f"Skills: {[skill.name for skill in ALTERNATIVE_USER_PROFILE.skills[:4]]}")
    print("Top recommendations:")
    for rec in user2_recs[:3]:
        print(f"  • {rec.career.title} (Score: {rec.score.total_score:.3f})")
    print()


def statistics_example():
    """
    Example of getting recommendation statistics.
    """
    print("=== Recommendation Statistics Example ===\n")
    
    engine = RecommendationEngine(skills_db=MOCK_SKILLS)
    
    # Get comprehensive statistics
    stats = engine.get_recommendation_statistics(MOCK_USER_PROFILE, MOCK_CAREERS)
    
    print("Filtering Statistics:")
    filter_stats = stats['filtering_stats']
    print(f"  • Original careers: {filter_stats['original_count']}")
    print(f"  • After initial filters: {filter_stats['after_initial_filters']}")
    print(f"  • After skill filters: {filter_stats['after_skill_filters']}")
    print(f"  • After interest filters: {filter_stats['after_interest_filters']}")
    
    print("\nCategory Distribution:")
    cat_dist = stats['category_distribution']
    print(f"  • Safe Zone: {cat_dist['safe_zone']} recommendations")
    print(f"  • Stretch Zone: {cat_dist['stretch_zone']} recommendations")
    print(f"  • Adventure Zone: {cat_dist['adventure_zone']} recommendations")
    
    print("\nScore Statistics:")
    score_stats = stats['score_statistics']
    print(f"  • Average Score: {score_stats['average_score']:.3f}")
    print(f"  • Highest Score: {score_stats['highest_score']:.3f}")
    print(f"  • Lowest Score: {score_stats['lowest_score']:.3f}")
    print(f"  • Score Range: {score_stats['score_range']:.3f}")
    
    print(f"\nTotal Recommendations Generated: {stats['total_recommendations']}")
    print()


def create_custom_user_example():
    """
    Example of creating a custom user profile and getting recommendations.
    """
    print("=== Custom User Profile Example ===\n")
    
    # Create a custom user profile
    custom_user = UserProfile(
        user_id="custom_user_001",
        personal_info=PersonalInfo(
            age=26,
            location="Seattle, WA",
            salary_expectations=SalaryRange(min=70000, max=100000, currency="USD"),
            willing_to_relocate=True,
            preferred_work_style="remote"
        ),
        assessment_results=AssessmentResults(
            personality_traits=["Creative", "Collaborative", "Adaptable"],
            work_values=["Innovation", "Learning", "Impact"],
            interests={
                "Technology": InterestLevel.HIGH,
                "Design": InterestLevel.VERY_HIGH,
                "Problem Solving": InterestLevel.HIGH,
                "Leadership": InterestLevel.MEDIUM
            }
        ),
        professional_data=ProfessionalData(
            resume_skills=["JavaScript", "React", "UI/UX Design", "Python"],
            experience=[
                Experience(
                    title="Frontend Developer",
                    company="Design Studio",
                    duration_years=2.0,
                    description="Developed user interfaces for web applications",
                    skills_used=["JavaScript", "React", "CSS", "HTML"]
                )
            ],
            education="Bachelor's in Design",
            certifications=["Google UX Design Certificate"]
        ),
        skills=[
            UserSkill(
                skill_id="skill_8",
                name="JavaScript",
                level=SkillLevel.ADVANCED,
                years_experience=2.5,
                is_certified=False,
                last_used=datetime.utcnow() - timedelta(days=1)
            ),
            UserSkill(
                skill_id="skill_9",
                name="React",
                level=SkillLevel.INTERMEDIATE,
                years_experience=2.0,
                is_certified=False,
                last_used=datetime.utcnow() - timedelta(days=1)
            )
        ],
        user_interests=["User Experience", "Creative Technology", "Startup Culture"]
    )
    
    # Get recommendations for the custom user
    engine = RecommendationEngine(skills_db=MOCK_SKILLS)
    recommendations = engine.get_recommendations(custom_user, MOCK_CAREERS, limit=4)
    
    print(f"Recommendations for {custom_user.user_id}:")
    print(f"Background: {custom_user.professional_data.education}, {custom_user.professional_data.experience[0].title}")
    print(f"Key Skills: {[skill.name for skill in custom_user.skills]}")
    print(f"Salary Range: ${custom_user.personal_info.salary_expectations.min:,} - ${custom_user.personal_info.salary_expectations.max:,}")
    print()
    
    for i, rec in enumerate(recommendations, 1):
        print(f"{i}. {rec.career.title}")
        print(f"   Category: {rec.category.value.replace('_', ' ').title()}")
        print(f"   Score: {rec.score.total_score:.3f}")
        print(f"   Key Reason: {rec.reasons[0] if rec.reasons else 'N/A'}")
        print()


def run_all_examples():
    """
    Run all examples in sequence.
    """
    examples = [
        basic_example,
        categorized_recommendations_example,
        custom_configuration_example,
        detailed_explanation_example,
        comparison_example,
        statistics_example,
        create_custom_user_example
    ]
    
    for example in examples:
        try:
            example()
            print("-" * 60)
        except Exception as e:
            print(f"Error running {example.__name__}: {e}")
            print("-" * 60)


if __name__ == "__main__":
    # Run all examples when script is executed directly
    run_all_examples()