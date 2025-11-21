#!/bin/bash
# Custom build script for Render - forces Python 3.11

set -e

echo "🔨 Starting custom build process..."
echo "Current Python: $(python --version)"

# If we're on Python 3.13, we need to handle it differently
PYTHON_VERSION=$(python -c 'import sys; print(f"{sys.version_info.major}.{sys.version_info.minor}")')

if [[ "$PYTHON_VERSION" == "3.13" ]]; then
    echo "⚠️  Detected Python 3.13 - SQLAlchemy 2.0.x has compatibility issues"
    echo "Installing compatibility workaround..."
    
    # Install a patched version or use a workaround
    pip install --upgrade pip setuptools wheel
    
    # Try to install with compatibility flags
    pip install --no-cache-dir -r requirements.txt || {
        echo "❌ Standard install failed, trying with legacy resolver..."
        pip install --use-deprecated=legacy-resolver -r requirements.txt
    }
else
    echo "✅ Python $PYTHON_VERSION detected - proceeding normally"
    pip install --upgrade pip setuptools wheel
    pip install -r requirements.txt
fi

echo "✅ Build completed!"
