"""
Mock data for testing the recommendation engine.

This module provides sample data for users, careers, and skills to test
the recommendation engine functionality.
"""

from datetime import datetime, timedelta
from typing import List

from pydantic import BaseModel

# To avoid the Beanie/DB requirement in tests, we'll use Pydantic BaseModels
# that have the same shape as the Beanie Documents.
class Skill(BaseModel):
    skill_id: str
    name: str
    category: str
    related_skills: List[str]

class SalaryRange(BaseModel):
    min: int
    max: int
    currency: str = "USD"

class Career(BaseModel):
    career_id: str
    title: str
    description: str
    required_skills: List['RequiredSkill'] # Simplified for testing
    salary_range: SalaryRange
    demand: str
    related_careers: List[str]
    growth_potential: str
    work_environment: str
    education_requirements: str
    career_field: str = "other" # Add the missing field

class Experience(BaseModel):
    title: str
    company: str
    duration_years: float
    description: str
    skills_used: List[str]

class ProfessionalData(BaseModel):
    resume_skills: List[str]
    linkedin_skills: List[str]
    experience: List[Experience]
    education: str
    certifications: List[str]

class UserSkill(BaseModel):
    skill_id: str
    name: str
    level: str
    years_experience: float
    is_certified: bool = False
    last_used: datetime = None

class UserProfile(BaseModel):
    user_id: str
    personal_info: 'PersonalInfo'
    assessment_results: 'AssessmentResults'
    professional_data: ProfessionalData
    skills: List[UserSkill]
    user_interests: List[str]
    # Add fields from the original UserProfileModel that are used in the engine
    technicalSkills: List[str] = []
    softSkills: List[str] = []
    experience: float = 0.0
    industries: List[str] = []
    careerGoals: List[str] = []
    interests: List[str] = []
    workingWithData: int = 3
    workingWithPeople: int = 3
    creativeTasks: int = 3
    problemSolving: int = 3
    leadership: int = 3
    physicalHandsOnWork: int = 3
    mechanicalAptitude: int = 3
    salaryExpectations: dict = {}
    educationLevel: str = ""
    currentRole: str = ""
    location: str = ""
    resumeText: str = ""


# Enums as plain strings for simplicity in mock data
class SkillLevel:
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"
    EXPERT = "expert"

class InterestLevel:
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    VERY_HIGH = "very_high"

class Demand:
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    VERY_HIGH = "very_high"

# Re-define other necessary classes if they are not BaseModels
class PersonalInfo(BaseModel):
    age: int
    location: str
    salary_expectations: SalaryRange
    willing_to_relocate: bool
    preferred_work_style: str

class AssessmentResults(BaseModel):
    personality_traits: List[str]
    work_values: List[str]
    interests: dict

class RequiredSkill(BaseModel):
    skill_id: str
    name: str
    proficiency: str
    is_mandatory: bool = True
    weight: float = 1.0


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
    """Create a list of mock careers for testing using Pydantic models."""
    return [
        Career(
            career_id="career_1",
            title="Machine Learning Engineer",
            description="Designs and develops machine learning and deep learning systems to solve complex problems.",
            required_skills=[
                RequiredSkill(skill_id="skill_1", name="Python", proficiency="advanced"),
                RequiredSkill(skill_id="skill_2", name="Machine Learning", proficiency="advanced"),
                RequiredSkill(skill_id="skill_4", name="TensorFlow", proficiency="intermediate"),
            ],
            salary_range=SalaryRange(min=100000, max=160000, currency="USD"),
            demand="high",
            related_careers=["career_2", "career_3"],
            growth_potential="Excellent growth potential",
            work_environment="Tech companies",
            education_requirements="Bachelor's in Computer Science",
            career_field="technology_it"
        ),
        Career(
            career_id="career_2",
            title="Data Scientist",
            description="Analyzes complex data to extract insights.",
            required_skills=[
                RequiredSkill(skill_id="skill_1", name="Python", proficiency="advanced"),
                RequiredSkill(skill_id="skill_3", name="Data Analysis", proficiency="advanced"),
                RequiredSkill(skill_id="skill_5", name="SQL", proficiency="advanced"),
            ],
            salary_range=SalaryRange(min=90000, max=140000, currency="USD"),
            demand="high",
            related_careers=["career_1", "career_3"],
            growth_potential="Strong growth",
            work_environment="Various industries",
            education_requirements="Bachelor's in Statistics"
        ),
        Career(
            career_id="career_3",
            title="Data Analyst",
            description="Collects, processes, and performs statistical analyses.",
            required_skills=[
                RequiredSkill(skill_id="skill_3", name="Data Analysis", proficiency="advanced"),
                RequiredSkill(skill_id="skill_5", name="SQL", proficiency="advanced"),
                RequiredSkill(skill_id="skill_7", name="Data Visualization", proficiency="intermediate"),
            ],
            salary_range=SalaryRange(min=60000, max=90000, currency="USD"),
            demand="medium",
            related_careers=["career_1", "career_2"],
            growth_potential="Good growth potential",
            work_environment="Corporate environments",
            education_requirements="Bachelor's in Business"
        ),
        Career(
            career_id="career_4",
            title="Full Stack Developer",
            description="Develops both front-end and back-end components.",
            required_skills=[
                RequiredSkill(skill_id="skill_8", name="JavaScript", proficiency="advanced"),
                RequiredSkill(skill_id="skill_9", name="React", proficiency="intermediate"),
                RequiredSkill(skill_id="skill_10", name="Node.js", proficiency="intermediate"),
            ],
            salary_range=SalaryRange(min=70000, max=120000, currency="USD"),
            demand="high",
            related_careers=["career_5", "career_6"],
            growth_potential="Excellent growth",
            work_environment="Tech companies",
            education_requirements="Bachelor's in Computer Science"
        ),
        Career(
            career_id="career_5",
            title="DevOps Engineer",
            description="Manages infrastructure and deployment pipelines.",
            required_skills=[
                RequiredSkill(skill_id="skill_14", name="Cloud Computing", proficiency="advanced"),
                RequiredSkill(skill_id="skill_15", name="AWS", proficiency="intermediate"),
                RequiredSkill(skill_id="skill_16", name="Docker", proficiency="intermediate"),
            ],
            salary_range=SalaryRange(min=85000, max=130000, currency="USD"),
            demand="high",
            related_careers=["career_4", "career_6"],
            growth_potential="Very strong growth",
            work_environment="Tech companies",
            education_requirements="Bachelor's in Computer Science"
        ),
        Career(
            career_id="career_6",
            title="Technical Project Manager",
            description="Manages technical projects and coordinates teams.",
            required_skills=[
                RequiredSkill(skill_id="skill_11", name="Project Management", proficiency="advanced"),
                RequiredSkill(skill_id="skill_12", name="Leadership", proficiency="advanced"),
                RequiredSkill(skill_id="skill_13", name="Communication", proficiency="advanced"),
            ],
            salary_range=SalaryRange(min=80000, max=125000, currency="USD"),
            demand="medium",
            related_careers=["career_4", "career_5"],
            growth_potential="Good growth",
            work_environment="Tech companies",
            education_requirements="Bachelor's in Engineering"
        )
    ]


