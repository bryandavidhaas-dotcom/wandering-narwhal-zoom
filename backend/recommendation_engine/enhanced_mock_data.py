"""
Enhanced mock data for the recommendation engine with diverse career paths.

This module provides comprehensive mock data including trades careers,
different experience levels, and various industries to test the enhanced
filtering capabilities.
"""

from datetime import datetime, timedelta
from .models import (
    UserProfile, Career, Skill, UserSkill, RequiredSkill, SalaryRange,
    PersonalInfo, AssessmentResults, ProfessionalData, Experience,
    SkillLevel, InterestLevel, Demand, ExperienceLevel
)

# Enhanced Skills Database with Trades and Professional Skills
ENHANCED_SKILLS = [
    # Technology Skills
    Skill(skill_id="tech_1", name="Python", category="Programming Language", related_skills=["tech_2", "tech_3"]),
    Skill(skill_id="tech_2", name="JavaScript", category="Programming Language", related_skills=["tech_1", "tech_4"]),
    Skill(skill_id="tech_3", name="Data Analysis", category="Technical Skill", related_skills=["tech_1", "tech_5"]),
    Skill(skill_id="tech_4", name="React", category="Framework", related_skills=["tech_2"]),
    Skill(skill_id="tech_5", name="Machine Learning", category="Technical Skill", related_skills=["tech_1", "tech_3"]),
    
    # Trades Skills
    Skill(skill_id="trade_1", name="Electrical Wiring", category="Trades Skill", related_skills=["trade_2", "trade_3"]),
    Skill(skill_id="trade_2", name="Circuit Analysis", category="Trades Skill", related_skills=["trade_1"]),
    Skill(skill_id="trade_3", name="Safety Protocols", category="Trades Skill", related_skills=["trade_1", "trade_4"]),
    Skill(skill_id="trade_4", name="Blueprint Reading", category="Trades Skill", related_skills=["trade_3", "trade_5"]),
    Skill(skill_id="trade_5", name="Hand Tools", category="Trades Skill", related_skills=["trade_4"]),
    Skill(skill_id="trade_6", name="Welding", category="Trades Skill", related_skills=["trade_7"]),
    Skill(skill_id="trade_7", name="Metal Fabrication", category="Trades Skill", related_skills=["trade_6"]),
    Skill(skill_id="trade_8", name="Plumbing", category="Trades Skill", related_skills=["trade_9"]),
    Skill(skill_id="trade_9", name="Pipe Fitting", category="Trades Skill", related_skills=["trade_8"]),
    
    # Business Skills
    Skill(skill_id="biz_1", name="Project Management", category="Soft Skill", related_skills=["biz_2", "biz_3"]),
    Skill(skill_id="biz_2", name="Leadership", category="Soft Skill", related_skills=["biz_1", "biz_3"]),
    Skill(skill_id="biz_3", name="Communication", category="Soft Skill", related_skills=["biz_1", "biz_2"]),
    Skill(skill_id="biz_4", name="Sales", category="Business Skill", related_skills=["biz_3"]),
    Skill(skill_id="biz_5", name="Marketing", category="Business Skill", related_skills=["biz_4"]),
]

