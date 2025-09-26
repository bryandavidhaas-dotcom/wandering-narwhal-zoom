#!/usr/bin/env python3

import requests
import json

def test_bryan_real_resume():
    """Test with Bryan's actual resume data"""
    
    url = "http://localhost:8002/api/recommendations"
    
    # Bryan's actual profile with real resume
    bryan_profile = {
        "age": "45",
        "location": "Petaluma, CA",
        "educationLevel": "Master's Degree",
        "currentRole": "SVP, Product, Project Management, Real Estate & Facilities",
        "experience": "20+ years",
        "resumeText": """BRYAN HAAS 
Forward-thinking executive with 20+ years of cross-functional leadership in digital product strategy, customer 
experience transformation, and operational excellence across fintech, financial services, and high-growth 
platforms, including early-stage and growth-stage start-ups. Renowned for scaling innovation in complex 
environments by combining disciplined execution, user-first design, and enterprise alignment. Known for driving 
growth, launching new business lines, and optimizing agile operating models.

WORK EXPERIENCE 
Redwood Credit Union – San Francisco Bay Area, CA 2021 – 6/2025 
SVP, Product, Project Management, Real Estate & Facilities 2024 – 6/2025 
Executive sponsor for enterprise product strategy, project delivery, and infrastructure. Oversaw 40+ 
concurrent initiatives and led 3 direct and 20+ indirect reports across product, PMO, and real estate/facilities.

SVP, Marketing, Communications, Product & Market Analytics 2021 – 2024 
Led enterprise marketing, internal/external communications, positioning, and go-to-market execution. 
Managed 4 direct and 20+ indirect team members.

Western Union – San Francisco Bay Area, CA 2016 – 2021 
Head of Customer Experience Strategy, UI/UX & Content   
Led enterprise-wide CX strategy and design execution across global web and app ecosystem. Managed 4 
direct and 25 indirect team members across design, content, and analytics.

Xoom (a PayPal Company) – San Francisco Bay Area, CA 2011 – 2016 
Manager, Product Management (Product, Content, UI/UX)         
Owned end-to-end product lifecycle for core remittance platform across 40+ countries. Managed 6 direct and 
2 indirect reports, and served as primary business lead across product, design, and content.""",
        "technicalSkills": ["Product Strategy", "Customer Experience", "Digital Transformation", "Project Management", "Analytics", "SQL", "Jira", "Amplitude"],
        "softSkills": ["Leadership", "Strategic Planning", "Cross-functional Collaboration", "Team Management"],
        "industries": ["Financial Services", "Fintech", "Technology"],
        "salaryExpectations": "$200,000 - $300,000",
        "explorationLevel": 3
    }
    
    print(f"Testing with Bryan's REAL resume data...")
    print(f"URL: {url}")
    print(f"Profile: {bryan_profile['currentRole']}, {bryan_profile['experience']}")
    print(f"Salary: {bryan_profile['salaryExpectations']}")
    
    try:
        response = requests.post(url, json=bryan_profile, timeout=15)
        print(f"\nResponse Status: {response.status_code}")
        
        if response.status_code == 200:
            recommendations = response.json()
            print(f"✅ SUCCESS! Got {len(recommendations)} recommendations")
            
            # Check for problematic careers
            problematic_careers = []
            appropriate_careers = []
            
            for career in recommendations:
                title = career.get('title', 'Unknown')
                salary_min = career.get('salaryMin', career.get('minSalary', 0))
                salary_max = career.get('salaryMax', career.get('maxSalary', 0))
                
                if 'Medical Assistant' in title or 'Delivery Driver' in title:
                    problematic_careers.append({
                        'title': title,
                        'salary_min': salary_min,
                        'salary_max': salary_max
                    })
                else:
                    appropriate_careers.append({
                        'title': title,
                        'salary_min': salary_min,
                        'salary_max': salary_max
                    })
            
            if problematic_careers:
                print(f"\n❌ PROBLEM: Found {len(problematic_careers)} inappropriate careers:")
                for career in problematic_careers:
                    print(f"  - {career['title']}: ${career['salary_min']:,}-${career['salary_max']:,}")
            else:
                print("\n✅ SUCCESS: No inappropriate careers found!")
            
            print(f"\nTop 5 appropriate recommendations:")
            for i, career in enumerate(appropriate_careers[:5]):
                print(f"  {i+1}. {career['title']}: ${career['salary_min']:,}-${career['salary_max']:,}")
                
        else:
            print(f"❌ Error: {response.status_code}")
            print(f"Response: {response.text}")
            
    except Exception as e:
        print(f"❌ ERROR: {e}")

if __name__ == "__main__":
    test_bryan_real_resume()