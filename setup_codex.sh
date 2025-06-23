#!/bin/bash
set -euo pipefail

# Detect OS and install system dependencies
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    echo "Detected Linux - installing system dependencies..."
    sudo apt-get update -y
    sudo apt-get install -y build-essential libblas-dev gfortran
elif [[ "$OSTYPE" == "darwin"* ]]; then
    echo "Detected macOS - checking for Homebrew dependencies..."
    # Check if Homebrew is installed
    if ! command -v brew &> /dev/null; then
        echo "Warning: Homebrew not found. Please install it from https://brew.sh/"
        echo "Some packages may require compilation tools."
    else
        echo "Homebrew found - system should have necessary build tools."
    fi
else
    echo "Unknown OS: $OSTYPE - proceeding without system package installation."
fi

# Create venv if not exists
if [ ! -d ".venv" ]; then
    echo "Creating Python virtual environment..."
    python3 -m venv .venv
fi

echo "Activating virtual environment..."
source .venv/bin/activate

# Install Python packages
echo "Installing Python dependencies..."
if [ -d "/work/cache" ]; then
    # Use cache directory if available (e.g., in containerized environments)
    pip install -r requirements.txt --cache-dir /work/cache
else
    pip install -r requirements.txt
fi

echo "✓ Setup completed successfully!"
echo "To activate the environment in future sessions, run:"
echo "  source .venv/bin/activate"
