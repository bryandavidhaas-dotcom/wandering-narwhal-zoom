"""
Minimal FastAPI backend server for testing
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Any, Optional

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

@app.get("/api/career/{career_type}")
async def get_career_detail(career_type: str):
    """Get detailed information about a specific career."""
    # Generate career data based on career type
    career_titles = {
        "vp-product": "VP of Product",
        "director-product-management": "Director of Product Management",
        "senior-product-manager": "Senior Product Manager",
        "product-manager": "Product Manager",
        "junior-product-manager": "Junior Product Manager"
    }
    
    title = career_titles.get(career_type, career_type.replace("-", " ").title())
    
    # Generate appropriate salary ranges based on seniority
    if "vp" in career_type.lower():
        salary_min, salary_max = 200000, 300000
        exp_level = "executive"
    elif "director" in career_type.lower():
        salary_min, salary_max = 150000, 200000
        exp_level = "senior"
    elif "senior" in career_type.lower():
        salary_min, salary_max = 120000, 160000
        exp_level = "senior"
    elif "junior" in career_type.lower():
        salary_min, salary_max = 80000, 110000
        exp_level = "junior"
    else:
        salary_min, salary_max = 100000, 140000
        exp_level = "mid"
    
    mock_career = {
        "title": title,
        "careerType": career_type,
        "description": f"Lead and manage {title.lower()} responsibilities with strategic focus",
        "salaryRange": f"${salary_min:,} - ${salary_max:,}",
        "requiredTechnicalSkills": ["Product Management", "Strategy", "Data Analysis", "User Research"],
        "requiredSoftSkills": ["Leadership", "Communication", "Strategic Thinking", "Problem Solving"],
        "companies": ["Google", "Microsoft", "Amazon", "Meta", "Netflix"],
        "experienceLevel": exp_level,
        "salaryMin": salary_min,
        "salaryMax": salary_max,
        "workEnvironments": ["office", "hybrid", "remote"],
        "remoteOptions": "Remote available",
        "dayInLife": f"Strategic planning, team management, stakeholder collaboration for {title.lower()} role"
    }
    return mock_career

@app.post("/api/recommendations")
async def get_recommendations_direct(request: Dict[str, Any]):
    """Direct API endpoint for frontend - returns mock recommendations"""
    # Mock recommendations for testing
    mock_recommendations = [
        {
            "title": "Director of Product Management",
            "careerType": "director-product-management",
            "zone": "safe",
            "relevanceScore": 95,
            "salaryMin": 150000,
            "salaryMax": 200000,
            "matchReasons": ["Strong product management background", "Leadership experience"]
        },
        {
            "title": "Senior Product Manager",
            "careerType": "senior-product-manager", 
            "zone": "safe",
            "relevanceScore": 90,
            "salaryMin": 120000,
            "salaryMax": 160000,
            "matchReasons": ["Direct role match", "Experience level alignment"]
        }
    ]
    
    return mock_recommendations

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8002)