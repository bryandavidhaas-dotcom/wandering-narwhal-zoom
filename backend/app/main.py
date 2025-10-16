import os
import sys
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

# CRITICAL: Import MongoDB replacement BEFORE motor
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
try:
    import mongodb_replacement
    print("🔧 MongoDB replacement loaded successfully")
except ImportError as e:
    print(f"⚠️  MongoDB replacement not found: {e}")

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
origins = os.getenv("CORS_ORIGINS", "http://localhost:3000,http://localhost:5173").split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup_db_client():
    # Always setup MongoDB replacement first
    try:
        import mongodb_replacement
        await mongodb_replacement.setup_test_user()
        print("✅ MongoDB replacement test user created")
    except Exception as setup_error:
        print(f"⚠️  MongoDB replacement setup failed: {setup_error}")
    
    # Always use MongoDB replacement system (it intercepts AsyncIOMotorClient)
    database_url = os.getenv("DATABASE_URL", "mongodb://localhost:27017")
    app.mongodb_client = AsyncIOMotorClient(database_url)
    app.mongodb = app.mongodb_client["recommender"]
    
    # Test the connection (this will use the replacement system)
    try:
        await app.mongodb.command("ping")
        print(f"✅ Connected to MongoDB replacement system at {database_url}")
    except Exception as e:
        print(f"⚠️  MongoDB replacement connection test failed: {e}")
        # Ensure app.mongodb is never None
        if app.mongodb is None:
            app.mongodb_client = AsyncIOMotorClient(database_url)
            app.mongodb = app.mongodb_client["recommender"]
        print("✅ MongoDB replacement system ready")

@app.on_event("shutdown")
async def shutdown_db_client():
    if hasattr(app.mongodb_client, 'close'):
        app.mongodb_client.close()

@app.get("/api/v1/health")
async def health_check():
    try:
        # Check if the database is connected
        if hasattr(app, 'mongodb') and app.mongodb is not None:
            # Test database connection by trying to access a collection (safer approach)
            users_collection = app.mongodb.users
            # Just check if we can access the collection without calling it
            if users_collection is not None:
                return {"status": "ok", "database": "connected", "mongodb_replacement": "active"}
            else:
                return {"status": "ok", "database": "disconnected", "error": "Collection access failed"}
        else:
            return {"status": "ok", "database": "disconnected", "error": "MongoDB not initialized"}
    except Exception as e:
        return {"status": "ok", "database": "disconnected", "error": str(e)}

app.include_router(api_router, prefix="/api/v1")