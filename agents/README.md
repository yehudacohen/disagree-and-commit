# Disagree and Commit - Agent Implementation

## Architecture

```
Orchestrator Agent
    ↓
[Jeff Barr] [Swami] [Werner Vogels]
    ↓
AgentCore Memory (Session-based)
    ↓
Synthesis Agent → Mermaid Diagram
```

## Debate Flow

- **Round 1**: 3 min (Jeff: 1min → Swami: 1min → Werner: 1min)
- **Round 2**: 3 min (Jeff: 1min → Swami: 1min → Werner: 1min)
- **Consensus**: 3 min (Jeff: 1min → Swami: 1min → Werner: 1min)
- **Total**: 9 minutes

## Local Testing

```bash
# Install dependencies
pip install -r requirements.txt

# Test locally
python test_local.py
```

## Deploy to AgentCore Runtime

```bash
# Configure AgentCore
agentcore configure

# Deploy orchestrator
cd orchestrator
agentcore deploy

# Invoke
agentcore invoke --payload '{"problem": "Your problem statement here"}'
```

## Memory Structure

```
Session: debate_{hash}_{timestamp}
├── User: jeff_barr
│   ├── Round 1, 2, 3
├── User: swami
│   ├── Round 1, 2, 3
├── User: werner_vogels
│   └── Round 1, 2, 3
```

## Problem Statements

See `problem_statements.json` for sample problems:
1. Mars/Moon Digital Currency
2. Air Taxi Pollution Reduction
3. Personal Air Taxi Safety

## Agent Personalities

- **Jeff Barr**: Serverless simplicity advocate
- **Swami**: Ship-fast AI/ML enthusiast
- **Werner Vogels**: Scale-first distributed systems architect
