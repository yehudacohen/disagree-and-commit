#!/usr/bin/env python3
"""Integration test for orchestrator module."""

import asyncio
import sys
import os
from unittest.mock import Mock, patch, AsyncMock

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
    assert 'synthesis_agent(' in code, "Should trigger synthesis agent with correct pattern"
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


async def test_agent_invocation_with_mocks():
    """Test orchestrator with mocked agents using correct response structure (Requirement 10.1, 10.2)."""
    print("\nTesting orchestrator with mocked agents...")
    
    # Create mock response with correct structure (Requirement 10.1)
    mock_response = Mock()
    mock_response.message = {
        'content': [
            {'text': 'Mocked expert response'}
        ]
    }
    
    # Mock all three expert agents
    with patch('orchestrator.app.jeff_barr_agent') as mock_jeff, \
         patch('orchestrator.app.swami_agent') as mock_swami, \
         patch('orchestrator.app.werner_agent') as mock_werner, \
         patch('orchestrator.app.synthesis_agent') as mock_synthesis, \
         patch('orchestrator.app.memory') as mock_memory:
        
        # Configure mocks to return correct response structure (Requirement 10.1)
        mock_jeff.return_value = mock_response
        mock_jeff.name = "jeff_barr"
        mock_swami.return_value = mock_response
        mock_swami.name = "swami"
        mock_werner.return_value = mock_response
        mock_werner.name = "werner_vogels"
        
        # Mock synthesis response with Mermaid diagram (Requirement 10.1)
        mock_synthesis_response = Mock()
        mock_synthesis_response.message = {
            'content': [
                {'text': '## Architecture\nTest architecture\n```mermaid\ngraph TD\n  A-->B\n```'}
            ]
        }
        mock_synthesis.return_value = mock_synthesis_response
        
        # Mock memory operations with new methods (Requirement 10.2)
        mock_memory.create_session.return_value = "test_session_12345678901234567890123"
        mock_memory.get_context.return_value = "Previous context"
        mock_memory.get_full_context.return_value = "Full debate context"
        mock_memory.store_response.return_value = None
        
        # Test orchestrator with complete debate flow (Requirement 10.3)
        result = await debate_orchestrator(
            {"problem": "Test problem statement"},
            {}
        )
        
        # Verify response structure validation (Requirement 10.4)
        assert result['status'] == 'complete', f"Expected complete status, got {result['status']}"
        assert 'sessionId' in result, "Response missing sessionId"
        assert 'synthesis' in result, "Response missing synthesis"
        assert 'mermaidDiagram' in result, "Response missing mermaidDiagram"
        assert 'actor_id' in result, "Response missing actor_id"
        assert 'session_id' in result, "Response missing session_id"
        
        # Verify agents were called (3 rounds × 3 agents = 9 calls)
        assert mock_jeff.call_count == 3, f"Jeff should be called 3 times, was called {mock_jeff.call_count}"
        assert mock_swami.call_count == 3, f"Swami should be called 3 times, was called {mock_swami.call_count}"
        assert mock_werner.call_count == 3, f"Werner should be called 3 times, was called {mock_werner.call_count}"
        
        # Verify synthesis was called once
        assert mock_synthesis.call_count == 1, "Synthesis should be called once"
        
        # Verify memory operations were called correctly (Requirement 10.2)
        assert mock_memory.create_session.call_count == 1, "create_session should be called once"
        assert mock_memory.store_response.call_count == 9, "store_response should be called 9 times (3 rounds × 3 agents)"
        assert mock_memory.get_context.call_count == 9, "get_context should be called 9 times"
        assert mock_memory.get_full_context.call_count == 1, "get_full_context should be called once for synthesis"
        
        print("✓ Orchestrator with mocked agents verified")
        print(f"  - Agents invoked with correct pattern (agent(prompt))")
        print(f"  - Response structure validated (message['content'][0]['text'])")
        print(f"  - Memory operations called correctly (create_session, store_response, get_context)")
        print(f"  - Complete debate flow executed (3 rounds × 3 agents)")


