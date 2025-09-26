"""
MongoDB database configuration and connection setup.
"""

import os
from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
from typing import Optional
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Database:
    client: Optional[AsyncIOMotorClient] = None
    database = None

# Database instance
db = Database()

async def connect_to_mongo():
    """Create database connection"""
    mongodb_url = os.getenv("MONGODB_URL", "mongodb://localhost:27017")
    database_name = os.getenv("MONGODB_DATABASE", "career_recommendations")
    
    # Create Motor client
    db.client = AsyncIOMotorClient(mongodb_url)
    db.database = db.client[database_name]
    
    # Import models for Beanie initialization
    from .models import UserProfileModel, CareerModel, RecommendationModel, SkillModel
    
    # Initialize Beanie with the models
    await init_beanie(
        database=db.database,
        document_models=[
            UserProfileModel,
            CareerModel, 
            RecommendationModel,
            SkillModel
        ]
    )
    
    print(f"Connected to MongoDB: {mongodb_url}/{database_name}")

async def close_mongo_connection():
    """Close database connection"""
    if db.client:
        db.client.close()
        print("Disconnected from MongoDB")

def get_database():
    """Get database instance"""
    return db.database