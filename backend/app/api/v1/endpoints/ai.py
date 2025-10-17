from fastapi import APIRouter, Depends, HTTPException
from app.models.assessment import UserAssessment
from app.models.ai import RecommendationSet, TuningPrompt
from app.models.user import User
from app.api.v1.endpoints.auth import get_current_user
from app.ai.ai_client import AIClient
from app.core.config import settings

router = APIRouter()

@router.post("/recommendations", response_model=RecommendationSet)
async def get_ai_recommendations(assessment_data: dict, current_user: dict = Depends(get_current_user)):
    try:
        print(f"API Key: {settings.AI_API_KEY}")
        # Add user_id to assessment data (current_user is a dict from MongoDB)
        assessment_data["user_id"] = str(current_user["_id"])
        
        # Create UserAssessment object for validation
        assessment = UserAssessment(**assessment_data)
        
        ai_client = AIClient(api_key=settings.AI_API_KEY)
        recommendations = await ai_client.get_recommendations(assessment.model_dump())
        return RecommendationSet(recommendations=recommendations)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error in get_ai_recommendations: {e}")

@router.post("/tune", response_model=RecommendationSet)
async def tune_ai_recommendations(tuning_prompt: TuningPrompt, current_user: dict = Depends(get_current_user)):
    try:
        ai_client = AIClient(api_key=settings.AI_API_KEY)
        recommendations = await ai_client.tune_recommendations(tuning_prompt.current_recommendations, tuning_prompt.prompt)
        return RecommendationSet(recommendations=recommendations)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error in tune_ai_recommendations: {e}")