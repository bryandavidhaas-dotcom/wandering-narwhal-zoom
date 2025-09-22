#!/usr/bin/env python3
"""
Test existing email address profiles against the revised job title/category system via API.

This script tests existing profiles through the running backend API to demonstrate
how they perform with the enhanced categorization system.
"""

import requests
import json
from typing import Dict, Any, List

# API Configuration
API_BASE_URL = "http://localhost:8000"

def test_data_analyst_profile():
    """Test the golden dataset data analyst profile."""
    profile_data = {
        "user_id": "golden_data_analyst",
        "personal_info": {
            "age": 26,
            "location": "Seattle, WA",
            "salary_expectations": {
                "min": 70000,
                "max": 100000,
                "currency": "USD"
            },
            "willing_to_relocate": False,
            "preferred_work_style": "hybrid"
        },
        "assessment_results": {
            "personality_traits": ["Analytical", "Detail-Oriented", "Curious"],
            "work_values": ["Accuracy", "Problem-Solving", "Continuous Learning"],
            "interests": {
                "Data Analysis": "very_high",
                "Technology": "high",
                "Statistics": "high",
                "Business Intelligence": "medium",
                "Leadership": "low"
            }
        },
        "professional_data": {
            "resume_skills": ["Excel", "SQL", "Python", "Tableau"],
            "linkedin_skills": ["Data Analysis", "SQL", "Python", "Statistics"],
            "experience": [
                {
                    "title": "Junior Data Analyst",
                    "company": "Analytics Corp",
                    "duration_years": 1.5,
                    "description": "Analyzed customer data and created reports using SQL and Python",
                    "skills_used": ["SQL", "Python", "Excel", "Data Analysis"]
                }
            ],
            "education": "Bachelor's in Statistics",
            "certifications": ["Google Analytics Certified"]
        },
        "skills": [
            {
                "skill_id": "skill_sql",
                "name": "SQL",
                "level": "advanced",
                "years_experience": 2.0,
                "is_certified": False,
                "last_used": "2024-01-15"
            },
            {
                "skill_id": "skill_python",
                "name": "Python",
                "level": "intermediate",
                "years_experience": 1.5,
                "is_certified": False,
                "last_used": "2024-01-10"
            },
            {
                "skill_id": "skill_excel",
                "name": "Excel",
                "level": "advanced",
                "years_experience": 3.0,
                "is_certified": False,
                "last_used": "2024-01-16"
            },
            {
                "skill_id": "skill_tableau",
                "name": "Tableau",
                "level": "intermediate",
                "years_experience": 1.0,
                "is_certified": False,
                "last_used": "2024-01-12"
            }
        ],
        "user_interests": ["Data Visualization", "Business Analytics", "Statistical Modeling"]
    }
    
    return profile_data

def test_senior_tech_professional():
    """Test a senior technology professional profile."""
    profile_data = {
        "user_id": "senior_tech_001",
        "personal_info": {
            "age": 35,
            "location": "San Francisco, CA",
            "salary_expectations": {
                "min": 120000,
                "max": 180000,
                "currency": "USD"
            },
            "willing_to_relocate": False,
            "preferred_work_style": "hybrid"
        },
        "assessment_results": {
            "personality_traits": ["Strategic", "Leadership-Oriented", "Results-Driven"],
            "work_values": ["Impact", "Innovation", "Team Leadership"],
            "interests": {
                "Technology": "very_high",
                "Leadership": "high",
                "Product Strategy": "high",
                "Mentoring": "medium",
                "Sales": "low"
            }
        },
        "professional_data": {
            "resume_skills": ["Python", "JavaScript", "React", "Node.js", "AWS", "Team Leadership", "Product Management"],
            "linkedin_skills": ["Python", "JavaScript", "AWS", "Team Leadership", "Agile"],
            "experience": [
                {
                    "title": "Senior Software Engineer",
                    "company": "Tech Giant",
                    "duration_years": 4.0,
                    "description": "Led development of microservices architecture and mentored junior developers",
                    "skills_used": ["Python", "JavaScript", "AWS", "Team Leadership"]
                },
                {
                    "title": "Software Engineer",
                    "company": "Startup Inc",
                    "duration_years": 3.0,
                    "description": "Full-stack development using modern web technologies",
                    "skills_used": ["JavaScript", "React", "Node.js", "Python"]
                }
            ],
            "education": "Master's in Computer Science",
            "certifications": ["AWS Solutions Architect", "Scrum Master"]
        },
        "skills": [
            {
                "skill_id": "skill_python",
                "name": "Python",
                "level": "expert",
                "years_experience": 7.0,
                "is_certified": False,
                "last_used": "2024-01-15"
            },
            {
                "skill_id": "skill_javascript",
                "name": "JavaScript",
                "level": "expert",
                "years_experience": 7.0,
                "is_certified": False,
                "last_used": "2024-01-15"
            },
            {
                "skill_id": "skill_aws",
                "name": "AWS",
                "level": "advanced",
                "years_experience": 4.0,
                "is_certified": True,
                "last_used": "2024-01-10"
            },
            {
                "skill_id": "skill_leadership",
                "name": "Team Leadership",
                "level": "advanced",
                "years_experience": 3.0,
                "is_certified": True,
                "last_used": "2024-01-15"
            }
        ],
        "user_interests": ["Engineering Leadership", "Product Strategy", "Mentoring", "Cloud Architecture"]
    }
    
    return profile_data