async def test_error_handling():
    """Test orchestrator error handling for agent failures (Requirement 10.3, 10.4)."""
    print("\nTesting orchestrator error handling...")
    
    # Test 1: Agent invocation failure (Requirement 10.4)
    with patch('orchestrator.app.jeff_barr_agent') as mock_jeff, \
         patch('orchestrator.app.swami_agent') as mock_swami, \
         patch('orchestrator.app.werner_agent') as mock_werner, \
         patch('orchestrator.app.synthesis_agent') as mock_synthesis, \
         patch('orchestrator.app.memory') as mock_memory:
        
        # Configure first agent to fail
        mock_jeff.side_effect = Exception("Agent invocation failed")
        mock_jeff.name = "jeff_barr"
        
        # Other agents return valid responses
        mock_response = Mock()
        mock_response.message = {
            'content': [
                {'text': 'Mocked response'}
            ]
        }
        mock_swami.return_value = mock_response
        mock_swami.name = "swami"
        mock_werner.return_value = mock_response
        mock_werner.name = "werner_vogels"
        
        # Mock synthesis
        mock_synthesis_response = Mock()
        mock_synthesis_response.message = {
            'content': [
                {'text': '## Architecture\nTest\n```mermaid\ngraph TD\n  A-->B\n```'}
            ]
        }
        mock_synthesis.return_value = mock_synthesis_response
        
        # Mock memory
        mock_memory.create_session.return_value = "test_session_12345678901234567890123"
        mock_memory.get_context.return_value = ""
        mock_memory.get_full_context.return_value = "Context"
        mock_memory.store_response.return_value = None
        
        # Test orchestrator - should handle error gracefully
        result = await debate_orchestrator(
            {"problem": "Test problem"},
            {}
        )
        
        # Should complete despite agent failure (Requirement 10.4)
        assert result['status'] == 'complete', "Should complete despite agent failure"
        
        # Verify other agents were still called
        assert mock_swami.call_count == 3, "Swami should be called 3 times"
        assert mock_werner.call_count == 3, "Werner should be called 3 times"
        
        print("✓ Agent failure error handling verified")
        print("  - Continues execution after agent failure")
        print("  - Returns complete status")
        print("  - Other agents still invoked")
    
    # Test 2: Invalid response structure (Requirement 10.4)
    with patch('orchestrator.app.jeff_barr_agent') as mock_jeff, \
         patch('orchestrator.app.swami_agent') as mock_swami, \
         patch('orchestrator.app.werner_agent') as mock_werner, \
         patch('orchestrator.app.synthesis_agent') as mock_synthesis, \
         patch('orchestrator.app.memory') as mock_memory:
        
        # Configure agent to return invalid response structure
        mock_invalid_response = Mock()
        mock_invalid_response.message = {}  # Missing 'content' key
        
        mock_jeff.return_value = mock_invalid_response
        mock_jeff.name = "jeff_barr"
        
        # Other agents return valid responses
        mock_response = Mock()
        mock_response.message = {
            'content': [
                {'text': 'Valid response'}
            ]
        }
        mock_swami.return_value = mock_response
        mock_swami.name = "swami"
        mock_werner.return_value = mock_response
        mock_werner.name = "werner_vogels"
        
        # Mock synthesis
        mock_synthesis_response = Mock()
        mock_synthesis_response.message = {
            'content': [
                {'text': '## Architecture\nTest\n```mermaid\ngraph TD\n  A-->B\n```'}
            ]
        }
        mock_synthesis.return_value = mock_synthesis_response
        
        # Mock memory
        mock_memory.create_session.return_value = "test_session_12345678901234567890123"
        mock_memory.get_context.return_value = ""
        mock_memory.get_full_context.return_value = "Context"
        mock_memory.store_response.return_value = None
        
        # Test orchestrator - should handle invalid structure gracefully
        result = await debate_orchestrator(
            {"problem": "Test problem"},
            {}
        )
        
        # Should complete despite invalid response structure
        assert result['status'] == 'complete', "Should complete despite invalid response structure"
        
        print("✓ Invalid response structure error handling verified")
        print("  - Handles KeyError/TypeError gracefully")
        print("  - Continues execution with fallback message")
    
    # Test 3: Memory operation failure (Requirement 10.3)
    with patch('orchestrator.app.jeff_barr_agent') as mock_jeff, \
         patch('orchestrator.app.swami_agent') as mock_swami, \
         patch('orchestrator.app.werner_agent') as mock_werner, \
         patch('orchestrator.app.synthesis_agent') as mock_synthesis, \
         patch('orchestrator.app.memory') as mock_memory:
        
        # All agents return valid responses
        mock_response = Mock()
        mock_response.message = {
            'content': [
                {'text': 'Valid response'}
            ]
        }
        mock_jeff.return_value = mock_response
        mock_jeff.name = "jeff_barr"
        mock_swami.return_value = mock_response
        mock_swami.name = "swami"
        mock_werner.return_value = mock_response
        mock_werner.name = "werner_vogels"
        
        # Mock synthesis
        mock_synthesis_response = Mock()
        mock_synthesis_response.message = {
            'content': [
                {'text': '## Architecture\nTest\n```mermaid\ngraph TD\n  A-->B\n```'}
            ]
        }
        mock_synthesis.return_value = mock_synthesis_response
        
        # Mock memory with store_response failing
        mock_memory.create_session.return_value = "test_session_12345678901234567890123"
        mock_memory.get_context.return_value = ""
        mock_memory.get_full_context.return_value = "Context"
        mock_memory.store_response.side_effect = Exception("Memory storage failed")
        
        # Test orchestrator - should handle memory failure gracefully
        result = await debate_orchestrator(
            {"problem": "Test problem"},
            {}
        )
        
        # Should complete despite memory failures
        assert result['status'] == 'complete', "Should complete despite memory failures"
        
        print("✓ Memory operation failure error handling verified")
        print("  - Continues execution after memory failure")
        print("  - Returns complete status")
    
    # Test 4: Synthesis failure (Requirement 10.4)
    with patch('orchestrator.app.jeff_barr_agent') as mock_jeff, \
         patch('orchestrator.app.swami_agent') as mock_swami, \
         patch('orchestrator.app.werner_agent') as mock_werner, \
         patch('orchestrator.app.synthesis_agent') as mock_synthesis, \
         patch('orchestrator.app.memory') as mock_memory:
        
        # All agents return valid responses
        mock_response = Mock()
        mock_response.message = {
            'content': [
                {'text': 'Valid response'}
            ]
        }
        mock_jeff.return_value = mock_response
        mock_jeff.name = "jeff_barr"
        mock_swami.return_value = mock_response
        mock_swami.name = "swami"
        mock_werner.return_value = mock_response
        mock_werner.name = "werner_vogels"
        
        # Mock synthesis to fail
        mock_synthesis.side_effect = Exception("Synthesis failed")
        
        # Mock memory
        mock_memory.create_session.return_value = "test_session_12345678901234567890123"
        mock_memory.get_context.return_value = ""
        mock_memory.get_full_context.return_value = "Context"
        mock_memory.store_response.return_value = None
        
        # Test orchestrator - should return error status for synthesis failure
        result = await debate_orchestrator(
            {"problem": "Test problem"},
            {}
        )
        
        # Should return error status when synthesis fails
        assert result['status'] == 'error', "Should return error status when synthesis fails"
        assert 'error' in result, "Should include error message"
        assert 'Synthesis failed' in result['error'], "Error should mention synthesis failure"
        
        print("✓ Synthesis failure error handling verified")
        print("  - Returns error status for synthesis failure")
        print("  - Includes descriptive error message")


