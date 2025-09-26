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

async def init_db():
    """Initializes the database connection and Beanie."""
    mongo_url = os.getenv("MONGODB_URL")
    if not mongo_url:
        raise ValueError("MONGODB_URL environment variable not set.")

    client = AsyncIOMotorClient(mongo_url)
    db_name = os.getenv("MONGODB_DATABASE", "career_platform")
    
    from .models import SkillModel, CareerModel, UserProfileModel, RecommendationModel

    await init_beanie(
        database=client[db_name],
        document_models=[
            SkillModel,
            CareerModel,
            UserProfileModel,
            RecommendationModel,
        ],
    )
    print(f"Successfully connected to MongoDB database: {db_name}")