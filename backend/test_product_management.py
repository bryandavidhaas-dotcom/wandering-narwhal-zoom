#!/usr/bin/env python3
"""
Test script to validate Product Management career recommendations
"""

import requests
import json

def test_product_management_profile():
    """Test with a realistic Product Management profile"""
    
    # Bryan's Product Management profile
    test_profile = {
        "age": "35-44",
        "location": "San Francisco, CA",
        "educationLevel": "Bachelor's degree",
        "certifications": ["Product Management", "Agile/Scrum"],
        "currentSituation": "Currently employed",
        "currentRole": "Senior Product Manager",
        "experience": "20+",
        "resumeText": "Senior Product Manager with 20+ years experience in product management, product strategy, roadmap planning, user research, A/B testing, go-to-market strategy, cross-functional team leadership, agile development, product analytics, and product launches at technology companies.",
        "linkedinProfile": "https://linkedin.com/in/bryan-haas-product-manager",
        "technicalSkills": ["Product Management", "Product Strategy", "User Research", "A/B Testing", "Analytics", "Roadmap Planning", "Agile", "Scrum"],
        "softSkills": ["Leadership", "Communication", "Strategic Thinking", "Problem Solving"],
        "workingWithData": 4,
        "workingWithPeople": 5,
        "creativeTasks": 4,
        "problemSolving": 5,
        "leadership": 5,
        "physicalHandsOnWork": 2,
        "outdoorWork": 1,
        "mechanicalAptitude": 2,
        "interests": ["Technology", "Innovation", "User Experience"],
        "industries": ["Technology", "Software"],
        "workEnvironment": "Office/Remote",
        "careerGoals": "Continue growing in product leadership",
        "workLifeBalance": "Important",
        "salaryExpectations": "150k-250k",
        "explorationLevel": 1
    }
    
    try:
        print("🧪 Testing Product Management Profile Recognition...")
        print(f"📋 Profile: {test_profile['currentRole']}, {test_profile['experience']} years experience")
        print(f"💰 Salary expectations: {test_profile['salaryExpectations']}")
        print(f"🎯 Resume contains: Product Management, Strategy, Leadership")
        print()
        
        # Make API request
        response = requests.post(
            "http://localhost:8000/api/recommendations",
            json=test_profile,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            recommendations = response.json()
            
            print(f"✅ API Response: {response.status_code}")
            print(f"📊 Total recommendations: {len(recommendations)}")
            print()
            
            # Analyze recommendations by zone
            zones = {"safe": [], "stretch": [], "adventure": []}
            for rec in recommendations:
                zone = rec.get("zone", "unknown")
                if zone in zones:
                    zones[zone].append(rec)
            
            print("🎯 RECOMMENDATIONS BY ZONE:")
            print(f"Safe Zone: {len(zones['safe'])} recommendations")
            print(f"Stretch Zone: {len(zones['stretch'])} recommendations")
            print(f"Adventure Zone: {len(zones['adventure'])} recommendations")
            print()
            
            # Check for Product Management roles
            product_roles = []
            for rec in recommendations:
                title = rec.get("title", "")
                if any(keyword in title.lower() for keyword in ["product manager", "product lead", "head of product", "vp product", "chief product officer", "director of product"]):
                    product_roles.append(rec)
            
            print(f"🎯 PRODUCT MANAGEMENT ROLES FOUND: {len(product_roles)}")
            
            if product_roles:
                print("✅ SUCCESS: Product Management roles detected!")
                for role in product_roles:
                    print(f"  • {role['title']} (Zone: {role.get('zone', 'unknown')}, Score: {role.get('relevanceScore', 0)})")
                    if role.get('matchReasons'):
                        print(f"    Reasons: {', '.join(role['matchReasons'])}")
            else:
                print("❌ FAILURE: No Product Management roles found!")
                print("Top 5 recommendations instead:")
                for i, rec in enumerate(recommendations[:5]):
                    print(f"  {i+1}. {rec['title']} (Zone: {rec.get('zone', 'unknown')}, Score: {rec.get('relevanceScore', 0)})")
            
            print()
            print("🔍 DETAILED ANALYSIS:")
            
            # Show top recommendations with scores
            print("Top 10 recommendations with scoring breakdown:")
            for i, rec in enumerate(recommendations[:10]):
                title = rec.get("title", "Unknown")
                zone = rec.get("zone", "unknown")
                score = rec.get("relevanceScore", 0)
                role_boost = rec.get("roleBoost", 0)
                exp_boost = rec.get("experienceBoost", 0)
                salary_boost = rec.get("salaryBoost", 0)
                
                print(f"{i+1:2d}. {title:<35} | Zone: {zone:<9} | Score: {score:3d} | Role: +{role_boost:2d} | Exp: +{exp_boost:2d} | Sal: +{salary_boost:2d}")
            
            return len(product_roles) > 0
            
        else:
            print(f"❌ API Error: {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Test failed with error: {str(e)}")
        return False

if __name__ == "__main__":
    success = test_product_management_profile()
    if success:
        print("\n🎉 TEST PASSED: Product Management recommendations working!")
    else:
        print("\n💥 TEST FAILED: Product Management recommendations not working!")