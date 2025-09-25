#!/usr/bin/env python3
"""
Test the actual API endpoint that the frontend calls to see if
Medical Assistant and Delivery Driver are being returned.
"""

import requests
import json

def test_api_recommendations():
    """Test the actual /api/recommendations endpoint"""
    
    # Bryan's actual profile data
    bryan_profile = {
        "age": "45-54",
        "location": "Petaluma, CA",
        "educationLevel": "Master's Degree",
        "certifications": ["Northwestern University Kellogg School of Management - Certificate in AI Strategies for Business Transformation"],
        "currentSituation": "Employed",
        "currentRole": "SVP, Product, Project Management, Real Estate & Facilities",
        "experience": "20+ years",
        "resumeText": """BRYAN HAAS 
707-478-7636 I bryandavidhaas@gmail.com I LinkedIn I Petaluma, CA  
Forward-thinking executive with 20+ years of cross-functional leadership in digital product strategy, customer 
experience transformation, and operational excellence across fintech, financial services, and high-growth 
platforms, including early-stage and growth-stage start-ups. Renowned for scaling innovation in complex 
environments by combining disciplined execution, user-first design, and enterprise alignment. Known for driving 
growth, launching new business lines, and optimizing agile operating models. Track record of cross-functional 
influence, technical fluency, and values-led leadership that builds trust and delivers real-world impact. 

WORK EXPERIENCE 
Redwood Credit Union – San Francisco Bay Area, CA            
2021 – 6/2025 
A financial cooperative with $8B in assets, serving 500K members & recognized among the top 10 credit unions in CA. 
SVP, Product, Project Management, Real Estate & Facilities                        
2024 – 6/2025 
Executive sponsor for enterprise product strategy, project delivery, and infrastructure. Oversaw 40+ 
concurrent initiatives and led 3 direct and 20+ indirect reports across product, PMO, and real estate/facilities. 
• Enterprise Strategy Execution: Spearheaded one of five company-wide strategies to transform Business 
Services into a scalable growth engine; achieved 11% business membership growth, 14% loan lift, 15% 
deposit increase, and 13% increase in products per business member over three years.  
• Product Innovation & Launches: Delivered multiple new and overhauled products, including consumer and 
business checking accounts, savings products, and enhanced business services offerings as part of the 3-year 
roadmap; aligned launches with targeted marketing and operational readiness to accelerate revenue impact. 
• Portfolio Leadership: Directed enterprise PMO overseeing 40+ initiatives spanning systems modernization, 
new product development, and business line enablement; improved risk visibility and delivered more projects 
than originally planned within established timelines and budgets. 
• Customer Experience Redesign: Reimagined onboarding and post-sale communications for business 
clients, increasing adoption velocity and contributing to a 6-point NPS gain in under 24 months. 
• Digital & Data Infrastructure: Enabled new CRM and lead tracking systems across three verticals; 
eliminated legacy workflows, improved conversion tracking, and enabled segment-specific reporting. 
• Vendor Accountability & Delivery Oversight: Provided executive-level escalation support across the 
enterprise project portfolio, stepping in when critical milestones were at risk; notably course-corrected a CRM 
rollout by renegotiating deliverables and realigning timelines to keep the program on track. 
SVP, Marketing, Communications, Product & Market Analytics                             
2021 – 2024 
Led enterprise marketing, internal/external communications, positioning, and go-to-market execution. 
Managed 4 direct and 20+ indirect team members. 
• Integrated Growth Strategy: Orchestrated full-funnel acquisition strategy that drove ~7% membership 
growth during tenure; aligned digital, broadcast, and grassroots outreach with product growth objectives. 
• Marketing Intelligence: Led market analytics team to embed machine learning models into acquisition 
campaigns; improved segmentation precision & lifted engagement/conversion by 20%+ over legacy criteria. 
• Brand Modernization: Shifted brand toward authentic member-first storytelling; improved community trust, 
credibility, and digital engagement across multi-channel campaigns. 
• Organizational Leadership: Built a culture of internal promotion and succession planning; sustained 90%+ 
engagement and extremely low turnover across high-performing teams during key transformation period. 
• Cross-Functional Integration: Operationalized campaign analytics and creative feedback loops, improving 
cycle time, reducing message fatigue, and aligning campaign investment with member LTV. 
Western Union – San Francisco Bay Area, CA               
2016 – 2021 
A global leader in cross-border money transfers, moving billions annually for 150M customers across 200+ countries. 
Head of Customer Experience Strategy, UI/UX & Content   
Led enterprise-wide CX strategy and design execution across global web and app ecosystem. Managed 4 
direct and 25 indirect team members across design, content, and analytics.    
• CX Modernization at Scale: Ch Expanded measurement approach beyond traditional NPS dashboards to 
include enterprise Customer Journey Analytics and Straight-Through Processing (STP) metrics, uncovering 
failure points and directly influencing operational improvements. 
• Multi-Country UX Deployment: Directed redesign and localization of 150+ websites and mobile 
experiences; ensured compliance, cultural relevance, and customer trust across diverse markets. 
• New Product Expansion: Served as strategic partner to Deloitte and internal execs in launching Western 
Union's global digital banking solution; led UI/UX architecture and content alignment across customer flows. 
• Customer Retention Enablement: Established escalation and analytics feedback systems that reduced 
resolution cycles, closed root-cause issues, and improved digital satisfaction KPIs. 
• Leadership Development: Built and scaled a distributed CX organization, instilling data fluency, customer 
empathy, and rapid delivery standards across design, content, and analytics functions. 
Xoom (a PayPal Company) – San Francisco Bay Area, CA              
2011 – 2016 
A digital payment platform enabling fast international money transfers for 1.6M customers across 40+ countries. 
Manager, Product Management (Product, Content, UI/UX)         
Owned end-to-end product lifecycle for core remittance platform across 40+ countries. Managed 6 direct and 
2 indirect reports, and served as primary business lead across product, design, and content.        
• Vertical Launch Execution: Designed and launched two new product verticals (bill pay, mobile reload) from 
concept through release; expanded addressable market and drove new revenue streams. 
• Conversion Optimization & Journey Rebuilds: Reimagined both first-time and repeat user transaction 
experiences, cutting interaction steps by 60% and boosting conversion by 11%. 
• Enterprise Co-Branding: Led Walmart cobranded site implementation, aligning with external stakeholders 
and delivering on-brand, on-budget, and on-time; also managed PayPal rebranding post-acquisition. 
• Agile Systems Delivery: Embedded A/B testing and analytics into agile development cycles, improving 
experimentation velocity and decision-making accuracy across product org. 
• Cross-Functional Collaboration: Worked hand-in-hand with engineering, compliance, marketing, and 
design to accelerate roadmap while maintaining global coverage and scalability. 
OTHER EXPERIENCES 
Bank of the West | Pay By Touch | Copart | GreenPoint Mortgage | NextCard            
1998 – 2011  
Held VP & Director roles across process improvement, analytics, risk operations, and CX.  
EDUCATION & CERTIFICATIONS                   
Golden Gate University – MS in Human Resources, Organizational Development  
Sonoma State University – Bachelor of Arts (BA) in Psychology   
Northwestern University Kellogg School of Management – Certificate in AI Strategies for 
Business Transformation 
TOOLS 
SQL, Lucid Chart, Medallia, Amplitude, Access, BI Tools, Customer Journey Analytics, Visio, Jira""",
        "linkedinProfile": "https://linkedin.com/in/bryandavidhaas",
        "technicalSkills": [
            "SQL", "Lucid Chart", "Medallia", "Amplitude", "Access", "BI Tools", 
            "Customer Journey Analytics", "Visio", "Jira", "Product Management",
            "Strategic Planning", "Digital Product Strategy", "Customer Experience",
            "Product Analytics", "A/B Testing", "Machine Learning Models",
            "Marketing Strategy", "Brand Management", "Go-to-Market"
        ],
        "softSkills": [
            "Executive Leadership", "Strategic Thinking", "Cross-functional Leadership",
            "Team Management", "Communication", "Problem Solving", "Change Management"
        ],
        "workingWithData": 5,
        "workingWithPeople": 5,
        "creativeTasks": 4,
        "problemSolving": 5,
        "leadership": 5,
        "physicalHandsOnWork": 2,
        "outdoorWork": 2,
        "mechanicalAptitude": 3,
        "interests": [
            "Product Strategy", "Digital Transformation", "Customer Experience",
            "Team Leadership", "Innovation", "Data Analytics", "Financial Services"
        ],
        "industries": [
            "Financial Services", "Fintech", "Banking", "Credit Unions",
            "Digital Payments", "Technology", "Startups"
        ],
        "workEnvironment": "Hybrid",
        "careerGoals": "Continue executive leadership in product strategy and digital transformation",
        "workLifeBalance": "Important",
        "salaryExpectations": "150000-250000",  # Bryan's actual expectations
        "explorationLevel": 3
    }
    
    print("🧪 Testing Actual API Endpoint")
    print("=" * 60)
    print(f"👤 Profile: {bryan_profile['currentRole']}")
    print(f"💰 Salary: {bryan_profile['salaryExpectations']}")
    print(f"📈 Experience: {bryan_profile['experience']}")
    print(f"🎯 Exploration Level: {bryan_profile['explorationLevel']}")
    
    try:
        # Call the actual API endpoint
        response = requests.post(
            "http://localhost:8000/api/recommendations",
            json=bryan_profile,
            headers={"Content-Type": "application/json"},
            timeout=30
        )
        
        if response.status_code == 200:
            recommendations = response.json()
            print(f"\n✅ API Response: {len(recommendations)} recommendations")
            
            # Check for problematic careers
            problematic_found = []
            for rec in recommendations:
                title = rec.get("title", "").lower()
                if ("medical assistant" in title or 
                    "delivery driver" in title or
                    "assistant" in title and "executive" not in title):
                    problematic_found.append(rec)
            
            if problematic_found:
                print(f"\n🚨 PROBLEM: Found {len(problematic_found)} inappropriate recommendations:")
                for rec in problematic_found:
                    salary_min = rec.get("salaryMin", rec.get("minSalary", 0))
                    salary_max = rec.get("salaryMax", rec.get("maxSalary", 0))
                    zone = rec.get("zone", "unknown")
                    score = rec.get("relevanceScore", 0)
                    print(f"   - {rec['title']}: ${salary_min:,}-${salary_max:,} ({zone} zone, score: {score})")
            else:
                print(f"\n✅ SUCCESS: No inappropriate recommendations found")
            
            # Show sample appropriate recommendations
            print(f"\n📋 Sample Recommendations:")
            for i, rec in enumerate(recommendations[:10], 1):
                salary_min = rec.get("salaryMin", rec.get("minSalary", 0))
                salary_max = rec.get("salaryMax", rec.get("maxSalary", 0))
                zone = rec.get("zone", "unknown")
                score = rec.get("relevanceScore", 0)
                print(f"   {i}. {rec['title']}")
                print(f"      💰 ${salary_min:,} - ${salary_max:,}")
                print(f"      🎯 {zone} zone (score: {score})")
            
            return len(problematic_found) == 0
            
        else:
            print(f"❌ API Error: {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except requests.exceptions.ConnectionError:
        print("❌ Connection Error: Make sure the server is running on localhost:8000")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    success = test_api_recommendations()
    
    print(f"\n" + "="*60)
    if success:
        print("🎉 API TEST PASSED")
        print("✅ No inappropriate recommendations found")
        print("✅ The salary filtering is working correctly in the API")
    else:
        print("❌ API TEST FAILED")
        print("🔧 The API is returning inappropriate recommendations")
        print("\n🔍 This confirms the issue is in the production API endpoint")