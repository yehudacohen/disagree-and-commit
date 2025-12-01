#!/usr/bin/env python3
"""Test script for extract_mermaid utility function."""

from synthesis.synthesizer import extract_mermaid


def test_valid_mermaid_block():
    """Test extraction of valid mermaid block."""
    test_input = """## Architecture Overview
Some text here

```mermaid
graph TD
  A[User] --> B[API Gateway]
  B --> C[Lambda]
```

## Trade-offs
More text"""
    
    result = extract_mermaid(test_input)
    expected = """graph TD
  A[User] --> B[API Gateway]
  B --> C[Lambda]"""
    
    assert result == expected, f"Expected:\n{expected}\n\nGot:\n{result}"
    print("✓ Test 1 passed: Valid mermaid block extracted correctly")


def test_no_mermaid_block():
    """Test when no mermaid block is present."""
    test_input = """## Architecture Overview
Some text without mermaid"""
    
    result = extract_mermaid(test_input)
    assert result == "", f"Expected empty string, got: {repr(result)}"
    print("✓ Test 2 passed: Returns empty string when no mermaid block")


def test_multiple_lines():
    """Test mermaid block with multiple lines."""
    test_input = """
```mermaid
graph LR
  Start --> Process
  Process --> End
  End --> Start
```
"""
    
    result = extract_mermaid(test_input)
    expected = """graph LR
  Start --> Process
  Process --> End
  End --> Start"""
    
    assert result == expected, f"Expected:\n{expected}\n\nGot:\n{result}"
    print("✓ Test 3 passed: Multiple line mermaid block extracted correctly")


def test_complex_mermaid():
    """Test complex mermaid diagram with various elements."""
    test_input = """## Synthesis

```mermaid
graph TD
  A[Client] -->|HTTPS| B[CloudFront]
  B --> C[API Gateway]
  C --> D[Lambda]
  D --> E[DynamoDB]
  D --> F[S3]
```

## Summary"""
    
    result = extract_mermaid(test_input)
    assert "graph TD" in result
    assert "CloudFront" in result
    assert "Lambda" in result
    print("✓ Test 4 passed: Complex mermaid diagram extracted correctly")


if __name__ == "__main__":
    test_valid_mermaid_block()
    test_no_mermaid_block()
    test_multiple_lines()
    test_complex_mermaid()
    print("\n✅ All tests passed!")
