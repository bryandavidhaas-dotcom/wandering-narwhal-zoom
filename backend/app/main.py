import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from motor.motor_asyncio import AsyncIOMotorClient
from .api.v1.router import api_router

# Load environment variables from .env file
load_dotenv()

app = FastAPI(
    title="AI-Powered Recommendation Engine",
    description="API for the AI-Powered Recommendation Engine.",
    version="1.0.0",
)

# Configure CORS
origins = os.getenv("CORS_ORIGINS", "http://localhost:3000").split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup_db_client():
    try:
        database_url = os.getenv("DATABASE_URL", "mongodb://localhost:27017")
        app.mongodb_client = AsyncIOMotorClient(database_url)
        app.mongodb = app.mongodb_client["recommender"]
        # Test the connection
        await app.mongodb.command("ping")
        print(f"✅ Connected to MongoDB at {database_url}")
    except Exception as e:
        print(f"⚠️  MongoDB connection failed: {e}")
        print("🔄 Server will continue without database functionality")
        app.mongodb_client = None
        app.mongodb = None

@app.on_event("shutdown")
async def shutdown_db_client():
    app.mongodb_client.close()

@app.get("/api/v1/health")
async def health_check():
    try:
        # Check if the database is connected
        await app.mongodb.command("ping")
        return {"status": "ok", "database": "connected"}
    except Exception as e:
        return {"status": "ok", "database": "disconnected", "error": str(e)}

app.include_router(api_router, prefix="/api/v1")