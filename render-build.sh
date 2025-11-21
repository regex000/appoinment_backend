#!/bin/bash
# Render build script for Modern Hospital API

set -e

echo "🔨 Building Modern Hospital Backend..."
echo "Python version: $(python --version)"

# Upgrade pip
echo "📦 Upgrading pip..."
pip install --upgrade pip

# Install dependencies
echo "📦 Installing dependencies from requirements.txt..."
pip install -r requirements.txt

echo "✅ Build completed successfully!"
