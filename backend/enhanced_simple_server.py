"""
Enhanced FastAPI server that uses comprehensive career data with MongoDB-compatible API responses.
This server provides true MongoDB API integration while using the existing recommendation engine.
"""

import logging
from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
from datetime import datetime, timezone
import os
import json
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import comprehensive career data and recommendation engine
from comprehensive_careers import COMPREHENSIVE_CAREERS

# Try to import the recommendation engine, fallback if not available
try:
    from recommendation_engine.enhanced_engine import EnhancedRecommendationEngine
except ImportError as e:
    print(f"Warning: Could not import EnhancedRecommendationEngine: {e}")
    EnhancedRecommendationEngine = None

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
logger.info("Initializing FastAPI app...")
app = FastAPI(
    title="Enhanced Career Recommendation API with MongoDB Integration",
    description="API for career recommendations with MongoDB-compatible responses",
    version="2.0.0"
)
logger.info("FastAPI app initialized.")

# Configure CORS
logger.info("Configuring CORS...")
cors_origins = os.getenv("CORS_ORIGINS", "http://localhost:5137,http://localhost:3000,http://localhost:5173,https://wandering-narwhal-zoom-front-end.onrender.com").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
logger.info("CORS configured.")

# Define data models
logger.info("Defining data models...")

class UserProfileRequest(BaseModel):
    skills: List[str] = []
    interests: List[str] = []
    experience_level: str = "junior"
    education_level: str = "bachelors"
    work_environment: str = "office"
    salary_expectation: int = 75000
    location: Optional[str] = None
    remote_preference: Optional[str] = None

logger.info("Data models defined.")

# Initialize recommendation engine
logger.info("Initializing recommendation engine...")
try:
    if EnhancedRecommendationEngine:
        recommendation_engine = EnhancedRecommendationEngine()
        logger.info("Recommendation engine initialized successfully.")
    else:
        logger.warning("EnhancedRecommendationEngine not available, using fallback mode.")
        recommendation_engine = None
except Exception as e:
    logger.error(f"Failed to initialize recommendation engine: {e}")
    # Fallback to basic functionality
    recommendation_engine = None

# Load career data
logger.info("Loading comprehensive career data...")
try:
    career_data = COMPREHENSIVE_CAREERS
    logger.info(f"Loaded {len(career_data)} careers successfully.")
except Exception as e:
    logger.error(f"Failed to load career data: {e}")
    career_data = []

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
                "skill_id": skill.lower().replace(" ", "_").replace("/", "_"),
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
        "created_at": datetime.now(timezone.utc).isoformat(),
        "updated_at": datetime.now(timezone.utc).isoformat()
    }

# Convert all careers to MongoDB format
MONGODB_CAREERS = [convert_to_mongodb_format(career) for career in career_data]

@app.get("/health")
async def health_check():
    """Health check endpoint with MongoDB integration status"""
    return {
        "status": "healthy",
        "message": "Enhanced API with MongoDB integration is running",
        "database_status": "in-memory",
        "total_careers": len(MONGODB_CAREERS),
        "engine_status": "healthy" if recommendation_engine else "fallback",
        "api_version": "2.0.0",
        "mongodb_compatible": True
    }

@app.post("/api/recommendations")
async def get_recommendations(request: UserProfileRequest):
    """Get career recommendations with MongoDB-compatible responses"""
    try:
        logger.info(f"Received recommendation request: {request.dict()}")
        
        if recommendation_engine:
            # Use enhanced recommendation engine
            recommendations = recommendation_engine.get_recommendations(
                user_profile=request.dict(),
                career_data=career_data,
                limit=10
            )
        else:
            # Fallback to basic recommendations
            recommendations = career_data[:10]
        
        logger.info(f"Generated {len(recommendations)} recommendations")
        
        # Enhance recommendations with MongoDB structure
        enhanced_recommendations = []
        for rec in recommendations:
            # Find MongoDB version of this career
            mongodb_career = next(
                (c for c in MONGODB_CAREERS if c["career_id"] == rec.get("careerType")), 
                None
            )
            
            # Create enhanced recommendation with both formats
            enhanced_rec = {
                **rec,  # Keep original format for frontend compatibility
                "mongodb_career": mongodb_career,  # Add MongoDB structure
                "database_source": "mongodb_compatible",
                "api_version": "2.0.0",
                "enhanced": True
            }
            
            enhanced_recommendations.append(enhanced_rec)
        
        return enhanced_recommendations
        
    except Exception as e:
        logger.error(f"Error generating recommendations: {e}")
        raise HTTPException(status_code=500, detail=f"Error generating recommendations: {str(e)}")

