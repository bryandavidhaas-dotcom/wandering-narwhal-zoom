"""
Mock data for testing the recommendation engine.

This module provides sample data for users, careers, and skills to test
the recommendation engine functionality.
"""

from datetime import datetime, timedelta
from typing import List
from ..models import (
    UserProfileModel as UserProfile, CareerModel as Career, SkillModel as Skill, UserSkill, RequiredSkill, SalaryRange,
    PersonalInfo, AssessmentResults, ProfessionalData, Experience,
    SkillLevel, InterestLevel, Demand
)


def create_mock_skills() -> List[Skill]:
    """Create a list of mock skills for testing."""
    return [
        Skill(
            skill_id="skill_1",
            name="Python",
            category="Programming Language",
            related_skills=["skill_2", "skill_3", "skill_15"]
        ),
        Skill(
            skill_id="skill_2",
            name="Machine Learning",
            category="Technical Skill",
            related_skills=["skill_1", "skill_3", "skill_4"]
        ),
        Skill(
            skill_id="skill_3",
            name="Data Analysis",
            category="Technical Skill",
            related_skills=["skill_1", "skill_2", "skill_5"]
        ),
        Skill(
            skill_id="skill_4",
            name="TensorFlow",
            category="Framework",
            related_skills=["skill_2", "skill_6"]
        ),
        Skill(
            skill_id="skill_5",
            name="SQL",
            category="Database",
            related_skills=["skill_3", "skill_7"]
        ),
        Skill(
            skill_id="skill_6",
            name="Deep Learning",
            category="Technical Skill",
            related_skills=["skill_2", "skill_4"]
        ),
        Skill(
            skill_id="skill_7",
            name="Data Visualization",
            category="Technical Skill",
            related_skills=["skill_3", "skill_5"]
        ),
        Skill(
            skill_id="skill_8",
            name="JavaScript",
            category="Programming Language",
            related_skills=["skill_9", "skill_10"]
        ),
        Skill(
            skill_id="skill_9",
            name="React",
            category="Framework",
            related_skills=["skill_8", "skill_10"]
        ),
        Skill(
            skill_id="skill_10",
            name="Node.js",
            category="Runtime",
            related_skills=["skill_8", "skill_9"]
        ),
        Skill(
            skill_id="skill_11",
            name="Project Management",
            category="Soft Skill",
            related_skills=["skill_12", "skill_13"]
        ),
        Skill(
            skill_id="skill_12",
            name="Leadership",
            category="Soft Skill",
            related_skills=["skill_11", "skill_13"]
        ),
        Skill(
            skill_id="skill_13",
            name="Communication",
            category="Soft Skill",
            related_skills=["skill_11", "skill_12"]
        ),
        Skill(
            skill_id="skill_14",
            name="Cloud Computing",
            category="Technical Skill",
            related_skills=["skill_15", "skill_16"]
        ),
        Skill(
            skill_id="skill_15",
            name="AWS",
            category="Cloud Platform",
            related_skills=["skill_14", "skill_16"]
        ),
        Skill(
            skill_id="skill_16",
            name="Docker",
            category="DevOps Tool",
            related_skills=["skill_14", "skill_15"]
        )
    ]


