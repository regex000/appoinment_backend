#!/bin/bash
# Build script for Render deployment

set -e

# Change to backend directory if not already there
if [ ! -f "requirements.txt" ]; then
    cd backend
fi

echo "🔨 Building Modern Hospital Backend..."
echo "Python version: $(python --version)"
echo "Python executable: $(which python)"
echo "Current directory: $(pwd)"

# Verify we're using Python 3.11
PYTHON_VERSION=$(python -c 'import sys; print(f"{sys.version_info.major}.{sys.version_info.minor}")')
echo "Detected Python version: $PYTHON_VERSION"

if [[ ! "$PYTHON_VERSION" =~ ^3\.11 ]]; then
    echo "⚠️  WARNING: Expected Python 3.11.x but got $PYTHON_VERSION"
    echo "This may cause compatibility issues with SQLAlchemy"
fi

# Upgrade pip, setuptools, and wheel
echo "📦 Upgrading pip, setuptools, and wheel..."
pip install --upgrade pip setuptools wheel

# Install dependencies
echo "📦 Installing dependencies..."
pip install -r requirements.txt

# Verify uvicorn.workers is available
echo "✅ Verifying uvicorn.workers availability..."
python -c "from uvicorn.workers import UvicornWorker; print('✅ UvicornWorker available')" || echo "⚠️  UvicornWorker not found"

# Make start scripts executable
chmod +x start.sh render.sh 2>/dev/null || true

echo "✅ Build completed successfully!"
