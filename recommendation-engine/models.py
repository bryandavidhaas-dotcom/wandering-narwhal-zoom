"""
Data models for the recommendation engine.

This module defines the core data structures used throughout the recommendation
engine, including UserProfile, Career, and Skill models with validation.
"""

from typing import List, Optional, Dict, Any
from enum import Enum
from pydantic import BaseModel, Field, validator
from datetime import datetime


class ExperienceLevel(str, Enum):
    """Experience level enumeration."""
    ENTRY = "entry"
    JUNIOR = "junior"
    MID = "mid"
    SENIOR = "senior"
    EXPERT = "expert"


class SkillLevel(str, Enum):
    """Skill proficiency level enumeration."""
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"
    EXPERT = "expert"


class InterestLevel(str, Enum):
    """Interest level enumeration."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    VERY_HIGH = "very_high"


class Demand(str, Enum):
    """Career demand level enumeration."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    VERY_HIGH = "very_high"


class Skill(BaseModel):
    """
    Represents a skill with proficiency level and optional metadata.
    
    Attributes:
        skill_id: Unique identifier for the skill
        name: The skill name (e.g., "Python", "Project Management")
        category: Skill category (e.g., "Programming Language", "Soft Skill")
        related_skills: List of related skill IDs
    """
    skill_id: str = Field(..., min_length=1)
    name: str = Field(..., min_length=1, max_length=100)
    category: str = Field(..., max_length=100)
    related_skills: List[str] = Field(default_factory=list)
    
    @validator('name')
    def validate_name(cls, v):
        return v.strip().title()


class UserSkill(BaseModel):
    """
    Represents a user's skill with proficiency level and experience.
    
    Attributes:
        skill_id: Reference to the skill
        name: The skill name
        level: The user's proficiency level
        years_experience: Years of experience with this skill
        is_certified: Whether the user has certification in this skill
        last_used: When the skill was last used
    """
    skill_id: str = Field(..., min_length=1)
    name: str = Field(..., min_length=1, max_length=100)
    level: SkillLevel
    years_experience: Optional[float] = Field(None, ge=0, le=50)
    is_certified: bool = False
    last_used: Optional[datetime] = None


class RequiredSkill(BaseModel):
    """
    Represents a skill required for a career with proficiency level.
    
    Attributes:
        skill_id: Reference to the skill
        name: The skill name
        proficiency: Required proficiency level
        is_mandatory: Whether this skill is mandatory or preferred
        weight: Importance weight for scoring (0.0 to 1.0)
    """
    skill_id: str = Field(..., min_length=1)
    name: str = Field(..., min_length=1, max_length=100)
    proficiency: SkillLevel
    is_mandatory: bool = True
    weight: float = Field(1.0, ge=0.0, le=1.0)


class SalaryRange(BaseModel):
    """
    Represents a salary range with currency.
    
    Attributes:
        min: Minimum salary
        max: Maximum salary
        currency: Currency code (e.g., "USD", "EUR")
    """
    min: int = Field(..., ge=0)
    max: int = Field(..., ge=0)
    currency: str = Field("USD", min_length=3, max_length=3)
    
    @validator('max')
    def validate_max_greater_than_min(cls, v, values):
        if 'min' in values and v < values['min']:
            raise ValueError('max salary must be greater than or equal to min salary')
        return v


class PersonalInfo(BaseModel):
    """
    User's personal information and preferences.
    
    Attributes:
        age: User's age
        location: User's location
        salary_expectations: Expected salary range
        willing_to_relocate: Whether user is willing to relocate
        preferred_work_style: Remote, hybrid, or on-site preference
    """
    age: Optional[int] = Field(None, ge=16, le=100)
    location: Optional[str] = Field(None, max_length=200)
    salary_expectations: Optional[SalaryRange] = None
    willing_to_relocate: bool = False
    preferred_work_style: Optional[str] = Field(None, pattern="^(remote|hybrid|on-site)$")


class AssessmentResults(BaseModel):
    """
    Results from user assessments.
    
    Attributes:
        personality_traits: List of personality traits
        work_values: List of work values
        interests: List of interests with levels
    """
    personality_traits: List[str] = Field(default_factory=list)
    work_values: List[str] = Field(default_factory=list)
    interests: Dict[str, InterestLevel] = Field(default_factory=dict)


class Experience(BaseModel):
    """
    Represents work experience.
    
    Attributes:
        title: Job title
        company: Company name
        duration_years: Duration in years
        description: Job description
        skills_used: Skills used in this role
    """
    title: str = Field(..., min_length=1, max_length=200)
    company: str = Field(..., min_length=1, max_length=200)
    duration_years: float = Field(..., ge=0, le=50)
    description: Optional[str] = Field(None, max_length=1000)
    skills_used: List[str] = Field(default_factory=list)


class ProfessionalData(BaseModel):
    """
    User's professional data from resume and LinkedIn.
    
    Attributes:
        resume_skills: Skills extracted from resume
        linkedin_skills: Skills from LinkedIn profile
        experience: List of work experiences
        education: Education background
        certifications: Professional certifications
    """
    resume_skills: List[str] = Field(default_factory=list)
    linkedin_skills: List[str] = Field(default_factory=list)
    experience: List[Experience] = Field(default_factory=list)
    education: Optional[str] = Field(None, max_length=500)
    certifications: List[str] = Field(default_factory=list)


