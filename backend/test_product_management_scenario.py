#!/usr/bin/env python3
"""
Test the career path consistency penalty with a realistic product management scenario
to ensure healthcare careers like "Family Medicine Physician" are properly penalized.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from simple_server import generate_enhanced_recommendations

def test_product_management_profile():
    """Test with a realistic product management profile that should NOT get healthcare recommendations"""
    
    print("🧪 Testing Product Management Profile Against Healthcare Career Suggestions")
    print("=" * 80)
    
    # Realistic product management user profile with strong product signals
    user_data = {
        "age": "30-35",
        "location": "San Francisco, CA",
        "education_level": "Bachelor's Degree",
        "certifications": ["Product Management Certificate", "Agile Certification"],
        "current_situation": "Currently employed",
        "current_role": "Senior Product Manager",
        "experience": "5-10 years",
        "resume_text": """
        Senior Product Manager with 7 years of experience in product management and strategy.
        
        EXPERIENCE:
        Senior Product Manager at TechCorp (2020-2024)
        - Led product roadmap for core platform serving 2M+ users
        - Managed cross-functional teams of 15+ engineers, designers, and analysts
        - Drove product strategy resulting in 40% increase in user engagement
        - Conducted user research and A/B testing to optimize product features
        - Collaborated with engineering teams on technical product requirements
        
        Product Manager at StartupXYZ (2018-2020)
        - Owned product lifecycle from ideation to launch for mobile application
        - Worked closely with UX designers on user experience optimization
        - Analyzed product metrics and user feedback to drive product decisions
        - Managed product backlog and sprint planning with engineering teams
        
        Associate Product Manager at BigTech (2017-2018)
        - Supported senior product managers on feature development
        - Conducted market research and competitive analysis
        - Created product requirements documents and user stories
        
        SKILLS:
        Product Management, Product Strategy, User Research, A/B Testing, Data Analysis,
        Agile/Scrum, Roadmap Planning, Cross-functional Leadership, User Experience Design,
        Product Analytics, Go-to-Market Strategy, Stakeholder Management
        """,
        "linkedin_profile": "https://linkedin.com/in/product-manager-profile",
        "technical_skills": ["Product Management", "User Research", "Data Analysis", "A/B Testing", "Agile/Scrum", "Product Analytics"],
        "soft_skills": ["Leadership", "Communication", "Strategic Thinking", "Problem Solving"],
        "working_with_data": 4,
        "working_with_people": 5,
        "creative_tasks": 4,
        "problem_solving": 5,
        "leadership": 5,
        "physical_hands_on_work": 2,
        "outdoor_work": 1,
        "mechanical_aptitude": 2,
        "interests": ["Technology", "User Experience", "Business Strategy", "Innovation"],
        "industries": ["Technology", "Software", "SaaS"],
        "work_environment": "Office/Remote",
        "career_goals": "Advance to VP of Product or Chief Product Officer",
        "work_life_balance": "Important",
        "salary_expectations": "150,000 - 200,000"
    }
    
    print("👤 User Profile Summary:")
    print(f"   Role: {user_data['current_role']}")
    print(f"   Experience: {user_data['experience']}")
    print(f"   Key Skills: {', '.join(user_data['technical_skills'][:4])}")
    print(f"   Industries: {', '.join(user_data['industries'])}")
    print(f"   Salary Target: {user_data['salary_expectations']}")
    print()
    
    # Generate recommendations
    recommendations = generate_enhanced_recommendations(user_data, exploration_level=1)
    
    print(f"📊 Generated {len(recommendations)} recommendations")
    print()
    
    # Analyze recommendations for healthcare careers
    healthcare_careers = []
    product_careers = []
    tech_careers = []
    other_careers = []
    
    for rec in recommendations:
        career_field = rec.get("careerField", "unknown")
        title = rec.get("title", "")
        score = rec.get("relevanceScore", 0)
        penalty = rec.get("consistencyPenalty", 0)
        
        if career_field == "healthcare":
            healthcare_careers.append((title, score, penalty))
        elif career_field == "product_management":
            product_careers.append((title, score, penalty))
        elif career_field == "technology":
            tech_careers.append((title, score, penalty))
        else:
            other_careers.append((title, score, penalty, career_field))
    
    print("🏥 Healthcare Career Recommendations:")
    if healthcare_careers:
        for title, score, penalty in healthcare_careers:
            print(f"   ❌ {title}: Score={score}, Penalty={penalty}")
        print(f"   ⚠️  WARNING: {len(healthcare_careers)} healthcare careers were recommended!")
    else:
        print("   ✅ No healthcare careers recommended (as expected)")
    print()
    
    print("🎯 Product Management Career Recommendations:")
    for title, score, penalty in product_careers[:5]:  # Show top 5
        print(f"   ✅ {title}: Score={score}, Penalty={penalty}")
    print()
    
    print("💻 Technology Career Recommendations:")
    for title, score, penalty in tech_careers[:3]:  # Show top 3
        print(f"   ✅ {title}: Score={score}, Penalty={penalty}")
    print()
    
    if other_careers:
        print("🔄 Other Career Recommendations:")
        for title, score, penalty, field in other_careers[:3]:  # Show top 3
            print(f"   📋 {title} ({field}): Score={score}, Penalty={penalty}")
        print()
    
    # Verify that healthcare careers are properly penalized
    print("🔍 Verification Results:")
    
    # Check 1: Healthcare careers should have very low scores due to penalties
    healthcare_scores = [score for _, score, _ in healthcare_careers]
    if healthcare_scores:
        max_healthcare_score = max(healthcare_scores)
        print(f"   📉 Highest healthcare career score: {max_healthcare_score}")
        if max_healthcare_score < 30:
            print("   ✅ Healthcare careers properly penalized (score < 30)")
        else:
            print(f"   ❌ Healthcare careers not sufficiently penalized (score = {max_healthcare_score})")
    else:
        print("   ✅ No healthcare careers in recommendations")
    
    # Check 2: Product management careers should have high scores
    pm_scores = [score for _, score, _ in product_careers]
    if pm_scores:
        avg_pm_score = sum(pm_scores) / len(pm_scores)
        print(f"   📈 Average product management career score: {avg_pm_score:.1f}")
        if avg_pm_score > 70:
            print("   ✅ Product management careers properly prioritized")
        else:
            print(f"   ⚠️  Product management careers may need higher scores (avg = {avg_pm_score:.1f})")
    
    # Check 3: Verify specific problematic career is penalized
    family_medicine_found = False
    for title, score, penalty in healthcare_careers:
        if "family medicine" in title.lower():
            family_medicine_found = True
            print(f"   🎯 Family Medicine Physician: Score={score}, Penalty={penalty}")
            if score < 20:
                print("   ✅ Family Medicine Physician properly penalized for PM profile")
            else:
                print(f"   ❌ Family Medicine Physician not sufficiently penalized (score = {score})")
            break
    
    if not family_medicine_found:
        print("   ✅ Family Medicine Physician not in recommendations (ideal outcome)")
    
    print()
    print("📋 Summary:")
    print(f"   Total recommendations: {len(recommendations)}")
    print(f"   Healthcare careers: {len(healthcare_careers)}")
    print(f"   Product management careers: {len(product_careers)}")
    print(f"   Technology careers: {len(tech_careers)}")
    print(f"   Other careers: {len(other_careers)}")
    
    # Final assessment
    if len(healthcare_careers) == 0 or (healthcare_scores and max(healthcare_scores) < 30):
        print("\n🎉 SUCCESS: Career path consistency penalty is working!")
        print("   Healthcare careers are properly filtered out or heavily penalized.")
        return True
    else:
        print("\n❌ ISSUE: Healthcare careers are still being recommended with high scores.")
        print("   The consistency penalty may need to be stronger.")
        return False

if __name__ == "__main__":
    print("🚀 Testing Career Path Consistency with Product Management Profile")
    print("=" * 80)
    print("This test verifies that healthcare careers like 'Family Medicine Physician'")
    print("are NOT recommended to users with strong product management backgrounds.")
    print()
    
    try:
        success = test_product_management_profile()
        
        if success:
            print("\n✅ TEST PASSED: Career path consistency penalty is working correctly!")
        else:
            print("\n❌ TEST FAILED: Healthcare careers are still being inappropriately recommended!")
            sys.exit(1)
            
    except Exception as e:
        print(f"\n💥 UNEXPECTED ERROR: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)