def create_mock_careers() -> List[Career]:
    """Create a list of mock careers for testing."""
    return [
        Career(
            career_id="career_1",
            title="Machine Learning Engineer",
            description="Designs and develops machine learning and deep learning systems to solve complex problems.",
            required_skills=[
                RequiredSkill(skill_id="skill_1", name="Python", proficiency=SkillLevel.ADVANCED, is_mandatory=True, weight=1.0),
                RequiredSkill(skill_id="skill_2", name="Machine Learning", proficiency=SkillLevel.ADVANCED, is_mandatory=True, weight=1.0),
                RequiredSkill(skill_id="skill_4", name="TensorFlow", proficiency=SkillLevel.INTERMEDIATE, is_mandatory=True, weight=0.8),
                RequiredSkill(skill_id="skill_6", name="Deep Learning", proficiency=SkillLevel.INTERMEDIATE, is_mandatory=False, weight=0.7),
                RequiredSkill(skill_id="skill_5", name="SQL", proficiency=SkillLevel.INTERMEDIATE, is_mandatory=False, weight=0.6)
            ],
            salary_range=SalaryRange(min=100000, max=160000, currency="USD"),
            demand=Demand.HIGH,
            related_careers=["career_2", "career_3"],
            growth_potential="Excellent growth potential with increasing demand for AI solutions",
            work_environment="Tech companies, startups, research institutions",
            education_requirements="Bachelor's in Computer Science, Mathematics, or related field"
        ),
        Career(
            career_id="career_2",
            title="Data Scientist",
            description="Analyzes complex data to extract insights and build predictive models for business decisions.",
            required_skills=[
                RequiredSkill(skill_id="skill_1", name="Python", proficiency=SkillLevel.ADVANCED, is_mandatory=True, weight=1.0),
                RequiredSkill(skill_id="skill_3", name="Data Analysis", proficiency=SkillLevel.ADVANCED, is_mandatory=True, weight=1.0),
                RequiredSkill(skill_id="skill_2", name="Machine Learning", proficiency=SkillLevel.INTERMEDIATE, is_mandatory=True, weight=0.9),
                RequiredSkill(skill_id="skill_5", name="SQL", proficiency=SkillLevel.ADVANCED, is_mandatory=True, weight=0.8),
                RequiredSkill(skill_id="skill_7", name="Data Visualization", proficiency=SkillLevel.INTERMEDIATE, is_mandatory=False, weight=0.7)
            ],
            salary_range=SalaryRange(min=90000, max=140000, currency="USD"),
            demand=Demand.HIGH,
            related_careers=["career_1", "career_3"],
            growth_potential="Strong growth with increasing data-driven decision making",
            work_environment="Various industries including tech, finance, healthcare",
            education_requirements="Bachelor's in Statistics, Mathematics, Computer Science, or related field"
        ),
        Career(
            career_id="career_3",
            title="Data Analyst",
            description="Collects, processes, and performs statistical analyses on large datasets to support business decisions.",
            required_skills=[
                RequiredSkill(skill_id="skill_3", name="Data Analysis", proficiency=SkillLevel.ADVANCED, is_mandatory=True, weight=1.0),
                RequiredSkill(skill_id="skill_5", name="SQL", proficiency=SkillLevel.ADVANCED, is_mandatory=True, weight=1.0),
                RequiredSkill(skill_id="skill_7", name="Data Visualization", proficiency=SkillLevel.INTERMEDIATE, is_mandatory=True, weight=0.8),
                RequiredSkill(skill_id="skill_1", name="Python", proficiency=SkillLevel.INTERMEDIATE, is_mandatory=False, weight=0.7),
                RequiredSkill(skill_id="skill_2", name="Machine Learning", proficiency=SkillLevel.BEGINNER, is_mandatory=False, weight=0.5)
            ],
            salary_range=SalaryRange(min=60000, max=90000, currency="USD"),
            demand=Demand.MEDIUM,
            related_careers=["career_1", "career_2"],
            growth_potential="Good growth potential with digital transformation trends",
            work_environment="Corporate environments across various industries",
            education_requirements="Bachelor's in Business, Statistics, Mathematics, or related field"
        ),
        Career(
            career_id="career_4",
            title="Full Stack Developer",
            description="Develops both front-end and back-end components of web applications.",
            required_skills=[
                RequiredSkill(skill_id="skill_8", name="JavaScript", proficiency=SkillLevel.ADVANCED, is_mandatory=True, weight=1.0),
                RequiredSkill(skill_id="skill_9", name="React", proficiency=SkillLevel.INTERMEDIATE, is_mandatory=True, weight=0.9),
                RequiredSkill(skill_id="skill_10", name="Node.js", proficiency=SkillLevel.INTERMEDIATE, is_mandatory=True, weight=0.8),
                RequiredSkill(skill_id="skill_5", name="SQL", proficiency=SkillLevel.INTERMEDIATE, is_mandatory=False, weight=0.6),
                RequiredSkill(skill_id="skill_14", name="Cloud Computing", proficiency=SkillLevel.BEGINNER, is_mandatory=False, weight=0.5)
            ],
            salary_range=SalaryRange(min=70000, max=120000, currency="USD"),
            demand=Demand.HIGH,
            related_careers=["career_5", "career_6"],
            growth_potential="Excellent growth with increasing web application demand",
            work_environment="Tech companies, startups, digital agencies",
            education_requirements="Bachelor's in Computer Science or equivalent experience"
        ),
        Career(
            career_id="career_5",
            title="DevOps Engineer",
            description="Manages infrastructure, deployment pipelines, and ensures reliable software delivery.",
            required_skills=[
                RequiredSkill(skill_id="skill_14", name="Cloud Computing", proficiency=SkillLevel.ADVANCED, is_mandatory=True, weight=1.0),
                RequiredSkill(skill_id="skill_15", name="AWS", proficiency=SkillLevel.INTERMEDIATE, is_mandatory=True, weight=0.9),
                RequiredSkill(skill_id="skill_16", name="Docker", proficiency=SkillLevel.INTERMEDIATE, is_mandatory=True, weight=0.8),
                RequiredSkill(skill_id="skill_1", name="Python", proficiency=SkillLevel.INTERMEDIATE, is_mandatory=False, weight=0.7),
                RequiredSkill(skill_id="skill_8", name="JavaScript", proficiency=SkillLevel.BEGINNER, is_mandatory=False, weight=0.5)
            ],
            salary_range=SalaryRange(min=85000, max=130000, currency="USD"),
            demand=Demand.HIGH,
            related_careers=["career_4", "career_6"],
            growth_potential="Very strong growth with cloud adoption trends",
            work_environment="Tech companies, enterprises adopting cloud technologies",
            education_requirements="Bachelor's in Computer Science, Engineering, or equivalent experience"
        ),
        Career(
            career_id="career_6",
            title="Technical Project Manager",
            description="Manages technical projects, coordinates teams, and ensures successful delivery of software products.",
            required_skills=[
                RequiredSkill(skill_id="skill_11", name="Project Management", proficiency=SkillLevel.ADVANCED, is_mandatory=True, weight=1.0),
                RequiredSkill(skill_id="skill_12", name="Leadership", proficiency=SkillLevel.ADVANCED, is_mandatory=True, weight=1.0),
                RequiredSkill(skill_id="skill_13", name="Communication", proficiency=SkillLevel.ADVANCED, is_mandatory=True, weight=0.9),
                RequiredSkill(skill_id="skill_8", name="JavaScript", proficiency=SkillLevel.INTERMEDIATE, is_mandatory=False, weight=0.6),
                RequiredSkill(skill_id="skill_1", name="Python", proficiency=SkillLevel.BEGINNER, is_mandatory=False, weight=0.5)
            ],
            salary_range=SalaryRange(min=80000, max=125000, currency="USD"),
            demand=Demand.MEDIUM,
            related_careers=["career_4", "career_5"],
            growth_potential="Good growth with increasing complexity of technical projects",
            work_environment="Tech companies, consulting firms, enterprise organizations",
            education_requirements="Bachelor's in Engineering, Computer Science, or Business with technical background"
        )
    ]


