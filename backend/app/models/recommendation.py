from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime
import uuid

class JobRecommendation(BaseModel):
    job_id: str
    title: str
    seniority: str
    location: str
    score: float
    highlights: List[str]
    role: str
    tech: List[str]
    employment_type: str
    industry: str

class RecommendationSet(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), alias="_id")
    user_id: str
    recommendations: List[JobRecommendation]
    created_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        allow_population_by_field_name = True
        schema_extra = {
            "example": {
                "user_id": "user123",
                "recommendations": [
                    {
                        "job_id": "12345",
                        "title": "Backend Engineer",
                        "seniority": "Senior",
                        "location": "Remote",
                        "score": 0.92,
                        "highlights": ["Python", "Django", "5+ yrs"],
                        "role": "Backend Engineer",
                        "tech": ["Python", "Django"],
                        "employment_type": "Full-time",
                        "industry": "Fintech"
                    }
                ]
            }
        }