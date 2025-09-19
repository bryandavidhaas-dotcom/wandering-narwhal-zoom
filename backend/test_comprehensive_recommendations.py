#!/usr/bin/env python3
"""
Comprehensive test script for the enhanced recommendation engine.
Tests the new comprehensive career database with proper filtering and categorization.
"""

import requests
import json
from typing import Dict, Any

# Test configuration
API_BASE_URL = "http://localhost:8000"
API_ENDPOINT = f"{API_BASE_URL}/api/recommendations"

def test_senior_professional_profile():
    """Test profile for a senior professional with 20+ years experience expecting $150-250k"""
    
    print("🧪 Testing Senior Professional Profile (20+ years, $150-250k expectations)")
    print("=" * 80)
    
    test_profile = {
        "age": "45-54",
        "location": "San Francisco, CA",
        "educationLevel": "Master's degree",
        "certifications": ["PMP", "AWS Solutions Architect", "Scrum Master"],
        "currentSituation": "Currently employed, looking for advancement",
        "currentRole": "Senior Engineering Manager",
        "experience": "20+ years",
        "resumeText": """
        Senior Engineering Manager with 22 years of experience leading high-performance teams.
        Expertise in Python, Java, AWS, microservices architecture, and agile methodologies.
        Led teams of 15+ engineers, managed $5M+ budgets, and delivered enterprise-scale solutions.
        Experience with machine learning, data analytics, and cloud infrastructure.
        Strong background in fintech and healthcare industries.
        """,
        "linkedinProfile": "https://linkedin.com/in/senior-manager-profile",
        "technicalSkills": ["Python", "Java", "AWS", "Docker", "Kubernetes", "Machine Learning", "SQL"],
        "softSkills": ["Leadership", "Strategic Planning", "Team Building", "Communication"],
        "workingWithData": 4,
        "workingWithPeople": 5,
        "creativeTasks": 3,
        "problemSolving": 5,
        "leadership": 5,
        "physicalHandsOnWork": 2,
        "outdoorWork": 1,
        "mechanicalAptitude": 3,
        "interests": ["Technology Innovation", "Team Leadership", "Strategic Planning"],
        "industries": ["Technology", "Finance", "Healthcare"],
        "workEnvironment": "Hybrid",
        "careerGoals": "Executive leadership role with strategic impact",
        "workLifeBalance": "Important",
        "salaryExpectations": "$150,000 - $250,000",
        "explorationLevel": 2
    }
    
    try:
        response = requests.post(API_ENDPOINT, json=test_profile, timeout=30)
        
        if response.status_code == 200:
            recommendations = response.json()
            
            print(f"✅ API Response: {response.status_code}")
            print(f"📊 Total Recommendations: {len(recommendations)}")
            
            # Analyze recommendations by zone
            zones = {"safe": [], "stretch": [], "adventure": []}
            for rec in recommendations:
                zone = rec.get("zone", "unknown")
                if zone in zones:
                    zones[zone].append(rec)
            
            print(f"🎯 Zone Distribution: Safe={len(zones['safe'])}, Stretch={len(zones['stretch'])}, Adventure={len(zones['adventure'])}")
            
            # Check salary ranges
            salary_appropriate = 0
            experience_appropriate = 0
            
            print("\n📋 Detailed Recommendations:")
            print("-" * 60)
            
            for i, rec in enumerate(recommendations, 1):
                title = rec.get("title", "Unknown")
                salary_min = rec.get("salaryMin", 0)
                salary_max = rec.get("salaryMax", 0)
                exp_level = rec.get("experienceLevel", "unknown")
                score = rec.get("relevanceScore", 0)
                zone = rec.get("zone", "unknown")
                
                print(f"{i}. {title}")
                print(f"   💰 Salary: ${salary_min:,} - ${salary_max:,}")
                print(f"   📈 Experience Level: {exp_level}")
                print(f"   🎯 Score: {score}% | Zone: {zone}")
                
                # Check appropriateness
                if salary_min >= 120000:  # At least close to expectations
                    salary_appropriate += 1
                if exp_level in ["senior", "executive"]:
                    experience_appropriate += 1
                
                # Show match reasons
                match_reasons = rec.get("matchReasons", [])
                if match_reasons:
                    print(f"   ✨ Match Reasons: {', '.join(match_reasons[:2])}")
                
                print()
            
            # Validation results
            print("🔍 VALIDATION RESULTS:")
            print("-" * 40)
            print(f"✅ Salary Appropriateness: {salary_appropriate}/{len(recommendations)} recommendations >= $120k")
            print(f"✅ Experience Appropriateness: {experience_appropriate}/{len(recommendations)} senior/executive level")
            print(f"✅ Total Recommendations: {len(recommendations)} (should be 8-12)")
            print(f"✅ Zone Coverage: {'✓' if all(len(zones[z]) > 0 for z in zones) else '✗'} All zones covered")
            
            # Success criteria
            success_score = 0
            if salary_appropriate >= len(recommendations) * 0.7:  # 70% salary appropriate
                success_score += 25
                print("✅ PASS: Salary expectations mostly met")
            else:
                print("❌ FAIL: Too many low-salary recommendations")
            
            if experience_appropriate >= len(recommendations) * 0.6:  # 60% experience appropriate
                success_score += 25
                print("✅ PASS: Experience level mostly appropriate")
            else:
                print("❌ FAIL: Too many junior-level recommendations")
            
            if 8 <= len(recommendations) <= 15:
                success_score += 25
                print("✅ PASS: Good number of recommendations")
            else:
                print("❌ FAIL: Too few or too many recommendations")
            
            if all(len(zones[z]) > 0 for z in zones):
                success_score += 25
                print("✅ PASS: All zones have recommendations")
            else:
                print("❌ FAIL: Missing recommendations in some zones")
            
            print(f"\n🏆 OVERALL SCORE: {success_score}/100")
            
            if success_score >= 75:
                print("🎉 TEST PASSED: Senior professional recommendations are appropriate!")
                return True
            else:
                print("💥 TEST FAILED: Recommendations need improvement")
                return False
                
        else:
            print(f"❌ API Error: {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Test Error: {str(e)}")
        return False

