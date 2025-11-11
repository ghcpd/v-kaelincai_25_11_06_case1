#!/bin/bash

# Setup script for Project B - Post-Feature Enhanced Search

echo "Setting up Project B - Post-Feature Enhanced Search..."

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Create necessary directories
echo "Creating directories..."
mkdir -p results
mkdir -p logs
mkdir -p data

echo "Setup complete!"
echo "To activate the virtual environment, run: source venv/bin/activate"

