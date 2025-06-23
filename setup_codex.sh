#!/bin/bash
set -euo pipefail

# Install system deps
sudo apt-get update -y
sudo apt-get install -y build-essential libblas-dev gfortran

# Create venv if not exists
if [ ! -d ".venv" ]; then
    python3 -m venv .venv
fi
source .venv/bin/activate

pip install -r requirements.txt --cache-dir /work/cache
