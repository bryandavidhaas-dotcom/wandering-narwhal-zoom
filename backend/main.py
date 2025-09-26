"""
FastAPI backend server for the Career Recommendation Engine.

This server provides REST API endpoints for the recommendation engine,
allowing the frontend to interact with the recommendation system.
"""

from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
import sys
import os

# Add the project root to the path to allow absolute imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from backend.recommendation_engine import engine, config
from backend import models
import motor.motor_asyncio
from beanie import init_beanie

async def init_db():
    client = motor.motor_asyncio.AsyncIOMotorClient("mongodb://localhost:27017")
    await init_beanie(database=client.db_name, document_models=[models.SkillModel, models.CareerModel, models.UserProfileModel, models.RecommendationModel])



# Import the classes
RecommendationEngine = engine.RecommendationEngine
UserProfile = models.UserProfileModel
Career = models.CareerModel
CareerRecommendation = models.RecommendationModel
RecommendationConfig = config.RecommendationConfig
ScoringWeights = config.ScoringWeights

# Initialize FastAPI app
app = FastAPI(
    title="Career Recommendation API",
    description="API for career recommendations based on user profiles",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5137", "http://localhost:3000", "http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize the recommendation engine
recommendation_engine = None

# Request/Response models
class RecommendationRequest(BaseModel):
    user_profile: Dict[str, Any]
    limit: Optional[int] = 10

class RecommendationResponse(BaseModel):
    recommendations: List[Dict[str, Any]]
    total_count: int
    categories: Dict[str, int]

class HealthResponse(BaseModel):
    status: str
@app.on_event("startup")
async def on_startup():
    await init_db()
    from backend.recommendation_engine import mock_data
    global recommendation_engine, MOCK_SKILLS, MOCK_CAREERS, MOCK_USER_PROFILE
    MOCK_SKILLS = mock_data.MOCK_SKILLS
    MOCK_CAREERS = mock_data.MOCK_CAREERS
    MOCK_USER_PROFILE = mock_data.MOCK_USER_PROFILE
    recommendation_engine = RecommendationEngine(skills_db=MOCK_SKILLS)
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
    try:
        # Test the recommendation engine
        test_recs = recommendation_engine.get_recommendations(
            user_profile=MOCK_USER_PROFILE,
            available_careers=MOCK_CAREERS[:2],
            limit=1
        )
        engine_status = "healthy" if test_recs else "degraded"
    except Exception as e:
        engine_status = f"error: {str(e)}"
    
    return HealthResponse(
        status="healthy",
        message="API is running",
        engine_status=engine_status
    )

@app.post("/recommendations", response_model=RecommendationResponse)
async def get_recommendations(request: RecommendationRequest):
    """
    Get career recommendations for a user profile.
    
    Args:
        request: Contains user profile data and optional limit
        
    Returns:
        Recommendations with categories and metadata
    """
    try:
        # Convert dict to UserProfile (simplified for demo)
        # In production, you'd want proper validation and conversion
        user_profile = MOCK_USER_PROFILE  # Using mock for now
        
        # Get recommendations
        recommendations = recommendation_engine.get_recommendations(
            user_profile=user_profile,
            available_careers=MOCK_CAREERS,
            limit=request.limit
        )
        
        # Convert to response format
        rec_data = []
        categories = {"safe_zone": 0, "stretch_zone": 0, "adventure_zone": 0}
        
        for rec in recommendations:
            categories[rec.category.value] += 1
            rec_data.append({
                "career_id": rec.career.career_id,
                "title": rec.career.title,
                "description": rec.career.description,
                "category": rec.category.value,
                "score": {
                    "total": rec.score.total_score,
                    "skill_match": rec.score.skill_match_score,
                    "interest_match": rec.score.interest_match_score,
                    "salary_compatibility": rec.score.salary_compatibility_score,
                    "experience_match": rec.score.experience_match_score
                },
                "confidence": rec.confidence,
                "reasons": rec.reasons,
                "salary_range": {
                    "min": rec.career.salary_range.min,
                    "max": rec.career.salary_range.max,
                    "currency": rec.career.salary_range.currency
                },
                "required_skills": [
                    {
                        "name": skill.name,
                        "proficiency": skill.proficiency.value,
                        "is_mandatory": skill.is_mandatory
                    }
                    for skill in rec.career.required_skills
                ]
            })
        
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
        categorized = recommendation_engine.get_recommendations_by_category(
            user_profile=MOCK_USER_PROFILE,
            available_careers=MOCK_CAREERS,
            limit_per_category=5
        )
        
        result = {}
        for category, recs in categorized.items():
            result[category] = [
                {
                    "career_id": rec.career.career_id,
                    "title": rec.career.title,
                    "score": rec.score.total_score,
                    "confidence": rec.confidence,
                    "reasons": rec.reasons[:3]  # Top 3 reasons
                }
                for rec in recs
            ]
        
        return result
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting categorized recommendations: {str(e)}")

@app.get("/careers")
async def get_careers():
    """Get all available careers."""
    try:
        careers_data = []
        for career in MOCK_CAREERS:
            careers_data.append({
                "career_id": career.career_id,
                "title": career.title,
                "description": career.description,
                "salary_range": {
                    "min": career.salary_range.min,
                    "max": career.salary_range.max,
                    "currency": career.salary_range.currency
                },
                "demand": career.demand.value,
                "required_skills": [skill.name for skill in career.required_skills]
            })
        
        return {
            "careers": careers_data,
            "total_count": len(careers_data)
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching careers: {str(e)}")

@app.get("/skills")
async def get_skills():
    """Get all available skills."""
    try:
        skills_data = []
        for skill in MOCK_SKILLS:
            skills_data.append({
                "skill_id": skill.skill_id,
                "name": skill.name,
                "category": skill.category,
                "related_skills": skill.related_skills
            })
        
        return {
            "skills": skills_data,
            "total_count": len(skills_data)
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching skills: {str(e)}")

@app.post("/recommendations/explain")
async def explain_recommendation(career_id: str):
    """Get detailed explanation for a specific career recommendation."""
    try:
        # Find the career
        career = None
        for c in MOCK_CAREERS:
            if c.career_id == career_id:
                career = c
                break
        
        if not career:
            raise HTTPException(status_code=404, detail="Career not found")
        
        # Get explanation
        explanation = recommendation_engine.explain_recommendation(
            user_profile=MOCK_USER_PROFILE,
            career=career
        )
        
        return explanation
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error explaining recommendation: {str(e)}")

@app.get("/statistics")
async def get_recommendation_statistics():
    """Get comprehensive statistics about the recommendation process."""
    try:
        stats = recommendation_engine.get_recommendation_statistics(
            user_profile=MOCK_USER_PROFILE,
            available_careers=MOCK_CAREERS
        )
        
        return stats
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting statistics: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)