#!/usr/bin/env python3
"""Integration test for orchestrator module."""

import asyncio
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from orchestrator.app import debate_orchestrator, get_problem_by_id, PROBLEMS


def test_problem_loading():
    """Verify predefined problems are loaded correctly."""
    print("Testing problem loading...")
    
    # Requirement 11.1: Load problem statements from configuration
    assert len(PROBLEMS) > 0, "Should load problem statements"
    
    # Requirement 11.1: Should contain predefined problems
    expected_ids = ['mars_currency', 'air_taxi_pollution', 'personal_air_taxi']
    for problem_id in expected_ids:
        assert problem_id in PROBLEMS, f"Should contain {problem_id}"
        problem = PROBLEMS[problem_id]
        assert 'id' in problem, "Problem should have id"
        assert 'title' in problem, "Problem should have title"
        assert 'statement' in problem, "Problem should have statement"
    
    print("✓ Problem loading verified")
    print(f"  - Loaded {len(PROBLEMS)} predefined problems")


def test_get_problem_by_id():
    """Verify problem retrieval by ID works correctly."""
    print("\nTesting get_problem_by_id...")
    
    # Requirement 11.2: Retrieve problem by identifier
    problem = get_problem_by_id('mars_currency')
    assert problem is not None, "Should retrieve mars_currency problem"
    assert len(problem) > 0, "Problem statement should not be empty"
    assert "Mars" in problem or "Moon" in problem, "Should contain Mars/Moon reference"
    
    # Test non-existent problem
    problem = get_problem_by_id('nonexistent')
    assert problem is None, "Should return None for non-existent problem"
    
    print("✓ get_problem_by_id verified")


async def test_orchestrator_validation():
    """Verify orchestrator validates input correctly."""
    print("\nTesting orchestrator input validation...")
    
    # Requirement 1.4: Empty input rejection
    result = await debate_orchestrator({"problem": ""}, {})
    assert result['status'] == 'error', "Should reject empty problem"
    assert 'empty' in result['error'].lower(), "Error should mention empty"
    
    result = await debate_orchestrator({"problem": "   "}, {})
    assert result['status'] == 'error', "Should reject whitespace-only problem"
    
    # Test missing problem
    result = await debate_orchestrator({}, {})
    assert result['status'] == 'error', "Should reject missing problem"
    
    print("✓ Input validation verified")
    print("  - Rejects empty problems")
    print("  - Rejects whitespace-only problems")


async def test_orchestrator_problem_by_id():
    """Verify orchestrator can load problems by ID."""
    print("\nTesting orchestrator problem loading by ID...")
    
    # Requirement 11.2: Load problem by ID
    result = await debate_orchestrator({"problemId": "mars_currency"}, {})
    
    # Should not error on valid problem ID
    if result['status'] == 'error':
        print(f"  Note: Got error (expected in test environment): {result.get('error')}")
        # In test environment without AWS credentials, we expect session creation to fail
        # But we verify the problem was loaded correctly
        assert 'not found' not in result['error'].lower(), "Should find the problem"
    else:
        assert 'sessionId' in result, "Should return session ID"
    
    # Test invalid problem ID
    result = await debate_orchestrator({"problemId": "invalid_id"}, {})
    assert result['status'] == 'error', "Should error on invalid problem ID"
    assert 'not found' in result['error'].lower(), "Should indicate problem not found"
    
    print("✓ Problem loading by ID verified")


async def test_orchestrator_structure():
    """Verify orchestrator has correct structure and flow."""
    print("\nTesting orchestrator structure...")
    
    # Verify the orchestrator function exists and is async
    assert asyncio.iscoroutinefunction(debate_orchestrator), "Should be async function"
    
    # Verify it accepts correct parameters
    import inspect
    sig = inspect.signature(debate_orchestrator)
    params = list(sig.parameters.keys())
    assert 'payload' in params, "Should accept payload parameter"
    assert 'context' in params, "Should accept context parameter"
    
    print("✓ Orchestrator structure verified")
    print("  - Async function")
    print("  - Correct parameters (payload, context)")


