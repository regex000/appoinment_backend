"""
FastAPI application entry point for Render deployment.
Uses uvicorn directly (no gunicorn needed on Render free tier).
"""

import sys
from pathlib import Path

# Add the backend directory to the Python path
backend_dir = Path(__file__).parent
sys.path.insert(0, str(backend_dir))

# Apply Python 3.13 compatibility patches BEFORE importing SQLAlchemy
try:
    import python313_compat  # noqa: F401
except ImportError:
    pass

# Import the FastAPI app
from app.main import app

# Export for uvicorn
__all__ = ["app"]

if __name__ == "__main__":
    import uvicorn
    import os
    
    port = int(os.getenv('PORT', 8000))
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=port,
        log_level="info"
    )
