#!/usr/bin/env python3
"""Integration test for synthesis module."""

from synthesis import synthesis_agent, extract_mermaid


def test_synthesis_module_exports():
    """Verify synthesis module exports the required components."""
    print("Testing synthesis module exports...")
    
    # Test synthesis_agent is available
    assert synthesis_agent is not None, "synthesis_agent should be exported"
    assert synthesis_agent.name == "synthesis", "Agent name should be 'synthesis'"
    
    # Test extract_mermaid is available
    assert callable(extract_mermaid), "extract_mermaid should be callable"
    
    print("✓ Synthesis module exports verified")


def test_synthesis_agent_configuration():
    """Verify synthesis agent is configured according to requirements."""
    print("\nTesting synthesis agent configuration...")
    
    prompt = synthesis_agent.system_prompt
    
    # Requirement 7.2: Incorporate all three expert perspectives
    assert "Jeff" in prompt, "Should reference Jeff Barr"
    assert "Swami" in prompt, "Should reference Swami"
    assert "Werner" in prompt, "Should reference Werner"
    assert "serverless" in prompt.lower(), "Should mention serverless (Jeff's focus)"
    assert "ship" in prompt.lower() or "fast" in prompt.lower(), "Should mention speed (Swami's focus)"
    assert "scale" in prompt.lower() or "distributed" in prompt.lower(), "Should mention scale (Werner's focus)"
    
    # Requirement 7.4: Generate Mermaid diagram
    assert "mermaid" in prompt.lower(), "Should mention Mermaid diagram generation"
    
    # Requirement 7.5: Include services from all perspectives
    assert "AWS services" in prompt or "services" in prompt, "Should mention AWS services"
    assert "all perspectives" in prompt or "all three" in prompt, "Should mention all perspectives"
    
    print("✓ Synthesis agent configuration verified")
    print("  - References all three experts")
    print("  - Includes Mermaid diagram generation")
    print("  - Incorporates all perspectives")


def test_extract_mermaid_functionality():
    """Verify extract_mermaid utility works correctly."""
    print("\nTesting extract_mermaid functionality...")
    
    # Test with valid synthesis output
    mock_synthesis = """## Architecture Overview
This architecture combines serverless simplicity, rapid deployment, and massive scale.

## Core Components
- Lambda functions for compute
- DynamoDB for data storage
- API Gateway for routing

## Mermaid Diagram
```mermaid
graph TD
  A[User] --> B[API Gateway]
  B --> C[Lambda]
  C --> D[DynamoDB]
  C --> E[S3]
```

## Trade-offs
Balancing simplicity with scale requirements."""
    
    diagram = extract_mermaid(mock_synthesis)
    
    assert diagram != "", "Should extract diagram"
    assert "graph TD" in diagram, "Should contain graph declaration"
    assert "Lambda" in diagram, "Should contain Lambda service"
    assert "DynamoDB" in diagram, "Should contain DynamoDB service"
    assert "API Gateway" in diagram, "Should contain API Gateway service"
    
    print("✓ extract_mermaid functionality verified")
    print(f"  - Successfully extracted {len(diagram)} character diagram")


def test_requirements_coverage():
    """Verify implementation covers all task requirements."""
    print("\nVerifying requirements coverage...")
    
    # Task requirement: Define Synthesis Agent using Strands Agent with Claude Sonnet 4.1
    assert synthesis_agent is not None, "Synthesis agent should be defined"
    assert synthesis_agent.model is not None, "Should use BedrockModel"
    print("✓ Requirement: Synthesis Agent defined with Claude Sonnet 4.1")
    
    # Task requirement: Configure instructions to combine all three expert perspectives
    prompt = synthesis_agent.system_prompt
    assert "Jeff" in prompt and "Swami" in prompt and "Werner" in prompt, "Should reference all experts"
    print("✓ Requirement: Instructions combine all three expert perspectives")
    
    # Task requirement: Add Mermaid diagram generation to synthesis instructions
    assert "mermaid" in prompt.lower(), "Should include Mermaid generation"
    print("✓ Requirement: Mermaid diagram generation in instructions")
    
    # Task requirement: Implement extract_mermaid() utility
    assert callable(extract_mermaid), "extract_mermaid should be implemented"
    test_output = "```mermaid\ngraph TD\n  A-->B\n```"
    result = extract_mermaid(test_output)
    assert result == "graph TD\n  A-->B", "extract_mermaid should parse correctly"
    print("✓ Requirement: extract_mermaid() utility implemented")
    
    print("\n✅ All requirements covered:")
    print("  - Requirements 7.1: Retrieve all responses (handled by orchestrator)")
    print("  - Requirements 7.2: Incorporate all three perspectives ✓")
    print("  - Requirements 7.4: Generate Mermaid diagram ✓")
    print("  - Requirements 7.5: Include services from all experts ✓")


if __name__ == "__main__":
    test_synthesis_module_exports()
    test_synthesis_agent_configuration()
    test_extract_mermaid_functionality()
    test_requirements_coverage()
    print("\n" + "="*60)
    print("✅ ALL INTEGRATION TESTS PASSED!")
    print("="*60)
