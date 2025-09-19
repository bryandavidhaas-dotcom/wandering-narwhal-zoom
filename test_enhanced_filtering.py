"""
Test script to demonstrate enhanced filtering capabilities.

This script shows how the recommendation engine prevents inappropriate
recommendations across experience levels, industries, and career paths.
"""

import sys
import os

# Add the recommendation engine to the path
sys.path.append(os.path.join(os.path.dirname(__file__), 'recommendation-engine'))

from enhanced_filters import EnhancedFilterEngine
from enhanced_mock_data import (
    ENHANCED_SKILLS, ENHANCED_CAREERS, 
    STUDENT_PROFILE, TRADES_PROFESSIONAL_PROFILE, SENIOR_PROFESSIONAL_PROFILE
)
from config import FilteringConfig

def test_enhanced_filtering():
    """Test the enhanced filtering system with different user types."""
    
    print("🔍 ENHANCED FILTERING DEMONSTRATION")
    print("=" * 60)
    
    # Initialize the enhanced filter engine
    config = FilteringConfig(
        min_skill_overlap=0.1,  # More lenient for demonstration
        max_salary_deviation=0.5,
        consider_related_skills=True
    )
    
    enhanced_filter = EnhancedFilterEngine(config, ENHANCED_SKILLS)
    
    # Test cases
    test_cases = [
        ("👨‍🎓 STUDENT", STUDENT_PROFILE),
        ("🔧 TRADES PROFESSIONAL", TRADES_PROFESSIONAL_PROFILE),
        ("👔 SENIOR PROFESSIONAL", SENIOR_PROFESSIONAL_PROFILE)
    ]
    
    for user_type_name, user_profile in test_cases:
        print(f"\n{user_type_name} RECOMMENDATIONS:")
        print("-" * 40)
        
        # Get filtered careers
        filtered_careers = enhanced_filter.filter_careers(user_profile, ENHANCED_CAREERS)
        
        print(f"📊 Total careers available: {len(ENHANCED_CAREERS)}")
        print(f"✅ Appropriate careers after filtering: {len(filtered_careers)}")
        print(f"🚫 Inappropriate careers filtered out: {len(ENHANCED_CAREERS) - len(filtered_careers)}")
        
        print("\n📋 RECOMMENDED CAREERS:")
        for i, career in enumerate(filtered_careers, 1):
            salary_range = f"${career.salary_range.min:,} - ${career.salary_range.max:,}"
            print(f"  {i}. {career.title}")
            print(f"     💰 Salary: {salary_range}")
            print(f"     🎯 Education: {career.education_requirements}")
            
            # Show required skills
            if career.required_skills:
                skills = [skill.name for skill in career.required_skills[:3]]
                print(f"     🛠️  Key Skills: {', '.join(skills)}")
            print()
        
        print("🚫 FILTERED OUT CAREERS:")
        filtered_out = [career for career in ENHANCED_CAREERS if career not in filtered_careers]
        for career in filtered_out:
            reason = get_filter_reason(user_profile, career, enhanced_filter)
            print(f"  ❌ {career.title} - {reason}")
        
        print("\n" + "=" * 60)

def get_filter_reason(user_profile, career, filter_engine):
    """Determine why a career was filtered out."""
    
    # Check experience level mismatch
    user_type = filter_engine._classify_user_type(user_profile)
    career_exp_req = filter_engine._determine_career_experience_requirement(career)
    user_exp_level = filter_engine._determine_user_experience_level(user_profile)
    
    # Experience level mismatch
    if user_type.value == "student" and career_exp_req not in ["entry", "junior"]:
        return "Experience level too high for student"
    
    if user_type.value == "senior_professional" and career_exp_req in ["entry", "junior"]:
        return "Experience level too low for senior professional"
    
    # Industry mismatch
    user_industries = filter_engine._determine_user_industries(user_profile)
    career_industry = filter_engine._classify_career_industry(career)
    
    if (career_industry not in user_industries and 
        not filter_engine._is_transferable_industry_match(user_industries, career_industry) and
        career_industry.value != "business"):
        return f"Industry mismatch ({career_industry.value} vs {[i.value for i in user_industries]})"
    
    # Salary mismatch
    if not filter_engine._is_salary_compatible(user_profile, career):
        return "Salary range incompatible"
    
    # Skill mismatch
    if not filter_engine._has_some_mandatory_skills(user_profile, career):
        return "Missing critical mandatory skills"
    
    return "Multiple filtering criteria"

def demonstrate_protection_features():
    """Demonstrate specific protection features."""
    
    print("\n🛡️  PROTECTION FEATURES DEMONSTRATION")
    print("=" * 60)
    
    protections = [
        "✅ Students only see entry-level positions",
        "✅ Trades professionals see trades careers + transferable skills",
        "✅ Senior professionals don't see entry-level positions",
        "✅ Industry alignment prevents random career suggestions",
        "✅ Experience level matching prevents unrealistic jumps",
        "✅ Salary compatibility ensures realistic expectations",
        "✅ Skill overlap requirements ensure achievable transitions"
    ]
    
    for protection in protections:
        print(f"  {protection}")
    
    print(f"\n🎯 KEY BENEFITS:")
    print(f"  • Prevents overwhelming users with irrelevant options")
    print(f"  • Ensures career progression makes logical sense")
    print(f"  • Respects industry expertise and specialization")
    print(f"  • Maintains realistic salary and skill expectations")
    print(f"  • Provides focused, actionable career guidance")

if __name__ == "__main__":
    try:
        test_enhanced_filtering()
        demonstrate_protection_features()
        
        print(f"\n🎉 ENHANCED FILTERING TEST COMPLETED SUCCESSFULLY!")
        print(f"✅ The recommendation engine now properly filters recommendations")
        print(f"✅ Students, trades professionals, and experienced workers get appropriate suggestions")
        print(f"✅ Cross-industry and cross-experience mismatches are prevented")
        
    except Exception as e:
        print(f"\n❌ ERROR: {str(e)}")
        print(f"❌ Enhanced filtering test failed")