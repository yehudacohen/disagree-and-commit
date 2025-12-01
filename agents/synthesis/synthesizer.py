import re
import logging
from strands import Agent
from strands.models.bedrock import BedrockModel

# Get logger instance for this module
logger = logging.getLogger(__name__)

logger.info("Initializing synthesis agent")

synthesis_agent = Agent(
    model=BedrockModel(
        model_id="us.anthropic.claude-sonnet-4-20250514-v1:0",
        temperature=0.7,
        max_tokens=2048
    ),
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
        diagram = match.group(1).strip()
        logger.info(f"Successfully extracted Mermaid diagram ({len(diagram)} characters)")
        return diagram
    
    logger.warning("No Mermaid diagram found in synthesis output")
    return ""
