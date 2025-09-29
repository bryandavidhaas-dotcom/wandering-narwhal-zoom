"""
MongoDB-compatible FastAPI server that uses the comprehensive career data
but structures responses in MongoDB format for true API integration.
"""

import logging
from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv
import json

# Load environment variables
load_dotenv()

# Import comprehensive career data and recommendation engine
from comprehensive_careers import COMPREHENSIVE_CAREERS
from recommendation_engine.enhanced_engine import EnhancedRecommendationEngine

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Career Recommendation API with MongoDB Structure",
    description="API for career recommendations using MongoDB-compatible data structures",
    version="2.0.0"
)

# Configure CORS
cors_origins = os.getenv("CORS_ORIGINS", "http://localhost:5137,http://localhost:3000,http://localhost:5173").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize recommendation engine
logger.info("Initializing recommendation engine...")
recommendation_engine = EnhancedRecommendationEngine()
logger.info("Recommendation engine initialized successfully.")

# Convert comprehensive careers to MongoDB-compatible format
def convert_to_mongodb_format(career_data):
    """Convert career data to MongoDB-compatible format"""
    return {
        "career_id": career_data.get("careerType", "unknown"),
        "title": career_data.get("title", "Unknown Career"),
        "description": career_data.get("description", ""),
        "salary_range": {
            "min": career_data.get("minSalary", 50000),
            "max": career_data.get("maxSalary", 80000),
            "currency": "USD"
        },
        "demand": "high",  # Default value
        "required_skills": [
            {
                "skill_id": skill.lower().replace(" ", "_"),
                "name": skill,
                "proficiency": "intermediate",
                "is_mandatory": True
            }
            for skill in career_data.get("requiredTechnicalSkills", [])
        ],
        "experience_level": career_data.get("experienceLevel", "junior"),
        "min_years_experience": career_data.get("minExperienceYears", 0),
        "max_years_experience": career_data.get("maxExperienceYears", 5),
        "companies": career_data.get("companies", []),
        "learning_path": career_data.get("learningPath", "Self-directed learning"),
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    }

# Convert all careers to MongoDB format
MONGODB_CAREERS = [convert_to_mongodb_format(career) for career in COMPREHENSIVE_CAREERS]

# Health check endpoint
@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "message": "MongoDB-compatible API is running",
        "database_status": "in-memory",
        "total_careers": len(MONGODB_CAREERS),
        "api_version": "2.0.0"
    }

# Career endpoints
@app.get("/careers")
async def get_careers(skip: int = 0, limit: int = 100):
    """Get all careers with pagination"""
    try:
        total_count = len(MONGODB_CAREERS)
        careers = MONGODB_CAREERS[skip:skip + limit]
        
        return {
            "careers": careers,
            "total_count": total_count,
            "skip": skip,
            "limit": limit
        }
        
    except Exception as e:
        logger.error(f"Error fetching careers: {e}")
        raise HTTPException(status_code=500, detail=f"Error fetching careers: {str(e)}")

@app.get("/careers/{career_id}")
async def get_career(career_id: str):
    """Get specific career by ID"""
    try:
        career = next((c for c in MONGODB_CAREERS if c["career_id"] == career_id), None)
        if not career:
            raise HTTPException(status_code=404, detail="Career not found")
        
        return career
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching career: {e}")
        raise HTTPException(status_code=500, detail=f"Error fetching career: {str(e)}")

# Recommendation endpoint compatible with current frontend
@app.post("/api/recommendations")
async def get_recommendations(request: Dict[str, Any]):
    """Get career recommendations using the enhanced recommendation engine"""
    try:
        logger.info(f"Received recommendation request: {request}")
        
        # Use the enhanced recommendation engine
        recommendations = recommendation_engine.get_recommendations(
            user_profile=request,
            career_data=COMPREHENSIVE_CAREERS,  # Use original format for engine
            limit=request.get("limit", 10)
        )
        
        logger.info(f"Generated {len(recommendations)} recommendations")
        
        # Convert to MongoDB-compatible response format but keep current structure for frontend
        mongodb_recommendations = []
        for rec in recommendations:
            # Find the MongoDB version of this career
            mongodb_career = next(
                (c for c in MONGODB_CAREERS if c["career_id"] == rec.get("careerType")), 
                None
            )
            
            # Enhance the recommendation with MongoDB structure while keeping frontend compatibility
            enhanced_rec = {
                **rec,  # Keep all original fields for frontend compatibility
                "mongodb_career": mongodb_career,  # Add MongoDB structure
                "database_source": "mongodb_compatible",
                "api_version": "2.0.0"
            }
            
            mongodb_recommendations.append(enhanced_rec)
        
        return mongodb_recommendations
        
    except Exception as e:
        logger.error(f"Error generating recommendations: {e}")
        raise HTTPException(status_code=500, detail=f"Error generating recommendations: {str(e)}")

