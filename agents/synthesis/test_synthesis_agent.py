#!/usr/bin/env python3
"""Test script for synthesis agent."""

from synthesis.synthesizer import synthesis_agent, extract_mermaid


def test_synthesis_agent_initialization():
    """Test that synthesis agent is properly initialized."""
    assert synthesis_agent is not None, "Synthesis agent should be initialized"
    assert synthesis_agent.name == "synthesis", f"Expected name 'synthesis', got '{synthesis_agent.name}'"
    assert synthesis_agent.model is not None, "Synthesis agent should have a model"
    print("✓ Synthesis agent initialized correctly")
    print(f"  - Name: {synthesis_agent.name}")
    print(f"  - Model: {type(synthesis_agent.model).__name__}")


def test_synthesis_agent_system_prompt():
    """Test that synthesis agent has proper system prompt."""
    assert synthesis_agent.system_prompt is not None, "Synthesis agent should have system prompt"
    
    # Check for key elements in the system prompt
    prompt = synthesis_agent.system_prompt
    assert "Synthesize expert debate" in prompt, "Should mention synthesizing debate"
    assert "Jeff" in prompt, "Should reference Jeff Barr"
    assert "Swami" in prompt, "Should reference Swami"
    assert "Werner" in prompt, "Should reference Werner"
    assert "Mermaid" in prompt, "Should mention Mermaid diagram"
    assert "serverless" in prompt.lower(), "Should mention serverless"
    assert "scale" in prompt.lower(), "Should mention scale"
    
    print("✓ Synthesis agent system prompt contains all required elements")


def test_extract_mermaid_integration():
    """Test extract_mermaid function is available."""
    # Simulate a synthesis output
    mock_output = """## Architecture Overview
This is a unified architecture.

## Core Components
- Lambda functions
- DynamoDB tables

## Mermaid Diagram
```mermaid
graph TD
  A[User] --> B[API Gateway]
  B --> C[Lambda]
  C --> D[DynamoDB]
```

## Trade-offs
Balancing simplicity with scale."""
    
    diagram = extract_mermaid(mock_output)
    assert diagram != "", "Should extract mermaid diagram"
    assert "graph TD" in diagram, "Should contain graph declaration"
    assert "Lambda" in diagram, "Should contain Lambda service"
    
    print("✓ extract_mermaid function works correctly")
    print(f"  - Extracted diagram length: {len(diagram)} characters")


if __name__ == "__main__":
    test_synthesis_agent_initialization()
    test_synthesis_agent_system_prompt()
    test_extract_mermaid_integration()
    print("\n✅ All synthesis agent tests passed!")
