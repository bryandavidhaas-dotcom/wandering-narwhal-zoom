"""
Test script to verify the new balanced distribution logic.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from simple_server import generate_enhanced_recommendations

def test_balanced_distribution():
    """Test that the new distribution logic produces balanced results."""
    
    # Test data simulating a product manager profile
    test_user_data = {
        "age": "30-35",
        "location": "San Francisco, CA",
        "education_level": "Bachelor's Degree",
        "certifications": [],
        "current_situation": "Currently employed",
        "current_role": "Product Manager",
        "experience": "5-10 years",
        "resume_text": """
        Senior Product Manager with 7 years of experience in product management, product strategy, 
        and product development. Led product teams, managed product roadmaps, conducted user research, 
        and drove product launches. Experience with agile methodologies, data analysis, and 
        cross-functional collaboration. Strong background in product management and product strategy.
        """,
        "linkedin_profile": "https://linkedin.com/in/productmanager",
        "technical_skills": ["Product Management", "Data Analysis", "User Research", "Agile"],
        "soft_skills": ["Leadership", "Communication", "Strategic Thinking"],
        "working_with_data": 4,
        "working_with_people": 5,
        "creative_tasks": 4,
        "problem_solving": 5,
        "leadership": 4,
        "physical_hands_on_work": 2,
        "outdoor_work": 1,
        "mechanical_aptitude": 2,
        "interests": ["Technology", "Innovation", "Strategy"],
        "industries": ["Technology", "SaaS"],
        "work_environment": "Office/Remote",
        "career_goals": "Advance to senior product leadership",
        "work_life_balance": "Important",
        "salary_expectations": "$150,000 - $200,000"
    }
    
    print("🧪 Testing Balanced Distribution Logic")
    print("=" * 50)
    
    # Test with different exploration levels to ensure consistency
    exploration_levels = [1, 2, 3, 4, 5]
    
    for level in exploration_levels:
        print(f"\n🔍 Testing with exploration level: {level}")
        print("-" * 30)
        
        try:
            recommendations = generate_enhanced_recommendations(test_user_data, level)
            
            # Count recommendations by zone
            safe_count = len([r for r in recommendations if r.get('zone') == 'safe'])
            stretch_count = len([r for r in recommendations if r.get('zone') == 'stretch'])
            adventure_count = len([r for r in recommendations if r.get('zone') == 'adventure'])
            total_count = len(recommendations)
            
            print(f"📊 Results:")
            print(f"   Safe Zone: {safe_count} recommendations")
            print(f"   Stretch Zone: {stretch_count} recommendations")
            print(f"   Adventure Zone: {adventure_count} recommendations")
            print(f"   Total: {total_count} recommendations")
            
            # Check if distribution is balanced (3 per zone)
            target_per_zone = 3
            is_balanced = (safe_count == target_per_zone and 
                          stretch_count == target_per_zone and 
                          adventure_count == target_per_zone)
            
            if is_balanced:
                print(f"   ✅ BALANCED: Perfect 3-3-3 distribution achieved!")
            else:
                print(f"   ⚠️  UNBALANCED: Expected 3-3-3, got {safe_count}-{stretch_count}-{adventure_count}")
            
            # Show sample recommendations from each zone
            print(f"   📝 Sample recommendations:")
            for rec in recommendations[:6]:  # Show first 6
                zone_emoji = {"safe": "🟢", "stretch": "🟡", "adventure": "🔵"}.get(rec.get('zone'), '❓')
                print(f"      {zone_emoji} {rec.get('title', 'Unknown')} (Score: {rec.get('relevanceScore', 0)})")
                
        except Exception as e:
            print(f"   ❌ ERROR: {str(e)}")
    
    print("\n" + "=" * 50)
    print("🎯 Test Summary:")
    print("The new balanced distribution algorithm should:")
    print("1. Always return exactly 3 recommendations per zone (9 total)")
    print("2. Use redistribution to backfill zones with fewer than 3 careers")
    print("3. Maintain consistency regardless of exploration level")
    print("4. Prioritize relevance when redistributing careers")

if __name__ == "__main__":
    test_balanced_distribution()