def create_mock_user_profile() -> UserProfile:
    """Create a mock user profile for testing."""
    return UserProfile(
        user_id="user_123",
        personal_info=PersonalInfo(
            age=28,
            location="San Francisco, CA",
            salary_expectations=SalaryRange(min=80000, max=120000, currency="USD"),
            willing_to_relocate=False,
            preferred_work_style="hybrid"
        ),
        assessment_results=AssessmentResults(
            personality_traits=["Analytical", "Detail-Oriented", "Introverted"],
            work_values=["Autonomy", "Innovation", "Work-Life Balance"],
            interests={
                "Technology": InterestLevel.VERY_HIGH,
                "Data Analysis": InterestLevel.HIGH,
                "Problem Solving": InterestLevel.HIGH,
                "Machine Learning": InterestLevel.MEDIUM,
                "Leadership": InterestLevel.LOW
            }
        ),
        professional_data=ProfessionalData(
            resume_skills=["Python", "SQL", "Data Analysis", "Machine Learning"],
            linkedin_skills=["Python", "Data Analysis", "Statistical Analysis"],
            experience=[
                Experience(
                    title="Data Analyst",
                    company="Tech Corp",
                    duration_years=2.0,
                    description="Analyzed customer data to identify trends and improve business decisions",
                    skills_used=["Python", "SQL", "Data Analysis", "Data Visualization"]
                ),
                Experience(
                    title="Junior Developer",
                    company="StartupXYZ",
                    duration_years=1.5,
                    description="Developed web applications using Python and JavaScript",
                    skills_used=["Python", "JavaScript", "SQL"]
                )
            ],
            education="Bachelor's in Computer Science",
            certifications=["AWS Cloud Practitioner"]
        ),
        skills=[
            UserSkill(
                skill_id="skill_1",
                name="Python",
                level=SkillLevel.ADVANCED,
                years_experience=3.5,
                is_certified=False,
                last_used=datetime.utcnow() - timedelta(days=1)
            ),
            UserSkill(
                skill_id="skill_3",
                name="Data Analysis",
                level=SkillLevel.ADVANCED,
                years_experience=2.5,
                is_certified=False,
                last_used=datetime.utcnow() - timedelta(days=2)
            ),
            UserSkill(
                skill_id="skill_5",
                name="SQL",
                level=SkillLevel.INTERMEDIATE,
                years_experience=3.0,
                is_certified=False,
                last_used=datetime.utcnow() - timedelta(days=5)
            ),
            UserSkill(
                skill_id="skill_2",
                name="Machine Learning",
                level=SkillLevel.INTERMEDIATE,
                years_experience=1.0,
                is_certified=False,
                last_used=datetime.utcnow() - timedelta(days=30)
            ),
            UserSkill(
                skill_id="skill_8",
                name="JavaScript",
                level=SkillLevel.INTERMEDIATE,
                years_experience=1.5,
                is_certified=False,
                last_used=datetime.utcnow() - timedelta(days=60)
            ),
            UserSkill(
                skill_id="skill_15",
                name="AWS",
                level=SkillLevel.BEGINNER,
                years_experience=0.5,
                is_certified=True,
                last_used=datetime.utcnow() - timedelta(days=90)
            )
        ],
        user_interests=["AI Ethics", "Sustainable Technology", "Data Privacy"]
    )