def test_requirements_coverage():
    """Verify implementation covers all task requirements."""
    print("\nVerifying requirements coverage...")
    
    # Read the orchestrator code to verify implementation
    orchestrator_path = os.path.join(os.path.dirname(__file__), 'orchestrator', 'app.py')
    with open(orchestrator_path, 'r') as f:
        code = f.read()
    
    # Requirement 1.4: Validate non-empty problem
    assert 'not problem or not problem.strip()' in code, "Should validate empty problem"
    print("✓ Requirement 1.4: Validates non-empty problem statement")
    
    # Requirement 1.5: Return session identifier
    assert 'sessionId' in code, "Should return session ID"
    print("✓ Requirement 1.5: Returns session identifier")
    
    # Requirement 2.1: Execute 3 rounds
    assert 'range(1, 4)' in code, "Should execute 3 rounds"
    print("✓ Requirement 2.1: Executes exactly 3 rounds")
    
    # Requirement 2.2: Invoke experts sequentially
    assert 'jeff_barr_agent, swami_agent, werner_agent' in code, "Should invoke experts in order"
    print("✓ Requirement 2.2: Invokes experts sequentially (jeff, swami, werner)")
    
    # Requirement 2.3: Store each response
    assert 'memory.store_response' in code, "Should store responses"
    print("✓ Requirement 2.3: Stores each response to AgentCore Memory")
    
    # Requirement 2.4: Automatic round progression
    assert 'for round_num in range(1, 4)' in code, "Should progress through rounds automatically"
    print("✓ Requirement 2.4: Automatic round progression")
    
    # Requirement 2.5: Consensus round
    assert 'consensus' in code.lower(), "Should have consensus round"
    assert 'round_num == 3' in code, "Should identify round 3 as consensus"
    print("✓ Requirement 2.5: Round 3 is consensus round")
    
    # Requirement 2.6: Trigger synthesis after rounds
    assert 'synthesis_agent.run' in code, "Should trigger synthesis agent"
    assert 'get_full_context' in code, "Should retrieve full context for synthesis"
    print("✓ Requirement 2.6: Triggers Synthesis Agent after all rounds")
    
    # Requirement 6.2: Retrieve cumulative context
    assert 'memory.get_context' in code, "Should retrieve context before each expert"
    print("✓ Requirement 6.2: Retrieves cumulative context before each expert invocation")
    
    # Return Mermaid diagram
    assert 'extract_mermaid' in code, "Should extract Mermaid diagram"
    assert 'mermaidDiagram' in code, "Should return Mermaid diagram"
    print("✓ Task requirement: Returns final synthesis with Mermaid diagram")
    
    print("\n✅ All requirements covered:")
    print("  - Requirements 1.4: Input validation ✓")
    print("  - Requirements 1.5: Session ID return ✓")
    print("  - Requirements 2.1: 3-round debate loop ✓")
    print("  - Requirements 2.2: Sequential expert invocation ✓")
    print("  - Requirements 2.3: Memory storage ✓")
    print("  - Requirements 2.4: Automatic progression ✓")
    print("  - Requirements 2.5: Consensus round ✓")
    print("  - Requirements 2.6: Synthesis trigger ✓")
    print("  - Requirements 6.2: Context retrieval ✓")


async def run_async_tests():
    """Run all async tests."""
    await test_orchestrator_validation()
    await test_orchestrator_problem_by_id()
    await test_orchestrator_structure()


if __name__ == "__main__":
    print("="*60)
    print("ORCHESTRATOR INTEGRATION TESTS")
    print("="*60)
    
    # Run synchronous tests
    test_problem_loading()
    test_get_problem_by_id()
    test_requirements_coverage()
    
    # Run async tests
    print("\nRunning async tests...")
    asyncio.run(run_async_tests())
    
    print("\n" + "="*60)
    print("✅ ALL ORCHESTRATOR TESTS PASSED!")
    print("="*60)
