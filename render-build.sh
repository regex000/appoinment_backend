#!/bin/bash
# Build script for Render deployment

set -e

# Change to backend directory if not already there
if [ ! -f "requirements.txt" ]; then
    cd backend
fi

echo "🔨 Building Modern Hospital Backend..."
echo "Python version: $(python --version)"
echo "Current directory: $(pwd)"

# Upgrade pip, setuptools, and wheel
echo "📦 Upgrading pip, setuptools, and wheel..."
pip install --upgrade pip setuptools wheel

# Install dependencies
echo "📦 Installing dependencies..."
pip install -r requirements.txt

# Make start scripts executable
chmod +x start.sh render.sh 2>/dev/null || true

echo "✅ Build completed successfully!"
