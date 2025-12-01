# Quick Start Guide

Get up and running with the AWS Executive Panel Discussion in 5 minutes.

## 1. Setup (1 minute)

```bash
# Clone or navigate to the project directory
cd /path/to/panel-discussion

# Run setup script
./setup.sh

# Activate virtual environment
source venv/bin/activate
```

## 2. Test Your AWS Configuration (30 seconds)

```bash
python test_credentials.py
```

You should see:
```
✓ All tests passed! You're ready to run the panel discussion.
```

If you see errors, check:
- AWS CLI is installed: `aws --version`
- Profile exists: `aws configure list --profile scratchspace`
- Bedrock access is enabled in AWS Console

## 3. Run Your First Discussion (2-3 minutes)

```bash
python panel_discussion.py "Should we use serverless or containers for our new app?"
```

Watch as Jeff, Swami, and Werner debate through 4 rounds:
1. Initial opinions
2. Disagreements
3. Personal callouts
4. Disagree and commit

## 4. Try Different Problems

```bash
# Microservices debate
python panel_discussion.py "Should we migrate our monolith to microservices?"

# AI strategy
python panel_discussion.py "How should we integrate AI agents into our platform?"

# Database choice
python panel_discussion.py "Should we use SQL or NoSQL for our new application?"

# Architecture decision
python panel_discussion.py "What's the best approach for building a real-time analytics system?"
```

## Common Issues

### "No module named 'boto3'"
```bash
source venv/bin/activate
pip install boto3
```

### "Unable to locate credentials"
```bash
# Configure AWS profile
aws configure --profile scratchspace

# Or set environment variable
export AWS_PROFILE=scratchspace
```

### "Access denied to Bedrock"
1. Go to AWS Console → Bedrock
2. Navigate to "Model access"
3. Enable Claude Sonnet 4.5
4. Wait a few minutes for activation

### "Model not found"
The model ID is: `us.anthropic.claude-sonnet-4-20250514`

Make sure:
- You're using `us-east-1` region
- Model access is enabled in Bedrock console
- You have the latest model ID (check AWS docs if needed)

## Tips

### Better Prompts
Be specific and technical:
- ✓ "How should we design a multi-region disaster recovery strategy for our e-commerce platform?"
- ✗ "What should we do about the cloud?"

### Interesting Debates
Topics that create good disagreements:
- Serverless vs containers
- Microservices vs monoliths
- SQL vs NoSQL
- Build vs buy
- Cost optimization strategies
- AI/ML implementation approaches

### Saving Output
```bash
# Save to file
python panel_discussion.py "Your problem" > discussion.txt

# Save with timestamp
python panel_discussion.py "Your problem" | tee "discussion_$(date +%Y%m%d_%H%M%S).txt"
```

## Next Steps

- Read [README.md](README.md) for detailed documentation
- Check [EXAMPLE_OUTPUT.md](EXAMPLE_OUTPUT.md) to see what output looks like
- Review [PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md) to understand the architecture
- Modify persona prompts to customize personalities
- Extend the code to add new rounds or panelists

## Need Help?

1. Run the test script: `python test_credentials.py`
2. Check AWS credentials: `aws sts get-caller-identity --profile scratchspace`
3. Verify Bedrock access: `aws bedrock list-foundation-models --profile scratchspace --region us-east-1`
4. Review error messages - they usually point to the issue

Happy debating! 🎭
