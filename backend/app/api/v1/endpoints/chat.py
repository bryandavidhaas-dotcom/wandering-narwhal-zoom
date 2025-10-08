from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.security import get_current_user
from app.models.user import User
from app.schemas.chat import ChatRequest, ChatResponse
from app.services.chat_service import get_ai_chat_response

router = APIRouter()

# Helper functions
def get_db():
    # This should yield a database session. You'll need to implement the actual session creation.
    # For now, we'll just return None.
    yield None

def get_latest_assessment(db: Session, user_id: int):
    # This should query the database for the user's latest assessment.
    # For now, we'll return some mock data.
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
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Handles chat messages from the user and returns an AI-generated response.
    """
    try:
        # Get the user's most recent assessment data (you'll need to implement this)
        assessment_data = get_latest_assessment(db, current_user.id)

        if not assessment_data:
            raise HTTPException(status_code=404, detail="No assessment found for this user.")

        # Get a response from the AI service
        ai_reply = get_ai_chat_response(chat_request.message, assessment_data)

        return ChatResponse(reply=ai_reply)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
