from pydantic import BaseModel, Field
from typing import List, Optional, Union
from datetime import datetime
import uuid

class UserAssessment(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), alias="_id")
    user_id: str
    
    # Basic Information
    age: Optional[str] = None
    location: Optional[str] = None
    educationLevel: Optional[str] = None
    currentSituation: Optional[str] = None
    currentRole: Optional[str] = None
    experience: Optional[str] = None
    resumeText: Optional[str] = None
    linkedinProfile: Optional[str] = None
    
    # Certifications
    certifications: Optional[List[str]] = []
    otherTradesCert: Optional[str] = None
    otherTechCert: Optional[str] = None
    otherBusinessCert: Optional[str] = None
    otherHealthcareCert: Optional[str] = None
    
    # Skills
    technicalSkills: Optional[List[str]] = []
    softSkills: Optional[List[str]] = []
    
    # Work Preferences (can be int or list with single int)
    workingWithData: Optional[Union[int, List[int]]] = 3
    workingWithPeople: Optional[Union[int, List[int]]] = 3
    creativeTasks: Optional[Union[int, List[int]]] = 3
    problemSolving: Optional[Union[int, List[int]]] = 3
    leadership: Optional[Union[int, List[int]]] = 3
    physicalHandsOnWork: Optional[Union[int, List[int]]] = 3
    outdoorWork: Optional[Union[int, List[int]]] = 3
    mechanicalAptitude: Optional[Union[int, List[int]]] = 3
    
    # Interests and Industries
    interests: Optional[List[str]] = []
    industries: Optional[List[str]] = []
    workEnvironment: Optional[str] = None
    
    # Goals and Expectations
    careerGoals: Optional[str] = None
    workLifeBalance: Optional[str] = None
    salaryExpectations: Optional[str] = None
    
    # Legacy fields for backward compatibility
    skills: Optional[List[str]] = None
    career_goals: Optional[str] = None
    preferences: Optional[dict] = None
    
    created_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        populate_by_name = True
        json_schema_extra = {
            "example": {
                "user_id": "user123",
                "age": "30-35",
                "location": "San Francisco, CA",
                "educationLevel": "bachelors",
                "currentSituation": "employed",
                "currentRole": "Software Engineer",
                "experience": "5-10",
                "technicalSkills": ["Python", "JavaScript", "React"],
                "softSkills": ["Communication", "Problem Solving"],
                "workingWithData": 4,
                "workingWithPeople": 3,
                "creativeTasks": 4,
                "problemSolving": 5,
                "leadership": 3,
                "physicalHandsOnWork": 2,
                "outdoorWork": 2,
                "mechanicalAptitude": 3,
                "interests": ["Technology & Software", "Data & Analytics"],
                "industries": ["Technology & Software", "Financial Services"],
                "careerGoals": "Transition to a senior engineering role",
                "workLifeBalance": "important",
                "salaryExpectations": "100000-150000"
            }
        }