from pydantic import BaseModel
from typing import Optional

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenWithAssessment(BaseModel):
    access_token: str
    token_type: str
    assessment_completed: bool

class TokenData(BaseModel):
    email: Optional[str] = None