from pydantic import BaseModel
from typing import List, Dict

class UserAssessment(BaseModel):
    skills: List[str]
    experience: List[str]
    career_goals: List[str]
    preferences: Dict

class Recommendation(BaseModel):
    job_title: str
    company: str
    location: str
    description: str
    requirements: List[str]

class RecommendationSet(BaseModel):
    recommendations: List[Recommendation]

class TuningPrompt(BaseModel):
    recommendations: RecommendationSet
    prompt: str