def create_alternative_user_profile() -> UserProfile:
    """Create an alternative mock user profile for testing different scenarios."""
    return UserProfile(
        user_id="user_456",
        personal_info=PersonalInfo(
            age=32,
            location="Austin, TX",
            salary_expectations=SalaryRange(min=90000, max=140000, currency="USD"),
            willing_to_relocate=True,
            preferred_work_style="remote"
        ),
        assessment_results=AssessmentResults(
            personality_traits=["Extroverted", "Creative", "Leadership-Oriented"],
            work_values=["Impact", "Growth", "Collaboration"],
            interests={
                "Leadership": InterestLevel.VERY_HIGH,
                "Technology": InterestLevel.HIGH,
                "Project Management": InterestLevel.HIGH,
                "Innovation": InterestLevel.MEDIUM,
                "Data Analysis": InterestLevel.LOW
            }
        ),
        professional_data=ProfessionalData(
            resume_skills=["JavaScript", "React", "Node.js", "Project Management", "Leadership"],
            linkedin_skills=["JavaScript", "React", "Team Leadership", "Agile"],
            experience=[
                Experience(
                    title="Senior Full Stack Developer",
                    company="WebTech Solutions",
                    duration_years=4.0,
                    description="Led development team and built scalable web applications",
                    skills_used=["JavaScript", "React", "Node.js", "Leadership", "Project Management"]
                ),
                Experience(
                    title="Frontend Developer",
                    company="Digital Agency",
                    duration_years=2.5,
                    description="Developed responsive web interfaces for various clients",
                    skills_used=["JavaScript", "React", "CSS", "HTML"]
                )
            ],
            education="Bachelor's in Information Systems",
            certifications=["PMP", "Scrum Master"]
        ),
        skills=[
            UserSkill(
                skill_id="skill_8",
                name="JavaScript",
                level=SkillLevel.EXPERT,
                years_experience=6.5,
                is_certified=False,
                last_used=datetime.utcnow() - timedelta(days=1)
            ),
            UserSkill(
                skill_id="skill_9",
                name="React",
                level=SkillLevel.ADVANCED,
                years_experience=4.0,
                is_certified=False,
                last_used=datetime.utcnow() - timedelta(days=1)
            ),
            UserSkill(
                skill_id="skill_10",
                name="Node.js",
                level=SkillLevel.ADVANCED,
                years_experience=3.5,
                is_certified=False,
                last_used=datetime.utcnow() - timedelta(days=3)
            ),
            UserSkill(
                skill_id="skill_11",
                name="Project Management",
                level=SkillLevel.ADVANCED,
                years_experience=3.0,
                is_certified=True,
                last_used=datetime.utcnow() - timedelta(days=1)
            ),
            UserSkill(
                skill_id="skill_12",
                name="Leadership",
                level=SkillLevel.ADVANCED,
                years_experience=4.0,
                is_certified=True,
                last_used=datetime.utcnow() - timedelta(days=1)
            ),
            UserSkill(
                skill_id="skill_13",
                name="Communication",
                level=SkillLevel.EXPERT,
                years_experience=6.0,
                is_certified=False,
                last_used=datetime.utcnow() - timedelta(days=1)
            )
        ],
        user_interests=["Team Building", "Innovation", "Startup Culture"]
    )


# Global instances for easy access
MOCK_SKILLS = create_mock_skills()
MOCK_CAREERS = create_mock_careers()
MOCK_USER_PROFILE = create_mock_user_profile()
ALTERNATIVE_USER_PROFILE = create_alternative_user_profile()