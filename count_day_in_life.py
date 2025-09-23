import asyncio
import os
from pymongo import MongoClient
from dotenv import load_dotenv

async def count_day_in_life_descriptions():
    """
    Connects to the MongoDB database using pymongo and counts the number of careers
    with and without a 'day_in_life' description.
    """
    # Load environment variables from .env file
    load_dotenv()

    mongodb_url = os.getenv("MONGODB_URL", "mongodb://localhost:27017")
    database_name = os.getenv("MONGODB_DATABASE", "career_recommendations")

    client = MongoClient(mongodb_url)
    db = client[database_name]
    careers_collection = db["careers"]

    # Count careers that have the 'day_in_life' field and it's not empty or null
    with_day_in_life = careers_collection.count_documents(
        {"day_in_life": {"$exists": True, "$ne": None, "$ne": ""}}
    )

    # Count careers that do not have the 'day_in_life' field or it is empty or null
    without_day_in_life = careers_collection.count_documents(
        {"$or": [
            {"day_in_life": {"$exists": False}},
            {"day_in_life": None},
            {"day_in_life": ""}
        ]}
    )

    total_careers = careers_collection.count_documents({})

    print(f"Total careers in the database: {total_careers}")
    print(f"Careers WITH a personalized 'Day in the Life' description: {with_day_in_life}")
    print(f"Careers WITHOUT a personalized 'Day in the Life' description: {without_day_in_life}")

    client.close()

if __name__ == "__main__":
    asyncio.run(count_day_in_life_descriptions())