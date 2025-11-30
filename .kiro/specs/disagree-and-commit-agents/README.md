# Disagree and Commit - Agent Layer Spec

> **This spec will be developed by the Agent Team**

## Overview

This spec covers the AI agent layer that powers the expert debate, including personality-driven responses, voice generation, and architecture synthesis.

## Tech Stack (from AWS Documentation)

### Amazon Bedrock AgentCore Runtime
- Serverless agent deployment using `BedrockAgentCoreApp` wrapper
- Entry point decorator pattern: `@app.entrypoint`
- Local testing via `curl -X POST http://localhost:8080/invocations`
- CLI deployment: `agentcore configure` → `agentcore deploy` → `agentcore invoke`

```python
from bedrock_agentcore.runtime import BedrockAgentCoreApp
app = BedrockAgentCoreApp()

@app.entrypoint
def agent_invocation(payload, context):
    # Agent logic here
    return {"result": result.message}

app.run()
```

### Strands Agents SDK
- Model-driven orchestration framework
- Native AWS integrations
- Multi-agent primitives: handoffs, swarms, graph workflows
- Built-in A2A (Agent-to-Agent) support

```python
from strands import Agent
from strands_tools import file_read, file_write

agent = Agent(tools=[file_read, file_write])
result = agent("Your prompt here")
```

### Amazon Nova Sonic (Speech-to-Speech)
- Model for real-time conversational AI via Bedrock's bidirectional streaming API
- Key capabilities:
  - Bidirectional audio streaming
  - Adaptive speech response based on input prosody
  - Graceful interruption handling
  - Function calling and agentic workflow support
  - Multilingual support (EN-US, EN-UK, FR, IT, DE, ES)
- Event-driven architecture with JSON events for session lifecycle, audio streaming, text responses

### Amazon Nova Canvas (Image Generation)
- Model ID: `amazon.nova-canvas-v1:0`
- Text-to-image generation for architecture diagrams and reaction images
- Max prompt: 1024 characters
- Max output: 4.19M pixels (2048x2048)
- Regions: us-east-1, eu-west-1, ap-northeast-1

## Agents to Implement

1. **Master Orchestrator Agent** - Coordinates debate flow, manages rounds, triggers finale
2. **Jeff Barr Agent** - "The Simplifier" personality, wants everything serverless and simple
3. **Swami Agent** - "The Shipper" personality, obsessed with getting to market fast
4. **Werner Vogels Agent** - "The Scale Architect" personality, everything must scale to billions
5. **Synthesis Agent** - Combines all recommendations into an absurdly over-engineered final design

## Integration Points with UI Spec

The agent layer communicates with the UI via API Gateway WebSocket.

### WebSocket Message Types (sent TO frontend)

```typescript
type WebSocketMessage =
  | { type: 'expert_speaking'; expertId: string }
  | { type: 'expert_response'; expertId: string; content: string; audioUrl?: string; isComplete: boolean }
  | { type: 'frustration_update'; expertId: string; level: 1|2|3|4|5; reactionImageUrl?: string }
  | { type: 'round_complete'; roundNumber: number }
  | { type: 'disagree_and_commit' }
  | { type: 'architecture_ready'; diagram: string; cost: CostEstimate; endorsements: Record<string, string>; assets: AssetsFolder };
```

### WebSocket Message Types (received FROM frontend)

```typescript
interface ClientMessage {
  action: 'submitProblem';
  problem: string;
  sessionId: string;
}
```

## References

- UI/Infrastructure Spec: `.kiro/specs/disagree-and-commit-ui/`
- AgentCore Docs: https://aws.github.io/bedrock-agentcore-starter-toolkit/
- Strands Docs: https://strandsagents.com/latest/
- Nova Sonic Docs: https://docs.aws.amazon.com/nova/latest/userguide/speech.html
- Nova Canvas Docs: https://docs.aws.amazon.com/nova/latest/userguide/image-generation.html
