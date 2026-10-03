"""
Root entry point for FIRE-X Platform API
Runs the backend.main application
"""
import uvicorn
from backend.main import app

if __name__ == "__main__":
    uvicorn.run("backend.main:app", host="0.0.0.0", port=8000, reload=True)
