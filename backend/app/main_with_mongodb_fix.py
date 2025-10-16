#!/usr/bin/env python3
"""
Fixed Backend Main with MongoDB Replacement
==========================================
This version patches MongoDB to work immediately
"""

# CRITICAL: Import the MongoDB replacement FIRST before any motor imports
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
import mongodb_replacement

# Now import the rest normally
from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
from app.core.config import settings
from app.core.security import verify_token, create_access_token
from app.models.user import User, UserCreate, UserLogin
from app.models.recommendation import RecommendationRequest, RecommendationResponse
from app.api.v1.router import api_router
import asyncio
from datetime import datetime
import hashlib
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(
    title="Career Recommendation API",
    description="AI-powered career recommendation system",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Security
security = HTTPBearer()

# Database connection
client = None
db = None

@app.on_event("startup")
async def startup_event():
    global client, db
    print("🚀 Starting up with MongoDB replacement...")
    
    # Setup the test user in the in-memory database
    await mongodb_replacement.setup_test_user()
    
    # Connect using the patched client (will use in-memory database)
    db_url = os.getenv('DATABASE_URL') or os.getenv('MONGODB_URL') or 'mongodb://localhost:27017'
    client = AsyncIOMotorClient(db_url)
    db = client['recommender']
    
    print("✅ MongoDB replacement connected successfully")

@app.on_event("shutdown")
async def shutdown_event():
    if client:
        client.close()

# Include API routes
app.include_router(api_router, prefix="/api/v1")

# Health check
@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "database": "in-memory-mongodb-replacement"
    }

# Root endpoint
@app.get("/")
async def root():
    return {
        "message": "Career Recommendation API",
        "version": "1.0.0",
        "database": "MongoDB Replacement (In-Memory)",
        "status": "ready"
    }

# Test endpoint to verify user exists
@app.get("/test-user")
async def test_user():
    try:
        user = await db.users.find_one({"email": "bryandavidhaas@gmail.com"})
        if user:
            # Convert ObjectId to string for JSON serialization
            user['_id'] = str(user['_id'])
            return {
                "status": "success",
                "user_found": True,
                "user": user
            }
        else:
            return {
                "status": "success",
                "user_found": False,
                "message": "User not found"
            }
    except Exception as e:
        return {
            "status": "error",
            "error": str(e)
        }

if __name__ == "__main__":
    import uvicorn
    print("🚀 Starting Career Recommendation API with MongoDB replacement...")
    uvicorn.run(app, host="0.0.0.0", port=8000)