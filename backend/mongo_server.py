"""
FastAPI backend server with MongoDB integration for the Career Recommendation Engine.
"""

from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import database and models
from .database import connect_to_mongo, close_mongo_connection
from .models import (
    UserProfileModel, CareerModel, RecommendationModel, SkillModel,
    CreateUserProfileRequest, UpdateUserProfileRequest,
    RecommendationRequest, RecommendationResponse,
    RecommendationCategory, SkillLevel, Demand
)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    await connect_to_mongo()
    yield
    # Shutdown
    await close_mongo_connection()

# Initialize FastAPI app with lifespan
app = FastAPI(
    title="Career Recommendation API with MongoDB",
    description="API for career recommendations with MongoDB persistence",
    version="2.0.0",
    lifespan=lifespan
)

# Configure CORS
cors_origins = os.getenv("CORS_ORIGINS", "http://localhost:5137,http://localhost:3000,http://localhost:5173,https://wandering-narwhal-zoom-front-end.onrender.com").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Health check endpoint
@app.get("/health")
async def health_check():
    """Health check endpoint with database connectivity test."""
    try:
        # Test database connection
        await SkillModel.find_one()
        db_status = "connected"
    except Exception as e:
        db_status = f"error: {str(e)}"
    
    return {
        "status": "healthy",
        "message": "API is running",
        "database_status": db_status,
        "mongodb_url": os.getenv("MONGODB_URL", "not configured"),
        "database_name": os.getenv("MONGODB_DATABASE", "not configured")
    }

# User Profile endpoints
@app.post("/users", status_code=status.HTTP_201_CREATED)
async def create_user_profile(user_data: CreateUserProfileRequest):
    """Create a new user profile."""
    try:
        # Check if user already exists
        existing_user = await UserProfileModel.find_one(UserProfileModel.user_id == user_data.user_id)
        if existing_user:
            raise HTTPException(status_code=400, detail="User already exists")
        
        # Create new user profile
        user_profile = UserProfileModel(
            user_id=user_data.user_id,
            personal_info=user_data.personal_info or {},
            assessment_results=user_data.assessment_results or {},
            professional_data=user_data.professional_data or {},
            skills=user_data.skills,
            user_interests=user_data.user_interests
        )
        
        await user_profile.insert()
        return {"message": "User profile created successfully", "user_id": user_data.user_id}
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating user profile: {str(e)}")

@app.get("/users/{user_id}")
async def get_user_profile(user_id: str):
    """Get user profile by ID."""
    try:
        user_profile = await UserProfileModel.find_one(UserProfileModel.user_id == user_id)
        if not user_profile:
            raise HTTPException(status_code=404, detail="User not found")
        
        return user_profile
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching user profile: {str(e)}")

@app.put("/users/{user_id}")
async def update_user_profile(user_id: str, update_data: UpdateUserProfileRequest):
    """Update user profile."""
    try:
        user_profile = await UserProfileModel.find_one(UserProfileModel.user_id == user_id)
        if not user_profile:
            raise HTTPException(status_code=404, detail="User not found")
        
        # Update fields if provided
        update_dict = {}
        if update_data.personal_info is not None:
            update_dict["personal_info"] = update_data.personal_info
        if update_data.assessment_results is not None:
            update_dict["assessment_results"] = update_data.assessment_results
        if update_data.professional_data is not None:
            update_dict["professional_data"] = update_data.professional_data
        if update_data.skills is not None:
            update_dict["skills"] = update_data.skills
        if update_data.user_interests is not None:
            update_dict["user_interests"] = update_data.user_interests
        
        update_dict["updated_at"] = datetime.utcnow()
        
        await user_profile.update({"$set": update_dict})
        return {"message": "User profile updated successfully"}
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error updating user profile: {str(e)}")