# Enhanced Career Database with Diverse Paths
ENHANCED_CAREERS = [
    # Entry-Level Technology Careers
    Career(
        career_id="tech_entry_1",
        title="Junior Software Developer",
        description="Entry-level position developing software applications using modern programming languages",
        required_skills=[
            RequiredSkill(skill_id="tech_1", name="Python", proficiency=SkillLevel.BEGINNER, is_mandatory=True, weight=1.0),
            RequiredSkill(skill_id="tech_2", name="JavaScript", proficiency=SkillLevel.BEGINNER, is_mandatory=False, weight=0.7)
        ],
        salary_range=SalaryRange(min=50000, max=70000, currency="USD"),
        demand=Demand.HIGH,
        education_requirements="Bachelor's degree in Computer Science or related field"
    ),
    
    # Mid-Level Technology Careers
    Career(
        career_id="tech_mid_1",
        title="Data Scientist",
        description="Analyzes complex data using Python and machine learning to extract business insights",
        required_skills=[
            RequiredSkill(skill_id="tech_1", name="Python", proficiency=SkillLevel.ADVANCED, is_mandatory=True, weight=1.0),
            RequiredSkill(skill_id="tech_3", name="Data Analysis", proficiency=SkillLevel.ADVANCED, is_mandatory=True, weight=1.0),
            RequiredSkill(skill_id="tech_5", name="Machine Learning", proficiency=SkillLevel.INTERMEDIATE, is_mandatory=True, weight=0.8)
        ],
        salary_range=SalaryRange(min=90000, max=140000, currency="USD"),
        demand=Demand.HIGH,
        education_requirements="Bachelor's or Master's degree in Data Science, Statistics, or related field"
    ),
    
    # Senior Technology Careers
    Career(
        career_id="tech_senior_1",
        title="Senior Software Engineering Manager",
        description="Lead software development teams and architect complex systems",
        required_skills=[
            RequiredSkill(skill_id="tech_1", name="Python", proficiency=SkillLevel.EXPERT, is_mandatory=True, weight=0.8),
            RequiredSkill(skill_id="biz_1", name="Project Management", proficiency=SkillLevel.ADVANCED, is_mandatory=True, weight=1.0),
            RequiredSkill(skill_id="biz_2", name="Leadership", proficiency=SkillLevel.ADVANCED, is_mandatory=True, weight=1.0)
        ],
        salary_range=SalaryRange(min=150000, max=220000, currency="USD"),
        demand=Demand.MEDIUM,
        education_requirements="Bachelor's degree + 8+ years experience"
    ),
    
    # Entry-Level Trades Careers
    Career(
        career_id="trade_entry_1",
        title="Apprentice Electrician",
        description="Learn electrical installation and maintenance under supervision of licensed electricians",
        required_skills=[
            RequiredSkill(skill_id="trade_3", name="Safety Protocols", proficiency=SkillLevel.BEGINNER, is_mandatory=True, weight=1.0),
            RequiredSkill(skill_id="trade_5", name="Hand Tools", proficiency=SkillLevel.BEGINNER, is_mandatory=True, weight=0.8)
        ],
        salary_range=SalaryRange(min=35000, max=45000, currency="USD"),
        demand=Demand.HIGH,
        education_requirements="High school diploma, trade school preferred"
    ),
    
    # Mid-Level Trades Careers
    Career(
        career_id="trade_mid_1",
        title="Licensed Electrician",
        description="Install, maintain, and repair electrical systems in residential and commercial buildings",
        required_skills=[
            RequiredSkill(skill_id="trade_1", name="Electrical Wiring", proficiency=SkillLevel.ADVANCED, is_mandatory=True, weight=1.0),
            RequiredSkill(skill_id="trade_2", name="Circuit Analysis", proficiency=SkillLevel.INTERMEDIATE, is_mandatory=True, weight=0.9),
            RequiredSkill(skill_id="trade_4", name="Blueprint Reading", proficiency=SkillLevel.INTERMEDIATE, is_mandatory=True, weight=0.8)
        ],
        salary_range=SalaryRange(min=55000, max=75000, currency="USD"),
        demand=Demand.HIGH,
        education_requirements="Trade school certificate + apprenticeship completion"
    ),
    
    # Senior Trades Careers
    Career(
        career_id="trade_senior_1",
        title="Master Electrician / Electrical Contractor",
        description="Supervise electrical projects, manage teams, and run electrical contracting business",
        required_skills=[
            RequiredSkill(skill_id="trade_1", name="Electrical Wiring", proficiency=SkillLevel.EXPERT, is_mandatory=True, weight=1.0),
            RequiredSkill(skill_id="biz_1", name="Project Management", proficiency=SkillLevel.ADVANCED, is_mandatory=True, weight=0.9),
            RequiredSkill(skill_id="biz_2", name="Leadership", proficiency=SkillLevel.ADVANCED, is_mandatory=True, weight=0.8)
        ],
        salary_range=SalaryRange(min=75000, max=120000, currency="USD"),
        demand=Demand.MEDIUM,
        education_requirements="Master electrician license + business experience"
    ),
    
    # Welding Careers
    Career(
        career_id="trade_weld_1",
        title="Certified Welder",
        description="Perform welding operations on various metals for construction and manufacturing",
        required_skills=[
            RequiredSkill(skill_id="trade_6", name="Welding", proficiency=SkillLevel.ADVANCED, is_mandatory=True, weight=1.0),
            RequiredSkill(skill_id="trade_7", name="Metal Fabrication", proficiency=SkillLevel.INTERMEDIATE, is_mandatory=True, weight=0.8),
            RequiredSkill(skill_id="trade_3", name="Safety Protocols", proficiency=SkillLevel.INTERMEDIATE, is_mandatory=True, weight=0.9)
        ],
        salary_range=SalaryRange(min=45000, max=65000, currency="USD"),
        demand=Demand.HIGH,
        education_requirements="Welding certification"
    ),
    
    # Business Entry Level
    Career(
        career_id="biz_entry_1",
        title="Sales Associate",
        description="Support sales team with customer interactions and basic sales activities",
        required_skills=[
            RequiredSkill(skill_id="biz_3", name="Communication", proficiency=SkillLevel.INTERMEDIATE, is_mandatory=True, weight=1.0),
            RequiredSkill(skill_id="biz_4", name="Sales", proficiency=SkillLevel.BEGINNER, is_mandatory=False, weight=0.7)
        ],
        salary_range=SalaryRange(min=35000, max=50000, currency="USD"),
        demand=Demand.MEDIUM,
        education_requirements="High school diploma"
    ),
    
    # Cross-Industry Career (Should be filtered out for trades professionals)
    Career(
        career_id="unrelated_1",
        title="Brain Surgeon",
        description="Perform complex neurosurgical procedures requiring extensive medical training",
        required_skills=[
            RequiredSkill(skill_id="med_1", name="Surgery", proficiency=SkillLevel.EXPERT, is_mandatory=True, weight=1.0),
            RequiredSkill(skill_id="med_2", name="Medical Knowledge", proficiency=SkillLevel.EXPERT, is_mandatory=True, weight=1.0)
        ],
        salary_range=SalaryRange(min=400000, max=800000, currency="USD"),
        demand=Demand.LOW,
        education_requirements="Medical degree + neurosurgery residency + fellowship"
    )
]

