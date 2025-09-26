# Backend Server for Career Recommendation Engine

This directory contains the FastAPI backend server that powers the career recommendation engine.

## Running the Server

To run the backend server for development, use the following command from the root directory of the project:

```bash
uvicorn backend.simple_server:app --host 0.0.0.0 --port 8002 --reload
```

### Port Configuration

-   **Backend Server**: The server is configured to run on **port 8002**. This is defined in `backend/simple_server.py`.
-   **Frontend API Calls**: The frontend is configured to make API calls to `http://localhost:8002`. This is defined in `frontend/src/config/api.ts`.

**Important**: Ensure that the port in `backend/simple_server.py` and the API URL in `frontend/src/config/api.ts` are aligned to prevent connection errors.