class UserProfile(BaseModel):
    """
    Comprehensive user profile for career recommendations.
    
    Attributes:
        user_id: Unique identifier for the user
        personal_info: Personal information and preferences
        assessment_results: Results from personality and interest assessments
        professional_data: Professional background data
        skills: User's skills with proficiency levels
        user_interests: Additional interests specified by user
        created_at: Profile creation timestamp
        updated_at: Last update timestamp
    """
    user_id: str = Field(..., min_length=1)
    personal_info: PersonalInfo = Field(default_factory=PersonalInfo)
    assessment_results: AssessmentResults = Field(default_factory=AssessmentResults)
    professional_data: ProfessionalData = Field(default_factory=ProfessionalData)
    skills: List[UserSkill] = Field(default_factory=list)
    user_interests: List[str] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    def get_skill_by_name(self, skill_name: str) -> Optional[UserSkill]:
        """Get a user skill by name."""
        for skill in self.skills:
            if skill.name.lower() == skill_name.lower():
                return skill
        return None
    
    def has_skill(self, skill_name: str, min_level: SkillLevel = SkillLevel.BEGINNER) -> bool:
        """Check if user has a skill at minimum level."""
        skill = self.get_skill_by_name(skill_name)
        if not skill:
            return False
        
        level_order = [SkillLevel.BEGINNER, SkillLevel.INTERMEDIATE, SkillLevel.ADVANCED, SkillLevel.EXPERT]
        return level_order.index(skill.level) >= level_order.index(min_level)


class Career(BaseModel):
    """
    Represents a career path with requirements and attributes.
    
    Attributes:
        career_id: Unique identifier for the career
        title: Career title
        description: Career description
        required_skills: Skills required for this career
        salary_range: Expected salary range
        demand: Market demand level
        related_careers: List of related career IDs
        growth_potential: Career growth potential description
        work_environment: Typical work environment
        education_requirements: Education requirements
        career_field: Career field category for consistency checking
    """
    career_id: str = Field(..., min_length=1)
    title: str = Field(..., min_length=1, max_length=200)
    description: str = Field(..., min_length=1, max_length=1000)
    required_skills: List[RequiredSkill] = Field(default_factory=list)
    salary_range: SalaryRange
    demand: Demand = Demand.MEDIUM
    related_careers: List[str] = Field(default_factory=list)
    growth_potential: Optional[str] = Field(None, max_length=500)
    work_environment: Optional[str] = Field(None, max_length=200)
    education_requirements: Optional[str] = Field(None, max_length=300)
    career_field: Optional[str] = Field(None, max_length=100, description="Career field category (e.g., 'technology', 'healthcare', 'business_finance')")
    
    def get_required_skill_names(self) -> List[str]:
        """Get list of required skill names."""
        return [skill.name for skill in self.required_skills]
    
    def get_mandatory_skills(self) -> List[RequiredSkill]:
        """Get list of mandatory skills."""
        return [skill for skill in self.required_skills if skill.is_mandatory]
    
    def get_preferred_skills(self) -> List[RequiredSkill]:
        """Get list of preferred (non-mandatory) skills."""
        return [skill for skill in self.required_skills if not skill.is_mandatory]


class RecommendationScore(BaseModel):
    """
    Represents a recommendation score for a career.
    
    Attributes:
        career_id: Career being scored
        total_score: Total recommendation score (0.0 to 1.0)
        skill_match_score: Score based on skill matching
        interest_match_score: Score based on interest alignment
        salary_compatibility_score: Score based on salary compatibility
        experience_match_score: Score based on experience level
        consistency_penalty: Penalty for career field mismatch (negative value)
        breakdown: Detailed score breakdown
    """
    career_id: str = Field(..., min_length=1)
    total_score: float = Field(..., ge=0.0, le=1.0)
    skill_match_score: float = Field(..., ge=0.0, le=1.0)
    interest_match_score: float = Field(..., ge=0.0, le=1.0)
    salary_compatibility_score: float = Field(..., ge=0.0, le=1.0)
    experience_match_score: float = Field(..., ge=0.0, le=1.0)
    consistency_penalty: float = Field(0.0, description="Penalty for career field mismatch (negative values reduce total score)")
    breakdown: Dict[str, Any] = Field(default_factory=dict)


class RecommendationCategory(str, Enum):
    """Recommendation category enumeration."""
    SAFE_ZONE = "safe_zone"
    STRETCH_ZONE = "stretch_zone"
    ADVENTURE_ZONE = "adventure_zone"


class CareerRecommendation(BaseModel):
    """
    Represents a career recommendation with score and category.
    
    Attributes:
        career: The recommended career
        score: Recommendation score details
        category: Recommendation category (Safe/Stretch/Adventure)
        reasons: List of reasons for the recommendation
        confidence: Confidence level in the recommendation (0.0 to 1.0)
    """
    career: Career
    score: RecommendationScore
    category: RecommendationCategory
    reasons: List[str] = Field(default_factory=list)
    confidence: float = Field(..., ge=0.0, le=1.0)