# MongoDB-style recommendation endpoint
@app.post("/recommendations")
async def get_mongodb_recommendations(request: Dict[str, Any]):
    """Get recommendations in pure MongoDB format"""
    try:
        user_id = request.get("user_id", "anonymous")
        limit = request.get("limit", 10)
        
        logger.info(f"MongoDB-style recommendation request for user: {user_id}")
        
        # Use the enhanced recommendation engine
        recommendations = recommendation_engine.get_recommendations(
            user_profile=request,
            career_data=COMPREHENSIVE_CAREERS,
            limit=limit
        )
        
        # Convert to pure MongoDB response format
        mongodb_response = {
            "recommendations": [],
            "total_count": len(recommendations),
            "categories": {"safe_zone": 0, "stretch_zone": 0, "adventure_zone": 0},
            "cached": False,
            "generated_at": datetime.utcnow()
        }
        
        for rec in recommendations:
            # Map zones to MongoDB categories
            zone = rec.get("zone", "safe")
            category = "safe_zone" if zone == "safe" else "stretch_zone" if zone == "stretch" else "adventure_zone"
            mongodb_response["categories"][category] += 1
            
            # Find MongoDB career data
            mongodb_career = next(
                (c for c in MONGODB_CAREERS if c["career_id"] == rec.get("careerType")), 
                None
            )
            
            mongodb_rec = {
                "career_id": rec.get("careerType", "unknown"),
                "title": rec.get("title", "Unknown"),
                "description": rec.get("description", ""),
                "category": category,
                "score": rec.get("relevanceScore", 50) / 100.0,  # Convert to 0-1 scale
                "confidence": rec.get("confidenceLevel", 50) / 100.0,  # Convert to 0-1 scale
                "reasons": rec.get("matchReasons", []),
                "salary_range": mongodb_career["salary_range"] if mongodb_career else {
                    "min": rec.get("minSalary", 50000),
                    "max": rec.get("maxSalary", 80000),
                    "currency": "USD"
                },
                "created_at": datetime.utcnow()
            }
            
            mongodb_response["recommendations"].append(mongodb_rec)
        
        return mongodb_response
        
    except Exception as e:
        logger.error(f"Error generating MongoDB recommendations: {e}")
        raise HTTPException(status_code=500, detail=f"Error generating recommendations: {str(e)}")

# Skills endpoint
@app.get("/skills")
async def get_skills(skip: int = 0, limit: int = 100):
    """Get all skills with pagination"""
    try:
        # Extract unique skills from all careers
        all_skills = set()
        for career in MONGODB_CAREERS:
            for skill in career.get("required_skills", []):
                all_skills.add(skill["name"])
        
        skills_list = [
            {
                "skill_id": skill.lower().replace(" ", "_"),
                "name": skill,
                "category": "general",
                "created_at": datetime.utcnow()
            }
            for skill in sorted(all_skills)
        ]
        
        total_count = len(skills_list)
        paginated_skills = skills_list[skip:skip + limit]
        
        return {
            "skills": paginated_skills,
            "total_count": total_count,
            "skip": skip,
            "limit": limit
        }
        
    except Exception as e:
        logger.error(f"Error fetching skills: {e}")
        raise HTTPException(status_code=500, detail=f"Error fetching skills: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    host = os.getenv("API_HOST", "0.0.0.0")
    port = int(os.getenv("MONGODB_API_PORT", 8003))  # Use different port to avoid conflicts
    
    logger.info(f"Starting MongoDB-compatible server on {host}:{port}")
    uvicorn.run(app, host=host, port=port, reload=True)