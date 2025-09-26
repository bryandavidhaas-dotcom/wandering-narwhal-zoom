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
        # For demo purposes, return mock recommendations
        # In production, this would use the actual recommendation engine
        recommendations = MOCK_CAREERS[:request.limit] if request.limit else MOCK_CAREERS
        
        # Count categories
        categories = {"safe_zone": 0, "stretch_zone": 0, "adventure_zone": 0}
        for rec in recommendations:
            categories[rec["category"]] += 1
        
        return RecommendationResponse(
            recommendations=recommendations,
            total_count=len(recommendations),
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
        # Import the comprehensive career database (same as used in recommendations)
        try:
            from comprehensive_careers import COMPREHENSIVE_CAREERS
        except ImportError:
            # Fallback to relative import
            import sys
            import os
            sys.path.append(os.path.dirname(os.path.abspath(__file__)))
            from comprehensive_careers import COMPREHENSIVE_CAREERS
        
        # First try to find in comprehensive careers database (same as dashboard uses)
        career = next((c for c in COMPREHENSIVE_CAREERS if c.get("careerType") == career_type), None)
        if career:
            # Return the same detailed career data that the dashboard uses
            return career
        
        # If not found in comprehensive database, try existing CAREER_DATA as fallback
        career = next((c for c in CAREER_DATA if c.get("careerType") == career_type), None)
        if career:
            return career
        
        # If still not found, generate dynamic career data (fallback)
        career_titles = {
            "vp-product": "VP of Product",
            "director-product-management": "Director of Product Management",
            "senior-product-manager": "Senior Product Manager",
            "product-manager": "Product Manager",
            "junior-product-manager": "Junior Product Manager",
            "head-of-product": "Head of Product"
        }
        
        title = career_titles.get(career_type, career_type.replace("-", " ").title())
        
        # Generate appropriate salary ranges based on seniority
        if "vp" in career_type.lower() or "head" in career_type.lower():
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
        
        dynamic_career = {
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
        
        return dynamic_career
        
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
        
        # For now, return enhanced mock data based on user profile
        # TODO: Integrate with the actual recommendation engine
        enhanced_recommendations = generate_enhanced_recommendations(user_data, request.explorationLevel or 1)
        
        print(f"✅ Generated {len(enhanced_recommendations)} recommendations")
        return enhanced_recommendations
        
    except Exception as e:
        print(f"❌ Error in /api/recommendations: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to generate recommendations: {str(e)}")

def calculate_dynamic_distribution(exploration_level: int) -> tuple[int, int, int, int]:
    """
    Calculate dynamic distribution based on exploration level (1-5 scale).
    Returns (safe_target, stretch_target, adventure_target, total_target)
    
    Exploration Level Distribution Strategy:
    - Level 1 (Conservative): Heavy Safe Zone focus - 5 Safe, 3 Stretch, 1 Adventure (9 total)
    - Level 2 (Cautious): Safe Zone preference - 4 Safe, 4 Stretch, 2 Adventure (10 total)
    - Level 3 (Balanced): Equal distribution - 3 Safe, 4 Stretch, 4 Adventure (11 total)
    - Level 4 (Adventurous): Adventure Zone focus - 2 Safe, 4 Stretch, 5 Adventure (11 total)
    - Level 5 (Explorer): Maximum Adventure - 2 Safe, 3 Stretch, 6 Adventure (11 total)
    """
    # Ensure exploration level is within valid range
    exploration_level = max(1, min(5, exploration_level or 1))
    
    distribution_map = {
        1: (5, 3, 1, 9),   # Conservative: Heavy Safe Zone
        2: (4, 4, 2, 10),  # Cautious: Safe Zone preference
        3: (3, 4, 4, 11),  # Balanced: Equal focus on Stretch/Adventure
        4: (2, 4, 5, 11),  # Adventurous: Adventure Zone focus
        5: (2, 3, 6, 11)   # Explorer: Maximum Adventure
    }
    
    safe_target, stretch_target, adventure_target, total_target = distribution_map[exploration_level]
    
    print(f"🎯 Exploration Level {exploration_level} Distribution:")
    print(f"   Safe Zone: {safe_target} recommendations")
    print(f"   Stretch Zone: {stretch_target} recommendations")
    print(f"   Adventure Zone: {adventure_target} recommendations")
    print(f"   Total Target: {total_target} recommendations")
    
    return safe_target, stretch_target, adventure_target, total_target

def generate_enhanced_recommendations(user_data: Dict[str, Any], exploration_level: int) -> List[Dict[str, Any]]:
    """
    Generate enhanced recommendations based on user profile using comprehensive career database
    
    ⚠️  CRITICAL SAFETY GUARDRAILS IMPLEMENTED ⚠️
    This function includes mandatory safety checks to prevent recommending safety-critical
    careers (like medical professionals) to users without proper qualifications.
    DO NOT REMOVE OR MODIFY THESE SAFETY CHECKS WITHOUT CAREFUL REVIEW.
    """
    
    # Import the comprehensive career database
    try:
        from comprehensive_careers import (
            COMPREHENSIVE_CAREERS,
            get_careers_by_experience_level,
            get_careers_by_salary_range,
            parse_experience_years,
            parse_salary_expectations
        )
    except ImportError:
        # Fallback to relative import
        import sys
        import os
        sys.path.append(os.path.dirname(os.path.abspath(__file__)))
        from comprehensive_careers import (
            COMPREHENSIVE_CAREERS,
            get_careers_by_experience_level,
            get_careers_by_salary_range,
            parse_experience_years,
            parse_salary_expectations
        )
    
    # Extract insights from resume and LinkedIn profile
    resume_insights = extract_resume_insights(user_data.get("resume_text", ""))
    linkedin_insights = extract_linkedin_insights(user_data.get("linkedin_profile", ""))
    
    print(f"📄 Resume insights: {resume_insights}")
    print(f"💼 LinkedIn insights: {linkedin_insights}")
    
    # Parse user experience and salary expectations
    experience_years = parse_experience_years(user_data.get("experience", ""))
    min_salary, max_salary = parse_salary_expectations(user_data.get("salary_expectations", ""))
    
    print(f"👤 User profile: {experience_years} years experience, ${min_salary:,}-${max_salary:,} salary target")
    
    # Filter careers by experience level and salary expectations
    experience_filtered = get_careers_by_experience_level(experience_years)
    salary_filtered = get_careers_by_salary_range(min_salary, max_salary)
    
    # Get intersection of both filters
    filtered_careers = [career for career in experience_filtered if career in salary_filtered]
    
    print(f"🔍 Filtered careers: {len(filtered_careers)} careers match experience and salary criteria")
    
    # ⚠️  CRITICAL SAFETY GUARDRAILS: Filter out safety-critical careers for unqualified users
    # This prevents dangerous recommendations like suggesting Product Managers become Nurse Anesthetists
    safety_filtered_careers = []
    for career in filtered_careers:
        try:
            if is_safety_critical_career(career):
                if has_relevant_background_for_safety_critical(career, user_data, resume_insights):
                    safety_filtered_careers.append(career)
                    print(f"✅ SAFETY CHECK PASSED: {career.get('title', '')} - user has relevant background")
                else:
                    print(f"🚫 SAFETY CHECK FAILED: {career.get('title', '')} - BLOCKED for safety (user lacks medical/licensed background)")
            else:
                safety_filtered_careers.append(career)
        except Exception as e:
            print(f"❌ ERROR in safety filtering for career {career.get('title', 'Unknown')}: {str(e)}")
            # Skip this career if there's an error
            continue
    
    # Update filtered careers to use safety-filtered list
    filtered_careers = safety_filtered_careers
    print(f"🛡️  After safety filtering: {len(filtered_careers)} careers remain")
    
    # NEW: PREREQUISITE CHECKING: Flag careers requiring specific backgrounds
    # This doesn't block careers but adds metadata for Adventure Zone indicators
    prerequisite_checked_careers = []
    for career in filtered_careers:
        try:
            career_copy = career.copy()
            
            if requires_specific_background(career):
                has_background = has_relevant_background_for_prerequisites(career, user_data, resume_insights)
                career_copy["requires_prerequisites"] = True
                career_copy["has_required_background"] = has_background
                
                if has_background:
                    print(f"✅ PREREQUISITE CHECK PASSED: {career.get('title', '')} - user has relevant background")
                else:
                    print(f"⚠️  PREREQUISITE CHECK: {career.get('title', '')} - user lacks specific background (will show in Adventure Zone with warning)")
            else:
                career_copy["requires_prerequisites"] = False
                career_copy["has_required_background"] = True
            
            prerequisite_checked_careers.append(career_copy)
        except Exception as e:
            print(f"❌ ERROR in prerequisite checking for career {career.get('title', 'Unknown')}: {str(e)}")
            # Add career without prerequisite metadata if there's an error
            career_copy = career.copy()
            career_copy["requires_prerequisites"] = False
            career_copy["has_required_background"] = True
            prerequisite_checked_careers.append(career_copy)
    
    # Update filtered careers to use prerequisite-checked list
    filtered_careers = prerequisite_checked_careers
    print(f"🎯 After prerequisite checking: {len(filtered_careers)} careers remain")
    
    # ENHANCED: Apply trades/medical filtering immediately after safety filtering
    # Check if user has minimal profile OR lacks relevant trades/medical background
    has_minimal_profile = (
        not user_data.get("resume_text") or len(user_data.get("resume_text", "")) < 50
    ) and (
        not user_data.get("technical_skills") or len(user_data.get("technical_skills", [])) == 0
    )
    
    # Check if user has trades-relevant skills
    user_technical_skills = user_data.get("technical_skills", [])
    
    # Ensure we have a valid list of strings
    if user_technical_skills is None:
        user_technical_skills = []
    
    # Filter out None values and ensure all are strings
    user_technical_skills = [str(skill) for skill in user_technical_skills if skill is not None]
    
    trades_relevant_skills = [
        "electrical", "plumbing", "hvac", "welding", "carpentry", "mechanical", "automotive",
        "construction", "maintenance", "machining", "fabrication", "installation", "repair"
    ]
    has_trades_skills = any(
        any(trades_skill in skill.lower() for trades_skill in trades_relevant_skills)
        for skill in user_technical_skills
    )
    
    # Check if user has medical-relevant skills
    medical_relevant_skills = [
        "medical", "clinical", "healthcare", "patient", "nursing", "laboratory", "radiology",
        "pharmacy", "medical equipment", "medical device", "healthcare technology"
    ]
    has_medical_skills = any(
        any(medical_skill in skill.lower() for medical_skill in medical_relevant_skills)
        for skill in user_technical_skills
    )
    
    # ENHANCED: Apply more comprehensive skills-based filtering
    user_field = identify_user_field(resume_insights, user_data)
    
    # Apply filtering for users without relevant background
    should_filter_trades_medical = has_minimal_profile or (not has_trades_skills and not has_medical_skills)
    
    if should_filter_trades_medical:
        if has_minimal_profile:
            print("👤 MINIMAL PROFILE DETECTED - Applying comprehensive filtering")
        else:
            print("👤 NO TRADES/MEDICAL SKILLS DETECTED - Filtering inappropriate careers")
            print(f"🔧 User skills: {user_technical_skills}")
            print(f"🔧 Has trades skills: {has_trades_skills}")
            print(f"🏥 Has medical skills: {has_medical_skills}")
        
        inappropriate_careers = [
            "medical equipment technician", "clinical research coordinator", "plumber",
            "electrician", "hvac technician", "welder", "carpenter", "mechanic",
            "radiologic technologist", "medical laboratory technologist", "pharmacy technician",
            "diesel mechanic", "auto body technician", "sheet metal worker", "boilermaker",
            "pipefitter", "mason", "roofer", "concrete finisher", "drywall installer",
            "flooring installer", "heavy equipment operator", "automotive technician",
            "motorcycle technician", "machinist", "cnc operator", "industrial maintenance technician",
            "millwright", "glazier", "insulation worker", "power line technician", "locksmith",
            "refrigeration technician", "industrial electrician"
        ]
        
        trades_filtered_careers = []
        for career in filtered_careers:
            career_title_lower = career.get("title", "").lower()
            if any(inappropriate in career_title_lower for inappropriate in inappropriate_careers):
                if has_minimal_profile:
                    print(f"❌ MINIMAL PROFILE FILTER: Blocked {career['title']} - inappropriate for minimal profile user")
                else:
                    print(f"❌ SKILLS FILTER: Blocked {career['title']} - user lacks relevant trades/medical background")
            else:
                trades_filtered_careers.append(career)
        
        filtered_careers = trades_filtered_careers
        print(f"🔍 After trades/medical filtering: {len(filtered_careers)} careers remain")
    
    # ENHANCED: Additional field-based filtering to prevent cross-field recommendations
    if user_field != "unknown":
        print(f"🎯 User field identified as: {user_field} - Applying field-based filtering")
        
        # Define highly inappropriate cross-field recommendations to block
        field_blocks = {
            "skilled_trades": [
                # Block business/marketing roles for trades people
                "junior product manager", "marketing analyst", "digital marketing specialist",
                "content creator", "social media manager", "account manager", "business analyst"
            ],
            "sales_marketing": [
                # Block hospitality management for marketing people (unless they have hospitality experience)
                "restaurant manager", "spa manager", "banquet manager", "hotel manager",
                "front desk manager", "concierge"
            ]
        }
        
        if user_field in field_blocks:
            blocked_titles = field_blocks[user_field]
            field_filtered_careers = []
            
            for career in filtered_careers:
                career_title_lower = career.get("title", "").lower()
                should_block = False
                
                for blocked_title in blocked_titles:
                    if blocked_title in career_title_lower:
                        # Special exception: Allow if user has relevant industry experience
                        if user_field == "sales_marketing" and "manager" in blocked_title:
                            # Check if user has hospitality industry experience
                            industry_indicators = resume_insights.get("industry_indicators", [])
                            if "hospitality" in industry_indicators or any(
                                hosp_word in user_data.get("resume_text", "").lower()
                                for hosp_word in ["restaurant", "hotel", "hospitality", "service industry"]
                            ):
                                print(f"✅ EXCEPTION: Allowing {career['title']} - user has hospitality experience")
                                continue
                        
                        should_block = True
                        print(f"❌ FIELD FILTER: Blocked {career['title']} - inappropriate cross-field recommendation for {user_field} user")
                        break
                
                if not should_block:
                    field_filtered_careers.append(career)
            
            filtered_careers = field_filtered_careers
            print(f"🔍 After field-based filtering: {len(filtered_careers)} careers remain")
    
    # If no careers match strict criteria, relax OTHER requirements but MAINTAIN salary filtering
    if len(filtered_careers) < 3:
        print("⚠️  Relaxing experience requirements but MAINTAINING salary filtering to prevent inappropriate recommendations")
        
        # CRITICAL FIX: Apply salary filter to broader experience range instead of removing salary filter entirely
        # Get careers with broader experience range but still within salary expectations
        broader_experience_careers = []
        for career in COMPREHENSIVE_CAREERS[:50]:  # Look at more careers
            career_min = career.get("minSalary", 0)
            career_max = career.get("maxSalary", 0)
            # MAINTAIN salary compatibility check
            if career_min <= max_salary and career_max >= min_salary:
                broader_experience_careers.append(career)
        
        print(f"🔍 Broader experience + salary filter: {len(broader_experience_careers)} careers found")
        
        # Apply safety filtering to salary-compatible careers
        safety_filtered_relaxed = []
        for career in broader_experience_careers:
            if is_safety_critical_career(career):
                if has_relevant_background_for_safety_critical(career, user_data, resume_insights):
                    safety_filtered_relaxed.append(career)
                    print(f"✅ RELAXED SAFETY CHECK PASSED: {career.get('title', '')} - user has relevant background")
                else:
                    print(f"🚫 RELAXED SAFETY CHECK FAILED: {career.get('title', '')} - BLOCKED for safety")
            else:
                safety_filtered_relaxed.append(career)
        
        # Apply trades/medical filtering to relaxed careers too
        if should_filter_trades_medical:
            trades_filtered_relaxed = []
            for career in safety_filtered_relaxed:
                career_title_lower = career.get("title", "").lower()
                if any(inappropriate in career_title_lower for inappropriate in inappropriate_careers):
                    print(f"❌ RELAXED FILTER: Blocked {career['title']} - inappropriate for user background")
                else:
                    trades_filtered_relaxed.append(career)
            filtered_careers = trades_filtered_relaxed
        else:
            filtered_careers = safety_filtered_relaxed
    
    # FINAL FALLBACK: If still not enough, apply MINIMUM salary threshold to prevent extreme mismatches
    if len(filtered_careers) < 3:
        print("⚠️  Final fallback: Applying minimum salary threshold to prevent extreme mismatches")
        
        # Calculate minimum acceptable salary (50% of user's minimum expectation)
        minimum_threshold = max(min_salary * 0.5, 40000)  # Never go below $40k for executive-level users
        print(f"💰 Minimum salary threshold: ${minimum_threshold:,.0f} (50% of user minimum: ${min_salary:,.0f})")
        
        # Check if user has minimal profile
        has_minimal_profile = (
            not user_data.get("resume_text") or len(user_data.get("resume_text", "")) < 50
        ) and (
            not user_data.get("technical_skills") or len(user_data.get("technical_skills", [])) == 0
        )
        
        if has_minimal_profile:
            print("👤 Minimal profile detected - prioritizing general business/tech roles")
            # For minimal profiles, prioritize general business and entry-level tech roles
            preferred_titles = [
                "data analyst", "business analyst", "marketing", "customer success",
                "project manager", "account manager", "sales", "administrative",
                "coordinator", "specialist", "junior", "associate", "entry"
            ]
            
            # Filter COMPREHENSIVE_CAREERS to prioritize general roles for minimal profiles
            general_careers = []
            trades_careers = []
            
            for career in COMPREHENSIVE_CAREERS[:30]:  # Look at more careers
                # CRITICAL: Apply minimum salary threshold even in final fallback
                career_max = career.get("maxSalary", 0)
                if career_max < minimum_threshold:
                    print(f"❌ SALARY THRESHOLD: Blocked {career.get('title', '')} - max salary ${career_max:,.0f} below threshold ${minimum_threshold:,.0f}")
                    continue
                
                title_lower = career.get("title", "").lower()
                is_general_role = any(keyword in title_lower for keyword in preferred_titles)
                is_trades_role = any(keyword in title_lower for keyword in [
                    "electrician", "plumber", "welder", "mechanic", "technician",
                    "carpenter", "hvac", "diesel", "equipment operator"
                ])
                
                if is_general_role and not is_trades_role:
                    general_careers.append(career)
                elif is_trades_role:
                    trades_careers.append(career)
                else:
                    general_careers.append(career)  # Default to general
            
            # Prioritize general careers for minimal profiles
            broad_careers = general_careers[:20] + trades_careers[:5]
        else:
            # For experienced users, apply salary threshold to all careers
            broad_careers = []
            for career in COMPREHENSIVE_CAREERS[:25]:
                career_max = career.get("maxSalary", 0)
                if career_max >= minimum_threshold:
                    broad_careers.append(career)
                else:
                    print(f"❌ SALARY THRESHOLD: Blocked {career.get('title', '')} - max salary ${career_max:,.0f} below threshold ${minimum_threshold:,.0f}")
        
        safety_filtered_broad = []
        for career in broad_careers:
            if is_safety_critical_career(career):
                if has_relevant_background_for_safety_critical(career, user_data, resume_insights):
                    safety_filtered_broad.append(career)
                    print(f"✅ BROAD SAFETY CHECK PASSED: {career.get('title', '')} - user has relevant background")
                else:
                    print(f"🚫 BROAD SAFETY CHECK FAILED: {career.get('title', '')} - BLOCKED for safety")
            else:
                safety_filtered_broad.append(career)
        filtered_careers = safety_filtered_broad
        
        print(f"🛡️  After final salary threshold filtering: {len(filtered_careers)} careers remain")
    
    # Enhanced scoring algorithm with career path consistency penalty
    scored_careers = []
    
    # Get keyword frequencies and dominant theme from resume
    keyword_frequencies = resume_insights.get("keyword_frequencies", {})
    dominant_theme = resume_insights.get("dominant_theme")
    
    # CAREER PATH CONSISTENCY: Define career field categories and adjacency
    career_field_categories = get_career_field_categories()
    field_adjacency_map = get_field_adjacency_map()
    
    for career in filtered_careers:
        # IMPROVED: Base score varies based on user profile completeness
        # Users with minimal profiles get lower base scores to prevent irrelevant recommendations
        profile_completeness = 0
        if user_data.get("resume_text") and len(user_data.get("resume_text", "")) > 50:
            profile_completeness += 20
        if user_data.get("technical_skills") and len(user_data.get("technical_skills", [])) > 0:
            profile_completeness += 15
        if user_data.get("current_role") and user_data.get("current_role") != "":
            profile_completeness += 10
        if user_data.get("experience") and user_data.get("experience") != "":
            profile_completeness += 5
        
        # Base score: 30 for minimal profiles, up to 50 for complete profiles
        base_score = 30 + min(20, profile_completeness)
        
        # CAREER PATH CONSISTENCY PENALTY: Identify career field and apply penalties
        career_field = identify_career_field(career)
        user_field = identify_user_field(resume_insights, user_data)
        consistency_penalty = calculate_consistency_penalty(career_field, user_field, field_adjacency_map, dominant_theme, keyword_frequencies, exploration_level)
        
        print(f"🔍 Career: '{career.get('title', '')}' | Field: {career_field} | User Field: {user_field} | Consistency Penalty: {consistency_penalty}")
        
        # ENHANCED: Keyword frequency-based role matching
        role_boost = 0
        theme_alignment_boost = 0
        user_current_role = resume_insights.get("current_role")
        user_roles = resume_insights.get("roles", [])
        career_title = career.get("title", "").lower()
        career_desc = career.get("description", "").lower()
        
        print(f"🔍 Matching career '{career_title}' against dominant theme: {dominant_theme}")
        
        # PRIORITY 1: Keyword frequency-based matching
        product_freq = keyword_frequencies.get("product", 0)
        engineering_freq = keyword_frequencies.get("engineering", 0)
        data_science_freq = keyword_frequencies.get("data_science", 0)
        management_freq = keyword_frequencies.get("management", 0)
        communications_freq = keyword_frequencies.get("communications", 0)
        creative_freq = keyword_frequencies.get("creative", 0)
        
        # ENHANCED: Role categorization
        is_product_role = any(keyword in career_title for keyword in [
            "product manager", "product lead", "head of product", "vp product",
            "chief product officer", "director of product", "principal product", "group product"
        ])
        
        is_technical_role = any(keyword in career_title for keyword in [
            "engineer", "scientist", "developer", "analyst", "architect"
        ])
        
        is_communications_role = any(keyword in career_title for keyword in [
            "marketing", "communications", "social media", "content", "copywriter",
            "public relations", "pr", "brand", "campaign", "digital marketing",
            "content marketing", "social media marketing", "community manager"
        ])
        
        is_creative_role = any(keyword in career_title for keyword in [
            "designer", "creative", "graphic", "visual", "art director", "creative director",
            "ux designer", "ui designer", "web designer", "video editor", "photographer", "illustrator"
        ])
        
        # COMMUNICATIONS & MARKETING role matching with frequency weighting
        if is_communications_role and communications_freq >= 10:  # Very strong communications signal
            theme_alignment_boost = 45
            print(f"📢 VERY STRONG COMMUNICATIONS ALIGNMENT: {career_title} gets +45 boost ({communications_freq} mentions)")
        elif is_communications_role and communications_freq >= 5:  # Strong communications signal
            theme_alignment_boost = 35
            print(f"📢 STRONG COMMUNICATIONS ALIGNMENT: {career_title} gets +35 boost ({communications_freq} mentions)")
        elif is_communications_role and communications_freq >= 2:  # Moderate communications signal
            theme_alignment_boost = 25
            print(f"📢 MODERATE COMMUNICATIONS ALIGNMENT: {career_title} gets +25 boost ({communications_freq} mentions)")
        elif is_communications_role:  # Communications role without strong resume signal
            theme_alignment_boost = 15
            print(f"📢 COMMUNICATIONS ROLE: {career_title} gets +15 boost")
        
        # CREATIVE role matching with frequency weighting
        elif is_creative_role and creative_freq >= 10:  # Very strong creative signal
            theme_alignment_boost = 45
            print(f"🎨 VERY STRONG CREATIVE ALIGNMENT: {career_title} gets +45 boost ({creative_freq} mentions)")
        elif is_creative_role and creative_freq >= 5:  # Strong creative signal
            theme_alignment_boost = 35
            print(f"🎨 STRONG CREATIVE ALIGNMENT: {career_title} gets +35 boost ({creative_freq} mentions)")
        elif is_creative_role and creative_freq >= 2:  # Moderate creative signal
            theme_alignment_boost = 25
            print(f"🎨 MODERATE CREATIVE ALIGNMENT: {career_title} gets +25 boost ({creative_freq} mentions)")
        elif is_creative_role:  # Creative role without strong resume signal
            theme_alignment_boost = 15
            print(f"🎨 CREATIVE ROLE: {career_title} gets +15 boost")
        
        # Product role matching with frequency weighting
        elif is_product_role and product_freq >= 10:  # Very strong product signal
            theme_alignment_boost = 45
            print(f"🎯 VERY STRONG PRODUCT ALIGNMENT: {career_title} gets +45 boost ({product_freq} mentions)")
        elif is_product_role and product_freq >= 5:  # Strong product signal
            theme_alignment_boost = 35
            print(f"🎯 STRONG PRODUCT ALIGNMENT: {career_title} gets +35 boost ({product_freq} mentions)")
        elif is_product_role and product_freq >= 2:  # Moderate product signal
            theme_alignment_boost = 25
            print(f"🎯 MODERATE PRODUCT ALIGNMENT: {career_title} gets +25 boost ({product_freq} mentions)")
        
        # REDUCED BIAS: Technical roles get penalties unless resume emphasizes them
        elif is_technical_role:
            if engineering_freq >= 5 or data_science_freq >= 5:
                theme_alignment_boost = 15  # Reduced boost even with technical emphasis
                print(f"🔧 Technical role with resume support: {career_title} gets +15 boost")
            else:
                theme_alignment_boost = -15  # Stronger penalty for technical roles without emphasis
                print(f"⚠️ Technical role without resume emphasis: {career_title} gets -15 penalty")
        
        # FIXED: Management roles only get boost if they're in related fields
        elif "manager" in career_title or "director" in career_title:
            # Check if it's a relevant management role based on user's field
            user_field = identify_user_field(resume_insights, user_data)
            career_field = identify_career_field(career)
            
            # Only boost management roles in same or adjacent fields
            if user_field != "unknown" and career_field != "unknown":
                adjacency_score = field_adjacency_map.get(user_field, {}).get(career_field, 0)
                if adjacency_score >= 1:  # Same or adjacent field
                    if management_freq >= 3:
                        theme_alignment_boost = 20
                        print(f"👔 Relevant management role with resume support: {career_title} gets +20 boost")
                    else:
                        theme_alignment_boost = 5
                        print(f"👔 Relevant management role: {career_title} gets +5 boost")
                else:
                    # Unrelated management role gets penalty instead of boost
                    theme_alignment_boost = -10
                    print(f"⚠️ Unrelated management role: {career_title} gets -10 penalty")
            else:
                # Unknown fields get small boost only
                theme_alignment_boost = 2
                print(f"👔 Management role (unknown field): {career_title} gets +2 boost")
        
        # Traditional role matching (reduced weight)
        if user_current_role:
            if user_current_role == "Product Management":
                if any(keyword in career_title for keyword in ["product manager", "product lead", "head of product", "vp product", "chief product officer"]):
                    role_boost = 20  # Reduced from 40 since theme_alignment_boost handles this better
                    print(f"🎯 Traditional PM match: {career_title} gets +20 boost")
                elif any(keyword in career_title for keyword in ["program manager", "project manager", "business analyst"]):
                    role_boost = 15  # Reduced from 25
                    print(f"🎯 Adjacent PM match: {career_title} gets +15 boost")
            
            # Other role matches (reduced weight)
            elif user_current_role in user_roles:
                if user_current_role.lower() in career_title:
                    role_boost = 20  # Reduced from 35
                    print(f"🎯 Traditional role match: {career_title} gets +20 boost")
        
        # Experience level alignment boost
        experience_boost = 0
        career_exp_level = career.get("experienceLevel", "mid")
        if experience_years >= 15 and career_exp_level == "executive":
            experience_boost = 25
        elif experience_years >= 10 and career_exp_level == "senior":
            experience_boost = 20
        elif experience_years >= 5 and career_exp_level == "mid":
            experience_boost = 15
        elif experience_years < 5 and career_exp_level == "junior":
            experience_boost = 15
        elif abs(experience_years - {"junior": 2, "mid": 7, "senior": 12, "executive": 18}.get(career_exp_level, 7)) <= 3:
            experience_boost = 10  # Close match
        
        # Salary alignment boost
        salary_boost = 0
        career_min = career.get("minSalary", 0)
        career_max = career.get("maxSalary", 0)
        if career_min <= max_salary and career_max >= min_salary:
            # Overlapping salary ranges
            overlap = min(career_max, max_salary) - max(career_min, min_salary)
            total_range = max_salary - min_salary
            if total_range > 0:
                salary_boost = int(15 * (overlap / total_range))
        
        # Resume skills boost
        resume_boost = 0
        for skill in resume_insights.get("skills", []):
            if skill.lower() in [s.lower() for s in career.get("requiredTechnicalSkills", [])]:
                resume_boost += 3
        
        # LinkedIn insights boost
        linkedin_boost = 0
        if linkedin_insights.get("profile_strength") == "active" and "Leadership" in career.get("requiredSoftSkills", []):
            linkedin_boost += 5
        if linkedin_insights.get("network_indicators"):
            linkedin_boost += 2
        
        # Work preferences boost
        preferences_boost = 0
        if user_data.get("working_with_data", 3) >= 4:
            if "Data" in career.get("title", "") or "Analytics" in career.get("title", ""):
                preferences_boost += 8
        
        if user_data.get("working_with_people", 3) >= 4:
            if "Manager" in career.get("title", "") or "Leadership" in career.get("requiredSoftSkills", []):
                preferences_boost += 6
        
        if user_data.get("leadership", 3) >= 4:
            if "Manager" in career.get("title", "") or "Lead" in career.get("title", ""):
                preferences_boost += 10
        
        # Calculate final score with career path consistency penalty
        final_score = min(100, max(0, base_score + role_boost + theme_alignment_boost + experience_boost + salary_boost + resume_boost + linkedin_boost + preferences_boost + consistency_penalty))
        
        # Create career copy with enhanced data including consistency penalty
        career_copy = career.copy()
        career_copy["relevanceScore"] = final_score
        career_copy["roleBoost"] = role_boost
        career_copy["themeAlignmentBoost"] = theme_alignment_boost
        career_copy["experienceBoost"] = experience_boost
        career_copy["salaryBoost"] = salary_boost
        career_copy["resumeBoost"] = resume_boost
        career_copy["linkedinBoost"] = linkedin_boost
        career_copy["preferencesBoost"] = preferences_boost
        career_copy["consistencyPenalty"] = consistency_penalty
        career_copy["careerField"] = career_field
        career_copy["userField"] = user_field
        
        # Ensure salary fields are properly mapped for frontend
        career_copy["salaryMin"] = career.get("minSalary", 0)
        career_copy["salaryMax"] = career.get("maxSalary", 0)
        
        # Enhanced match reasons with theme alignment
        match_reasons = []
        if theme_alignment_boost >= 35:
            theme_name = dominant_theme.replace("_", " ").title() if dominant_theme else "primary focus"
            freq = keyword_frequencies.get(dominant_theme, 0) if dominant_theme else 0
            match_reasons.append(f"Excellent alignment with your {theme_name} background ({freq} relevant mentions in resume)")
        elif theme_alignment_boost >= 15:
            theme_name = dominant_theme.replace("_", " ").title() if dominant_theme else "background"
            match_reasons.append(f"Good match with your {theme_name} experience")
        elif theme_alignment_boost < 0:
            match_reasons.append("Role differs from your primary resume focus - consider as stretch opportunity")
        
        if role_boost >= 20:
            match_reasons.append(f"Direct role match with your {user_current_role} experience")
        elif role_boost >= 10:
            match_reasons.append(f"Adjacent match to your {user_current_role} background")
        
        if experience_boost >= 15:
            match_reasons.append(f"Perfect experience level match ({experience_years} years)")
        if salary_boost >= 10:
            match_reasons.append(f"Salary range aligns with expectations")
        if resume_boost >= 6:
            match_reasons.append(f"Strong technical skills match from resume")
        if linkedin_boost >= 3:
            match_reasons.append("Professional LinkedIn profile indicates engagement")
        if preferences_boost >= 8:
            match_reasons.append("Work preferences strongly align with role")
        
        career_copy["matchReasons"] = match_reasons
        scored_careers.append(career_copy)
    
    # Sort by relevance score (descending - highest match to lowest match)
    scored_careers.sort(key=lambda x: x["relevanceScore"], reverse=True)
    
    # NOTE: Trades/medical filtering has been moved to happen earlier in the pipeline (after safety filtering)
    # This ensures inappropriate careers are filtered out before scoring, improving performance and user experience
    
    # ENHANCED: Categorize into zones with theme alignment priority for Safe Zone population
    safe_zone = []
    stretch_zone = []
    adventure_zone = []
    
    for career in scored_careers:
        score = career["relevanceScore"]
        role_boost = career.get("roleBoost", 0)
        theme_boost = career.get("themeAlignmentBoost", 0)
        exp_boost = career.get("experienceBoost", 0)
        salary_boost = career.get("salaryBoost", 0)
        
        # PRIORITY 1: Strong theme alignment goes to Safe Zone (addresses your product-heavy resume)
        if theme_boost >= 35:  # Strong theme alignment (like 18 product mentions)
            safe_zone.append(career)
            print(f"🟢 SAFE ZONE (Theme): {career['title']} - theme_boost={theme_boost}, score={score}")
        # PRIORITY 2: Traditional direct role matches go to Safe Zone
        elif role_boost >= 20 and theme_boost >= 0:  # Direct role match without negative theme
            safe_zone.append(career)
            print(f"🟢 SAFE ZONE (Role): {career['title']} - role_boost={role_boost}, score={score}")
        # PRIORITY 3: High scores with good experience/salary alignment go to Stretch Zone
        elif score >= 80 and exp_boost >= 15 and salary_boost >= 5:
            stretch_zone.append(career)
            print(f"🟡 STRETCH ZONE (High Score): {career['title']} - score={score}")
        # PRIORITY 4: Moderate theme alignment or adjacent roles go to Stretch Zone
        elif theme_boost >= 15 or (role_boost >= 10 and theme_boost >= 0):
            stretch_zone.append(career)
            print(f"🟡 STRETCH ZONE (Moderate): {career['title']} - theme_boost={theme_boost}, role_boost={role_boost}")
        # PRIORITY 5: Decent scores without negative theme bias go to Adventure Zone
        elif score >= 60 and theme_boost >= -5:
            adventure_zone.append(career)
            print(f"🔵 ADVENTURE ZONE (Decent): {career['title']} - score={score}, theme_boost={theme_boost}")
        # PRIORITY 6: Only include careers with reasonable relevance (minimum 45 score)
        elif score >= 45:
            adventure_zone.append(career)
            print(f"🔵 ADVENTURE ZONE (Low): {career['title']} - score={score}, theme_boost={theme_boost}")
        # REJECT: Careers with very low relevance scores
        else:
            print(f"❌ REJECTED: {career['title']} - score too low ({score}), theme_boost={theme_boost}")
    
    # If we don't have enough in each zone, redistribute
    total_available = len(scored_careers)
    if len(adventure_zone) == 0 and total_available > 6:
        # Move some stretch to adventure
        if len(stretch_zone) > 3:
            adventure_zone.extend(stretch_zone[-2:])
            stretch_zone = stretch_zone[:-2]
    
    # DYNAMIC: Exploration-level based distribution with flexible zone allocation
    recommendations = []
    
    # Dynamic distribution based on exploration level (1-5 scale)
    safe_target, stretch_target, adventure_target, total_target = calculate_dynamic_distribution(exploration_level)
    
    print(f"🎯 Dynamic distribution for exploration level {exploration_level}:")
    print(f"   Safe: {safe_target}, Stretch: {stretch_target}, Adventure: {adventure_target} (Total: {total_target})")
    print(f"📊 Available: Safe={len(safe_zone)}, Stretch={len(stretch_zone)}, Adventure={len(adventure_zone)}")
    
    # Step 1: Fill each zone with available careers (up to dynamic target)
    safe_selected = safe_zone[:safe_target]
    stretch_selected = stretch_zone[:stretch_target]
    adventure_selected = adventure_zone[:adventure_target]
    
    # Step 2: Identify zones that need backfilling
    safe_deficit = safe_target - len(safe_selected)
    stretch_deficit = stretch_target - len(stretch_selected)
    adventure_deficit = adventure_target - len(adventure_selected)
    
    print(f"🔍 Deficits: Safe={safe_deficit}, Stretch={stretch_deficit}, Adventure={adventure_deficit}")
    
    # Step 3: Create redistribution pools from unused careers
    unused_safe = safe_zone[safe_target:]
    unused_stretch = stretch_zone[stretch_target:]
    unused_adventure = adventure_zone[adventure_target:]
    
    # Step 4: Redistribute careers to fill deficits
    # Priority: Fill Safe Zone first (most relevant), then Stretch, then Adventure
    
    # Fill Safe Zone deficit
    if safe_deficit > 0:
        # Try from unused stretch first (most relevant), then unused adventure
        backfill_candidates = unused_stretch + unused_adventure
        backfill_candidates.sort(key=lambda x: x["relevanceScore"], reverse=True)
        
        for career in backfill_candidates[:safe_deficit]:
            safe_selected.append(career)
            print(f"🔄 Backfilled Safe Zone: {career['title']} (score: {career['relevanceScore']})")
    
    # Fill Stretch Zone deficit
    if stretch_deficit > 0:
        # Try from unused safe first (high relevance), then unused adventure
        backfill_candidates = unused_safe + unused_adventure
        # Remove careers already used for safe zone backfill
        backfill_candidates = [c for c in backfill_candidates if c not in safe_selected[safe_target:]]
        backfill_candidates.sort(key=lambda x: x["relevanceScore"], reverse=True)
        
        for career in backfill_candidates[:stretch_deficit]:
            stretch_selected.append(career)
            print(f"🔄 Backfilled Stretch Zone: {career['title']} (score: {career['relevanceScore']})")
    
    # Fill Adventure Zone deficit
    if adventure_deficit > 0:
        # Try from unused safe and stretch
        backfill_candidates = unused_safe + unused_stretch
        # Remove careers already used for other zone backfills
        used_for_backfill = safe_selected[safe_target:] + stretch_selected[stretch_target:]
        backfill_candidates = [c for c in backfill_candidates if c not in used_for_backfill]
        backfill_candidates.sort(key=lambda x: x["relevanceScore"], reverse=True)
        
        for career in backfill_candidates[:adventure_deficit]:
            adventure_selected.append(career)
            print(f"🔄 Backfilled Adventure Zone: {career['title']} (score: {career['relevanceScore']})")
    
    # Step 5: If still insufficient careers, use remaining scored careers
    total_selected = len(safe_selected) + len(stretch_selected) + len(adventure_selected)
    if total_selected < total_target:
        all_selected = safe_selected + stretch_selected + adventure_selected
        remaining_careers = [c for c in scored_careers if c not in all_selected]
        remaining_careers.sort(key=lambda x: x["relevanceScore"], reverse=True)
        
        needed = total_target - total_selected
        for career in remaining_careers[:needed]:
            # Assign to the zone with the largest deficit first, then smallest current count
            safe_count = len(safe_selected)
            stretch_count = len(stretch_selected)
            adventure_count = len(adventure_selected)
            
            # Priority: Fill zones that are furthest from their target
            safe_remaining = safe_target - safe_count
            stretch_remaining = stretch_target - stretch_count
            adventure_remaining = adventure_target - adventure_count
            
            if safe_remaining > 0 and safe_remaining >= max(stretch_remaining, adventure_remaining):
                safe_selected.append(career)
                print(f"🔄 Emergency fill Safe Zone: {career['title']}")
            elif stretch_remaining > 0 and stretch_remaining >= adventure_remaining:
                stretch_selected.append(career)
                print(f"🔄 Emergency fill Stretch Zone: {career['title']}")
            elif adventure_remaining > 0:
                adventure_selected.append(career)
                print(f"🔄 Emergency fill Adventure Zone: {career['title']}")
            else:
                # All zones at target, assign to zone with smallest count
                if safe_count <= stretch_count and safe_count <= adventure_count:
                    safe_selected.append(career)
                    print(f"🔄 Overflow to Safe Zone: {career['title']}")
                elif stretch_count <= adventure_count:
                    stretch_selected.append(career)
                    print(f"🔄 Overflow to Stretch Zone: {career['title']}")
                else:
                    adventure_selected.append(career)
                    print(f"🔄 Overflow to Adventure Zone: {career['title']}")
    
    # Step 6: Assign zone labels and compile final recommendations
    for career in safe_selected:
        career["zone"] = "safe"
        recommendations.append(career)
    
    for career in stretch_selected:
        career["zone"] = "stretch"
        recommendations.append(career)
    
    for career in adventure_selected:
        career["zone"] = "adventure"
        recommendations.append(career)
    
    # CRITICAL: Sort final recommendations by relevance score (descending - highest to lowest)
    # This ensures all recommendations are properly ordered regardless of zone
    recommendations.sort(key=lambda x: x.get("relevanceScore", 0), reverse=True)
    
    # Final distribution summary
    safe_count = len([r for r in recommendations if r['zone'] == 'safe'])
    stretch_count = len([r for r in recommendations if r['zone'] == 'stretch'])
    adventure_count = len([r for r in recommendations if r['zone'] == 'adventure'])
    
    print(f"✅ DYNAMIC DISTRIBUTION ACHIEVED:")
    print(f"   🟢 Safe Zone: {safe_count} recommendations (target: {safe_target})")
    print(f"   🟡 Stretch Zone: {stretch_count} recommendations (target: {stretch_target})")
    print(f"   🔵 Adventure Zone: {adventure_count} recommendations (target: {adventure_target})")
    print(f"   📊 Total: {len(recommendations)} recommendations (target: {total_target})")
    print(f"   🎯 Exploration Level: {exploration_level} - Targets achieved: Safe={safe_count == safe_target}, Stretch={stretch_count == stretch_target}, Adventure={adventure_count == adventure_target}")
    
    if len(recommendations) > 0:
        avg_score = sum(r.get('relevanceScore', 0) for r in recommendations) / len(recommendations)
        print(f"   📈 Average relevance score: {avg_score:.1f}")
    
    return recommendations

def extract_resume_insights(resume_text: str) -> Dict[str, Any]:
    """
    Extract insights from resume text with keyword frequency analysis for better matching
    
    ⚠️  CRITICAL ENHANCEMENT (FIXED 2025-01-21):
    This function was enhanced to properly detect communications and creative skills
    to prevent users with those skills from getting irrelevant recommendations like
    "Sheet Metal Worker" instead of marketing/communications roles.
    
    KEY ADDITIONS:
    - Communications keyword detection: marketing, social media, content, PR, etc.
    - Creative keyword detection: design, creative, graphic design, video, etc.
    - Proper theme scoring to prioritize relevant career matches
    
    DO NOT REMOVE communications_keywords or creative_keywords without testing!
    """
    if not resume_text:
        return {"skills": [], "experience_indicators": [], "leadership_indicators": [], "industry_indicators": [], "roles": [], "current_role": None, "keyword_frequencies": {}, "dominant_theme": None}
    
    resume_lower = resume_text.lower()
    
    # ENHANCED: Count keyword frequencies for better role matching
    keyword_frequencies = {}
    
    # Product Management keyword frequency analysis
    product_keywords = ["product manager", "product management", "product", "pm", "product owner", "product lead", "head of product", "vp product", "chief product officer", "cpo", "roadmap", "feature", "user stories", "product strategy"]
    product_count = sum(resume_lower.count(keyword) for keyword in product_keywords)
    keyword_frequencies["product"] = product_count
    
    # Engineering keyword frequency analysis
    engineering_keywords = ["software engineer", "engineering", "developer", "programming", "code", "software development", "technical lead", "architect", "system design"]
    engineering_count = sum(resume_lower.count(keyword) for keyword in engineering_keywords)
    keyword_frequencies["engineering"] = engineering_count
    
    # Data Science keyword frequency analysis
    data_science_keywords = ["data scientist", "data science", "machine learning", "ml", "analytics", "statistical", "modeling", "algorithm", "data analysis"]
    data_science_count = sum(resume_lower.count(keyword) for keyword in data_science_keywords)
    keyword_frequencies["data_science"] = data_science_count
    
    # Management keyword frequency analysis
    management_keywords = ["manager", "management", "lead", "director", "head of", "vp", "chief", "team lead", "supervisor"]
    management_count = sum(resume_lower.count(keyword) for keyword in management_keywords)
    keyword_frequencies["management"] = management_count
    
    # COMMUNICATIONS & MARKETING keyword frequency analysis
    communications_keywords = ["communications", "communication", "marketing", "social media", "content", "copywriting", "public relations", "pr", "brand", "campaign", "digital marketing", "content marketing", "social media marketing", "community management"]
    communications_count = sum(resume_lower.count(keyword) for keyword in communications_keywords)
    keyword_frequencies["communications"] = communications_count
    
    # CREATIVE & DESIGN keyword frequency analysis
    creative_keywords = ["design", "creative", "graphic design", "visual", "branding", "creative director", "art director", "ux design", "ui design", "web design", "video", "photography", "illustration"]
    creative_count = sum(resume_lower.count(keyword) for keyword in creative_keywords)
    keyword_frequencies["creative"] = creative_count
    
    # Determine dominant theme based on keyword frequency
    theme_scores = {
        "product": product_count,
        "engineering": engineering_count,
        "data_science": data_science_count,
        "management": management_count,
        "communications": communications_count,
        "creative": creative_count
    }
    dominant_theme = max(theme_scores, key=theme_scores.get) if max(theme_scores.values()) > 0 else None
    
    print(f"📊 Keyword frequencies: Product={product_count}, Engineering={engineering_count}, Data Science={data_science_count}, Management={management_count}, Communications={communications_count}, Creative={creative_count}")
    print(f"🎯 Dominant theme: {dominant_theme} ({theme_scores[dominant_theme] if dominant_theme else 0} mentions)")
    
    # Extract current and past roles based on frequency analysis
    roles = []
    current_role = None
    
    # ENHANCED: Check for explicit role mentions in resume first
    # Look for "Aircraft Mechanic", "Social Media Manager", etc.
    explicit_role_patterns = [
        "aircraft mechanic", "social media manager", "product manager", "software engineer",
        "data scientist", "marketing manager", "sales manager", "project manager",
        "business analyst", "ux designer", "graphic designer", "content creator",
        "electrician", "plumber", "carpenter", "welder", "hvac technician",
        "nurse", "doctor", "teacher", "instructor"
    ]
    
    for role_pattern in explicit_role_patterns:
        if role_pattern in resume_lower:
            if "aircraft mechanic" in role_pattern:
                current_role = "Aircraft Mechanic"
                roles.append("Aircraft Mechanic")
                print(f"🎯 Explicit Aircraft Mechanic role detected")
                break
            elif "social media manager" in role_pattern:
                current_role = "Social Media Manager"
                roles.append("Social Media Manager")
                print(f"🎯 Explicit Social Media Manager role detected")
                break
            elif "product manager" in role_pattern:
                current_role = "Product Management"
                roles.append("Product Management")
                print(f"🎯 Explicit Product Manager role detected")
                break
    
    # Fallback: Determine primary role based on keyword frequency if no explicit role found
    if not current_role:
        if product_count >= 5:  # Strong product signal
            roles.append("Product Management")
            current_role = "Product Management"
            print(f"🎯 Strong Product Management signal detected ({product_count} mentions)")
        elif product_count >= 2:  # Moderate product signal
            roles.append("Product Management")
            if not current_role:
                current_role = "Product Management"
            print(f"🎯 Moderate Product Management signal detected ({product_count} mentions)")
    
    # Other role detection with frequency consideration
    role_patterns = {
        "Engineering Management": ["engineering manager", "engineering lead", "head of engineering", "vp engineering", "cto"],
        "Software Engineering": ["software engineer", "developer", "programmer", "full stack", "backend", "frontend"],
        "Data Science": ["data scientist", "machine learning engineer", "ai engineer", "data analyst"],
        "Marketing": ["marketing manager", "digital marketing", "growth marketing", "marketing lead"],
        "Sales": ["sales manager", "account manager", "business development", "sales lead"],
        "Operations": ["operations manager", "ops", "business operations", "program manager"],
        "Design": ["ux designer", "ui designer", "product designer", "design lead"],
        "Finance": ["financial analyst", "finance manager", "controller", "cfo"],
        "HR": ["hr manager", "people operations", "talent acquisition", "recruiter"]
    }
    
    # Only add roles if they have sufficient frequency or explicit mentions
    for role_name, keywords in role_patterns.items():
        role_mentions = 0
        for keyword in keywords:
            role_mentions += resume_lower.count(keyword)
        
        # Add role only if it has meaningful presence
        if role_mentions > 0:
            if role_name == "Software Engineering" and engineering_count >= 3:
                if role_name not in roles:
                    roles.append(role_name)
                if not current_role and engineering_count > product_count:
                    current_role = role_name
            elif role_name == "Data Science" and data_science_count >= 3:
                if role_name not in roles:
                    roles.append(role_name)
                if not current_role and data_science_count > product_count:
                    current_role = role_name
            elif role_mentions >= 2:  # Other roles need at least 2 mentions
                if role_name not in roles:
                    roles.append(role_name)
                if not current_role and role_mentions > product_count:
                    current_role = role_name
    
    # Technical skills extraction - expanded for Product Management
    tech_skills = []
    tech_keywords = [
        # Product Management skills
        "roadmap", "user stories", "agile", "scrum", "kanban", "jira", "confluence",
        "analytics", "a/b testing", "user research", "wireframing", "prototyping",
        "product strategy", "go-to-market", "gtm", "product launch", "feature prioritization",
        
        # Technical skills
        "python", "java", "javascript", "sql", "machine learning", "data analysis",
        "aws", "azure", "docker", "kubernetes", "react", "angular", "node.js",
        "tensorflow", "pytorch", "pandas", "numpy", "tableau", "power bi",
        "git", "jenkins", "rest api", "microservices", "figma", "sketch"
    ]
    
    for skill in tech_keywords:
        if skill in resume_lower:
            tech_skills.append(skill.title())
    
    # Experience level indicators
    experience_indicators = []
    if "senior" in resume_lower or "lead" in resume_lower:
        experience_indicators.append("senior_level")
    if "manager" in resume_lower or "director" in resume_lower or "head of" in resume_lower:
        experience_indicators.append("management_experience")
    if "vp" in resume_lower or "vice president" in resume_lower or "chief" in resume_lower:
        experience_indicators.append("executive_level")
    if "architect" in resume_lower:
        experience_indicators.append("architecture_experience")
    
    # Leadership indicators
    leadership_indicators = []
    leadership_keywords = ["managed", "led", "supervised", "coordinated", "mentored", "trained", "built team", "hired", "scaled"]
    for keyword in leadership_keywords:
        if keyword in resume_lower:
            leadership_indicators.append(keyword)
    
    # Industry indicators
    industry_indicators = []
    industry_keywords = {
        "healthcare": ["healthcare", "medical", "hospital", "clinical", "pharma"],
        "finance": ["finance", "banking", "investment", "trading", "fintech", "payments"],
        "technology": ["software", "tech", "startup", "saas", "platform", "mobile app"],
        "consulting": ["consulting", "advisory", "strategy", "implementation"],
        "education": ["education", "university", "academic", "research", "edtech"],
        "ecommerce": ["ecommerce", "e-commerce", "retail", "marketplace", "shopify"],
        "media": ["media", "entertainment", "streaming", "content", "publishing"]
    }
    
    for industry, keywords in industry_keywords.items():
        if any(keyword in resume_lower for keyword in keywords):
            industry_indicators.append(industry)
    
    return {
        "skills": tech_skills,
        "experience_indicators": experience_indicators,
        "leadership_indicators": leadership_indicators,
        "industry_indicators": industry_indicators,
        "roles": roles,
        "current_role": current_role,
        "keyword_frequencies": keyword_frequencies,
        "dominant_theme": dominant_theme
    }

def extract_linkedin_insights(linkedin_profile: str) -> Dict[str, Any]:
    """Extract insights from LinkedIn profile URL or text"""
    if not linkedin_profile:
        return {"profile_strength": "unknown", "network_indicators": [], "activity_indicators": []}
    
    linkedin_lower = linkedin_profile.lower()
    
    # Profile strength indicators
    profile_strength = "basic"
    if "linkedin.com/in/" in linkedin_lower:
        profile_strength = "active"
    
    # Network indicators
    network_indicators = []
    if "connections" in linkedin_lower or "network" in linkedin_lower:
        network_indicators.append("active_networker")
    
    # Activity indicators
    activity_indicators = []
    activity_keywords = ["posts", "articles", "shares", "comments", "recommendations"]
    for keyword in activity_keywords:
        if keyword in linkedin_lower:
            activity_indicators.append(keyword)
    
    return {
        "profile_strength": profile_strength,
        "network_indicators": network_indicators,
        "activity_indicators": activity_indicators
    }

def get_career_field_categories() -> Dict[str, List[str]]:
    """Define career field categories for consistency checking"""
    return {
        "technology": [
            "software engineer", "data scientist", "machine learning", "devops", "cloud",
            "cybersecurity", "full stack", "frontend", "backend", "qa engineer", "technical writer",
            "solutions architect", "principal engineer", "staff engineer", "engineering manager",
            "cto", "vp engineering", "cio", "technical program manager"
        ],
        "product_management": [
            "product manager", "senior product manager", "principal product manager",
            "group product manager", "director of product", "head of product", "vp product",
            "chief product officer", "cpo", "junior product manager", "technical product manager",
            "growth product manager", "platform product manager"
        ],
        "healthcare": [
            "physician", "doctor", "nurse", "surgeon", "cardiologist", "pediatrician",
            "physical therapist", "occupational therapist", "medical assistant",
            "healthcare administrator", "clinical psychologist", "social worker",
            "radiologic technologist", "medical records", "family medicine"
        ],
        "business_finance": [
            "financial analyst", "accountant", "controller", "cfo", "investment", "banking",
            "business analyst", "consultant", "operations manager", "project manager",
            "tax specialist", "treasury analyst", "budget analyst", "credit analyst"
        ],
        "sales_marketing": [
            "sales", "marketing", "digital marketing", "account manager", "business development",
            "sales development representative", "marketing specialist", "growth marketing",
            "recruiter", "marketing analyst"
        ],
        "design": [
            "ux designer", "ui designer", "product designer", "graphic designer", "design lead",
            "senior ux designer", "creative director"
        ],
        "creative_arts": [
            "creative director", "art director", "head of design", "chief creative officer",
            "graphic designer", "motion graphics", "brand designer", "creative producer",
            "web designer", "video editor", "photographer", "illustrator", "3d artist",
            "game artist", "concept artist", "sound designer", "animator", "content creator",
            "social media designer", "production assistant", "art teacher"
        ],
        "education": [
            "teacher", "professor", "instructor", "education", "academic", "curriculum",
            "school administrator", "principal"
        ],
        "skilled_trades": [
            "electrician", "plumber", "carpenter", "mechanic", "technician", "welder",
            "hvac", "construction", "maintenance", "aircraft mechanic", "automotive technician",
            "diesel mechanic", "industrial maintenance", "machinist", "cnc operator"
        ],
        "government_public_service": [
            "policy analyst", "government relations specialist", "public affairs manager",
            "regulatory affairs specialist", "city planner", "public administrator",
            "legislative director", "congressional staff director", "senior executive service (ses)",
            "legislative analyst", "government analyst", "federal", "state", "gs-"
        ],
        "hospitality_service": [
            "restaurant manager", "hotel manager", "spa manager", "banquet manager",
            "front desk manager", "concierge", "sommelier", "wedding planner"
        ],
        "agriculture_environment": [
            "organic farm manager", "agronomist", "environmental consultant", "wildlife biologist",
            "soil scientist", "sustainable agriculture", "water resource", "climate change analyst",
            "renewable energy", "environmental educator"
        ]
    }

def get_field_adjacency_map() -> Dict[str, Dict[str, int]]:
    """Define how adjacent/related different career fields are (0=unrelated, 1=adjacent, 2=closely related)"""
    return {
        "technology": {
            "product_management": 2,  # Very closely related
            "business_finance": 1,    # Adjacent (tech companies need business skills)
            "design": 2,              # Closely related (work together frequently)
            "creative_arts": 2,       # Closely related (digital media, game dev, web design)
            "sales_marketing": 1,     # Adjacent (tech sales, growth)
            "healthcare": 0,          # Unrelated
            "education": 0,           # Unrelated
            "skilled_trades": 0,      # Unrelated
            "government_public_service": 0,  # Unrelated
            "hospitality_service": 0,        # Unrelated
            "agriculture_environment": 0     # Unrelated
        },
        "product_management": {
            "technology": 2,          # Very closely related
            "business_finance": 2,    # Closely related (business strategy)
            "design": 2,              # Closely related (product design)
            "creative_arts": 2,       # Closely related (product design, UX)
            "sales_marketing": 2,     # Closely related (go-to-market)
            "healthcare": 0,          # Unrelated
            "education": 0,           # Unrelated
            "skilled_trades": 0,      # Unrelated
            "government_public_service": 0,  # Unrelated
            "hospitality_service": 0,        # Unrelated
            "agriculture_environment": 0     # Unrelated
        },
        "healthcare": {
            "technology": 0,          # Unrelated (unless health tech)
            "product_management": 0,  # Unrelated
            "business_finance": 1,    # Adjacent (healthcare admin)
            "design": 0,              # Unrelated
            "creative_arts": 0,       # Unrelated
            "sales_marketing": 0,     # Unrelated
            "education": 1,           # Adjacent (medical education)
            "skilled_trades": 0,      # Unrelated
            "government_public_service": 1,  # Adjacent (public health)
            "hospitality_service": 0,        # Unrelated
            "agriculture_environment": 0     # Unrelated
        },
        "business_finance": {
            "technology": 1,          # Adjacent
            "product_management": 2,  # Closely related
            "healthcare": 1,          # Adjacent (healthcare finance)
            "design": 0,              # Unrelated
            "creative_arts": 1,       # Adjacent (creative industry business)
            "sales_marketing": 2,     # Closely related
            "education": 1,           # Adjacent (education finance)
            "skilled_trades": 1,      # Adjacent (construction finance)
            "government_public_service": 1,  # Adjacent (public finance)
            "hospitality_service": 1,        # Adjacent (hospitality business)
            "agriculture_environment": 1     # Adjacent (agribusiness)
        },
        "sales_marketing": {
            "technology": 1,          # Adjacent
            "product_management": 2,  # Closely related
            "healthcare": 0,          # Unrelated
            "business_finance": 2,    # Closely related
            "design": 1,              # Adjacent (marketing design)
            "creative_arts": 2,       # Closely related (marketing creative, content)
            "education": 0,           # Unrelated
            "skilled_trades": 0,      # Unrelated
            "government_public_service": 0,  # Unrelated
            "hospitality_service": 1,        # Adjacent (hospitality marketing)
            "agriculture_environment": 0     # Unrelated
        },
        "design": {
            "technology": 2,          # Closely related
            "product_management": 2,  # Closely related
            "healthcare": 0,          # Unrelated
            "business_finance": 0,    # Unrelated
            "sales_marketing": 1,     # Adjacent
            "creative_arts": 2,       # Very closely related (overlapping skills)
            "education": 1,           # Adjacent (educational design)
            "skilled_trades": 0,      # Unrelated
            "government_public_service": 0,  # Unrelated
            "hospitality_service": 0,        # Unrelated
            "agriculture_environment": 0     # Unrelated
        },
        "creative_arts": {
            "technology": 2,          # Closely related (digital media, web, games)
            "product_management": 2,  # Closely related (UX, product design)
            "healthcare": 0,          # Unrelated
            "business_finance": 1,    # Adjacent (creative industry business)
            "sales_marketing": 2,     # Closely related (content, campaigns, branding)
            "design": 2,              # Very closely related (overlapping field)
            "education": 1,           # Adjacent (art education, instructional design)
            "skilled_trades": 0,      # Unrelated
            "government_public_service": 0,  # Unrelated
            "hospitality_service": 0,        # Unrelated
            "agriculture_environment": 0     # Unrelated
        },
        "education": {
            "technology": 0,          # Unrelated
            "product_management": 0,  # Unrelated
            "healthcare": 1,          # Adjacent
            "business_finance": 1,    # Adjacent
            "sales_marketing": 0,     # Unrelated
            "design": 1,              # Adjacent
            "creative_arts": 1,       # Adjacent (art education)
            "skilled_trades": 0,      # Unrelated
            "government_public_service": 1,  # Adjacent (public education)
            "hospitality_service": 0,        # Unrelated
            "agriculture_environment": 1     # Adjacent (environmental education)
        },
        "skilled_trades": {
            "technology": 0,          # Unrelated
            "product_management": 0,  # Unrelated
            "healthcare": 0,          # Unrelated
            "business_finance": 1,    # Adjacent
            "sales_marketing": 0,     # Unrelated
            "design": 0,              # Unrelated
            "creative_arts": 0,       # Unrelated
            "education": 0,           # Unrelated
            "government_public_service": 0,  # Unrelated
            "hospitality_service": 0,        # Unrelated
            "agriculture_environment": 1     # Adjacent (agricultural equipment)
        },
        "government_public_service": {
            "technology": 0,          # Unrelated
            "product_management": 0,  # Unrelated
            "healthcare": 1,          # Adjacent (public health)
            "business_finance": 1,    # Adjacent (public finance)
            "sales_marketing": 0,     # Unrelated
            "design": 0,              # Unrelated
            "creative_arts": 0,       # Unrelated
            "education": 1,           # Adjacent (public education)
            "skilled_trades": 0,      # Unrelated
            "hospitality_service": 0,        # Unrelated
            "agriculture_environment": 1     # Adjacent (environmental policy)
        },
        "hospitality_service": {
            "technology": 0,          # Unrelated
            "product_management": 0,  # Unrelated
            "healthcare": 0,          # Unrelated
            "business_finance": 1,    # Adjacent (hospitality business)
            "sales_marketing": 1,     # Adjacent (hospitality marketing)
            "design": 0,              # Unrelated
            "creative_arts": 0,       # Unrelated
            "education": 0,           # Unrelated
            "skilled_trades": 0,      # Unrelated
            "government_public_service": 0,  # Unrelated
            "agriculture_environment": 0     # Unrelated
        },
        "agriculture_environment": {
            "technology": 0,          # Unrelated
            "product_management": 0,  # Unrelated
            "healthcare": 0,          # Unrelated
            "business_finance": 1,    # Adjacent (agribusiness)
            "sales_marketing": 0,     # Unrelated
            "design": 0,              # Unrelated
            "creative_arts": 0,       # Unrelated
            "education": 1,           # Adjacent (environmental education)
            "skilled_trades": 1,      # Adjacent (agricultural equipment)
            "government_public_service": 1,  # Adjacent (environmental policy)
            "hospitality_service": 0         # Unrelated
        }
    }

def identify_career_field(career: Dict[str, Any]) -> str:
    """
    Identify which field a career belongs to based on title and description
    
    CRITICAL FIX: This function was misclassifying careers like:
    - "Tourism Director" as "technology" instead of "hospitality_service"
    - "Conservation Director" as "technology" instead of "agriculture_environment"
    - "Congressional Staff Director" as "technology" instead of "government_public_service"
    
    Fixed to use exact phrase matching and prioritize specific field terms.
    """
    career_title = career.get("title", "").lower()
    career_desc = career.get("description", "").lower()
    career_text = f"{career_title} {career_desc}"
    
    field_categories = get_career_field_categories()
    
    # PRIORITY 1: Check for exact government/public service matches first
    government_keywords = field_categories.get("government_public_service", [])
    for keyword in government_keywords:
        if keyword in career_title:  # Exact match in title
            print(f"🏛️ GOVERNMENT MATCH: '{career_title}' matched '{keyword}' -> government_public_service")
            return "government_public_service"
    
    # PRIORITY 2: Check for exact hospitality matches (including tourism)
    hospitality_keywords = field_categories.get("hospitality_service", [])
    # Add tourism-specific keywords
    tourism_keywords = ["tourism director", "tourism manager", "tourism", "travel", "hospitality"]
    all_hospitality_keywords = hospitality_keywords + tourism_keywords
    
    for keyword in all_hospitality_keywords:
        if keyword in career_title:  # Exact match in title
            print(f"🏨 HOSPITALITY/TOURISM MATCH: '{career_title}' matched '{keyword}' -> hospitality_service")
            return "hospitality_service"
    
    # PRIORITY 3: Check for exact agriculture/environment matches (including conservation)
    agriculture_keywords = field_categories.get("agriculture_environment", [])
    # Add conservation-specific keywords
    conservation_keywords = ["conservation director", "conservation manager", "conservation", "environmental director", "environmental manager", "sustainability"]
    all_agriculture_keywords = agriculture_keywords + conservation_keywords
    
    for keyword in all_agriculture_keywords:
        if keyword in career_title:  # Exact match in title
            print(f"🌱 AGRICULTURE/CONSERVATION MATCH: '{career_title}' matched '{keyword}' -> agriculture_environment")
            return "agriculture_environment"
    
    # PRIORITY 4: Check for skilled trades matches
    trades_keywords = field_categories.get("skilled_trades", [])
    for keyword in trades_keywords:
        if keyword in career_title:  # Exact match in title
            print(f"🔧 TRADES MATCH: '{career_title}' matched '{keyword}' -> skilled_trades")
            return "skilled_trades"
    
    # PRIORITY 5: Check for healthcare matches
    healthcare_keywords = field_categories.get("healthcare", [])
    for keyword in healthcare_keywords:
        if keyword in career_title:  # Exact match in title
            print(f"🏥 HEALTHCARE MATCH: '{career_title}' matched '{keyword}' -> healthcare")
            return "healthcare"
    
    # PRIORITY 6: Standard scoring for remaining fields
    field_scores = {}
    for field, keywords in field_categories.items():
        # Skip the fields we already handled with exact matching
        if field in ["government_public_service", "hospitality_service", "agriculture_environment", "skilled_trades", "healthcare"]:
            continue
            
        score = 0
        for keyword in keywords:
            if keyword in career_text:
                # Weight title matches higher than description matches
                if keyword in career_title:
                    score += 3
                else:
                    score += 1
        field_scores[field] = score
    
    # Return the field with the highest score, or "unknown" if no matches
    if field_scores and max(field_scores.values()) > 0:
        best_field = max(field_scores, key=field_scores.get)
        print(f"🔍 STANDARD MATCH: '{career_title}' -> {best_field} (score: {field_scores[best_field]})")
        return best_field
    else:
        print(f"❓ NO MATCH: '{career_title}' -> unknown")
        return "unknown"

def identify_user_field(resume_insights: Dict[str, Any], user_data: Dict[str, Any]) -> str:
    """
    Identify the user's primary career field based on resume and profile data
    
    CRITICAL FIX (2025-01-21): This function was misclassifying Aircraft Mechanics as "sales_marketing"
    instead of "skilled_trades", causing inappropriate recommendations like "Junior Product Manager"
    for aircraft mechanics. Fixed to properly prioritize current role and technical skills analysis.
    """
    keyword_frequencies = resume_insights.get("keyword_frequencies", {})
    dominant_theme = resume_insights.get("dominant_theme")
    current_role = resume_insights.get("current_role")
    
    # PRIORITY 1: Current role analysis (most reliable indicator)
    if current_role:
        role_lower = current_role.lower()
        
        # SKILLED TRADES - Check first to prevent misclassification
        if any(trades_word in role_lower for trades_word in [
            "mechanic", "aircraft mechanic", "technician", "electrician", "plumber",
            "welder", "carpenter", "hvac", "maintenance", "machinist", "operator"
        ]):
            return "skilled_trades"
        
        # PRODUCT MANAGEMENT
        elif "product" in role_lower and any(pm_word in role_lower for pm_word in ["manager", "management", "lead", "owner"]):
            return "product_management"
        
        # TECHNOLOGY
        elif any(tech_word in role_lower for tech_word in ["engineer", "developer", "data scientist", "technical", "software"]):
            # Exception: Aircraft mechanics are NOT technology workers
            if "aircraft" in role_lower or "aviation" in role_lower:
                return "skilled_trades"
            return "technology"
        
        # COMMUNICATIONS/MARKETING - FIXED: Added "coordinator" and more comprehensive matching
        elif any(comm_word in role_lower for comm_word in [
            "social media", "marketing", "communications", "content", "pr", "brand",
            "marketing coordinator", "marketing manager", "marketing assistant", "marketing specialist",
            "social media manager", "content creator", "communications coordinator", "communications manager"
        ]):
            return "sales_marketing"
        
        # CREATIVE ARTS
        elif any(creative_word in role_lower for creative_word in ["designer", "creative", "artist", "photographer", "illustrator"]):
            return "creative_arts"
        
        # HEALTHCARE
        elif any(health_word in role_lower for health_word in ["nurse", "doctor", "therapist", "medical", "clinical"]):
            return "healthcare"
        
        # EDUCATION
        elif any(edu_word in role_lower for edu_word in ["teacher", "instructor", "educator", "professor"]):
            return "education"
        
        # BUSINESS/FINANCE - FIXED: Moved this AFTER communications/marketing to prevent misclassification
        elif any(biz_word in role_lower for biz_word in ["analyst", "consultant", "finance", "business"]):
            return "business_finance"
        
        # GENERIC MANAGEMENT - Only if no other specific field matches
        elif "manager" in role_lower or "coordinator" in role_lower:
            # Try to determine management type from context
            if any(marketing_word in role_lower for marketing_word in ["marketing", "social", "brand", "communications"]):
                return "sales_marketing"
            elif any(product_word in role_lower for product_word in ["product"]):
                return "product_management"
            else:
                return "business_finance"  # Default for generic management roles
    
    # PRIORITY 2: Technical skills analysis (second most reliable)
    tech_skills = user_data.get("technical_skills", [])
    if tech_skills:
        tech_skill_text = " ".join(str(skill) for skill in tech_skills if skill).lower()
        
        # SKILLED TRADES - Check first to prevent misclassification
        if any(trades_skill in tech_skill_text for trades_skill in [
            "aircraft maintenance", "engine repair", "hydraulic systems", "electrical troubleshooting",
            "avionics", "faa regulations", "mechanical", "automotive", "hvac", "welding",
            "plumbing", "machining", "fabrication", "maintenance", "repair"
        ]):
            return "skilled_trades"
        
        # COMMUNICATIONS/MARKETING - ENHANCED: Added more comprehensive matching
        elif any(comm_skill in tech_skill_text for comm_skill in [
            "social media management", "content creation", "digital marketing", "copywriting",
            "seo", "email marketing", "brand", "communications", "google analytics", "facebook blueprint",
            "social media", "content", "marketing", "graphic design", "video editing", "photography",
            "adobe creative suite", "web design", "email management"
        ]):
            return "sales_marketing"
        
        # CREATIVE ARTS - REFINED: Removed overlapping skills that should go to sales_marketing
        elif any(creative_skill in tech_skill_text for creative_skill in [
            "illustrator", "photoshop", "design", "creative", "visual design", "art", "animation",
            "3d modeling", "ui design", "ux design"
        ]):
            return "creative_arts"
        
        # PRODUCT MANAGEMENT
        elif any(product_skill in tech_skill_text for product_skill in [
            "product management", "roadmap", "user research", "a/b testing", "product analytics",
            "jira", "confluence", "agile", "scrum"
        ]):
            return "product_management"
        
        # TECHNOLOGY
        elif any(tech_skill in tech_skill_text for tech_skill in [
            "python", "javascript", "sql", "aws", "machine learning", "programming", "software",
            "react", "node.js", "docker", "kubernetes", "git"
        ]):
            return "technology"
    
    # PRIORITY 3: Keyword frequency analysis (fallback)
    if keyword_frequencies.get("communications", 0) >= 5:
        return "sales_marketing"
    elif keyword_frequencies.get("creative", 0) >= 5:
        return "creative_arts"
    elif keyword_frequencies.get("product", 0) >= 5:
        return "product_management"
    elif keyword_frequencies.get("engineering", 0) >= 5:
        return "technology"
    elif keyword_frequencies.get("data_science", 0) >= 5:
        return "technology"
    elif keyword_frequencies.get("management", 0) >= 5:
        # Determine management type
        if current_role and "product" in current_role.lower():
            return "product_management"
        elif current_role and any(tech_word in current_role.lower() for tech_word in ["engineering", "technical", "software"]):
            return "technology"
        else:
            return "business_finance"
    
    return "unknown"

def calculate_consistency_penalty(career_field: str, user_field: str, field_adjacency_map: Dict[str, Dict[str, int]],
                                dominant_theme: str, keyword_frequencies: Dict[str, int], exploration_level: int = 1) -> int:
    """
    Calculate penalty for career path consistency - negative values are penalties
    
    ENHANCED FOR HIGH EXPLORATION LEVELS:
    This function now applies much stronger penalties for high exploration levels (4-5)
    to prevent inappropriate cross-category recommendations like:
    - Product Managers → Congressional Staff Director
    - Social Media Managers → Tax Specialist
    - Aircraft Mechanics → Spa Manager
    """
    
    if career_field == "unknown" or user_field == "unknown":
        return -5  # Small penalty for unknown fields
    
    if career_field == user_field:
        return 0  # No penalty for same field
    
    # Get adjacency score (0=unrelated, 1=adjacent, 2=closely related)
    adjacency_score = field_adjacency_map.get(user_field, {}).get(career_field, 0)
    
    # EXPLORATION LEVEL MULTIPLIERS: Higher exploration = stronger penalties for inappropriate matches
    exploration_multiplier = 1.0
    if exploration_level >= 5:
        exploration_multiplier = 2.5  # 2.5x stronger penalties for maximum exploration
    elif exploration_level >= 4:
        exploration_multiplier = 2.0  # 2x stronger penalties for high exploration
    elif exploration_level >= 3:
        exploration_multiplier = 1.5  # 1.5x stronger penalties for moderate exploration
    
    # STRONG PENALTIES for completely unrelated fields
    if adjacency_score == 0:
        # Base penalty calculation
        if dominant_theme and keyword_frequencies.get(dominant_theme, 0) >= 10:
            base_penalty = -60  # Very strong penalty for users with clear specialization
        elif dominant_theme and keyword_frequencies.get(dominant_theme, 0) >= 5:
            base_penalty = -45  # Strong penalty for users with moderate specialization
        else:
            base_penalty = -30  # Standard penalty for unrelated fields
        
        # Apply exploration level multiplier
        penalty = int(base_penalty * exploration_multiplier)
        
        # Cap the penalty to prevent extreme values
        penalty = max(penalty, -150)  # Maximum penalty of -150
        
        if exploration_level >= 4:
            print(f"🚫 HIGH EXPLORATION PENALTY: {career_field} career for {user_field} user (exploration {exploration_level}) = {penalty} (base: {base_penalty}, multiplier: {exploration_multiplier}x)")
        else:
            print(f"🚫 STANDARD CONSISTENCY PENALTY: {career_field} career for {user_field} user = {penalty}")
        return penalty
    
    # MODERATE PENALTIES for adjacent fields (also scaled by exploration level)
    elif adjacency_score == 1:
        base_penalty = -10  # Small penalty for adjacent fields
        penalty = int(base_penalty * exploration_multiplier)
        penalty = max(penalty, -25)  # Cap adjacent field penalties
        
        if exploration_level >= 4:
            print(f"⚠️ HIGH EXPLORATION ADJACENT PENALTY: {career_field} career for {user_field} user (exploration {exploration_level}) = {penalty}")
        else:
            print(f"⚠️ ADJACENT FIELD PENALTY: {career_field} career for {user_field} user = {penalty}")
        return penalty
    
    # NO PENALTY for closely related fields
    elif adjacency_score == 2:
        print(f"✅ CLOSELY RELATED FIELDS: {career_field} career for {user_field} user = 0 penalty")
        return 0
    
    return -5  # Default small penalty

def is_safety_critical_career(career: Dict[str, Any]) -> bool:
    """
    ⚠️⚠️⚠️  CRITICAL SAFETY FUNCTION - DO NOT MODIFY WITHOUT EXTREME CAUTION  ⚠️⚠️⚠️
    
    HISTORICAL CONTEXT:
    - This function was initially too aggressive, blocking legitimate careers like:
      * "Digital Marketing Specialist"
      * "Software Engineer"
      * "Junior UX Designer"
      * "Marketing Analyst"
    - This caused users with communications/social media skills to get irrelevant
      recommendations like "Sheet Metal Worker" instead of marketing roles
    
    CURRENT IMPLEMENTATION (FIXED 2025-01-21):
    - ONLY blocks careers where unqualified practice could IMMEDIATELY kill someone
    - Does NOT block general engineering, marketing, design, or business roles
    - Maintains essential protections for medical professionals and emergency responders
    
    ⚠️  CRITICAL: If you modify this function, you MUST test with these scenarios:
    1. User with "communications" and "social media" skills should get marketing recommendations
    2. "Digital Marketing Specialist" should NOT be blocked as safety-critical
    3. "Software Engineer" should NOT be blocked as safety-critical
    4. "Nurse Anesthetist" SHOULD be blocked as safety-critical
    
    DO NOT REMOVE OR MODIFY WITHOUT CAREFUL REVIEW - SAFETY IMPLICATIONS
    """
    career_title = career.get("title", "").lower().strip()
    
    # ONLY THE MOST CRITICAL LIFE-THREATENING CAREERS
    # These are careers where unqualified practice could directly kill someone
    truly_life_critical = [
        # Medical professionals who make life/death decisions
        "nurse anesthetist", "crna", "anesthetist", "anesthesiologist",
        "physician", "doctor", "surgeon", "cardiologist", "pediatrician",
        "psychiatrist", "radiologist", "pathologist", "emergency medicine physician",
        "family medicine physician", "internal medicine physician",
        "registered nurse", "nurse practitioner", "physician assistant",
        "pharmacist",
        
        # Emergency responders
        "paramedic", "emergency medical technician", "emt",
        
        # Transportation safety
        "airline pilot", "commercial pilot", "air traffic controller",
        
        # Public safety
        "firefighter", "police officer"
    ]
    
    # Check for EXACT matches only
    for safety_career in truly_life_critical:
        if career_title == safety_career:
            return True
        # Also check for titles that start with the safety career (e.g., "Senior Registered Nurse")
        if career_title.startswith(safety_career + " ") or career_title.endswith(" " + safety_career):
            return True
    
    # Special case: Check for nurse roles (but not "nurse aide" or similar non-licensed roles)
    if " nurse" in career_title or career_title.startswith("nurse "):
        # Allow non-licensed nursing support roles
        non_licensed_nurse_roles = ["nurse aide", "nurse assistant", "nursing assistant", "nurse technician"]
        if not any(role in career_title for role in non_licensed_nurse_roles):
            return True
    
    return False

def has_relevant_background_for_safety_critical(career: Dict[str, Any], user_data: Dict[str, Any], resume_insights: Dict[str, Any]) -> bool:
    """
    ⚠️  CRITICAL SAFETY FUNCTION ⚠️
    Determines if a user has the relevant background for a safety-critical career.
    
    This function prevents dangerous recommendations by ensuring users have appropriate
    education, experience, or licensing before recommending safety-critical roles.
    
    DO NOT REMOVE OR MODIFY WITHOUT CAREFUL REVIEW - SAFETY IMPLICATIONS
    """
    career_title = career.get("title", "").lower()
    career_desc = career.get("description", "").lower()
    
    # Extract user background information
    education_level = user_data.get("education_level", "").lower()
    certifications = [cert.lower() for cert in (user_data.get("certifications") or [])]
    technical_skills = [skill.lower() for skill in (user_data.get("technical_skills") or [])]
    resume_text = user_data.get("resume_text", "").lower()
    current_role = user_data.get("current_role", "").lower()
    industry_indicators = resume_insights.get("industry_indicators", [])
    
    # Medical/Healthcare careers - require medical background
    if any(keyword in career_title for keyword in ["nurse", "physician", "doctor", "medical", "clinical", "pharmacist", "therapist"]):
        # Check for medical education
        medical_education = any(edu in education_level for edu in ["medical", "nursing", "pharmacy", "clinical", "health"])
        
        # Check for medical certifications
        medical_certs = any(cert in " ".join(certifications) for cert in ["rn", "md", "pharmd", "dpt", "rrt", "medical", "nursing", "clinical"])
        
        # Check for healthcare industry experience
        healthcare_experience = "healthcare" in industry_indicators or any(
            keyword in resume_text for keyword in ["hospital", "clinic", "medical", "patient", "healthcare", "nursing", "clinical"]
        )
        
        # Check for medical role experience
        medical_role = any(keyword in current_role for keyword in ["nurse", "medical", "clinical", "healthcare", "patient"])
        
        return medical_education or medical_certs or healthcare_experience or medical_role
    
    # Engineering careers - require engineering background
    if "engineer" in career_title:
        engineering_education = any(edu in education_level for edu in ["engineering", "engineer"])
        engineering_certs = any(cert in " ".join(certifications) for cert in ["pe", "engineering", "engineer"])
        engineering_experience = any(keyword in resume_text for keyword in ["engineering", "engineer", "technical design", "systems"])
        engineering_role = "engineer" in current_role
        
        return engineering_education or engineering_certs or engineering_experience or engineering_role
    
    # Legal careers - require legal background
    if any(keyword in career_title for keyword in ["lawyer", "attorney", "judge", "legal"]):
        legal_education = any(edu in education_level for edu in ["law", "legal", "juris doctor", "jd"])
        legal_certs = any(cert in " ".join(certifications) for cert in ["bar", "legal", "law"])
        legal_experience = any(keyword in resume_text for keyword in ["legal", "law", "attorney", "litigation"])
        legal_role = any(keyword in current_role for keyword in ["legal", "attorney", "lawyer"])
        
        return legal_education or legal_certs or legal_experience or legal_role
    
    # Aviation careers - require aviation background
    if any(keyword in career_title for keyword in ["pilot", "air traffic"]):
        aviation_education = any(edu in education_level for edu in ["aviation", "aeronautical", "aerospace"])
        aviation_certs = any(cert in " ".join(certifications) for cert in ["pilot", "aviation", "faa", "atc"])
        aviation_experience = any(keyword in resume_text for keyword in ["aviation", "aircraft", "flight", "pilot", "aerospace"])
        aviation_role = any(keyword in current_role for keyword in ["pilot", "aviation", "aircraft", "flight"])
        
        return aviation_education or aviation_certs or aviation_experience or aviation_role
    
    # Public safety careers - require relevant background
    if any(keyword in career_title for keyword in ["police", "firefighter", "paramedic", "emt"]):
        safety_education = any(edu in education_level for edu in ["criminal justice", "fire science", "emergency", "public safety"])
        safety_certs = any(cert in " ".join(certifications) for cert in ["emt", "paramedic", "fire", "police", "safety"])
        safety_experience = any(keyword in resume_text for keyword in ["emergency", "public safety", "first responder", "law enforcement"])
        safety_role = any(keyword in current_role for keyword in ["police", "fire", "emergency", "safety", "security"])
        
        return safety_education or safety_certs or safety_experience or safety_role
    
    # Default: For any other safety-critical career, require some relevant background
    # This is a conservative approach to prevent dangerous recommendations
    return False

def requires_specific_background(career):
    """
    Check if a career requires specific background/prerequisites that most users won't have.
    This is different from safety-critical filtering - these careers aren't dangerous,
    but they have specific entry requirements.
    """
    title = career.get('title', '').lower()
    
    # Government/Law Enforcement careers requiring specific backgrounds
    government_prerequisite_careers = [
        'police chief', 'deputy secretary', 'federal agent', 'detective',
        'sheriff', 'marshal', 'corrections officer', 'probation officer',
        'border patrol agent', 'customs officer', 'immigration officer',
        'secret service agent', 'fbi agent', 'cia analyst', 'nsa analyst',
        'military officer', 'intelligence analyst', 'security clearance',
        'homeland security', 'federal investigator', 'state trooper'
    ]
    
    # Legal careers requiring law degree/bar admission
    legal_prerequisite_careers = [
        'judge', 'magistrate', 'prosecutor', 'district attorney',
        'public defender', 'legal counsel', 'attorney', 'lawyer',
        'law clerk', 'judicial clerk'
    ]
    
    # Academic careers requiring advanced degrees in specific fields
    academic_prerequisite_careers = [
        'professor', 'associate professor', 'assistant professor',
        'department chair', 'dean', 'provost', 'university president',
        'research scientist', 'principal investigator'
    ]
    
    all_prerequisite_careers = government_prerequisite_careers + legal_prerequisite_careers + academic_prerequisite_careers
    
    return any(prereq_career in title for prereq_career in all_prerequisite_careers)

def has_relevant_background_for_prerequisites(career, user_data, resume_insights):
    """
    Check if user has relevant background for careers with specific prerequisites.
    This is more lenient than safety checking - we look for any related experience.
    """
    title = career.get('title', '').lower()
    
    # Extract user background indicators
    skills = user_data.get('skills', [])
    skill_text = ' '.join(skills).lower() if skills else ''
    
    # Get resume indicators
    experience_indicators = resume_insights.get('experience_indicators', [])
    industry_indicators = resume_insights.get('industry_indicators', [])
    roles = resume_insights.get('roles', [])
    
    all_background_text = (skill_text + ' ' +
                          ' '.join(experience_indicators) + ' ' +
                          ' '.join(industry_indicators) + ' ' +
                          ' '.join(roles)).lower()
    
    # Government/Law Enforcement background indicators
    if any(gov_term in title for gov_term in ['police', 'deputy', 'federal', 'government', 'state', 'public service']):
        gov_indicators = [
            'government', 'federal', 'state', 'public service', 'law enforcement',
            'police', 'military', 'security', 'investigation', 'compliance',
            'regulatory', 'policy', 'administration', 'civil service'
        ]
        return any(indicator in all_background_text for indicator in gov_indicators)
    
    # Legal background indicators
    if any(legal_term in title for legal_term in ['judge', 'attorney', 'lawyer', 'legal', 'prosecutor']):
        legal_indicators = [
            'legal', 'law', 'attorney', 'lawyer', 'paralegal', 'litigation',
            'contract', 'compliance', 'regulatory', 'policy', 'juris doctor',
            'bar exam', 'legal research', 'legal writing'
        ]
        return any(indicator in all_background_text for indicator in legal_indicators)
    
    # Academic background indicators
    if any(academic_term in title for academic_term in ['professor', 'dean', 'research', 'university']):
        academic_indicators = [
            'professor', 'teaching', 'research', 'academic', 'university',
            'college', 'education', 'phd', 'doctorate', 'master', 'thesis',
            'publication', 'grant', 'curriculum'
        ]
        return any(indicator in all_background_text for indicator in academic_indicators)
    
    # Default: assume no specific background required
    return True

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8002, reload=True)