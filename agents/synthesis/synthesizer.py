import re
from strands import Agent
from strands.models import BedrockModel

synthesis_agent = Agent(
    model=BedrockModel(model_id="anthropic.claude-sonnet-4-v1"),
    system_prompt="""Synthesize expert debate into final architecture.

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

# Set the agent name after initialization
synthesis_agent.name = "synthesis"


def extract_mermaid(synthesis_output: str) -> str:
    """
    Extract Mermaid diagram code from synthesis output.
    
    Parses the synthesis agent's response to extract the Mermaid code block.
    Looks for content between ```mermaid and ``` markers.
    
    Args:
        synthesis_output: The full text output from the synthesis agent
    
    Returns:
        The Mermaid diagram code as a string, or empty string if not found
    
    Example:
        >>> output = "## Architecture\\n```mermaid\\ngraph TD\\n  A-->B\\n```\\n## Summary"
        >>> extract_mermaid(output)
        'graph TD\\n  A-->B'
    """
    # Pattern to match ```mermaid ... ``` code blocks
    pattern = r'```mermaid\s*\n(.*?)\n```'
    
    match = re.search(pattern, synthesis_output, re.DOTALL)
    
    if match:
        return match.group(1).strip()
    
    return ""