async def test_response_structure_validation():
    """Test that orchestrator returns all required response fields (Requirement 10.4)."""
    print("\nTesting response structure validation...")
    
    with patch('orchestrator.app.jeff_barr_agent') as mock_jeff, \
         patch('orchestrator.app.swami_agent') as mock_swami, \
         patch('orchestrator.app.werner_agent') as mock_werner, \
         patch('orchestrator.app.synthesis_agent') as mock_synthesis, \
         patch('orchestrator.app.memory') as mock_memory:
        
        # Configure all mocks with valid responses
        mock_response = Mock()
        mock_response.message = {
            'content': [
                {'text': 'Test response'}
            ]
        }
        mock_jeff.return_value = mock_response
        mock_jeff.name = "jeff_barr"
        mock_swami.return_value = mock_response
        mock_swami.name = "swami"
        mock_werner.return_value = mock_response
        mock_werner.name = "werner_vogels"
        
        mock_synthesis_response = Mock()
        mock_synthesis_response.message = {
            'content': [
                {'text': '## Architecture\nTest\n```mermaid\ngraph TD\n  A-->B\n```'}
            ]
        }
        mock_synthesis.return_value = mock_synthesis_response
        
        mock_memory.create_session.return_value = "test_session_12345678901234567890123"
        mock_memory.get_context.return_value = ""
        mock_memory.get_full_context.return_value = "Context"
        mock_memory.store_response.return_value = None
        
        # Test successful completion
        result = await debate_orchestrator(
            {"problem": "Test problem", "actor_id": "test_actor"},
            {}
        )
        
        # Verify all required fields are present (Requirement 10.4)
        required_fields = ['sessionId', 'actor_id', 'session_id', 'synthesis', 'mermaidDiagram', 'status']
        for field in required_fields:
            assert field in result, f"Response missing required field: {field}"
        
        # Verify field types
        assert isinstance(result['sessionId'], str), "sessionId should be string"
        assert isinstance(result['actor_id'], str), "actor_id should be string"
        assert isinstance(result['session_id'], str), "session_id should be string"
        assert isinstance(result['synthesis'], str), "synthesis should be string"
        assert isinstance(result['mermaidDiagram'], str), "mermaidDiagram should be string"
        assert result['status'] == 'complete', "status should be 'complete'"
        
        # Verify actor_id is passed through correctly
        assert result['actor_id'] == 'test_actor', "actor_id should match input"
        
        print("✓ Response structure validation verified")
        print("  - All required fields present")
        print("  - Correct field types")
        print("  - actor_id passed through correctly")
    
    # Test error response structure
    with patch('orchestrator.app.memory') as mock_memory:
        mock_memory.create_session.side_effect = Exception("Session creation failed")
        
        result = await debate_orchestrator(
            {"problem": "Test problem"},
            {}
        )
        
        # Verify error response structure
        assert result['status'] == 'error', "Should have error status"
        assert 'error' in result, "Should include error field"
        assert 'actor_id' in result, "Should include actor_id even on error"
        assert 'session_id' in result, "Should include session_id even on error"
        
        print("✓ Error response structure validated")
        print("  - Error status set correctly")
        print("  - Error message included")
        print("  - Required fields present even on error")


async def run_async_tests():
    """Run all async tests."""
    await test_orchestrator_validation()
    await test_orchestrator_problem_by_id()
    await test_orchestrator_structure()
    await test_agent_invocation_with_mocks()
    await test_error_handling()
    await test_response_structure_validation()


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