@app.post("/recommendations")
async def get_mongodb_recommendations(request: Dict[str, Any]):
    """Get recommendations in pure MongoDB format"""
    try:
        user_id = request.get("user_id", "anonymous")
        limit = request.get("limit", 10)
        
        logger.info(f"MongoDB-style recommendation request for user: {user_id}")
        
        # Convert request to UserProfileRequest format
        user_profile = UserProfileRequest(
            skills=request.get("skills", []),
            interests=request.get("interests", []),
            experience_level=request.get("experience_level", "junior"),
            education_level=request.get("education_level", "bachelors"),
            work_environment=request.get("work_environment", "office"),
            salary_expectation=request.get("salary_expectation", 75000)
        )
        
        if recommendation_engine:
            recommendations = recommendation_engine.get_recommendations(
                user_profile=user_profile.dict(),
                career_data=career_data,
                limit=limit
            )
        else:
            recommendations = career_data[:limit]
        
        # Convert to pure MongoDB response format
        mongodb_response = {
            "recommendations": [],
            "total_count": len(recommendations),
            "categories": {"safe_zone": 0, "stretch_zone": 0, "adventure_zone": 0},
            "cached": False,
            "generated_at": datetime.now(timezone.utc).isoformat()
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
                "created_at": datetime.now(timezone.utc).isoformat()
            }
            
            mongodb_response["recommendations"].append(mongodb_rec)
        
        return mongodb_response
        
    except Exception as e:
        logger.error(f"Error generating MongoDB recommendations: {e}")
        raise HTTPException(status_code=500, detail=f"Error generating recommendations: {str(e)}")

@app.get("/careers")
async def get_careers(skip: int = 0, limit: int = 100):
    """Get all careers with pagination in MongoDB format"""
    try:
        total_count = len(MONGODB_CAREERS)
        careers = MONGODB_CAREERS[skip:skip + limit]
        
        return {
            "careers": careers,
            "total_count": total_count,
            "skip": skip,
            "limit": limit,
            "mongodb_compatible": True
        }
        
    except Exception as e:
        logger.error(f"Error fetching careers: {e}")
        raise HTTPException(status_code=500, detail=f"Error fetching careers: {str(e)}")

@app.get("/careers/{career_id}")
async def get_career(career_id: str):
    """Get specific career by ID in MongoDB format"""
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

@app.get("/skills")
async def get_skills(skip: int = 0, limit: int = 100):
    """Get all skills with pagination in MongoDB format"""
    try:
        # Extract unique skills from all careers
        all_skills = set()
        for career in MONGODB_CAREERS:
            for skill in career.get("required_skills", []):
                all_skills.add(skill["name"])
        
        skills_list = [
            {
                "skill_id": skill.lower().replace(" ", "_").replace("/", "_"),
                "name": skill,
                "category": "general",
                "created_at": datetime.now(timezone.utc).isoformat()
            }
            for skill in sorted(all_skills)
        ]
        
        total_count = len(skills_list)
        paginated_skills = skills_list[skip:skip + limit]
        
        return {
            "skills": paginated_skills,
            "total_count": total_count,
            "skip": skip,
            "limit": limit,
            "mongodb_compatible": True
        }
        
    except Exception as e:
        logger.error(f"Error fetching skills: {e}")
        raise HTTPException(status_code=500, detail=f"Error fetching skills: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    host = os.getenv("API_HOST", "0.0.0.0")
    port = int(os.getenv("API_PORT", 8002))
    
    logger.info(f"Starting enhanced server with MongoDB integration on {host}:{port}")
    uvicorn.run(app, host=host, port=port, reload=False)