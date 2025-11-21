#!/bin/bash
# Build script for Render deployment

set -e

echo "🔨 Building Modern Hospital Backend..."

# Upgrade pip, setuptools, and wheel
echo "📦 Upgrading pip, setuptools, and wheel..."
pip install --upgrade pip setuptools wheel

# Install dependencies
echo "📦 Installing dependencies..."
pip install -r requirements.txt

# Make start scripts executable
chmod +x start.sh render.sh

echo "✅ Build completed successfully!"
