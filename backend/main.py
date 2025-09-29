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
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from backend.database import init_db
from backend.recommendation_engine import engine, config
from backend import models



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
    allow_origins=["http://localhost:5137", "http://localhost:3000", "http://localhost:5173", "https://wandering-narwhal-zoom-front-end.onrender.com"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize the recommendation engine
recommendation_engine = None

# Simple data store class to hold mock data
class MockDataStore:
    def __init__(self):
        self.user_profile = None
        self.careers = None
        self.skills = None
        self.initialized = False

# Global data store instance
mock_data = MockDataStore()

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
    print("Starting up the application...")
    try:
        await init_db()
        print("Database initialization successful.")
    except Exception as e:
        print(f"Error during database initialization: {e}")
        # Depending on the use case, you might want to exit the application
        # For now, we'll just log the error.
    
    # Initialize simple mock data (using dictionaries instead of Beanie Documents)
    global mock_data, recommendation_engine
    
    # Simple mock data as dictionaries
    mock_data.skills = [
        {"skill_id": "skill_1", "name": "Python", "category": "Programming Language"},
        {"skill_id": "skill_2", "name": "Machine Learning", "category": "Technical Skill"},
        {"skill_id": "skill_3", "name": "Data Analysis", "category": "Technical Skill"},
        {"skill_id": "skill_4", "name": "JavaScript", "category": "Programming Language"},
        {"skill_id": "skill_5", "name": "SQL", "category": "Database"}
    ]
    
    mock_data.careers = [
        {
            "career_id": "career_1",
            "title": "Data Scientist",
            "description": "Analyzes complex data to extract insights and build predictive models",
            "salary_range": {"min": 90000, "max": 140000, "currency": "USD"},
            "required_skills": [
                {"name": "Python", "proficiency": "advanced", "is_mandatory": True},
                {"name": "Machine Learning", "proficiency": "intermediate", "is_mandatory": True},
                {"name": "Data Analysis", "proficiency": "advanced", "is_mandatory": True}
            ],
            "demand": "high"
        },
        {
            "career_id": "career_2",
            "title": "Software Engineer",
            "description": "Designs and develops software applications and systems",
            "salary_range": {"min": 80000, "max": 130000, "currency": "USD"},
            "required_skills": [
                {"name": "Python", "proficiency": "advanced", "is_mandatory": True},
                {"name": "JavaScript", "proficiency": "intermediate", "is_mandatory": True}
            ],
            "demand": "high"
        },
        {
            "career_id": "career_3",
            "title": "Data Analyst",
            "description": "Collects and analyzes data to support business decisions",
            "salary_range": {"min": 60000, "max": 90000, "currency": "USD"},
            "required_skills": [
                {"name": "Data Analysis", "proficiency": "advanced", "is_mandatory": True},
                {"name": "SQL", "proficiency": "intermediate", "is_mandatory": True}
            ],
            "demand": "medium"
        }
    ]
    
    mock_data.user_profile = {
        "user_id": "user_123",
        "skills": [
            {"name": "Python", "level": "advanced", "years_experience": 3},
            {"name": "Data Analysis", "level": "intermediate", "years_experience": 2},
            {"name": "SQL", "level": "intermediate", "years_experience": 2}
        ],
        "interests": ["Technology", "Data Science", "Problem Solving"],
        "salary_expectations": {"min": 80000, "max": 120000, "currency": "USD"}
    }
    
    mock_data.initialized = True
    
    print("Mock data initialized.")
    
    recommendation_engine = RecommendationEngine(skills_db=[])
    print("Recommendation engine initialized.")

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
    return HealthResponse(status="healthy")

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
        if not mock_data.initialized:
            raise HTTPException(status_code=503, detail="Mock data not initialized")
            
        # For now, return simplified mock recommendations
        rec_data = []
        categories = {"safe_zone": 0, "stretch_zone": 0, "adventure_zone": 0}
        
        # Simple mock recommendations based on the careers
        for i, career in enumerate(mock_data.careers[:request.limit]):
            category = "safe_zone" if i == 0 else "stretch_zone" if i == 1 else "adventure_zone"
            categories[category] += 1
            
            rec_data.append({
                "career_id": career["career_id"],
                "title": career["title"],
                "description": career["description"],
                "category": category,
                "score": {
                    "total": 0.8 - (i * 0.1),
                    "skill_match": 0.9 - (i * 0.1),
                    "interest_match": 0.7 - (i * 0.1),
                    "salary_compatibility": 0.8,
                    "experience_match": 0.6
                },
                "confidence": 0.85 - (i * 0.05),
                "reasons": [f"Good match for {career['title']}", "Strong skill alignment", "Salary compatible"],
                "salary_range": career["salary_range"],
                "required_skills": career["required_skills"]
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
        if not mock_data.initialized:
            raise HTTPException(status_code=503, detail="Mock data not initialized")
            
        careers_data = []
        for career in mock_data.careers:
            careers_data.append({
                "career_id": career["career_id"],
                "title": career["title"],
                "description": career["description"],
                "salary_range": career["salary_range"],
                "demand": career["demand"],
                "required_skills": [skill["name"] for skill in career["required_skills"]]
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
        if not mock_data.initialized:
            raise HTTPException(status_code=503, detail="Mock data not initialized")
            
        skills_data = []
        for skill in mock_data.skills:
            skills_data.append({
                "skill_id": skill["skill_id"],
                "name": skill["name"],
                "category": skill["category"],
                "related_skills": skill.get("related_skills", [])
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
    port = int(os.environ.get("API_PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)