import requests
import json

def test_profile_test9():
    """
    Test the specific profile test9@example.com to demonstrate why Tourism Director 
    and Conservation Director recommendations appear and analyze if they're reasonable.
    """
    
    # Based on the terminal output, this appears to be a profile with:
    # - 1-2 years experience
    # - 15 technical skills including Microsoft Office, Creative Suite, etc.
    # - Exploration level 1 (conservative)
    # - $50k-70k salary expectations
    # - Sales/marketing field identification
    
    test9_profile = {
        'age': '25-30',
        'location': 'Los Angeles, CA',
        'educationLevel': 'Bachelor\'s Degree',
        'currentSituation': 'Currently employed',
        'currentRole': 'Marketing Coordinator',
        'experience': '1-2',
        'resumeText': '''
        Marketing Coordinator with 2 years of experience in digital marketing and content creation.
        Experience with social media management, graphic design, and basic data analysis.
        
        EXPERIENCE:
        • Marketing Coordinator at StartupXYZ (2022-2024) - Managed social media accounts and created marketing materials
        • Marketing Intern at AgencyABC (2021-2022) - Assisted with campaign development and content creation
        
        SKILLS:
        • Digital Marketing: Social media management, content creation, email marketing
        • Design: Adobe Creative Suite, Canva, basic graphic design
        • Analytics: Google Analytics, social media analytics, Excel
        • Communication: Copywriting, presentation skills, client communication
        ''',
        'linkedinProfile': 'https://linkedin.com/in/test9',
        'technicalSkills': [
            'Microsoft Office Suite', 'Word Processing', 'Data Entry', 'Excel/Spreadsheets',
            'Google Workspace', 'PowerPoint', 'Email Management', 'Basic Computer Skills',
            'Graphic Design', 'Video Editing', 'Social Media Management', 'Adobe Creative Suite',
            'Web Design', 'Content Creation', 'Photography'
        ],
        'softSkills': ['Communication', 'Creativity', 'Organization', 'Time Management'],
        'workingWithData': 3,
        'workingWithPeople': 4,
        'creativeTasks': 5,
        'problemSolving': 4,
        'leadership': 2,
        'physicalHandsOnWork': 2,
        'outdoorWork': 2,
        'mechanicalAptitude': 2,
        'interests': ['Marketing', 'Design', 'Social Media', 'Content Creation'],
        'industries': ['Marketing', 'Digital Media'],
        'workEnvironment': 'Office/Remote',
        'careerGoals': 'Marketing Manager or Creative Director',
        'workLifeBalance': 'High',
        'salaryExpectations': '50k-70k',
        'explorationLevel': 1  # Conservative exploration
    }
    
    print('=== ANALYZING test9@example.com PROFILE ===')
    print('Profile characteristics:')
    print(f'- Experience: {test9_profile["experience"]} years')
    print(f'- Technical Skills: {len(test9_profile["technicalSkills"])} skills')
    print(f'- Current Role: {test9_profile["currentRole"]}')
    print(f'- Salary Expectations: {test9_profile["salaryExpectations"]}')
    print(f'- Exploration Level: {test9_profile["explorationLevel"]} (Conservative)')
    print(f'- Creative Tasks Rating: {test9_profile["creativeTasks"]}/5')
    print(f'- Outdoor Work Interest: {test9_profile["outdoorWork"]}/5')
    print()
    
    response = requests.post('http://localhost:8000/api/recommendations', json=test9_profile)
    
    if response.status_code == 200:
        recommendations = response.json()
        print(f'✅ Got {len(recommendations)} recommendations')
        print()
        
        # Look specifically for Tourism Director and Conservation Director
        tourism_found = False
        conservation_found = False
        
        for i, rec in enumerate(recommendations, 1):
            title = rec.get('title', 'Unknown')
            score = rec.get('relevanceScore', 0)
            zone = rec.get('zone', 'unknown')
            career_field = rec.get('careerField', 'unknown')
            consistency_penalty = rec.get('consistencyPenalty', 0)
            theme_boost = rec.get('themeAlignmentBoost', 0)
            
            print(f'{i}. {title}')
            print(f'   Score: {score}, Zone: {zone}, Field: {career_field}')
            print(f'   Consistency Penalty: {consistency_penalty}, Theme Boost: {theme_boost}')
            
            # Check for Tourism Director
            if 'tourism' in title.lower() and 'director' in title.lower():
                tourism_found = True
                print(f'   🎯 FOUND TOURISM DIRECTOR: {title}')
                print(f'   📊 Analysis:')
                print(f'      - Career Field: {career_field}')
                print(f'      - User Field: sales_marketing (inferred)')
                print(f'      - Consistency Penalty: {consistency_penalty}')
                print(f'      - Theme Alignment: {theme_boost}')
                print(f'      - Final Score: {score}')
                
                # Analyze why this might be recommended
                reasons = []
                if consistency_penalty >= -15:
                    reasons.append("Low consistency penalty suggests field alignment")
                if theme_boost > 0:
                    reasons.append(f"Positive theme boost (+{theme_boost}) indicates skill match")
                if score >= 60:
                    reasons.append("Score above Adventure Zone threshold")
                
                print(f'      - Reasoning: {"; ".join(reasons) if reasons else "Low score, likely filtered out"}')
            
            # Check for Conservation Director
            if 'conservation' in title.lower() and 'director' in title.lower():
                conservation_found = True
                print(f'   🌱 FOUND CONSERVATION DIRECTOR: {title}')
                print(f'   📊 Analysis:')
                print(f'      - Career Field: {career_field}')
                print(f'      - User Field: sales_marketing (inferred)')
                print(f'      - Consistency Penalty: {consistency_penalty}')
                print(f'      - Theme Alignment: {theme_boost}')
                print(f'      - Final Score: {score}')
                
                # Analyze why this might be recommended
                reasons = []
                if consistency_penalty >= -15:
                    reasons.append("Low consistency penalty suggests field alignment")
                if theme_boost > 0:
                    reasons.append(f"Positive theme boost (+{theme_boost}) indicates skill match")
                if score >= 60:
                    reasons.append("Score above Adventure Zone threshold")
                
                print(f'      - Reasoning: {"; ".join(reasons) if reasons else "Low score, likely filtered out"}')
            
            print()
        
        print('=== ANALYSIS SUMMARY ===')
        if tourism_found:
            print('✅ Tourism Director found in recommendations')
        else:
            print('❌ Tourism Director NOT found in recommendations')
            
        if conservation_found:
            print('✅ Conservation Director found in recommendations')
        else:
            print('❌ Conservation Director NOT found in recommendations')
        
        print()
        print('=== REASONABLENESS ASSESSMENT ===')
        
        # Assess if these recommendations make sense
        user_skills = test9_profile['technicalSkills']
        creative_skills = [skill for skill in user_skills if any(word in skill.lower() for word in ['design', 'creative', 'video', 'photo', 'content'])]
        communication_skills = [skill for skill in user_skills if any(word in skill.lower() for word in ['social media', 'marketing', 'communication'])]
        
        print(f'User has {len(creative_skills)} creative skills: {creative_skills}')
        print(f'User has {len(communication_skills)} communication skills: {communication_skills}')
        print(f'User rates creative tasks: {test9_profile["creativeTasks"]}/5')
        print(f'User rates outdoor work: {test9_profile["outdoorWork"]}/5')
        
        # Tourism Director assessment
        print()
        print('🎯 TOURISM DIRECTOR REASONABLENESS:')
        tourism_reasons = []
        if len(communication_skills) > 0:
            tourism_reasons.append("✅ Has marketing/communication skills relevant to tourism promotion")
        if len(creative_skills) > 0:
            tourism_reasons.append("✅ Has creative skills useful for tourism marketing materials")
        if test9_profile["workingWithPeople"] >= 4:
            tourism_reasons.append("✅ High people skills (4/5) suitable for tourism industry")
        if test9_profile["creativeTasks"] >= 4:
            tourism_reasons.append("✅ High creative interest (5/5) aligns with tourism marketing")
        
        tourism_concerns = []
        if test9_profile["experience"] == "1-2":
            tourism_concerns.append("⚠️ Limited experience for director-level role")
        if test9_profile["outdoorWork"] <= 2:
            tourism_concerns.append("⚠️ Low outdoor work interest may not align with tourism")
        if "tourism" not in [industry.lower() for industry in test9_profile.get("industries", [])]:
            tourism_concerns.append("⚠️ No tourism industry experience indicated")
        
        print("Positive factors:")
        for reason in tourism_reasons:
            print(f"  {reason}")
        print("Concerns:")
        for concern in tourism_concerns:
            print(f"  {concern}")
        
        # Conservation Director assessment
        print()
        print('🌱 CONSERVATION DIRECTOR REASONABLENESS:')
        conservation_reasons = []
        if len(communication_skills) > 0:
            conservation_reasons.append("✅ Has marketing skills useful for conservation awareness campaigns")
        if len(creative_skills) > 0:
            conservation_reasons.append("✅ Has creative skills for environmental education materials")
        if test9_profile["creativeTasks"] >= 4:
            conservation_reasons.append("✅ High creative interest aligns with conservation outreach")
        
        conservation_concerns = []
        if test9_profile["experience"] == "1-2":
            conservation_concerns.append("⚠️ Limited experience for director-level role")
        if test9_profile["outdoorWork"] <= 2:
            conservation_concerns.append("⚠️ Low outdoor work interest concerning for conservation work")
        if "environment" not in [interest.lower() for interest in test9_profile.get("interests", [])]:
            conservation_concerns.append("⚠️ No environmental interests indicated")
        if not any(skill.lower() in ["environmental", "sustainability", "conservation"] for skill in user_skills):
            conservation_concerns.append("⚠️ No environmental/conservation technical skills")
        
        print("Positive factors:")
        for reason in conservation_reasons:
            print(f"  {reason}")
        print("Concerns:")
        for concern in conservation_concerns:
            print(f"  {concern}")
        
        print()
        print('=== FINAL VERDICT ===')
        print('Tourism Director: QUESTIONABLE - Creative/marketing skills transfer but lacks tourism experience and director-level qualifications')
        print('Conservation Director: INAPPROPRIATE - Lacks environmental background, outdoor interest, and relevant experience')
        print()
        print('RECOMMENDATION: These director-level roles should have higher experience requirements and better field alignment checks.')
        
    else:
        print(f'❌ Error: {response.status_code} - {response.text}')

if __name__ == "__main__":
    test_profile_test9()