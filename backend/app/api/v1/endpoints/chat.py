from fastapi import APIRouter, Depends, HTTPException, Request
from app.api.v1.endpoints.auth import get_current_user
from app.models.user import User
from app.schemas.chat import ChatRequest, ChatResponse
from app.services.chat_service import get_ai_chat_response
from motor.motor_asyncio import AsyncIOMotorDatabase

router = APIRouter()

async def get_latest_assessment(db: AsyncIOMotorDatabase, user_id: str):
    """Get the user's latest assessment from MongoDB"""
    assessment = await db.assessments.find_one(
        {"user_id": user_id},
        sort=[("created_at", -1)]
    )
    
    if assessment:
        return {
            "skills": assessment.get("skills", []),
            "interests": assessment.get("interests", []),
            "recommendations": assessment.get("recommendations", []),
        }
    
    # Return mock data if no assessment found
    return {
        "skills": ["Python", "FastAPI", "SQL"],
        "interests": ["Web Development", "Data Science"],
        "recommendations": [
            {"career": "Backend Developer", "match_score": 95},
            {"career": "Data Analyst", "match_score": 88},
        ],
    }

@router.post("/", response_model=ChatResponse)
async def chat_with_ai(
    chat_request: ChatRequest,
    request: Request,
    current_user: User = Depends(get_current_user),
):
    """
    Handles chat messages from the user and returns an AI-generated response.
    """
    try:
        db: AsyncIOMotorDatabase = request.app.mongodb
        
        # Get the user's most recent assessment data
        assessment_data = await get_latest_assessment(db, current_user["_id"])

        if not assessment_data:
            raise HTTPException(status_code=404, detail="No assessment found for this user.")

        # Get a response from the AI service
        ai_reply = get_ai_chat_response(chat_request.message, assessment_data)

        return ChatResponse(reply=ai_reply)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
