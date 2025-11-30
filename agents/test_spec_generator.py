"""Test script for the spec generator agent."""

import asyncio
import os
import sys

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from spec_generator import generate_spec_package
from spec_generator.parser import InputParser


# Sample synthesis output (similar to what the synthesis agent produces)
SAMPLE_SYNTHESIS = """## Architecture Overview

This gloriously over-engineered todo app combines the best (and worst) of all three expert perspectives. 
We've managed to create a system that could theoretically handle 10 billion users adding sticky notes, 
while shipping in just 2 weeks using nothing but managed services. Jeff is quietly sobbing.

## Core Components

- **API Gateway**: RESTful API with WebSocket support for real-time todo updates
- **Lambda**: 47 microservices for maximum "flexibility" (Jeff's compromise)
- **DynamoDB**: Global tables across 12 regions for Werner's scale requirements
- **Bedrock**: AI-powered todo prioritization using Claude (Swami insisted)
- **SageMaker**: ML pipeline for predicting which todos you'll never complete
- **Step Functions**: Orchestrating the chaos of todo state transitions
- **EventBridge**: Event-driven architecture for todo lifecycle events
- **S3**: Storing todo attachments with 11 9's of durability
- **ElastiCache**: Redis cluster for caching todos you'll check 47 times
- **Kinesis**: Real-time analytics on todo completion rates

## Mermaid Diagram

```mermaid
graph TD
    User[User] --> APIGW[API Gateway]
    APIGW --> Lambda1[Auth Lambda]
    APIGW --> Lambda2[Todo CRUD Lambda]
    Lambda2 --> DDB[(DynamoDB Global)]
    Lambda2 --> Cache[(ElastiCache)]
    Lambda2 --> Bedrock[Bedrock AI]
    Bedrock --> SageMaker[SageMaker]
    Lambda2 --> Events[EventBridge]
    Events --> Kinesis[Kinesis Analytics]
    Events --> StepFn[Step Functions]
    StepFn --> Lambda3[Notification Lambda]
    Lambda3 --> SNS[SNS]
```

## Trade-offs

- **Simplicity vs Scale**: Jeff wanted 1 Lambda, Werner wanted 47 regions. We compromised with 47 Lambdas in 12 regions.
- **Speed vs Perfection**: Swami's 2-week timeline means we're shipping the ML model before it's trained.
- **Cost vs Reliability**: The monthly bill could fund a small country, but your todos will survive nuclear war.
- **Serverless vs Control**: Everything is managed, which means nobody knows how it actually works.
"""


def test_parser():
    """Test the input parser."""
    print("=" * 60)
    print("Testing InputParser")
    print("=" * 60)
    
    parser = InputParser()
    
    # Test parsing
    try:
        architecture = parser.parse(SAMPLE_SYNTHESIS, "Build a simple todo app")
        print(f"✓ Feature name: {architecture.feature_name}")
        print(f"✓ Overview length: {len(architecture.overview)} chars")
        print(f"✓ Components found: {len(architecture.components)}")
        for c in architecture.components[:5]:
            print(f"  - {c.name} ({c.service_type})")
        print(f"✓ Mermaid diagram: {len(architecture.mermaid_diagram)} chars")
        print(f"✓ Trade-offs found: {len(architecture.trade_offs)}")
        return True
    except Exception as e:
        print(f"✗ Parser failed: {e}")
        return False


def test_feature_name_derivation():
    """Test feature name derivation."""
    print("\n" + "=" * 60)
    print("Testing Feature Name Derivation")
    print("=" * 60)
    
    parser = InputParser()
    
    test_cases = [
        ("Build a simple todo app", "build-a-simple-todo-app"),
        ("Create an AI-powered chatbot!!!", "create-an-aipowered-chatbot"),
        ("Mars Digital Currency System", "mars-digital-currency-system"),
        ("   Spaces   everywhere   ", "spaces-everywhere"),
    ]
    
    all_passed = True
    for problem, expected_prefix in test_cases:
        result = parser.derive_feature_name(problem)
        passed = result.startswith(expected_prefix.split('-')[0])
        status = "✓" if passed else "✗"
        print(f"{status} '{problem[:30]}...' -> '{result}'")
        if not passed:
            all_passed = False
    
    return all_passed


def test_spec_generation_local():
    """Test spec generation with local output (no S3)."""
    print("\n" + "=" * 60)
    print("Testing Spec Generation (Local)")
    print("=" * 60)
    
    # Extract mermaid diagram
    parser = InputParser()
    mermaid = parser.extract_mermaid(SAMPLE_SYNTHESIS)
    
    print("Generating spec package (this may take a minute)...")
    
    result = generate_spec_package(
        problem="Build a simple todo app that scales to billions of users",
        synthesis_output=SAMPLE_SYNTHESIS,
        mermaid_diagram=mermaid,
        session_id="test_session_001",
        local_only=True
    )
    
    print(f"\nResult:")
    print(f"  Status: {result.status}")
    print(f"  Feature Name: {result.feature_name}")
    
    if result.status == "complete":
        print(f"  Local Path: {result.local_path}")
        if result.local_path and os.path.exists(result.local_path):
            print(f"  ✓ ZIP file created successfully!")
            
            # Extract and show contents
            import zipfile
            with zipfile.ZipFile(result.local_path, 'r') as zf:
                print(f"  ZIP contents:")
                for name in zf.namelist():
                    info = zf.getinfo(name)
                    print(f"    - {name} ({info.file_size} bytes)")
            return True
    else:
        print(f"  Error: {result.error}")
        return False


def main():
    """Run all tests."""
    print("\n" + "=" * 60)
    print("SPEC GENERATOR AGENT TESTS")
    print("=" * 60)
    
    results = []
    
    # Test parser
    results.append(("Parser", test_parser()))
    
    # Test feature name derivation
    results.append(("Feature Name", test_feature_name_derivation()))
    
    # Test spec generation (requires AWS credentials)
    try:
        results.append(("Spec Generation", test_spec_generation_local()))
    except Exception as e:
        print(f"\n✗ Spec generation failed: {e}")
        results.append(("Spec Generation", False))
    
    # Summary
    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)
    
    for name, passed in results:
        status = "✓ PASSED" if passed else "✗ FAILED"
        print(f"  {name}: {status}")
    
    all_passed = all(r[1] for r in results)
    print(f"\nOverall: {'ALL TESTS PASSED' if all_passed else 'SOME TESTS FAILED'}")
    
    return 0 if all_passed else 1


if __name__ == "__main__":
    exit(main())
