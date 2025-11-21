#!/bin/bash
# Render start script for Modern Hospital API

set -e

echo "🚀 Starting Modern Hospital Backend on Render..."
echo "Environment: ${ENVIRONMENT:-production}"
echo "Port: ${PORT:-8000}"

# Start the application with uvicorn
exec uvicorn app:app \
  --host 0.0.0.0 \
  --port ${PORT:-8000} \
  --log-level info
