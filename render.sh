#!/bin/bash
# Render deployment script

set -e

echo "🚀 Starting Modern Hospital Backend on Render..."
echo "Environment: $ENVIRONMENT"
echo "Debug: $DEBUG"
echo "Port: $PORT"

# Run the application with gunicorn and uvicorn workers
exec gunicorn \
  --config gunicorn_config.py \
  wsgi:app