# Enhanced User Profiles for Different Types
STUDENT_PROFILE = UserProfile(
    user_id="student_001",
    personal_info=PersonalInfo(
        age=20,
        location="College Town, CA",
        salary_expectations=SalaryRange(min=40000, max=60000, currency="USD"),
        willing_to_relocate=True,
        preferred_work_style="hybrid"
    ),
    assessment_results=AssessmentResults(
        personality_traits=["Curious", "Analytical", "Collaborative"],
        work_values=["Learning", "Growth", "Innovation"],
        interests={
            "Technology": InterestLevel.HIGH,
            "Problem Solving": InterestLevel.VERY_HIGH,
            "Teamwork": InterestLevel.HIGH
        }
    ),
    professional_data=ProfessionalData(
        resume_skills=["Python", "JavaScript"],
        linkedin_skills=["Python"],
        experience=[
            Experience(
                title="Intern Software Developer",
                company="Local Startup",
                duration_years=0.5,
                description="Summer internship developing web applications",
                skills_used=["Python", "JavaScript"]
            )
        ],
        education="Bachelor's in Computer Science (in progress)",
        certifications=[]
    ),
    skills=[
        UserSkill(
            skill_id="tech_1",
            name="Python",
            level=SkillLevel.BEGINNER,
            years_experience=1.0,
            is_certified=False,
            last_used=datetime.utcnow() - timedelta(days=7)
        ),
        UserSkill(
            skill_id="tech_2",
            name="JavaScript",
            level=SkillLevel.BEGINNER,
            years_experience=0.5,
            is_certified=False,
            last_used=datetime.utcnow() - timedelta(days=14)
        )
    ],
    user_interests=["Software Development", "Web Development", "Learning New Technologies"]
)

