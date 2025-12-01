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

## Configuration

### Environment Variables

The system requires the following environment variables:

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `MEMORY_ID` | Yes | None | AgentCore Memory resource ID for storing debate history |
| `MODEL_ID` | No | `us.anthropic.claude-sonnet-4-20250514-v1:0` | Bedrock model identifier for all agents |
| `AWS_REGION` | No | `us-east-1` | AWS region for Bedrock and AgentCore services |

**Example:**
```bash
export MEMORY_ID="your-memory-resource-id"
export MODEL_ID="us.anthropic.claude-sonnet-4-20250514-v1:0"
export AWS_REGION="us-east-1"
```

### Creating AgentCore Memory Resource

Before running the orchestrator, you need to create an AgentCore Memory resource:

```python
from bedrock_agentcore.memory import MemoryClient

# Initialize memory client
memory_client = MemoryClient(region='us-east-1')

# Create memory resource
memory = memory_client.create_memory_and_wait(
    name='debate-memory',
    description='Memory for disagree-and-commit debate sessions'
)

# Use the memory ID in your environment
print(f"MEMORY_ID={memory.memory_id}")
```

## Local Testing

```bash
# Install dependencies
pip install -r requirements.txt

# Set required environment variables
export MEMORY_ID="your-memory-resource-id"

# Test locally
python test_local.py
```

## Deploy to AgentCore Runtime

### Prerequisites

1. Install AgentCore CLI:
```bash
pip install bedrock-agentcore
```

2. Configure AWS credentials:
```bash
aws configure
```

3. Create AgentCore Memory resource (see Configuration section above)

### Deployment Steps

```bash
# Navigate to orchestrator directory
cd orchestrator

# Configure AgentCore deployment
agentcore configure \
  --entrypoint app.py \
  --agent-name disagree-and-commit \
  --region us-east-1

# Deploy with environment variables
agentcore launch \
  --env MEMORY_ID=your-memory-resource-id \
  --env MODEL_ID=us.anthropic.claude-sonnet-4-20250514-v1:0 \
  --env AWS_REGION=us-east-1

# Invoke the deployed agent
agentcore invoke --payload '{
  "problem": "Design a Mars currency system",
  "actor_id": "user123"
}'
```

### Deployment with Custom Problem

```bash
# Using a custom problem statement
agentcore invoke --payload '{
  "problem": "Your custom problem statement here",
  "actor_id": "user123"
}'

# Using a predefined problem ID
agentcore invoke --payload '{
  "problemId": "mars_currency",
  "actor_id": "user123"
}'
```

### Expected Response

```json
{
  "sessionId": "debate_abc12345_2025-11-30T12:00:00.000000",
  "synthesis": "Full synthesis text with architecture...",
  "mermaidDiagram": "graph TD\n  A[Component A]-->B[Component B]...",
  "status": "complete",
  "actor_id": "user123",
  "session_id": "debate_abc12345_2025-11-30T12:00:00.000000"
}
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

## Troubleshooting

### MEMORY_ID Not Set

**Error:** `MEMORY_ID environment variable not set, memory operations may fail`

**Solution:** Set the MEMORY_ID environment variable to your AgentCore Memory resource ID:
```bash
export MEMORY_ID="your-memory-resource-id"
```

### Memory Operations Failing

**Error:** Memory storage or retrieval fails

**Possible causes:**
1. Invalid MEMORY_ID
2. Insufficient IAM permissions for bedrock-agent-runtime
3. Memory resource not in the correct region

**Solution:** 
- Verify MEMORY_ID is correct
- Ensure your AWS credentials have `bedrock:CreateEvent` and `bedrock:RetrieveMemory` permissions
- Check that AWS_REGION matches your memory resource region

### Agent Invocation Errors

**Error:** Agent fails to respond or returns invalid structure

**Possible causes:**
1. Invalid MODEL_ID
2. Insufficient IAM permissions for Bedrock
3. Model not available in the region

**Solution:**
- Verify MODEL_ID format: `us.anthropic.claude-sonnet-4-20250514-v1:0`
- Ensure IAM permissions include `bedrock:InvokeModel`
- Check model availability in your region

### Session ID Too Short

**Error:** Session ID validation fails

**Solution:** The system automatically generates session IDs with minimum 33 characters. If you see this error, it's likely a bug - please report it.

## Logging

The system uses Python's standard logging module with INFO level by default. Logs include:

- Agent initialization
- Session creation
- Agent invocations
- Memory operations
- Synthesis generation
- Error details

To change log level:
```python
import logging
logging.getLogger().setLevel(logging.DEBUG)
```
