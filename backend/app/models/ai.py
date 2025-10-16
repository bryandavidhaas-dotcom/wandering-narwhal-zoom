from pydantic import BaseModel
from typing import List, Dict, Any

class UserAssessment(BaseModel):
    skills: List[str]
    experience: List[str]
    career_goals: List[str]
    preferences: Dict

class Recommendation(BaseModel):
    job_id: str
    title: str
    company: str
    location: str
    description: str
    requirements: List[str]
    seniority: str
    score: float
    highlights: List[str]
    role: str
    tech: List[str]
    employment_type: str
    industry: str

class RecommendationSet(BaseModel):
    recommendations: List[Recommendation]

class TuningPrompt(BaseModel):
    current_recommendations: List[Dict[str, Any]]
    prompt: str