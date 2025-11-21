#!/bin/bash
# Startup script for Render deployment

set -e

echo "🚀 Starting Modern Hospital Backend..."
echo "Environment: $ENVIRONMENT"
echo "Debug: $DEBUG"
echo "Port: $PORT"

# Run the application with gunicorn and uvicorn workers
exec gunicorn \
  -w 4 \
  -k uvicorn.workers.UvicornWorker \
  --bind 0.0.0.0:${PORT:-8000} \
  --timeout 120 \
  --access-logfile - \
  --error-logfile - \
  wsgi:app