# Career endpoints
@app.get("/careers")
async def get_careers(skip: int = 0, limit: int = 100):
    """Get all careers with pagination."""
    try:
        careers = await CareerModel.find_all().skip(skip).limit(limit).to_list()
        total_count = await CareerModel.count()
        
        return {
            "careers": careers,
            "total_count": total_count,
            "skip": skip,
            "limit": limit
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching careers: {str(e)}")

@app.get("/careers/{career_id}")
async def get_career(career_id: str):
    """Get specific career by ID."""
    try:
        career = await CareerModel.find_one(CareerModel.career_id == career_id)
        if not career:
            raise HTTPException(status_code=404, detail="Career not found")
        
        return career
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching career: {str(e)}")

# Skills endpoints
@app.get("/skills")
async def get_skills(skip: int = 0, limit: int = 100):
    """Get all skills with pagination."""
    try:
        skills = await SkillModel.find_all().skip(skip).limit(limit).to_list()
        total_count = await SkillModel.count()
        
        return {
            "skills": skills,
            "total_count": total_count,
            "skip": skip,
            "limit": limit
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching skills: {str(e)}")

# Recommendation endpoints
@app.post("/recommendations")
async def get_recommendations(request: RecommendationRequest):
    """Get career recommendations for a user."""
    try:
        # Check if user exists
        user_profile = await UserProfileModel.find_one(UserProfileModel.user_id == request.user_id)
        if not user_profile:
            raise HTTPException(status_code=404, detail="User not found")
        
        # Check for cached recommendations (if not forcing refresh)
        if not request.force_refresh:
            cached_recs = await RecommendationModel.find(
                RecommendationModel.user_id == request.user_id,
                RecommendationModel.expires_at > datetime.utcnow()
            ).limit(request.limit).to_list()
            
            if cached_recs:
                # Return cached recommendations
                recommendations = []
                categories = {"safe_zone": 0, "stretch_zone": 0, "adventure_zone": 0}
                
                for rec in cached_recs:
                    categories[rec.category.value] += 1
                    career = await CareerModel.find_one(CareerModel.career_id == rec.career_id)
                    
                    recommendations.append({
                        "career_id": rec.career_id,
                        "title": career.title if career else "Unknown Career",
                        "category": rec.category.value,
                        "score": rec.score.total_score,
                        "confidence": rec.confidence,
                        "reasons": rec.reasons,
                        "created_at": rec.created_at
                    })
                
                return RecommendationResponse(
                    recommendations=recommendations,
                    total_count=len(recommendations),
                    categories=categories,
                    cached=True,
                    generated_at=cached_recs[0].created_at if cached_recs else datetime.utcnow()
                )
        
        # Generate new recommendations (simplified mock for now)
        # In production, this would use the actual recommendation engine
        careers = await CareerModel.find_all().limit(request.limit).to_list()
        recommendations = []
        categories = {"safe_zone": 0, "stretch_zone": 0, "adventure_zone": 0}
        
        for i, career in enumerate(careers):
            # Simple scoring logic (replace with actual engine)
            score = 0.8 - (i * 0.1)
            category = RecommendationCategory.SAFE_ZONE if score > 0.7 else \
                      RecommendationCategory.STRETCH_ZONE if score > 0.5 else \
                      RecommendationCategory.ADVENTURE_ZONE
            
            categories[category.value] += 1
            
            # Save recommendation to database
            rec_model = RecommendationModel(
                user_id=request.user_id,
                career_id=career.career_id,
                score={
                    "career_id": career.career_id,
                    "total_score": score,
                    "skill_match_score": score,
                    "interest_match_score": score * 0.9,
                    "salary_compatibility_score": score * 1.1,
                    "experience_match_score": score * 0.95,
                    "breakdown": {}
                },
                category=category,
                reasons=[f"Good match for {career.title}", "Aligns with your profile"],
                confidence=score,
                expires_at=datetime.utcnow() + timedelta(hours=24)  # Cache for 24 hours
            )
            await rec_model.insert()
            
            recommendations.append({
                "career_id": career.career_id,
                "title": career.title,
                "description": career.description,
                "category": category.value,
                "score": score,
                "confidence": score,
                "reasons": rec_model.reasons,
                "salary_range": {
                    "min": career.salary_range.min,
                    "max": career.salary_range.max,
                    "currency": career.salary_range.currency
                }
            })
        
        return RecommendationResponse(
            recommendations=recommendations,
            total_count=len(recommendations),
            categories=categories,
            cached=False,
            generated_at=datetime.utcnow()
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating recommendations: {str(e)}")

@app.get("/recommendations/{user_id}/history")
async def get_recommendation_history(user_id: str, skip: int = 0, limit: int = 50):
    """Get recommendation history for a user."""
    try:
        recommendations = await RecommendationModel.find(
            RecommendationModel.user_id == user_id
        ).sort(-RecommendationModel.created_at).skip(skip).limit(limit).to_list()
        
        return {
            "recommendations": recommendations,
            "total_count": len(recommendations),
            "skip": skip,
            "limit": limit
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching recommendation history: {str(e)}")

# Database management endpoints
@app.post("/admin/seed-data")
async def seed_database():
    """Seed the database with initial data (for development)."""
    try:
        # Check if data already exists
        skill_count = await SkillModel.count()
        career_count = await CareerModel.count()
        
        if skill_count > 0 or career_count > 0:
            return {"message": "Database already contains data", "skills": skill_count, "careers": career_count}
        
        # Seed skills
        skills_data = [
            {"skill_id": "skill_1", "name": "Python", "category": "Programming Language"},
            {"skill_id": "skill_2", "name": "JavaScript", "category": "Programming Language"},
            {"skill_id": "skill_3", "name": "Data Analysis", "category": "Technical Skill"},
            {"skill_id": "skill_4", "name": "Machine Learning", "category": "Technical Skill"},
            {"skill_id": "skill_5", "name": "Project Management", "category": "Soft Skill"},
        ]
        
        for skill_data in skills_data:
            skill = SkillModel(**skill_data)
            await skill.insert()
        
        # Seed careers
        careers_data = [
            {
                "career_id": "career_1",
                "title": "Data Scientist",
                "description": "Analyzes complex data to help organizations make informed decisions.",
                "salary_range": {"min": 90000, "max": 140000, "currency": "USD"},
                "demand": Demand.HIGH,
                "required_skills": [
                    {"skill_id": "skill_1", "name": "Python", "proficiency": SkillLevel.ADVANCED, "is_mandatory": True},
                    {"skill_id": "skill_3", "name": "Data Analysis", "proficiency": SkillLevel.ADVANCED, "is_mandatory": True}
                ]
            },
            {
                "career_id": "career_2",
                "title": "Full Stack Developer",
                "description": "Develops both front-end and back-end components of web applications.",
                "salary_range": {"min": 70000, "max": 120000, "currency": "USD"},
                "demand": Demand.HIGH,
                "required_skills": [
                    {"skill_id": "skill_2", "name": "JavaScript", "proficiency": SkillLevel.ADVANCED, "is_mandatory": True}
                ]
            }
        ]
        
        for career_data in careers_data:
            career = CareerModel(**career_data)
            await career.insert()
        
        return {"message": "Database seeded successfully", "skills": len(skills_data), "careers": len(careers_data)}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error seeding database: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    host = os.getenv("API_HOST", "0.0.0.0")
    port = int(os.getenv("API_PORT", 8000))
    uvicorn.run(app, host=host, port=port, reload=True)