TRADES_PROFESSIONAL_PROFILE = UserProfile(
    user_id="trades_001",
    personal_info=PersonalInfo(
        age=28,
        location="Industrial City, TX",
        salary_expectations=SalaryRange(min=50000, max=70000, currency="USD"),
        willing_to_relocate=False,
        preferred_work_style="on-site"
    ),
    assessment_results=AssessmentResults(
        personality_traits=["Practical", "Detail-Oriented", "Reliable"],
        work_values=["Craftsmanship", "Stability", "Hands-on Work"],
        interests={
            "Electrical Work": InterestLevel.VERY_HIGH,
            "Problem Solving": InterestLevel.HIGH,
            "Building Things": InterestLevel.VERY_HIGH
        }
    ),
    professional_data=ProfessionalData(
        resume_skills=["Electrical Wiring", "Circuit Analysis", "Safety Protocols"],
        linkedin_skills=["Electrical Wiring", "Hand Tools"],
        experience=[
            Experience(
                title="Electrician Apprentice",
                company="City Electric Co.",
                duration_years=3.0,
                description="Learned electrical installation and maintenance",
                skills_used=["Electrical Wiring", "Circuit Analysis", "Safety Protocols"]
            ),
            Experience(
                title="Maintenance Technician",
                company="Manufacturing Plant",
                duration_years=2.0,
                description="Maintained electrical systems in industrial setting",
                skills_used=["Electrical Wiring", "Hand Tools", "Safety Protocols"]
            )
        ],
        education="Trade School Certificate in Electrical Technology",
        certifications=["OSHA 10", "Electrical Safety Certification"]
    ),
    skills=[
        UserSkill(
            skill_id="trade_1",
            name="Electrical Wiring",
            level=SkillLevel.ADVANCED,
            years_experience=5.0,
            is_certified=True,
            last_used=datetime.utcnow() - timedelta(days=1)
        ),
        UserSkill(
            skill_id="trade_2",
            name="Circuit Analysis",
            level=SkillLevel.INTERMEDIATE,
            years_experience=3.0,
            is_certified=False,
            last_used=datetime.utcnow() - timedelta(days=2)
        ),
        UserSkill(
            skill_id="trade_3",
            name="Safety Protocols",
            level=SkillLevel.ADVANCED,
            years_experience=5.0,
            is_certified=True,
            last_used=datetime.utcnow() - timedelta(days=1)
        )
    ],
    user_interests=["Electrical Systems", "Industrial Automation", "Renewable Energy"]
)

SENIOR_PROFESSIONAL_PROFILE = UserProfile(
    user_id="senior_001",
    personal_info=PersonalInfo(
        age=42,
        location="Silicon Valley, CA",
        salary_expectations=SalaryRange(min=140000, max=200000, currency="USD"),
        willing_to_relocate=False,
        preferred_work_style="hybrid"
    ),
    assessment_results=AssessmentResults(
        personality_traits=["Strategic", "Leadership-Oriented", "Results-Driven"],
        work_values=["Impact", "Leadership", "Innovation"],
        interests={
            "Technology Strategy": InterestLevel.VERY_HIGH,
            "Team Leadership": InterestLevel.VERY_HIGH,
            "Business Growth": InterestLevel.HIGH
        }
    ),
    professional_data=ProfessionalData(
        resume_skills=["Python", "Project Management", "Leadership", "Data Analysis"],
        linkedin_skills=["Python", "Machine Learning", "Team Leadership"],
        experience=[
            Experience(
                title="Senior Software Engineer",
                company="Tech Giant Corp",
                duration_years=6.0,
                description="Led development of large-scale distributed systems",
                skills_used=["Python", "Data Analysis", "Project Management"]
            ),
            Experience(
                title="Engineering Manager",
                company="Startup Inc",
                duration_years=4.0,
                description="Managed engineering team of 12 developers",
                skills_used=["Leadership", "Project Management", "Python"]
            )
        ],
        education="Master's in Computer Science",
        certifications=["PMP", "AWS Solutions Architect"]
    ),
    skills=[
        UserSkill(
            skill_id="tech_1",
            name="Python",
            level=SkillLevel.EXPERT,
            years_experience=10.0,
            is_certified=False,
            last_used=datetime.utcnow() - timedelta(days=3)
        ),
        UserSkill(
            skill_id="biz_1",
            name="Project Management",
            level=SkillLevel.EXPERT,
            years_experience=8.0,
            is_certified=True,
            last_used=datetime.utcnow() - timedelta(days=1)
        ),
        UserSkill(
            skill_id="biz_2",
            name="Leadership",
            level=SkillLevel.EXPERT,
            years_experience=6.0,
            is_certified=False,
            last_used=datetime.utcnow() - timedelta(days=1)
        )
    ],
    user_interests=["Engineering Leadership", "Technology Strategy", "Mentoring"]
)