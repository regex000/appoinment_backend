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

# Copy public directory (doctor photos and other static assets)
echo "📁 Copying static files..."
if [ -d "public" ]; then
    mkdir -p /opt/render/project/public
    cp -r public/* /opt/render/project/public/ || true
    echo "✅ Static files copied successfully"
else
    echo "⚠️  Public directory not found, skipping static files copy"
fi

echo "✅ Build completed successfully!"