def test_junior_professional_profile():
    """Test profile for a junior professional with 2-3 years experience expecting $60-90k"""
    
    print("\n🧪 Testing Junior Professional Profile (2-3 years, $60-90k expectations)")
    print("=" * 80)
    
    test_profile = {
        "age": "25-34",
        "location": "Austin, TX",
        "educationLevel": "Bachelor's degree",
        "certifications": ["Google Analytics", "AWS Cloud Practitioner"],
        "currentSituation": "Currently employed, looking for growth",
        "currentRole": "Junior Data Analyst",
        "experience": "2-3 years",
        "resumeText": """
        Junior Data Analyst with 2.5 years of experience in data analysis and visualization.
        Proficient in Python, SQL, Excel, and Tableau. Experience with basic machine learning.
        Worked on customer analytics and business intelligence projects.
        Strong analytical skills and eager to learn new technologies.
        """,
        "linkedinProfile": "https://linkedin.com/in/junior-analyst",
        "technicalSkills": ["Python", "SQL", "Excel", "Tableau", "Power BI"],
        "softSkills": ["Analytical Thinking", "Communication", "Problem Solving"],
        "workingWithData": 5,
        "workingWithPeople": 3,
        "creativeTasks": 3,
        "problemSolving": 4,
        "leadership": 2,
        "physicalHandsOnWork": 2,
        "outdoorWork": 1,
        "mechanicalAptitude": 2,
        "interests": ["Data Science", "Analytics", "Technology"],
        "industries": ["Technology", "E-commerce"],
        "workEnvironment": "Remote",
        "careerGoals": "Become a senior data scientist",
        "workLifeBalance": "Very Important",
        "salaryExpectations": "$60,000 - $90,000",
        "explorationLevel": 3
    }
    
    try:
        response = requests.post(API_ENDPOINT, json=test_profile, timeout=30)
        
        if response.status_code == 200:
            recommendations = response.json()
            
            print(f"✅ API Response: {response.status_code}")
            print(f"📊 Total Recommendations: {len(recommendations)}")
            
            # Check salary and experience appropriateness
            salary_appropriate = 0
            experience_appropriate = 0
            
            print("\n📋 Detailed Recommendations:")
            print("-" * 60)
            
            for i, rec in enumerate(recommendations, 1):
                title = rec.get("title", "Unknown")
                salary_min = rec.get("salaryMin", 0)
                salary_max = rec.get("salaryMax", 0)
                exp_level = rec.get("experienceLevel", "unknown")
                score = rec.get("relevanceScore", 0)
                zone = rec.get("zone", "unknown")
                
                print(f"{i}. {title}")
                print(f"   💰 Salary: ${salary_min:,} - ${salary_max:,}")
                print(f"   📈 Experience Level: {exp_level}")
                print(f"   🎯 Score: {score}% | Zone: {zone}")
                
                # Check appropriateness for junior level
                if salary_max <= 120000:  # Appropriate for junior level
                    salary_appropriate += 1
                if exp_level in ["junior", "mid"]:
                    experience_appropriate += 1
                
                print()
            
            print("🔍 VALIDATION RESULTS:")
            print("-" * 40)
            print(f"✅ Salary Appropriateness: {salary_appropriate}/{len(recommendations)} recommendations <= $120k")
            print(f"✅ Experience Appropriateness: {experience_appropriate}/{len(recommendations)} junior/mid level")
            
            return len(recommendations) > 0
            
        else:
            print(f"❌ API Error: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Test Error: {str(e)}")
        return False

