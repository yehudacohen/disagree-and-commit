#!/bin/bash

# Setup script for AWS Executive Panel Discussion POC

echo "Setting up AWS Executive Panel Discussion POC..."

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment and install dependencies
echo "Installing dependencies..."
source venv/bin/activate
pip install -q boto3

echo ""
echo "Setup complete!"
echo ""
echo "To run the panel discussion:"
echo "  source venv/bin/activate"
echo "  python panel_discussion.py '<your problem statement>'"
echo ""
echo "Example:"
echo "  python panel_discussion.py 'Should we adopt microservices for our platform?'"
echo ""
echo "Make sure your AWS profile 'chrismiller' is configured with Bedrock access."
