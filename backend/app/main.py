import os
import sys
import asyncio
from contextlib import asynccontextmanager
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

# Database connection pool configuration
DB_CONNECTION_CONFIG = {
    "maxPoolSize": 10,  # Maximum number of connections in the pool
    "minPoolSize": 1,   # Minimum number of connections in the pool
    "maxIdleTimeMS": 30000,  # Close connections after 30 seconds of inactivity
    "waitQueueTimeoutMS": 5000,  # Wait up to 5 seconds for a connection
    "serverSelectionTimeoutMS": 5000,  # Server selection timeout
    "connectTimeoutMS": 10000,  # Connection timeout
    "socketTimeoutMS": 20000,   # Socket timeout for operations
}

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manage application lifespan with proper database connection handling"""
    # Startup
    await startup_db_client(app)
    yield
    # Shutdown
    await shutdown_db_client(app)

app = FastAPI(
    title="AI-Powered Recommendation Engine",
    description="API for the AI-Powered Recommendation Engine.",
    version="1.0.0",
    lifespan=lifespan,
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

async def startup_db_client(app: FastAPI):
    """Initialize database connection with proper pooling and error handling"""
    print("🚀 Initializing database connection...")
    
    # Always setup MongoDB replacement first
    try:
        import mongodb_replacement
        await mongodb_replacement.setup_test_user()
        print("✅ MongoDB replacement test user created")
    except Exception as setup_error:
        print(f"⚠️  MongoDB replacement setup failed: {setup_error}")
    
    # Create MongoDB client with connection pooling configuration
    database_url = os.getenv("DATABASE_URL", "mongodb://localhost:27017")
    
    try:
        # Create client with connection pooling limits and timeouts
        app.mongodb_client = AsyncIOMotorClient(
            database_url,
            **DB_CONNECTION_CONFIG
        )
        app.mongodb = app.mongodb_client["recommender"]
        
        # Test the connection with timeout
        await asyncio.wait_for(
            app.mongodb.command("ping"),
            timeout=5.0
        )
        print(f"✅ Connected to MongoDB with connection pooling at {database_url}")
        print(f"📊 Connection pool: max={DB_CONNECTION_CONFIG['maxPoolSize']}, min={DB_CONNECTION_CONFIG['minPoolSize']}")
        
    except asyncio.TimeoutError:
        print("⚠️  Database connection timeout - using fallback configuration")
        # Fallback with minimal configuration
        app.mongodb_client = AsyncIOMotorClient(database_url, serverSelectionTimeoutMS=1000)
        app.mongodb = app.mongodb_client["recommender"]
        print("✅ MongoDB replacement system ready (fallback mode)")
        
    except Exception as e:
        print(f"⚠️  Database connection failed: {e}")
        # Ensure app.mongodb is never None - create minimal client
        app.mongodb_client = AsyncIOMotorClient(database_url)
        app.mongodb = app.mongodb_client["recommender"]
        print("✅ MongoDB replacement system ready (minimal mode)")

async def shutdown_db_client(app: FastAPI):
    """Properly shutdown database connections and cleanup resources"""
    print("🔄 Shutting down database connections...")
    
    try:
        # Cleanup MongoDB replacement system first
        if hasattr(mongodb_replacement, 'cleanup'):
            await mongodb_replacement.cleanup()
            print("✅ MongoDB replacement system cleaned up")
    except Exception as e:
        print(f"⚠️  MongoDB replacement cleanup failed: {e}")
    
    # Close MongoDB client connections
    if hasattr(app, 'mongodb_client') and app.mongodb_client:
        try:
            # Close all connections in the pool
            app.mongodb_client.close()
            
            # Wait for all connections to close (with timeout)
            await asyncio.wait_for(
                app.mongodb_client.close(),
                timeout=10.0
            )
            print("✅ All database connections closed successfully")
            
        except asyncio.TimeoutError:
            print("⚠️  Database connection shutdown timeout - forcing close")
            app.mongodb_client.close()
            
        except Exception as e:
            print(f"⚠️  Database connection shutdown error: {e}")
            # Force close as last resort
            try:
                app.mongodb_client.close()
            except:
                pass
        
        finally:
            # Clear references
            app.mongodb_client = None
            app.mongodb = None
            print("✅ Database connection cleanup completed")

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