#!/bin/bash
# Build script for Render backend
set -e

echo "=== Installing Poetry ==="
pip install poetry

echo "=== Installing dependencies ==="
cd backend
poetry config virtualenvs.in-project true
poetry install --only main

echo "=== Build complete ==="
