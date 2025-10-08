from fastapi import APIRouter
from .endpoints import auth, assessment, recommendation, ai, chat

api_router = APIRouter()
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(assessment.router, prefix="/assessment", tags=["assessment"])
api_router.include_router(recommendation.router, prefix="/recommendation", tags=["recommendation"])
api_router.include_router(ai.router, prefix="/ai", tags=["ai"])
api_router.include_router(chat.router, prefix="/chat", tags=["chat"])