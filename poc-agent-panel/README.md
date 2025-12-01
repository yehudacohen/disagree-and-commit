# AWS Executive Panel Discussion POC

An agentic program that orchestrates a multi-round debate between three AWS executives: Jeff Barr, Swami Sivasubramanian, and Werner Vogels.

> **Quick Start**: See [QUICK_START.md](QUICK_START.md) for a 5-minute setup guide.  
> **Full Index**: See [INDEX.md](INDEX.md) for complete documentation guide.

## Overview

This POC simulates a panel discussion where each executive (represented as an AI agent with their unique persona) debates a problem through four rounds:

1. **Round 1: Initial Opinions** - Each panelist shares their approach to solving the problem
2. **Round 2: Disagreements** - Each panelist disagrees with others based on their worldview
3. **Round 3: Personal Callouts** - Panelists challenge each other in their characteristic style
4. **Round 4: Disagree and Commit** - Following Amazon's principle, they commit to one solution

## Setup

### Prerequisites

- Python 3.8+
- AWS CLI configured with the `scratchspace` profile
- Access to AWS Bedrock with Claude Sonnet 4.5 model enabled in `us-east-1`

### Quick Setup

```bash
./setup.sh
```

This will create a virtual environment and install dependencies.

### Manual Installation

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### AWS Configuration

Ensure your AWS profile `scratchspace` has:
- Bedrock access in `us-east-1` region
- Permission to invoke the Claude Sonnet 4.5 model (`us.anthropic.claude-sonnet-4-20250514`)

To verify your AWS configuration:
```bash
source venv/bin/activate
python test_credentials.py
```

This will check:
- AWS profile exists
- Credentials are valid
- Bedrock access is enabled
- Claude Sonnet 4.5 model is available

## Usage

First, activate the virtual environment:
```bash
source venv/bin/activate
```

Then run the panel discussion:
```bash
python panel_discussion.py '<your problem statement>'
```

### Examples

**Serverless vs Containers:**
```bash
python panel_discussion.py 'Should we build our new application using serverless architecture or traditional containers?'
```

**IoT Platform:**
```bash
python panel_discussion.py 'How should we approach building a real-time data processing platform for IoT devices?'
```

**Microservices Adoption:**
```bash
python panel_discussion.py 'Should we adopt microservices architecture for our new e-commerce platform?'
```

**AI/ML Strategy:**
```bash
python panel_discussion.py 'What is the best approach for integrating AI agents into our enterprise applications?'
```

## How It Works

1. The program loads persona prompts for each executive from their respective markdown files
2. For each round, it calls Claude Sonnet 4.5 via AWS Bedrock with:
   - The executive's persona as the system prompt
   - The problem and discussion context as the user message
3. Each response is printed to the console in real-time
4. Discussion history is maintained and passed to subsequent rounds for context

## Panelist Personas

- **Jeff Barr**: The pragmatic builder who grounds discussions in hands-on experience
- **Swami Sivasubramanian**: The eternal optimist who reframes challenges as opportunities
- **Werner Vogels**: The brutally direct technologist who challenges assumptions

## Output Format

The program prints all panelist responses to stdout with clear formatting:

```
================================================================================
ROUND 1: INITIAL OPINIONS
================================================================================

PROBLEM: <your problem>

────────────────────────────────────────────────────────────────────────────────
Jeff Barr:
────────────────────────────────────────────────────────────────────────────────
<Jeff's response>

[... continues for all panelists and rounds ...]
```

## Notes

- Each round builds on previous rounds, creating a dynamic conversation
- The personas are designed to create authentic disagreements and debates
- The final round demonstrates Amazon's "Disagree and Commit" leadership principle
