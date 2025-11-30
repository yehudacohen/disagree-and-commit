#!/bin/bash

# Deploy Disagree and Commit Agents
# This script deploys all four agents needed for the panel discussion

set -e

echo "=========================================="
echo "Deploying Disagree and Commit Agents"
echo "=========================================="

# Set AWS region
export AWS_DEFAULT_REGION=${AWS_DEFAULT_REGION:-us-east-1}
echo "Using AWS Region: $AWS_DEFAULT_REGION"

# Deploy the three expert agents first (they can be deployed in parallel)
echo ""
echo "Step 1: Deploying Expert Agents..."
echo "=========================================="

echo ""
echo "Deploying Jeff Barr Agent..."
cd jeff_barr_agent
python deploy.py
cd ..

echo ""
echo "Deploying Werner Vogels Agent..."
cd werner_vogels_agent
python deploy.py
cd ..

echo ""
echo "Deploying Swami Sivasubramanian Agent..."
cd swami_agent
python deploy.py
cd ..

# Deploy the orchestration agent last (it depends on the other three)
echo ""
echo "Step 2: Deploying Orchestration Agent..."
echo "=========================================="
cd orchestration_agent
python deploy.py
cd ..

echo ""
echo "=========================================="
echo "All agents deployed successfully!"
echo "=========================================="
echo ""
echo "Deployed agents:"
echo "  - ac_jeff_barr_agent"
echo "  - ac_werner_vogels_agent"
echo "  - ac_swami_agent"
echo "  - ac_orchestration_agent (main entry point)"
echo ""
echo "You can now call ac_orchestration_agent from your WebSocket server."
echo "The orchestration agent will coordinate the panel discussion."
