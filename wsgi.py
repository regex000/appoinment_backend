"""
WSGI entry point - DO NOT USE DIRECTLY
This is kept for reference only. Use app.py with uvicorn workers instead.
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

from app.main import app

# This exports the FastAPI app for use with gunicorn + uvicorn workers
# Command: gunicorn --worker-class uvicorn.workers.UvicornWorker wsgi:app

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
