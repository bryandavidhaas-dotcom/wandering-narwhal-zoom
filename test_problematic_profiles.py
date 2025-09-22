#!/usr/bin/env python3
"""
Test script to reproduce the problematic recommendation scenarios mentioned in the task.
This will help us identify and fix the core issues with the recommendation engine.
"""

import requests
import json
from typing import Dict, Any

# Backend API endpoint
API_BASE = "http://localhost:8000"

def test_profile(profile_name: str, profile_data: Dict[str, Any]) -> Dict[str, Any]:
    """Test a user profile and return recommendations"""
    print(f"\n{'='*60}")
    print(f"🧪 TESTING PROFILE: {profile_name}")
    print(f"{'='*60}")
    
    try:
        response = requests.post(f"{API_BASE}/api/recommendations", json=profile_data)
        response.raise_for_status()
        recommendations = response.json()
        
        print(f"✅ Got {len(recommendations)} recommendations")
        
        # Analyze recommendations by zone
        zones = {"safe": [], "stretch": [], "adventure": []}
        for rec in recommendations:
            zone = rec.get("zone", "unknown")
            if zone in zones:
                zones[zone].append(rec)
        
        print(f"\n📊 ZONE DISTRIBUTION:")
        print(f"   🟢 Safe Zone: {len(zones['safe'])} recommendations")
        print(f"   🟡 Stretch Zone: {len(zones['stretch'])} recommendations") 
        print(f"   🔵 Adventure Zone: {len(zones['adventure'])} recommendations")
        
        print(f"\n🎯 TOP 10 RECOMMENDATIONS:")
        for i, rec in enumerate(recommendations[:10], 1):
            title = rec.get("title", "Unknown")
            score = rec.get("relevanceScore", 0)
            zone = rec.get("zone", "unknown")
            zone_emoji = {"safe": "🟢", "stretch": "🟡", "adventure": "🔵"}.get(zone, "❓")
            print(f"   {i:2d}. {zone_emoji} {title} (score: {score})")
        
        return recommendations
        
    except requests.exceptions.RequestException as e:
        print(f"❌ API Error: {e}")
        return []
    except Exception as e:
        print(f"❌ Error: {e}")
        return []

