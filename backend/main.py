import uvicorn
import os

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8002, reload=True, reload_dirs=[os.path.join(os.path.dirname(__file__), "app")])