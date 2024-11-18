#!/bin/bash
cd Re-Sacrifice

# Create a virtual environment (if it doesn't exist)
python3 -m venv venv

# Activate the virtual environment
source venv/bin/activate

# Install the required dependencies
pip install -r requirements.txt

# Run the main.py script
python main.py
