from pydantic import BaseModel, Field
from typing import List, Dict, Any
from datetime import datetime
import uuid

class TuningInteraction(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), alias="_id")
    recommendation_set_id: str
    user_id: str
    prompt: str
    response: List[Dict[str, Any]]
    created_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        allow_population_by_field_name = True
        schema_extra = {
            "example": {
                "recommendation_set_id": "60d5ec49e7a4b2a3b8e3f4f7",
                "user_id": "60d5ec49e7a4b2a3b8e3f4f6",
                "prompt": "I want something with more outdoor work",
                "response": [
                    {"career": "Park Ranger", "score": 0.9},
                    {"career": "Landscaper", "score": 0.85},
                ]
            }
        }