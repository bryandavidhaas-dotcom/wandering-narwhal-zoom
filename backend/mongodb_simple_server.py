"""
Simplified MongoDB-compatible server for testing without complex dependencies.
This server provides MongoDB API integration with basic recommendation functionality.
"""

import logging
from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
from datetime import datetime
import os
import json
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import comprehensive career data
from comprehensive_careers import COMPREHENSIVE_CAREERS

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
logger.info("Initializing MongoDB-compatible FastAPI app...")
app = FastAPI(
    title="MongoDB-Compatible Career Recommendation API",
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
        "created_at": datetime.utcnow().isoformat(),
        "updated_at": datetime.utcnow().isoformat()
    }

def simple_recommendation_scoring(user_profile: Dict, career: Dict) -> float:
    """Simple scoring algorithm for recommendations"""
    score = 0.0
    
    # Skill matching (40% weight)
    user_skills = set(skill.lower() for skill in user_profile.get("skills", []))
    career_skills = set(skill.lower() for skill in career.get("requiredTechnicalSkills", []))
    
    if user_skills and career_skills:
        skill_overlap = len(user_skills.intersection(career_skills))
        skill_score = skill_overlap / max(len(user_skills), len(career_skills))
        score += skill_score * 0.4
    
    # Interest matching (30% weight)
    user_interests = set(interest.lower() for interest in user_profile.get("interests", []))
    career_text = f"{career.get('title', '')} {career.get('description', '')}".lower()
    interest_matches = sum(1 for interest in user_interests if interest in career_text)
    if user_interests:
        interest_score = interest_matches / len(user_interests)
        score += interest_score * 0.3
    
    # Experience level matching (20% weight)
    user_exp = user_profile.get("experience_level", "junior")
    career_exp = career.get("experienceLevel", "junior")
    if user_exp == career_exp:
        score += 0.2
    elif abs(["junior", "mid", "senior"].index(user_exp) - ["junior", "mid", "senior"].index(career_exp)) == 1:
        score += 0.1
    
    # Salary compatibility (10% weight)
    user_salary = user_profile.get("salary_expectation", 75000)
    career_min = career.get("minSalary", 50000)
    career_max = career.get("maxSalary", 80000)
    if career_min <= user_salary <= career_max:
        score += 0.1
    elif user_salary < career_min:
        # Penalty for salary too low
        score += max(0, 0.1 - (career_min - user_salary) / 50000)
    
    return min(score, 1.0)

def categorize_recommendation(score: float) -> str:
    """Categorize recommendation based on score"""
    if score >= 0.7:
        return "safe_zone"
    elif score >= 0.4:
        return "stretch_zone"
    else:
        return "adventure_zone"

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
        "engine_status": "simplified",
        "api_version": "2.0.0",
        "mongodb_compatible": True
    }

@app.post("/api/recommendations")
async def get_recommendations(request: UserProfileRequest):
    """Get career recommendations with MongoDB-compatible responses"""
    try:
        logger.info(f"Received recommendation request: {request.dict()}")
        
        # Score all careers
        scored_careers = []
        for career in career_data:
            score = simple_recommendation_scoring(request.dict(), career)
            scored_careers.append((career, score))
        
        # Sort by score and take top 10
        scored_careers.sort(key=lambda x: x[1], reverse=True)
        recommendations = []
        
        for career, score in scored_careers[:10]:
            # Find MongoDB version of this career
            mongodb_career = next(
                (c for c in MONGODB_CAREERS if c["career_id"] == career.get("careerType")), 
                None
            )
            
            # Create enhanced recommendation with both formats
            enhanced_rec = {
                **career,  # Keep original format for frontend compatibility
                "relevanceScore": int(score * 100),
                "confidenceLevel": int(score * 100),
                "zone": categorize_recommendation(score),
                "matchReasons": [
                    f"Skill match: {int(score * 100)}%",
                    f"Experience level: {career.get('experienceLevel', 'junior')}",
                    f"Salary range: ${career.get('minSalary', 50000):,} - ${career.get('maxSalary', 80000):,}"
                ],
                "mongodb_career": mongodb_career,  # Add MongoDB structure
                "database_source": "mongodb_compatible",
                "api_version": "2.0.0",
                "enhanced": True
            }
            
            recommendations.append(enhanced_rec)
        
        logger.info(f"Generated {len(recommendations)} recommendations")
        return recommendations
        
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
        
        # Score all careers
        scored_careers = []
        for career in career_data:
            score = simple_recommendation_scoring(user_profile.dict(), career)
            scored_careers.append((career, score))
        
        # Sort by score and take top limit
        scored_careers.sort(key=lambda x: x[1], reverse=True)
        
        # Convert to pure MongoDB response format
        mongodb_response = {
            "recommendations": [],
            "total_count": min(len(scored_careers), limit),
            "categories": {"safe_zone": 0, "stretch_zone": 0, "adventure_zone": 0},
            "cached": False,
            "generated_at": datetime.utcnow().isoformat()
        }
        
        for career, score in scored_careers[:limit]:
            # Map zones to MongoDB categories
            category = categorize_recommendation(score)
            mongodb_response["categories"][category] += 1
            
            # Find MongoDB career data
            mongodb_career = next(
                (c for c in MONGODB_CAREERS if c["career_id"] == career.get("careerType")), 
                None
            )
            
            mongodb_rec = {
                "career_id": career.get("careerType", "unknown"),
                "title": career.get("title", "Unknown"),
                "description": career.get("description", ""),
                "category": category,
                "score": score,  # 0-1 scale
                "confidence": score,  # 0-1 scale
                "reasons": [
                    f"Skill match: {int(score * 100)}%",
                    f"Experience level: {career.get('experienceLevel', 'junior')}",
                    f"Salary range: ${career.get('minSalary', 50000):,} - ${career.get('maxSalary', 80000):,}"
                ],
                "salary_range": mongodb_career["salary_range"] if mongodb_career else {
                    "min": career.get("minSalary", 50000),
                    "max": career.get("maxSalary", 80000),
                    "currency": "USD"
                },
                "created_at": datetime.utcnow().isoformat()
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
                "created_at": datetime.utcnow().isoformat()
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
    port = int(os.getenv("API_PORT", 8004))
    
    logger.info(f"Starting simplified MongoDB-compatible server on {host}:{port}")
    uvicorn.run(app, host=host, port=port, reload=True)