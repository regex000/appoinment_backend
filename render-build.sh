#!/bin/bash
# Build script for Render deployment

set -e

echo "🔨 Building Modern Hospital Backend..."
echo "Python version: $(python --version)"

# Upgrade pip, setuptools, and wheel
echo "📦 Upgrading pip, setuptools, and wheel..."
pip install --upgrade pip setuptools wheel

# Install dependencies with compatibility flags for Python 3.13
echo "📦 Installing dependencies..."
pip install --upgrade -r requirements.txt

# Make start scripts executable
chmod +x start.sh render.sh

echo "✅ Build completed successfully!"
