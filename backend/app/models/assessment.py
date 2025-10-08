from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime
import uuid

class UserAssessment(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), alias="_id")
    user_id: str
    skills: List[str]
    experience: str
    career_goals: str
    preferences: Optional[dict]
    created_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        allow_population_by_field_name = True
        schema_extra = {
            "example": {
                "user_id": "user123",
                "skills": ["Python", "FastAPI", "MongoDB"],
                "experience": "5 years as a backend developer",
                "career_goals": "Transition to a data science role",
                "preferences": {"remote": True, "salary": "150k"}
            }
        }