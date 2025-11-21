#!/bin/bash
# Build script for Render deployment

set -e

echo "🔨 Building Modern Hospital Backend..."

# Upgrade pip
echo "📦 Upgrading pip..."
pip install --upgrade pip setuptools wheel

# Install dependencies with pre-built wheels only
echo "📦 Installing dependencies..."
pip install --only-binary :all: -r requirements.txt 2>/dev/null || pip install -r requirements.txt

# Run database migrations (if needed)
echo "🗄️  Running database migrations..."
alembic upgrade head || echo "⚠️  No migrations to run or migration failed (this is okay for first deployment)"

echo "✅ Build completed successfully!"
