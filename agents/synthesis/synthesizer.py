from strands import Agent
from strands.models import BedrockModel

synthesis_agent = Agent(
    name="synthesis",
    model=BedrockModel("anthropic.claude-sonnet-4-v1"),
    instructions="""Synthesize expert debate into final architecture.

INPUT: All debate rounds from three experts
OUTPUT: 
1. Unified architecture combining all perspectives
2. Mermaid diagram
3. Key trade-offs

SYNTHESIS RULES:
- Honor each expert's core principles:
  * Jeff: Serverless and simplicity
  * Swami: Fast to ship, AI/ML focus
  * Werner: Scale and distributed systems
- Create comprehensive but functional design
- Generate Mermaid flowchart showing architecture
- Include AWS services from all perspectives
- Make it absurdly over-engineered but workable

FORMAT:
## Architecture Overview
[Summary paragraph]

## Core Components
[List key services and patterns]

## Mermaid Diagram
```mermaid
[Architecture diagram]
```

## Trade-offs
[Analysis of competing concerns]"""
)
