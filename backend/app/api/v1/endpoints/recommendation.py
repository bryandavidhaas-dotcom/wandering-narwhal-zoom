from fastapi import APIRouter, Depends, Request, HTTPException
from app.models.recommendation import RecommendationSet
from app.api.v1.endpoints.auth import get_current_user
from app.models.user import User
from motor.motor_asyncio import AsyncIOMotorDatabase
from pydantic import BaseModel

import os
from app.ai.ai_client import AIClient
from app.models.tuning import TuningInteraction

router = APIRouter()

# Initialize the AI Client
# In a real application, the API key should be managed securely (e.g., environment variables)
ai_client = AIClient(api_key=os.getenv("AI_API_KEY", "your-default-api-key"))

@router.post("/generate-recommendations", response_model=RecommendationSet)
async def generate_recommendations(
    request: Request,
    current_user: User = Depends(get_current_user)
):
    db: AsyncIOMotorDatabase = request.app.mongodb
    
    assessment = await db.assessments.find_one(
        {"user_id": current_user["_id"]},
        sort=[("created_at", -1)]
    )
    
    if not assessment:
        raise HTTPException(status_code=404, detail="No assessment found for the current user.")
        
    # The assessment data is passed directly to the AI client
    recommendations = await ai_client.get_recommendations(assessment)
    
    recommendation_set = RecommendationSet(
        user_id=current_user["_id"],
        recommendations=recommendations
    )
    
    await db.recommendations.insert_one(recommendation_set.dict(by_alias=True))
    
    return recommendation_set

class TuneRequest(BaseModel):
    recommendation_set_id: str
    prompt: str

@router.post("/tune-recommendations", response_model=RecommendationSet)
async def tune_recommendations(
    tune_request: TuneRequest,
    request: Request,
    current_user: User = Depends(get_current_user)
):
    db: AsyncIOMotorDatabase = request.app.mongodb

    recommendation_set = await db.recommendations.find_one({"_id": tune_request.recommendation_set_id})
    if not recommendation_set:
        raise HTTPException(status_code=404, detail="Recommendation set not found.")

    current_recommendations = recommendation_set["recommendations"]
    
    # The current recommendations and prompt are passed to the AI client
    refined_recommendations = await ai_client.tune_recommendations(current_recommendations, tune_request.prompt)
    
    new_recommendation_set = RecommendationSet(
        user_id=current_user["_id"],
        recommendations=refined_recommendations
    )
    
    await db.recommendations.insert_one(new_recommendation_set.dict(by_alias=True))
    
    tuning_interaction = TuningInteraction(
        recommendation_set_id=new_recommendation_set.id,
        user_id=current_user["_id"],
        prompt=tune_request.prompt,
        response=refined_recommendations
    )
    await db.tuning_interactions.insert_one(tuning_interaction.dict(by_alias=True))
    
    return new_recommendation_set

@router.get("/get-latest-recommendations", response_model=RecommendationSet)
async def get_latest_recommendations(
    request: Request,
    current_user: User = Depends(get_current_user)
):
    db: AsyncIOMotorDatabase = request.app.mongodb
    
    recommendation_set = await db.recommendations.find_one(
        {"user_id": current_user["_id"]},
        sort=[("created_at", -1)]
    )
    
    if not recommendation_set:
        raise HTTPException(status_code=404, detail="No recommendations found for the current user.")
        
    return recommendation_set