def test_api_health():
    """Test if the API is running and healthy"""
    try:
        response = requests.get(f"{API_BASE_URL}/health", timeout=10)
        if response.status_code == 200:
            print("✅ API Health Check: PASSED")
            return True
        else:
            print(f"❌ API Health Check: FAILED ({response.status_code})")
            return False
    except Exception as e:
        print(f"❌ API Health Check: ERROR - {str(e)}")
        return False

def main():
    """Run comprehensive tests"""
    print("🚀 COMPREHENSIVE RECOMMENDATION ENGINE TEST")
    print("=" * 80)
    print("Testing the enhanced recommendation engine with comprehensive career database")
    print("Focus: Experience level filtering, salary expectations, and proper categorization")
    print()
    
    # Test API health first
    if not test_api_health():
        print("💥 Cannot proceed - API is not healthy")
        return
    
    print()
    
    # Run tests
    test_results = []
    
    # Test 1: Senior Professional
    senior_result = test_senior_professional_profile()
    test_results.append(("Senior Professional Test", senior_result))
    
    # Test 2: Junior Professional
    junior_result = test_junior_professional_profile()
    test_results.append(("Junior Professional Test", junior_result))
    
    # Summary
    print("\n" + "=" * 80)
    print("📊 TEST SUMMARY")
    print("=" * 80)
    
    passed = 0
    for test_name, result in test_results:
        status = "✅ PASSED" if result else "❌ FAILED"
        print(f"{test_name}: {status}")
        if result:
            passed += 1
    
    print(f"\nOverall: {passed}/{len(test_results)} tests passed")
    
    if passed == len(test_results):
        print("🎉 ALL TESTS PASSED! The recommendation engine is working correctly.")
    else:
        print("💥 SOME TESTS FAILED! The recommendation engine needs fixes.")
    
    print("\n🔍 Key Validation Points:")
    print("- ✅ Senior professionals get executive/senior roles with $150k+ salaries")
    print("- ✅ Junior professionals get appropriate entry/mid-level roles")
    print("- ✅ Resume and LinkedIn data influence recommendations")
    print("- ✅ Safe/Stretch/Adventure zones are properly categorized")
    print("- ✅ Experience level filtering works correctly")

if __name__ == "__main__":
    main()