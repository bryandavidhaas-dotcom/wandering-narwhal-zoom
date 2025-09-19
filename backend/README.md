# Career Recommendation API Backend

A FastAPI-based backend service for the career recommendation engine with MongoDB support.

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- pip
- MongoDB (local installation or MongoDB Atlas)

### Installation
```bash
cd backend
pip install -r requirements.txt
```

### MongoDB Setup

#### Option 1: Local MongoDB
1. Install MongoDB locally: https://docs.mongodb.com/manual/installation/
2. Start MongoDB service:
   ```bash
   # Windows
   net start MongoDB
   
   # macOS/Linux
   sudo systemctl start mongod
   ```

#### Option 2: MongoDB Atlas (Cloud)
1. Create account at https://www.mongodb.com/atlas
2. Create a cluster and get connection string
3. Update `.env` file with your Atlas connection string

### Environment Configuration
Copy and configure the `.env` file:
```bash
# MongoDB Configuration
MONGODB_URL=mongodb://localhost:27017
MONGODB_DATABASE=career_recommendations

# For MongoDB Atlas:
# MONGODB_URL=mongodb+srv://<username>:<password>@<cluster>.mongodb.net/<database>?retryWrites=true&w=majority
```

### Running the Server

#### Simple Server (Mock Data)
```bash
python -m uvicorn simple_server:app --host 0.0.0.0 --port 8000 --reload
```

#### MongoDB-Enabled Server
```bash
python -m uvicorn mongo_server:app --host 0.0.0.0 --port 8000 --reload
```

## 📡 API Endpoints

### Health Check
- `GET /health` - Check server health status and database connectivity

### User Management (MongoDB Server)
- `POST /users` - Create new user profile
- `GET /users/{user_id}` - Get user profile by ID
- `PUT /users/{user_id}` - Update user profile

### Career Recommendations
- `POST /recommendations` - Get personalized career recommendations (with caching)
- `GET /recommendations/categories` - Get recommendations organized by category
- `GET /recommendations/{user_id}/history` - Get user's recommendation history
- `POST /recommendations/explain/{career_id}` - Get detailed explanation for a recommendation

### Career Data
- `GET /careers` - Get all available careers (with pagination)
- `GET /careers/{career_id}` - Get specific career details

### Skills Data
- `GET /skills` - Get all available skills (with pagination)

### Database Management
- `POST /admin/seed-data` - Seed database with initial data (development only)

### Analytics
- `GET /statistics` - Get comprehensive recommendation statistics

## 🔧 Configuration

Environment variables are configured in `.env`:

```env
API_HOST=0.0.0.0
API_PORT=8000
DEBUG=True
CORS_ORIGINS=http://localhost:5137,http://localhost:3000,http://localhost:5173
```

## 📊 API Documentation

Once the server is running, visit:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 🏗️ Architecture

The backend uses:
- **FastAPI** for the web framework
- **Pydantic** for data validation
- **Uvicorn** as the ASGI server
- **CORS middleware** for frontend integration

## 📁 Project Structure

```
backend/
├── .env                 # Environment configuration
├── .gitignore          # Git ignore rules
├── README.md           # This file
├── requirements.txt    # Python dependencies
├── simple_server.py    # Main FastAPI application
└── main.py            # Alternative server (with full engine integration)
```

## 🔄 Development

The server runs in development mode with auto-reload enabled. Any changes to the code will automatically restart the server.

## 🧪 Testing

Test the API endpoints:

```bash
# Health check
curl http://localhost:8000/health

# Get recommendations
curl -X POST http://localhost:8000/recommendations \
  -H "Content-Type: application/json" \
  -d '{"limit": 5}'

# Get all careers
curl http://localhost:8000/careers
```

## 🚀 Deployment

For production deployment:

1. Set `DEBUG=False` in `.env`
2. Use a production ASGI server like Gunicorn with Uvicorn workers
3. Configure proper CORS origins
4. Set up environment-specific configuration

## 📝 Notes

- The current implementation uses mock data for demonstration
- CORS is configured for local development (ports 3000, 5137, 5173)
- The server supports both JSON requests and responses
- All endpoints include proper error handling and HTTP status codes