"""
ASGI application entry point for Render deployment.
This file is used when Render runs: gunicorn app:app
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

# Export for gunicorn
__all__ = ["app"]

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
