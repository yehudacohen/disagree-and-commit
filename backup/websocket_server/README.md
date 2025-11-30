# WebSocket Server

A real-time WebSocket communication server that connects frontend applications with AWS Bedrock Nova Sonic model and integrates with intelligent agents deployed on AgentCore Runtime.

## Table of Contents

- [Features](#features)
- [Architecture Overview](#architecture-overview)
- [Quick Start](#quick-start)
- [Configuring AgentCore Runtime](#configuring-agentcore-runtime)
- [Environment Variables](#environment-variables)
- [Usage Guide](#usage-guide)
- [API Endpoints](#api-endpoints)
- [Troubleshooting](#troubleshooting)

## Features

- **Real-time WebSocket Communication**: Bidirectional real-time connection with frontend
- **Nova Sonic Integration**: Support for Amazon Bedrock Nova Sonic multimodal model
- **AgentCore Runtime Integration**: Invoke intelligent agents deployed on AgentCore
- **Multiple Agent Support**:
  - Orchestration Agent (Disagree and Commit Panel)
  - Supervisor Agent (Educational Coach System)
  - MCP Client
  - Strands Agent
- **HTTP API**: REST API endpoints for direct agent invocation
- **Health Checks**: Support for container orchestration and load balancer health checks

## Architecture Overview

```
┌─────────────┐         WebSocket          ┌──────────────────┐
│  Frontend   │ <─────────────────────────> │ WebSocket Server │
│    App      │                             │                  │
└─────────────┘                             └──────────────────┘
                                                     │
                                    ┌────────────────┼────────────────┐
                                    │                │                │
                                    v                v                v
                            ┌──────────────┐ ┌──────────────┐ ┌──────────────┐
                            │ Nova Sonic   │ │ AgentCore    │ │   Other      │
                            │ (Bedrock)    │ │ Runtime      │ │ Integrations │
                            └──────────────┘ └──────────────┘ └──────────────┘
```

## Quick Start

### 1. Install Dependencies

```bash
cd backup/websocket_server

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# or
venv\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt
```

### 2. Configure AWS Credentials

**Option A: Using AWS Profile (Recommended)**

```bash
export AWS_PROFILE="your-profile-name"
export AWS_DEFAULT_REGION="us-east-1"
```

**Option B: Using Access Keys**

```bash
export AWS_ACCESS_KEY_ID="your-access-key-id"
export AWS_SECRET_ACCESS_KEY="your-secret-access-key"
export AWS_DEFAULT_REGION="us-east-1"
```

### 3. Start the Server

```bash
# Use default configuration (Supervisor Agent)
python server.py

# Use Orchestration Agent
python server.py --agent orchestration

# Use other agents
python server.py --agent mcp
python server.py --agent strands
```

## Configuring AgentCore Runtime

### What is AgentCore Runtime?

AgentCore Runtime is a serverless agent execution environment provided by AWS Bedrock. You can deploy custom agents to AgentCore Runtime and invoke them via their ARN (Amazon Resource Name).

### How to Change AgentCore Runtime URL?

#### Step 1: Get the AgentCore Runtime ARN

First, you need to obtain the Runtime ARN of your deployed agent.

```bash
# Navigate to agent directory
cd backup/agent-core/orchestration_agent

# Check agent status (displays Runtime ARN)
agentcore status

# Example output:
# Agent Runtime ARN: arn:aws:bedrock-agentcore:us-east-1:123456789012:runtime/ac_orchestration_agent-xxxxx
```

#### Step 2: Configure Environment Variables

Set the appropriate environment variable based on the agent type you're using:

**Orchestration Agent (Disagree and Commit Panel)**

```bash
export ORCHESTRATION_RUNTIME_ARN="arn:aws:bedrock-agentcore:us-east-1:123456789012:runtime/ac_orchestration_agent-xxxxx"
```

**Supervisor Agent (Educational Coach)**

```bash
export SUPERVISOR_ENDPOINT="https://your-supervisor-endpoint"
# or use Runtime ARN
export SUPERVISOR_RUNTIME_ARN="arn:aws:bedrock-agentcore:us-east-1:123456789012:runtime/ac_supervisor_agent-xxxxx"
```

#### Step 3: Verify Configuration

```bash
# Check if environment variable is set
echo $ORCHESTRATION_RUNTIME_ARN

# Start the server
python server.py --agent orchestration

# Check logs to confirm ARN is loaded correctly
# Output should include:
# Using AgentCore Runtime ARN: arn:aws:bedrock-agentcore:...
```

#### Step 4: Test Connection

```bash
# Verify using test script
python test_orchestration_api.py

# Or test HTTP API using curl
curl -X POST http://localhost:8080/api/orchestration \
  -H "Content-Type: application/json" \
  -d '{"problem": "How to design a highly available web application?"}' | jq .
```

### Configuration File Approach (Optional)

If you prefer not to use environment variables, you can create a configuration file:

```bash
# Create .env file
cat > .env << EOF
AWS_PROFILE=personal
AWS_DEFAULT_REGION=us-east-1
HOST=localhost
WS_PORT=8081
API_PORT=8080
ORCHESTRATION_RUNTIME_ARN=arn:aws:bedrock-agentcore:us-east-1:123456789012:runtime/ac_orchestration_agent-xxxxx
LOGLEVEL=INFO
EOF

# Load using python-dotenv (install first: pip install python-dotenv)
# Add to the beginning of server.py:
# from dotenv import load_dotenv
# load_dotenv()
```

### Multi-Environment Configuration Examples

**Development Environment**

```bash
#!/bin/bash
# start-dev.sh

export AWS_PROFILE="dev-profile"
export AWS_DEFAULT_REGION="us-east-1"
export HOST="localhost"
export WS_PORT="8081"
export API_PORT="8080"
export ORCHESTRATION_RUNTIME_ARN="arn:aws:bedrock-agentcore:us-east-1:123456789012:runtime/ac_orchestration_agent-dev"
export LOGLEVEL="DEBUG"

python server.py --agent orchestration --debug
```

**Production Environment**

```bash
#!/bin/bash
# start-prod.sh

export AWS_PROFILE="prod-profile"
export AWS_DEFAULT_REGION="us-west-2"
export HOST="0.0.0.0"
export WS_PORT="8081"
export API_PORT="8080"
export HEALTH_PORT="80"
export ORCHESTRATION_RUNTIME_ARN="arn:aws:bedrock-agentcore:us-west-2:123456789012:runtime/ac_orchestration_agent-prod"
export LOGLEVEL="INFO"

python server.py --agent orchestration
```

## Environment Variables

### Required Environment Variables

| Variable | Description | Default | Example |
|----------|-------------|---------|---------|
| `AWS_PROFILE` | AWS profile name | None | `personal` |
| `AWS_ACCESS_KEY_ID` | AWS access key ID (alternative to AWS_PROFILE) | None | `AKIAIOSFODNN7EXAMPLE` |
| `AWS_SECRET_ACCESS_KEY` | AWS secret access key (alternative to AWS_PROFILE) | None | `wJalrXUt...` |
| `AWS_DEFAULT_REGION` | AWS region | `us-east-1` | `us-east-1` |

### WebSocket Server Configuration

| Variable | Description | Default | Example |
|----------|-------------|---------|---------|
| `HOST` | Server listening address | `localhost` | `0.0.0.0` |
| `WS_PORT` | WebSocket port | `8081` | `8081` |
| `API_PORT` | HTTP API port | None (optional) | `8080` |
| `HEALTH_PORT` | Health check port | None (optional) | `80` |

### AgentCore Runtime Configuration

| Variable | Description | When to Use | Example |
|----------|-------------|-------------|---------|
| `ORCHESTRATION_RUNTIME_ARN` | Orchestration Agent Runtime ARN | `--agent orchestration` | `arn:aws:bedrock-agentcore:us-east-1:123456789012:runtime/ac_orchestration_agent-xxxxx` |
| `SUPERVISOR_RUNTIME_ARN` | Supervisor Agent Runtime ARN | `--agent supervisor` | `arn:aws:bedrock-agentcore:us-east-1:123456789012:runtime/ac_supervisor_agent-xxxxx` |

### Other Configuration

| Variable | Description | Default | Options |
|----------|-------------|---------|---------|
| `LOGLEVEL` | Logging level | `INFO` | `DEBUG`, `INFO`, `WARNING`, `ERROR`, `CRITICAL` |
| `KB_ID` | Bedrock Knowledge Base ID | None | `your-kb-id` |
| `LAMBDA_ARN` | Lambda function ARN | None | `arn:aws:lambda:...` |

## Usage Guide

### Command Line Arguments

```bash
python server.py [OPTIONS]

Options:
  --agent TEXT    Specify the agent type to use
                  Options: mcp, strands, supervisor, orchestration
                  Default: supervisor
  
  --debug         Enable debug mode with detailed error stack traces
```

### Usage Examples

**1. Start Orchestration Agent (Disagree and Commit Panel)**

```bash
export ORCHESTRATION_RUNTIME_ARN="arn:aws:bedrock-agentcore:us-east-1:123456789012:runtime/ac_orchestration_agent-xxxxx"
python server.py --agent orchestration
```

**2. Start Supervisor Agent (Educational Coach)**

```bash
export SUPERVISOR_RUNTIME_ARN="arn:aws:bedrock-agentcore:us-east-1:123456789012:runtime/ac_supervisor_agent-xxxxx"
python server.py --agent supervisor
```

**3. Start MCP Client**

```bash
python server.py --agent mcp
```

**4. Enable HTTP API**

```bash
export API_PORT="8080"
export ORCHESTRATION_RUNTIME_ARN="arn:aws:bedrock-agentcore:us-east-1:123456789012:runtime/ac_orchestration_agent-xxxxx"
python server.py --agent orchestration
```

## API Endpoints

When the `API_PORT` environment variable is set, the server starts an HTTP API service.

### Health Check

```bash
GET /api/health

# Response
{
  "status": "healthy"
}
```

### Invoke Orchestration Agent

```bash
POST /api/orchestration
Content-Type: application/json

{
  "problem": "How to design a highly available web application?",
  "instruction": "Have the panel discuss this problem and propose an AWS solution"  # Optional
}

# Response
{
  "result": "Panel discussion results...",
  "error": false
}
```

Alias endpoint: `POST /api/panel` (same functionality as `/api/orchestration`)

### Invoke Supervisor Agent

```bash
POST /api/coach
Content-Type: application/json

{
  "query": "What is AWS Lambda?",
  "context": "I'm a beginner"  # Optional
}

# Response
{
  "result": "Educational coach response...",
  "error": false
}
```

## Troubleshooting

### Issue 1: Cannot Connect to AgentCore Runtime

**Symptoms:**
```
WARNING - ORCHESTRATION_RUNTIME_ARN not set - orchestration agent will not be available
```

**Solutions:**
1. Verify environment variable is set: `echo $ORCHESTRATION_RUNTIME_ARN`
2. Verify ARN format is correct: `arn:aws:bedrock-agentcore:REGION:ACCOUNT:runtime/AGENT_NAME`
3. Verify agent is deployed: `cd backup/agent-core/orchestration_agent && agentcore status`

### Issue 2: AWS Credentials Error

**Symptoms:**
```
botocore.exceptions.NoCredentialsError: Unable to locate credentials
```

**Solutions:**
1. Check AWS credentials configuration: `aws sts get-caller-identity`
2. Verify environment variables are set: `echo $AWS_PROFILE` or `echo $AWS_ACCESS_KEY_ID`
3. Verify AWS CLI config file exists: `cat ~/.aws/credentials`

### Issue 3: Region Mismatch

**Symptoms:**
```
An error occurred (ResourceNotFoundException) when calling the InvokeAgentRuntime operation
```

**Solutions:**
1. Verify `AWS_DEFAULT_REGION` matches the region in AgentCore Runtime ARN
2. Check ARN: `arn:aws:bedrock-agentcore:us-east-1:...` (region should be us-east-1)
3. Update environment variable: `export AWS_DEFAULT_REGION="us-east-1"`

### Issue 4: Port Already in Use

**Symptoms:**
```
OSError: [Errno 48] Address already in use
```

**Solutions:**
1. Check port usage: `lsof -i :8081`
2. Stop the process using the port: `kill -9 <PID>`
3. Or change the port: `export WS_PORT="8082"`

### Issue 5: WebSocket Connection Dropped

**Symptoms:**
Frontend shows connection dropped or no response

**Solutions:**
1. Check server logs for error messages
2. Verify firewall rules allow WebSocket port (8081)
3. Check network connection: `curl http://localhost:8081/health`
4. Enable debug mode: `python server.py --agent orchestration --debug`

### Debugging Tips

**1. Enable Verbose Logging**

```bash
export LOGLEVEL="DEBUG"
python server.py --agent orchestration --debug
```

**2. Use Test Scripts**

```bash
# Test WebSocket connection
python test_websocket_connection.py

# Test Orchestration API
python test_orchestration_api.py

# Test Bedrock streaming
python test_bedrock_streaming.py
```

**3. Check Environment Variables**

```bash
# Create check script
cat > check-env.sh << 'EOF'
#!/bin/bash
echo "AWS_PROFILE: ${AWS_PROFILE:-Not set}"
echo "AWS_DEFAULT_REGION: ${AWS_DEFAULT_REGION:-Not set}"
echo "ORCHESTRATION_RUNTIME_ARN: ${ORCHESTRATION_RUNTIME_ARN:-Not set}"
echo "HOST: ${HOST:-localhost}"
echo "WS_PORT: ${WS_PORT:-8081}"
echo "API_PORT: ${API_PORT:-Not set}"

# Verify AWS credentials
aws sts get-caller-identity
EOF

chmod +x check-env.sh
./check-env.sh
```

## Related Documentation

- [CREDENTIALS_SETUP.md](./CREDENTIALS_SETUP.md) - Detailed AWS credentials configuration guide
- [SUPERVISOR_API_GUIDE.md](./SUPERVISOR_API_GUIDE.md) - Supervisor Agent API usage guide
- [WEBSOCKET_ENV_VARS_AND_INTEGRATION.md](../../WEBSOCKET_ENV_VARS_AND_INTEGRATION.md) - Environment variables and integration details
- [AGENTCORE_INTEGRATION_GUIDE.md](../../AGENTCORE_INTEGRATION_GUIDE.md) - AgentCore integration guide

## License

This project follows the MIT License.