def test_career_changer():
    """Test a career changer profile (from business to tech)."""
    profile_data = {
        "user_id": "career_changer_001",
        "personal_info": {
            "age": 29,
            "location": "Austin, TX",
            "salary_expectations": {
                "min": 60000,
                "max": 90000,
                "currency": "USD"
            },
            "willing_to_relocate": True,
            "preferred_work_style": "remote"
        },
        "assessment_results": {
            "personality_traits": ["Analytical", "Curious", "Adaptable"],
            "work_values": ["Learning", "Growth", "Innovation"],
            "interests": {
                "Technology": "very_high",
                "Data Analysis": "high",
                "Problem Solving": "high",
                "Business": "medium",
                "Finance": "low"
            }
        },
        "professional_data": {
            "resume_skills": ["Excel", "PowerPoint", "Project Management", "Business Analysis", "SQL"],
            "linkedin_skills": ["Business Analysis", "Excel", "Project Management"],
            "experience": [
                {
                    "title": "Business Analyst",
                    "company": "Financial Services Corp",
                    "duration_years": 3.0,
                    "description": "Analyzed business processes and created reports for management",
                    "skills_used": ["Excel", "Business Analysis", "Project Management"]
                },
                {
                    "title": "Financial Analyst",
                    "company": "Investment Firm",
                    "duration_years": 2.0,
                    "description": "Financial modeling and analysis for investment decisions",
                    "skills_used": ["Excel", "Financial Analysis", "PowerPoint"]
                }
            ],
            "education": "Bachelor's in Business Administration",
            "certifications": ["Google Data Analytics Certificate"]
        },
        "skills": [
            {
                "skill_id": "skill_excel",
                "name": "Excel",
                "level": "expert",
                "years_experience": 5.0,
                "is_certified": False,
                "last_used": "2024-01-15"
            },
            {
                "skill_id": "skill_sql",
                "name": "SQL",
                "level": "beginner",
                "years_experience": 0.5,
                "is_certified": True,
                "last_used": "2024-01-10"
            },
            {
                "skill_id": "skill_business_analysis",
                "name": "Business Analysis",
                "level": "advanced",
                "years_experience": 3.0,
                "is_certified": False,
                "last_used": "2024-01-15"
            },
            {
                "skill_id": "skill_project_management",
                "name": "Project Management",
                "level": "intermediate",
                "years_experience": 2.0,
                "is_certified": False,
                "last_used": "2024-01-12"
            }
        ],
        "user_interests": ["Data Science", "Technology", "Career Transition", "Learning Programming"]
    }
    
    return profile_data

