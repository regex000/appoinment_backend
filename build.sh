#!/bin/bash
# Build script for Render deployment

set -e

echo "🔨 Building Modern Hospital Backend..."

# Install dependencies
echo "📦 Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Run database migrations (if needed)
echo "🗄️  Running database migrations..."
alembic upgrade head || echo "⚠️  No migrations to run or migration failed (this is okay for first deployment)"

echo "✅ Build completed successfully!"
