#!/usr/bin/env python3
"""
Test script for the enhanced recommendation algorithm
"""

from simple_server import extract_resume_insights, generate_enhanced_recommendations

def test_product_heavy_resume():
    """Test with a product-heavy resume (simulating the user's scenario)"""
    
    test_resume = """
    Product Manager at TechCorp leading product strategy and roadmap development. 
    Managed product lifecycle from conception to launch, working with engineering teams.
    Led product discovery sessions and defined product requirements.
    Collaborated with product marketing on go-to-market strategy.
    Drove product analytics and user research initiatives.
    Built product roadmaps and prioritized product features.
    Managed cross-functional product teams and stakeholders.
    Product management experience includes B2B and B2C products.
    Launched 5 major product releases with engineering collaboration.
    Product strategy focused on user experience and market fit.
    """
    
    print("=== TESTING ENHANCED ALGORITHM ===")
    print(f"Test resume has {test_resume.lower().count('product')} mentions of 'product'")
    print(f"Test resume has {test_resume.lower().count('engineering')} mentions of 'engineering'")
    print(f"Test resume has {test_resume.lower().count('scientist')} mentions of 'scientist'")
    print()
    
    # Extract insights
    insights = extract_resume_insights(test_resume)
    print("Resume insights:")
    print(f"  Current role: {insights.get('current_role')}")
    print(f"  Roles: {insights.get('roles')}")
    print(f"  Keyword frequencies: {insights.get('keyword_frequencies')}")
    print(f"  Dominant theme: {insights.get('dominant_theme')}")
    print()
    
    # Test user data
    user_data = {
        'experience': '5-10 years',
        'salary_expectations': '120,000 - 180,000',
        'industries': ['Technology', 'SaaS'],
        'technical_skills': ['Product Management', 'Analytics', 'User Research'],
        'working_with_data': 4,
        'working_with_people': 5,
        'leadership': 4,
        'resume_text': test_resume
    }
    
    # Generate recommendations
    recommendations = generate_enhanced_recommendations(user_data, 2)
    
    print(f"Generated {len(recommendations)} recommendations:")
    print()
    
    # Analyze results
    product_recs = 0
    engineering_recs = 0
    safe_zone_recs = 0
    
    for i, rec in enumerate(recommendations):
        title = rec.get('title', '')
        zone = rec.get('zone', 'unknown')
        score = rec.get('relevanceScore', 0)
        theme_boost = rec.get('themeAlignmentBoost', 0)
        
        if 'product' in title.lower():
            product_recs += 1
        if any(word in title.lower() for word in ['engineer', 'scientist', 'developer']):
            engineering_recs += 1
        if zone == 'safe':
            safe_zone_recs += 1
            
        print(f"{i+1}. {title}")
        print(f"   Zone: {zone} | Score: {score} | Theme Boost: {theme_boost}")
        print(f"   Match Reasons: {rec.get('matchReasons', [])}")
        print()
    
    print("=== ANALYSIS ===")
    print(f"Product-related recommendations: {product_recs}/{len(recommendations)} ({product_recs/len(recommendations)*100:.1f}%)")
    print(f"Engineering/Scientist recommendations: {engineering_recs}/{len(recommendations)} ({engineering_recs/len(recommendations)*100:.1f}%)")
    print(f"Safe Zone recommendations: {safe_zone_recs}/{len(recommendations)} ({safe_zone_recs/len(recommendations)*100:.1f}%)")
    print()
    
    # Expected: Most recommendations should be product-related, few should be engineering/scientist
    if product_recs >= len(recommendations) * 0.6:  # At least 60% product-related
        print("✅ SUCCESS: Majority of recommendations are product-related")
    else:
        print("❌ ISSUE: Not enough product-related recommendations")
        
    if engineering_recs <= len(recommendations) * 0.3:  # At most 30% engineering/scientist
        print("✅ SUCCESS: Reduced technical bias - fewer engineering/scientist recommendations")
    else:
        print("❌ ISSUE: Too many engineering/scientist recommendations despite minimal resume emphasis")
        
    if safe_zone_recs >= 2:  # At least 2 safe zone recommendations
        print("✅ SUCCESS: Safe Zone populated with relevant careers")
    else:
        print("❌ ISSUE: Safe Zone not properly populated")

if __name__ == "__main__":
    test_product_heavy_resume()