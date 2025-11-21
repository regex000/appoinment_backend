#!/bin/bash
# Render deployment script for Modern Hospital Backend

set -e

echo "🚀 Starting Modern Hospital Backend on Render..."
echo "Environment: ${ENVIRONMENT:-production}"
echo "Debug: ${DEBUG:-false}"
echo "Port: ${PORT:-8000}"

# Ensure we're in the backend directory
cd "$(dirname "$0")"

# Run the application with gunicorn and uvicorn workers
# This properly handles ASGI applications like FastAPI
exec gunicorn \
  --config gunicorn_config.py \
  --worker-class uvicorn.workers.UvicornWorker \
  --bind 0.0.0.0:${PORT:-8000} \
  --workers ${WORKERS:-4} \
  --timeout 120 \
  --access-logfile - \
  --error-logfile - \
  app:app
