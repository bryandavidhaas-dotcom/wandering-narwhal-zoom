from fastapi import APIRouter, Depends, HTTPException
from ....models.assessment import UserAssessment
from ....models.ai import RecommendationSet, TuningPrompt
from ....models.user import User
from ..endpoints.auth import get_current_user
from ....ai.ai_client import AIClient
from ....core.config import settings

router = APIRouter()

@router.post("/recommendations", response_model=RecommendationSet)
async def get_ai_recommendations(assessment: UserAssessment, current_user: User = Depends(get_current_user)):
    try:
        print(f"API Key: {settings.AI_API_KEY}")
        ai_client = AIClient(api_key=settings.AI_API_KEY)
        recommendations = ai_client.get_recommendations(assessment.model_dump())
        return RecommendationSet(recommendations=recommendations)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error in get_ai_recommendations: {e}")

@router.post("/tune", response_model=RecommendationSet)
async def tune_ai_recommendations(tuning_prompt: TuningPrompt, current_user: User = Depends(get_current_user)):
    try:
        ai_client = AIClient(api_key=settings.AI_API_KEY)
        recommendations = ai_client.tune_recommendations(tuning_prompt.current_recommendations, tuning_prompt.prompt)
        return RecommendationSet(recommendations=recommendations)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error in tune_ai_recommendations: {e}")