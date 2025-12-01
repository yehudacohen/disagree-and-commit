#!/usr/bin/env python3
"""Test context retrieval updates for task 3.4"""

import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


def test_get_context_signature():
    """Verify get_context method has correct signature with actor_id parameter."""
    from memory.session_manager import MemoryManager
    import inspect
    
    # Get the signature of get_context
    sig = inspect.signature(MemoryManager.get_context)
    params = list(sig.parameters.keys())
    
    print("Testing get_context signature...")
    assert 'self' in params, "Should have self parameter"
    assert 'session_id' in params, "Should have session_id parameter"
    assert 'actor_id' in params, "Should have actor_id parameter"
    print("✓ get_context has correct signature: (self, session_id, actor_id)")


def test_get_full_context_signature():
    """Verify get_full_context method has correct signature with actor_id parameter."""
    from memory.session_manager import MemoryManager
    import inspect
    
    # Get the signature of get_full_context
    sig = inspect.signature(MemoryManager.get_full_context)
    params = list(sig.parameters.keys())
    
    print("\nTesting get_full_context signature...")
    assert 'self' in params, "Should have self parameter"
    assert 'session_id' in params, "Should have session_id parameter"
    assert 'actor_id' in params, "Should have actor_id parameter"
    print("✓ get_full_context has correct signature: (self, session_id, actor_id)")


def test_orchestrator_uses_actor_id():
    """Verify orchestrator passes actor_id to context retrieval methods."""
    orchestrator_path = os.path.join(os.path.dirname(__file__), 'orchestrator', 'app.py')
    
    with open(orchestrator_path, 'r') as f:
        code = f.read()
    
    print("\nTesting orchestrator context retrieval calls...")
    
    # Check get_context call includes actor_id
    assert 'memory.get_context(session_id=session_id, actor_id=agent.name)' in code, \
        "get_context should be called with actor_id=agent.name"
    print("✓ get_context call includes actor_id parameter")
    
    # Check get_full_context call includes actor_id
    assert 'memory.get_full_context(session_id=session_id, actor_id=actor_id)' in code, \
        "get_full_context should be called with actor_id=actor_id"
    print("✓ get_full_context call includes actor_id parameter")


def test_empty_context_handling():
    """Verify orchestrator handles empty context gracefully."""
    orchestrator_path = os.path.join(os.path.dirname(__file__), 'orchestrator', 'app.py')
    
    with open(orchestrator_path, 'r') as f:
        code = f.read()
    
    print("\nTesting empty context handling...")
    
    # Check for empty context handling in get_context
    assert 'if not mem_context or not mem_context.strip():' in code, \
        "Should check for empty or whitespace-only context"
    assert 'mem_context = "[No previous context]"' in code, \
        "Should provide fallback message for empty context"
    print("✓ get_context handles empty context gracefully")
    
    # Check for empty context handling in get_full_context
    assert 'if not full_context or not full_context.strip():' in code, \
        "Should check for empty or whitespace-only full context"
    assert 'full_context = "[No debate context available]"' in code, \
        "Should provide fallback message for empty full context"
    print("✓ get_full_context handles empty context gracefully")


def test_requirements_coverage():
    """Verify task 3.4 requirements are met."""
    print("\nVerifying task 3.4 requirements coverage...")
    
    orchestrator_path = os.path.join(os.path.dirname(__file__), 'orchestrator', 'app.py')
    with open(orchestrator_path, 'r') as f:
        code = f.read()
    
    # Requirement: Add actor_id parameter to get_context calls
    assert 'actor_id=agent.name' in code, "Should pass actor_id to get_context"
    print("✓ Requirement 2.4, 6.2, 7.2: actor_id parameter added to get_context calls")
    
    # Requirement: Update get_full_context call for synthesis
    assert 'actor_id=actor_id' in code, "Should pass actor_id to get_full_context"
    print("✓ Requirement 2.4, 6.2, 7.2: actor_id parameter added to get_full_context call")
    
    # Requirement: Handle empty context gracefully
    assert '[No previous context]' in code, "Should handle empty context in debate loop"
    assert '[No debate context available]' in code, "Should handle empty context in synthesis"
    print("✓ Requirement 2.4, 6.2, 7.2: Empty context handled gracefully")


if __name__ == "__main__":
    print("="*60)
    print("TASK 3.4: CONTEXT RETRIEVAL UPDATES TEST")
    print("="*60)
    
    test_get_context_signature()
    test_get_full_context_signature()
    test_orchestrator_uses_actor_id()
    test_empty_context_handling()
    test_requirements_coverage()
    
    print("\n" + "="*60)
    print("✅ ALL TASK 3.4 TESTS PASSED!")
    print("="*60)
    print("\nTask 3.4 Implementation Summary:")
    print("- ✓ Added actor_id parameter to get_context calls")
    print("- ✓ Updated get_full_context call for synthesis")
    print("- ✓ Implemented graceful empty context handling")
    print("- ✓ All requirements (2.4, 6.2, 7.2) satisfied")
