"""
MongoDB models using Beanie ODM for the career recommendation system.
"""

from beanie import Document, Indexed
import uuid
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime
from enum import Enum

# Enums
class SkillLevel(str, Enum):
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"
    EXPERT = "expert"

class InterestLevel(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    VERY_HIGH = "very_high"

class RecommendationCategory(str, Enum):
    SAFE_ZONE = "safe_zone"
    STRETCH_ZONE = "stretch_zone"
    ADVENTURE_ZONE = "adventure_zone"

class Demand(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    VERY_HIGH = "very_high"

# Embedded documents
class SalaryRange(BaseModel):
    min: int = Field(..., ge=0)
    max: int = Field(..., ge=0)
    currency: str = Field("USD", min_length=3, max_length=3)

class UserSkill(BaseModel):
    skill_id: str
    name: str
    level: SkillLevel
    years_experience: Optional[float] = None
    is_certified: bool = False
    last_used: Optional[datetime] = None

class RequiredSkill(BaseModel):
    skill_id: str
    name: str
    proficiency: SkillLevel
    is_mandatory: bool = True
    weight: float = Field(1.0, ge=0.0, le=1.0)

class PersonalInfo(BaseModel):
    age: Optional[int] = Field(None, ge=16, le=100)
    location: Optional[str] = None
    salary_expectations: Optional[SalaryRange] = None
    willing_to_relocate: bool = False
    preferred_work_style: Optional[str] = None

class AssessmentResults(BaseModel):
    personality_traits: List[str] = Field(default_factory=list)
    work_values: List[str] = Field(default_factory=list)
    interests: Dict[str, InterestLevel] = Field(default_factory=dict)

class Experience(BaseModel):
    title: str
    company: str
    duration_years: float = Field(..., ge=0, le=50)
    description: Optional[str] = None
    skills_used: List[str] = Field(default_factory=list)

class ProfessionalData(BaseModel):
    resume_skills: List[str] = Field(default_factory=list)
    linkedin_skills: List[str] = Field(default_factory=list)
    experience: List[Experience] = Field(default_factory=list)
    education: Optional[str] = None
    certifications: List[str] = Field(default_factory=list)

class RecommendationScore(BaseModel):
    career_id: str
    total_score: float = Field(..., ge=0.0, le=1.0)
    skill_match_score: float = Field(..., ge=0.0, le=1.0)
    interest_match_score: float = Field(..., ge=0.0, le=1.0)
    salary_compatibility_score: float = Field(..., ge=0.0, le=1.0)
    experience_match_score: float = Field(..., ge=0.0, le=1.0)
    breakdown: Dict[str, Any] = Field(default_factory=dict)

# Document models (MongoDB collections)
class SkillModel(Document):
    skill_id: Indexed(str, unique=True)
    name: str
    category: str
    related_skills: List[str] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    class Settings:
        name = "skills"

class CareerModel(Document):
    career_id: Optional[str] = Field(default_factory=lambda: str(uuid.uuid4()), unique=True)
    title: str
    description: str
    requiredTechnicalSkills: List[str] = Field(default_factory=list)
    requiredSoftSkills: List[str] = Field(default_factory=list)
    preferredInterests: List[str] = Field(default_factory=list)
    preferredIndustries: List[str] = Field(default_factory=list)
    workDataWeight: float
    workPeopleWeight: float
    creativityWeight: float
    problemSolvingWeight: float
    leadershipWeight: float
    learningPath: str
    stretchLevel: str
    careerType: str
    requiresTechnical: bool
    companies: List[str] = Field(default_factory=list)
    dayInLife: str
    experienceLevel: str
    minYearsExperience: int
    maxYearsExperience: int
    salaryMin: int
    salaryMax: int
    remoteOptions: str
    workEnvironments: List[str] = Field(default_factory=list)
    requiredEducation: str
    preferredEducation: str
    valuedCertifications: List[str] = Field(default_factory=list)
    requiredCertifications: List[str] = Field(default_factory=list)
    workLifeBalanceRating: float
    agePreference: str
    locationFlexibility: str
    transitionFriendly: bool
    resumeKeywords: List[str] = Field(default_factory=list)
    relatedJobTitles: List[str] = Field(default_factory=list)
    valuedCompanies: List[str] = Field(default_factory=list)
    preferredIndustryExperience: List[str] = Field(default_factory=list)
    careerProgressionPatterns: List[str] = Field(default_factory=list)
    alternativeQualifications: List[str] = Field(default_factory=list)
    skillBasedEntry: bool
    experienceCanSubstitute: bool
    handsOnWorkWeight: float
    physicalWorkWeight: float
    outdoorWorkWeight: float
    mechanicalAptitudeWeight: float
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Settings:
        name = "careers"

class UserProfileModel(Document):
    user_id: Indexed(str, unique=True)
    personal_info: PersonalInfo = Field(default_factory=PersonalInfo)
    assessment_results: AssessmentResults = Field(default_factory=AssessmentResults)
    professional_data: ProfessionalData = Field(default_factory=ProfessionalData)
    skills: List[UserSkill] = Field(default_factory=list)
    user_interests: List[str] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    class Settings:
        name = "user_profiles"

class RecommendationModel(Document):
    user_id: Indexed(str)
    career_id: str
    score: RecommendationScore
    category: RecommendationCategory
    reasons: List[str] = Field(default_factory=list)
    confidence: float = Field(..., ge=0.0, le=1.0)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    expires_at: Optional[datetime] = None  # For caching recommendations
    
    class Settings:
        name = "recommendations"
        indexes = [
            [("user_id", 1), ("created_at", -1)],  # Compound index for user recommendations
            [("expires_at", 1)],  # TTL index for automatic cleanup
        ]

# Request/Response models for API
class CreateUserProfileRequest(BaseModel):
    user_id: str
    personal_info: Optional[PersonalInfo] = None
    assessment_results: Optional[AssessmentResults] = None
    professional_data: Optional[ProfessionalData] = None
    skills: List[UserSkill] = Field(default_factory=list)
    user_interests: List[str] = Field(default_factory=list)

class UpdateUserProfileRequest(BaseModel):
    personal_info: Optional[PersonalInfo] = None
    assessment_results: Optional[AssessmentResults] = None
    professional_data: Optional[ProfessionalData] = None
    skills: Optional[List[UserSkill]] = None
    user_interests: Optional[List[str]] = None

class RecommendationRequest(BaseModel):
    user_id: str
    limit: Optional[int] = 10
    force_refresh: bool = False  # Force new recommendations instead of cached

class RecommendationResponse(BaseModel):
    recommendations: List[Dict[str, Any]]
    total_count: int
    categories: Dict[str, int]
    cached: bool = False
    generated_at: datetime