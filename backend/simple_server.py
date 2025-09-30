"""
Simple FastAPI backend server for the Career Recommendation Engine.
This version includes a simplified recommendation engine directly.
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
from enum import Enum
from datetime import datetime
import json
import os
import logging
# Recommendation Engine Imports
# Recommendation Engine Imports
from recommendation_engine.engine import RecommendationEngine as EnhancedRecommendationEngine
from recommendation_engine.config import DEFAULT_CONFIG
try:
    from models import UserProfileModel as UserProfile, CareerModel as Career
    from comprehensive_careers import COMPREHENSIVE_CAREERS
except (ImportError, ModuleNotFoundError):
    # Fallback for different execution contexts
    import sys
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))
    from models import UserProfileModel as UserProfile, CareerModel as Career
    from comprehensive_careers import COMPREHENSIVE_CAREERS

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

logger.info("Initializing FastAPI app...")
# Initialize FastAPI app
app = FastAPI(
    title="Career Recommendation API",
    description="API for career recommendations based on user profiles",
    version="1.0.0"
)
logger.info("FastAPI app initialized.")
# Initialize the recommendation engine
logger.info("Initializing recommendation engine...")
recommendation_engine = EnhancedRecommendationEngine(config=DEFAULT_CONFIG)
logger.info("Recommendation engine initialized.")

# Configure CORS
logger.info("Configuring CORS...")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5137", "http://localhost:3000", "http://localhost:5173", "https://wandering-narwhal-zoom-front-end.onrender.com"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
logger.info("CORS configured.")

# Simple data models
logger.info("Defining data models...")
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
logger.info("Data models defined.")

# Load career data from JSON file
try:
    logger.info("Loading career data from JSON file...")
    CAREER_DATA_PATH = os.path.join(os.path.dirname(__file__), 'career_data.json')
    with open(CAREER_DATA_PATH, 'r') as f:
        CAREER_DATA = json.load(f)
    logger.info("Career data loaded successfully.")
except Exception as e:
    logger.error(f"Error loading career data: {e}")
    CAREER_DATA = []

# Request/Response models
class RecommendationRequest(BaseModel):
    user_profile: Optional[Dict[str, Any]] = None
    limit: Optional[int] = 10

# NEW: Direct API request model for frontend compatibility
class DirectRecommendationRequest(BaseModel):
    age: Optional[str] = None
    location: Optional[str] = None
    educationLevel: Optional[str] = None
    certifications: Optional[List[str]] = []
    currentSituation: Optional[str] = None
    currentRole: Optional[str] = None
    experience: Optional[str] = None
    resumeText: Optional[str] = None
    linkedinProfile: Optional[str] = None
    technicalSkills: Optional[List[str]] = []
    softSkills: Optional[List[str]] = []
    workingWithData: Optional[int] = 3
    workingWithPeople: Optional[int] = 3
    creativeTasks: Optional[int] = 3
    problemSolving: Optional[int] = 3
    leadership: Optional[int] = 3
    physicalHandsOnWork: Optional[int] = 3
    outdoorWork: Optional[int] = 3
    mechanicalAptitude: Optional[int] = 3
    interests: Optional[List[str]] = []
    industries: Optional[List[str]] = []
    workEnvironment: Optional[str] = None
    careerGoals: Optional[str] = None
    workLifeBalance: Optional[str] = None
    salaryExpectations: Optional[str] = None
    explorationLevel: Optional[int] = 1

class RecommendationResponse(BaseModel):
    recommendations: List[Dict[str, Any]]
    total_count: int
    categories: Dict[str, int]

class HealthResponse(BaseModel):
    status: str
    message: str
    engine_status: str

@app.get("/", response_model=Dict[str, str])
async def root():
    """Root endpoint with API information."""
    return {
        "message": "Career Recommendation API",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/health"
    }

@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint."""
    return HealthResponse(
        status="healthy",
        message="API is running",
        engine_status="healthy"
    )