def create_mock_user_profile() -> UserProfile:
    """Create a mock user profile for testing using Pydantic models."""
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
                "Technology": "very_high",
                "Data Analysis": "high",
                "Problem Solving": "high",
                "Machine Learning": "medium",
                "Leadership": "low"
            }
        ),
        professional_data={
            "resume_skills": ["Python", "SQL", "Data Analysis", "Machine Learning"],
            "linkedin_skills": ["Python", "Data Analysis", "Statistical Analysis"],
            "experience": [
                {
                    "title": "Data Analyst",
                    "company": "Tech Corp",
                    "duration_years": 2.0,
                    "description": "Analyzed customer data to identify trends and improve business decisions",
                    "skills_used": ["Python", "SQL", "Data Analysis", "Data Visualization"]
                },
                {
                    "title": "Junior Developer",
                    "company": "StartupXYZ",
                    "duration_years": 1.5,
                    "description": "Developed web applications using Python and JavaScript",
                    "skills_used": ["Python", "JavaScript", "SQL"]
                }
            ],
            "education": "Bachelor's in Computer Science",
            "certifications": ["AWS Cloud Practitioner"]
        },
        skills=[
            UserSkill(skill_id="skill_1", name="Python", level="advanced", years_experience=3.5, last_used=datetime.utcnow() - timedelta(days=1)),
            UserSkill(skill_id="skill_3", name="Data Analysis", level="advanced", years_experience=2.5, last_used=datetime.utcnow() - timedelta(days=2)),
            UserSkill(skill_id="skill_5", name="SQL", level="intermediate", years_experience=3.0, last_used=datetime.utcnow() - timedelta(days=5)),
            UserSkill(skill_id="skill_2", name="Machine Learning", level="intermediate", years_experience=1.0, last_used=datetime.utcnow() - timedelta(days=30)),
            UserSkill(skill_id="skill_8", name="JavaScript", level="intermediate", years_experience=1.5, last_used=datetime.utcnow() - timedelta(days=60)),
            UserSkill(skill_id="skill_15", name="AWS", level="beginner", years_experience=0.5, is_certified=True, last_used=datetime.utcnow() - timedelta(days=90))
        ],
        user_interests=["AI Ethics", "Sustainable Technology", "Data Privacy"],
        # Add the flat fields required by the engine
        technicalSkills=["Python", "SQL", "Data Analysis", "Machine Learning", "JavaScript", "AWS"],
        softSkills=["Communication", "Teamwork"], # Example soft skills
        experience=3.5,
        industries=["Technology", "Finance"],
        careerGoals=["Become a Senior Machine Learning Engineer"],
        interests=["AI Ethics", "Sustainable Technology", "Data Privacy"],
        salaryExpectations={"min": 80000, "max": 120000, "currency": "USD"},
        educationLevel="Bachelor's in Computer Science",
        currentRole="Data Analyst",
        location="San Francisco, CA",
        resumeText="A data analyst with 3.5 years of experience..."
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
# MOCK_SKILLS = create_mock_skills()
# MOCK_CAREERS = create_mock_careers()
# MOCK_USER_PROFILE = create_mock_user_profile()
# ALTERNATIVE_USER_PROFILE = create_alternative_user_profile()