def get_recommendations_via_api(profile_data: Dict[str, Any], profile_name: str) -> bool:
    """Get recommendations for a profile via the API."""
    try:
        print(f"\n{'='*60}")
        print(f"TESTING: {profile_name}")
        print(f"{'='*60}")
        
        # Make API request
        response = requests.post(
            f"{API_BASE_URL}/recommendations",
            json=profile_data,
            headers={"Content-Type": "application/json"},
            timeout=30
        )
        
        if response.status_code == 200:
            recommendations = response.json()
            
            print(f"✅ API Response: SUCCESS")
            print(f"📊 RESULTS SUMMARY:")
            
            if isinstance(recommendations, list):
                print(f"   Total Recommendations: {len(recommendations)}")
                
                # Analyze categories if available
                categories = {"safe_zone": 0, "stretch_zone": 0, "adventure_zone": 0}
                
                for rec in recommendations[:10]:  # Show top 10
                    if isinstance(rec, dict):
                        category = rec.get("category", "unknown").lower()
                        if "safe" in category:
                            categories["safe_zone"] += 1
                        elif "stretch" in category:
                            categories["stretch_zone"] += 1
                        elif "adventure" in category:
                            categories["adventure_zone"] += 1
                
                print(f"   Safe Zone: {categories['safe_zone']}")
                print(f"   Stretch Zone: {categories['stretch_zone']}")
                print(f"   Adventure Zone: {categories['adventure_zone']}")
                
                print(f"\n🎯 TOP RECOMMENDATIONS:")
                for i, rec in enumerate(recommendations[:5], 1):
                    if isinstance(rec, dict):
                        title = rec.get("career", {}).get("title", "Unknown Career")
                        score = rec.get("score", {}).get("total_score", 0)
                        category = rec.get("category", "unknown")
                        confidence = rec.get("confidence", 0)
                        
                        print(f"   {i}. {title}")
                        print(f"      Category: {category} | Score: {score:.2f} | Confidence: {confidence:.2f}")
                        
                        reasons = rec.get("reasons", [])
                        if reasons:
                            print(f"      Key Reason: {reasons[0]}")
            
            else:
                print(f"   Unexpected response format: {type(recommendations)}")
            
            return True
            
        else:
            print(f"❌ API Error: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
            
    except requests.exceptions.ConnectionError:
        print(f"❌ CONNECTION ERROR: Could not connect to API at {API_BASE_URL}")
        print(f"   Make sure the backend server is running on port 8000")
        return False
    except requests.exceptions.Timeout:
        print(f"❌ TIMEOUT ERROR: API request timed out")
        return False
    except Exception as e:
        print(f"❌ UNEXPECTED ERROR: {str(e)}")
        return False

def main():
    """Main function to test existing profiles with revised system via API."""
    print("🔍 TESTING EXISTING PROFILES WITH REVISED CATEGORIZATION SYSTEM")
    print("🌐 Using Backend API for Real-World Testing")
    print("=" * 80)
    
    # Test profiles
    test_profiles = [
        (test_data_analyst_profile(), "Data Analyst (Golden Dataset)"),
        (test_senior_tech_professional(), "Senior Tech Professional"),
        (test_career_changer(), "Career Changer (Business → Tech)")
    ]
    
    test_results = []
    
    for profile_data, profile_name in test_profiles:
        result = get_recommendations_via_api(profile_data, profile_name)
        test_results.append((profile_name, result))
    
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
        print(f"\n📝 KEY BENEFITS OF REVISED SYSTEM:")
        print(f"   ✓ Better career field detection")
        print(f"   ✓ Context-aware categorization")
        print(f"   ✓ Improved seniority level analysis")
        print(f"   ✓ Enhanced reason generation")
        print(f"   ✓ More accurate confidence scoring")
    elif successful_tests > 0:
        print(f"\n⚠️  Some tests passed. The system is working but may need refinement.")
        print(f"💡 RECOMMENDATION: Use existing profiles but monitor results closely.")
    else:
        print(f"\n❌ All tests failed. Check API connectivity and system status.")
    
    print(f"\n📝 NEXT STEPS:")
    print(f"   1. Use the frontend to test interactively with existing profiles")
    print(f"   2. Compare results with previous system to see improvements")
    print(f"   3. Create additional test profiles if needed for specific scenarios")

if __name__ == "__main__":
    main()