@app.post("/recommendations", response_model=RecommendationResponse)
async def get_recommendations(request: RecommendationRequest):
    """
    Get career recommendations for a user profile.
    """
    try:
        # Convert request to UserProfile
        user_profile = UserProfile(**request.user_profile) if request.user_profile else UserProfile()

        # Get recommendations from the engine
        recommendations = recommendation_engine.get_recommendations(
            user_profile=user_profile,
            available_careers=COMPREHENSIVE_CAREERS,
            limit=request.limit
        )

        # Format response
        rec_data = []
        categories = {"safe_zone": 0, "stretch_zone": 0, "adventure_zone": 0}
        for rec in recommendations:
            rec_data.append(rec.dict())
            if rec.category:
                categories[rec.category.value] += 1

        return RecommendationResponse(
            recommendations=rec_data,
            total_count=len(rec_data),
            categories=categories
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating recommendations: {str(e)}")

@app.get("/recommendations/categories")
async def get_recommendations_by_category():
    """Get recommendations organized by category."""
    try:
        result = {
            "safe_zone": [career for career in MOCK_CAREERS if career["category"] == "safe_zone"],
            "stretch_zone": [career for career in MOCK_CAREERS if career["category"] == "stretch_zone"],
            "adventure_zone": [career for career in MOCK_CAREERS if career["category"] == "adventure_zone"]
        }
        
        return result
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting categorized recommendations: {str(e)}")

@app.get("/careers")
async def get_careers():
    """Get all available careers."""
    try:
        return {
            "careers": MOCK_CAREERS,
            "total_count": len(MOCK_CAREERS)
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching careers: {str(e)}")

@app.get("/api/career/{career_type}")
async def get_career_detail(career_type: str):
    """Get detailed information about a specific career using the same comprehensive database as recommendations."""
    try:
        # Find the career in the CAREER_DATA list
        career = next((c for c in CAREER_DATA if c.get("careerType") == career_type), None)
        if career:
            return career
        
        # If still not found, return 404
        raise HTTPException(status_code=404, detail="Career not found")
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching career: {str(e)}")

@app.post("/recommendations/explain/{career_id}")
async def explain_recommendation(career_id: str):
    """Get detailed explanation for a specific career recommendation."""
    try:
        career = next((c for c in MOCK_CAREERS if c["career_id"] == career_id), None)
        if not career:
            raise HTTPException(status_code=404, detail="Career not found")
        
        explanation = {
            "career_title": career["title"],
            "total_score": career["score"],
            "category": career["category"],
            "confidence": career["confidence"],
            "reasons": career["reasons"],
            "score_breakdown": {
                "skill_match": 0.8,
                "interest_match": 0.7,
                "salary_compatibility": 0.9,
                "experience_match": 0.85
            },
            "detailed_breakdown": {
                "skill_details": {
                    "matched_skills": [
                        {"name": skill, "user_level": "intermediate", "required_level": "intermediate"}
                        for skill in career["required_skills"][:2]
                    ],
                    "missing_skills": career["required_skills"][2:] if len(career["required_skills"]) > 2 else []
                }
            }
        }
        
        return explanation
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error explaining recommendation: {str(e)}")

@app.get("/statistics")
async def get_recommendation_statistics():
    """Get comprehensive statistics about the recommendation process."""
    try:
        stats = {
            "filtering_stats": {
                "original_count": len(MOCK_CAREERS),
                "after_initial_filters": len(MOCK_CAREERS),
                "after_skill_filters": len(MOCK_CAREERS),
                "after_interest_filters": len(MOCK_CAREERS)
            },
            "category_distribution": {
                "safe_zone": len([c for c in MOCK_CAREERS if c["category"] == "safe_zone"]),
                "stretch_zone": len([c for c in MOCK_CAREERS if c["category"] == "stretch_zone"]),
                "adventure_zone": len([c for c in MOCK_CAREERS if c["category"] == "adventure_zone"])
            },
            "score_statistics": {
                "average_score": sum(c["score"] for c in MOCK_CAREERS) / len(MOCK_CAREERS),
                "highest_score": max(c["score"] for c in MOCK_CAREERS),
                "lowest_score": min(c["score"] for c in MOCK_CAREERS),
                "score_range": max(c["score"] for c in MOCK_CAREERS) - min(c["score"] for c in MOCK_CAREERS)
            },
            "total_recommendations": len(MOCK_CAREERS)
        }
        
        return stats
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting statistics: {str(e)}")

@app.post("/api/recommendations")
async def get_recommendations_direct(request: DirectRecommendationRequest):
    """Direct API endpoint for frontend - matches frontend data format"""
    try:
        print(f"🚀 Received recommendation request from frontend")
        print(f"📊 User profile: experience={request.experience}, skills={len(request.technicalSkills or [])}, exploration_level={request.explorationLevel}")
        
        # Convert frontend data to our format and generate enhanced recommendations
        user_data = {
            "age": request.age,
            "location": request.location,
            "education_level": request.educationLevel,
            "certifications": request.certifications or [],
            "current_situation": request.currentSituation,
            "current_role": request.currentRole,
            "experience": request.experience,
            "resume_text": request.resumeText,
            "linkedin_profile": request.linkedinProfile,
            "technical_skills": request.technicalSkills or [],
            "soft_skills": request.softSkills or [],
            "working_with_data": request.workingWithData,
            "working_with_people": request.workingWithPeople,
            "creative_tasks": request.creativeTasks,
            "problem_solving": request.problemSolving,
            "leadership": request.leadership,
            "physical_hands_on_work": request.physicalHandsOnWork,
            "outdoor_work": request.outdoorWork,
            "mechanical_aptitude": request.mechanicalAptitude,
            "interests": request.interests or [],
            "industries": request.industries or [],
            "work_environment": request.workEnvironment,
            "career_goals": request.careerGoals,
            "work_life_balance": request.workLifeBalance,
            "salary_expectations": request.salaryExpectations
        }
        
        # Convert frontend data to UserProfile
        # This is a simplified conversion. In a real scenario, you'd map all fields.
        user_profile_data = {
            'user_id': "api_user",
            'technicalSkills': user_data.get('technical_skills'),
            'softSkills': user_data.get('soft_skills'),
            'experience': user_data.get('experience'),
            'industries': user_data.get('industries'),
            'interests': user_data.get('interests'),
            'careerGoals': user_data.get('career_goals'),
            'salaryExpectations': user_data.get('salary_expectations'),
            'currentRole': user_data.get('current_role'),
            'educationLevel': user_data.get('education_level'),
            'location': user_data.get('location'),
            'resumeText': user_data.get('resume_text'),
            'workingWithData': user_data.get('working_with_data'),
            'workingWithPeople': user_data.get('working_with_people'),
            'creativeTasks': user_data.get('creative_tasks'),
            'problemSolving': user_data.get('problem_solving'),
            'leadership': user_data.get('leadership'),
            'physicalHandsOnWork': user_data.get('physical_hands_on_work'),
            'mechanicalAptitude': user_data.get('mechanical_aptitude'),
        }
        user_profile = UserProfile(**user_profile_data)

        # Get recommendations from the engine
        recommendations = recommendation_engine.get_recommendations(
            user_profile=user_profile,
            available_careers=COMPREHENSIVE_CAREERS,
            exploration_level=request.explorationLevel or 1
        )

        # Format response to be JSON serializable
        rec_data = []
        for rec in recommendations:
            rec_dict = rec.dict()
            # Convert enums to strings if they exist
            if 'category' in rec_dict and hasattr(rec_dict['category'], 'value'):
                rec_dict['category'] = rec_dict['category'].value
            rec_data.append(rec_dict)
        
        print(f"✅ Generated {len(rec_data)} recommendations")
        return rec_data
        
    except Exception as e:
        print(f"❌ Error in /api/recommendations: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to generate recommendations: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8002, reload=True)