def main():
    """Test the three problematic profiles mentioned in the task"""
    
    # Test Profile 1: Product Manager (Test9@example.com equivalent)
    # Should get product-related recommendations, NOT software engineer, tourism manager, etc.
    product_profile = {
        "age": "30-35",
        "location": "San Francisco, CA",
        "educationLevel": "Bachelor's Degree in Business",
        "certifications": ["Product Management Certificate", "Agile Certification"],
        "currentSituation": "Currently employed",
        "currentRole": "Product Manager",
        "experience": "5-10",
        "resumeText": """
        Senior Product Manager with 7 years of experience leading cross-functional teams to deliver innovative products. 
        Expertise in product strategy, roadmap planning, user research, and data-driven decision making.
        
        EXPERIENCE:
        • Product Manager at TechCorp (2019-2024) - Led product development for mobile app with 2M+ users
        • Associate Product Manager at StartupXYZ (2017-2019) - Managed product roadmap and feature prioritization
        • Business Analyst at ConsultingFirm (2015-2017) - Analyzed market trends and business requirements
        
        SKILLS:
        • Product Management: Roadmap planning, user research, A/B testing, product analytics
        • Data Analysis: SQL, Tableau, Google Analytics, user behavior analysis
        • Project Management: Agile, Scrum, Jira, Confluence
        • Communication: Stakeholder management, presentation skills, cross-functional collaboration
        """,
        "linkedinProfile": "https://linkedin.com/in/productmanager",
        "technicalSkills": ["Product Management", "SQL", "Tableau", "Google Analytics", "Jira", "Confluence", "A/B Testing", "User Research"],
        "softSkills": ["Leadership", "Communication", "Strategic Thinking", "Problem Solving"],
        "workingWithData": 5,
        "workingWithPeople": 5,
        "creativeTasks": 4,
        "problemSolving": 5,
        "leadership": 5,
        "physicalHandsOnWork": 1,
        "outdoorWork": 1,
        "mechanicalAptitude": 2,
        "interests": ["Technology", "Business Strategy", "User Experience"],
        "industries": ["Technology", "Software"],
        "workEnvironment": "Office/Remote",
        "careerGoals": "Advance to Senior Product Manager or Director of Product",
        "workLifeBalance": "Important",
        "salaryExpectations": "120k-180k",
        "explorationLevel": 2
    }
    
    # Test Profile 2: Airplane Mechanic (Test10@example.com equivalent)
    # Should get mechanical/aviation recommendations, NOT junior product manager, marketing analyst, etc.
    mechanic_profile = {
        "age": "25-30",
        "location": "Dallas, TX",
        "educationLevel": "Associate Degree in Aviation Maintenance",
        "certifications": ["A&P License", "FAA Certification"],
        "currentSituation": "Currently employed",
        "currentRole": "Aircraft Mechanic",
        "experience": "3-5",
        "resumeText": """
        Licensed Aircraft Mechanic with 4 years of experience maintaining and repairing commercial aircraft.
        Specialized in engine maintenance, hydraulic systems, and electrical troubleshooting.
        
        EXPERIENCE:
        • Aircraft Mechanic at AirlineXYZ (2020-2024) - Performed scheduled maintenance on Boeing 737 fleet
        • Junior Mechanic at MRO Services (2018-2020) - Assisted with aircraft inspections and repairs
        • Apprentice at Aviation Academy (2017-2018) - Learned fundamentals of aircraft systems
        
        SKILLS:
        • Aircraft Systems: Engine maintenance, hydraulics, electrical systems, avionics
        • Tools & Equipment: Torque wrenches, multimeters, borescopes, hydraulic test equipment
        • Safety & Compliance: FAA regulations, safety protocols, documentation procedures
        • Problem Solving: Troubleshooting mechanical issues, root cause analysis
        """,
        "linkedinProfile": "https://linkedin.com/in/aircraftmechanic",
        "technicalSkills": ["Aircraft Maintenance", "Engine Repair", "Hydraulic Systems", "Electrical Troubleshooting", "Avionics", "FAA Regulations"],
        "softSkills": ["Attention to Detail", "Problem Solving", "Safety Focus", "Teamwork"],
        "workingWithData": 2,
        "workingWithPeople": 3,
        "creativeTasks": 2,
        "problemSolving": 5,
        "leadership": 2,
        "physicalHandsOnWork": 5,
        "outdoorWork": 3,
        "mechanicalAptitude": 5,
        "interests": ["Aviation", "Mechanical Systems", "Technology"],
        "industries": ["Aviation", "Transportation"],
        "workEnvironment": "Hangar/Workshop",
        "careerGoals": "Become Lead Mechanic or Inspector",
        "workLifeBalance": "Moderate",
        "salaryExpectations": "60k-80k",
        "explorationLevel": 1
    }
    
    # Test Profile 3: Social Media & Communications (Test11@example.com equivalent)
    # Should get communications/marketing recommendations, NOT restaurant manager, spa manager, etc.
    communications_profile = {
        "age": "26-30",
        "location": "Los Angeles, CA",
        "educationLevel": "Bachelor's Degree in Communications",
        "certifications": ["Google Analytics", "Facebook Blueprint", "HubSpot Content Marketing"],
        "currentSituation": "Currently employed",
        "currentRole": "Social Media Manager",
        "experience": "3-5",
        "resumeText": """
        Creative Social Media Manager with 4 years of experience developing and executing digital marketing campaigns.
        Expertise in content creation, community management, and social media analytics.
        
        EXPERIENCE:
        • Social Media Manager at MarketingAgency (2021-2024) - Managed social media for 15+ clients
        • Content Creator at InfluencerCorp (2020-2021) - Created engaging content for Instagram and TikTok
        • Communications Intern at PR Firm (2019-2020) - Assisted with press releases and media outreach
        
        SKILLS:
        • Social Media: Instagram, Facebook, Twitter, TikTok, LinkedIn, YouTube
        • Content Creation: Copywriting, graphic design, video editing, photography
        • Analytics: Google Analytics, Facebook Insights, social media metrics
        • Communications: Public relations, brand messaging, community management
        """,
        "linkedinProfile": "https://linkedin.com/in/socialmediamanager",
        "technicalSkills": ["Social Media Management", "Content Creation", "Google Analytics", "Adobe Creative Suite", "Copywriting", "SEO", "Email Marketing"],
        "softSkills": ["Creativity", "Communication", "Brand Awareness", "Trend Analysis"],
        "workingWithData": 4,
        "workingWithPeople": 5,
        "creativeTasks": 5,
        "problemSolving": 4,
        "leadership": 3,
        "physicalHandsOnWork": 1,
        "outdoorWork": 1,
        "mechanicalAptitude": 1,
        "interests": ["Digital Marketing", "Social Media", "Content Creation", "Brand Strategy"],
        "industries": ["Marketing", "Media", "Technology"],
        "workEnvironment": "Office/Remote",
        "careerGoals": "Advance to Marketing Manager or Brand Manager",
        "workLifeBalance": "Important",
        "salaryExpectations": "55k-75k",
        "explorationLevel": 3
    }
    
    # Test all profiles
    profiles = [
        ("Product Manager Profile", product_profile),
        ("Aircraft Mechanic Profile", mechanic_profile),
        ("Social Media & Communications Profile", communications_profile)
    ]
    
    results = {}
    for profile_name, profile_data in profiles:
        results[profile_name] = test_profile(profile_name, profile_data)
    
    # Summary analysis
    print(f"\n{'='*80}")
    print(f"📋 SUMMARY ANALYSIS")
    print(f"{'='*80}")
    
    for profile_name, recommendations in results.items():
        if not recommendations:
            continue
            
        print(f"\n🔍 {profile_name}:")
        top_5 = recommendations[:5]
        for i, rec in enumerate(top_5, 1):
            title = rec.get("title", "Unknown")
            score = rec.get("relevanceScore", 0)
            print(f"   {i}. {title} (score: {score})")
        
        # Check for problematic recommendations
        problematic = []
        for rec in recommendations[:10]:
            title = rec.get("title", "").lower()
            if profile_name == "Product Manager Profile":
                if any(bad in title for bad in ["software engineer", "tourism", "conservation", "data officer"]):
                    problematic.append(rec.get("title"))
            elif profile_name == "Aircraft Mechanic Profile":
                if any(bad in title for bad in ["product manager", "marketing", "principal", "curriculum", "banquet"]):
                    problematic.append(rec.get("title"))
            elif profile_name == "Social Media & Communications Profile":
                if any(bad in title for bad in ["restaurant", "spa", "banquet", "school counselor", "maintenance", "special education"]):
                    problematic.append(rec.get("title"))
        
        if problematic:
            print(f"   ❌ PROBLEMATIC RECOMMENDATIONS: {', '.join(problematic)}")
        else:
            print(f"   ✅ No obviously problematic recommendations in top 10")

if __name__ == "__main__":
    main()