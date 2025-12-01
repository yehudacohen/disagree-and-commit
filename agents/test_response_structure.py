"""
Test to verify response structure updates for task 3.5
"""
import pytest
from unittest.mock import Mock, patch, MagicMock
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Mock the expert agents before importing orchestrator
sys.modules['experts.jeff_barr'] = MagicMock()
sys.modules['experts.swami'] = MagicMock()
sys.modules['experts.werner_vogels'] = MagicMock()
sys.modules['synthesis.synthesizer'] = MagicMock()


@pytest.mark.asyncio
async def test_error_response_includes_actor_id_and_session_id():
    """Test that error responses include actor_id and session_id fields"""
    
    # Mock the dependencies
    with patch('orchestrator.app.memory') as mock_memory, \
         patch('orchestrator.app.jeff_barr_agent') as mock_jeff, \
         patch('orchestrator.app.swami_agent') as mock_swami, \
         patch('orchestrator.app.werner_agent') as mock_werner:
        
        # Import after patching
        from orchestrator.app import debate_orchestrator
        
        # Test 1: Empty problem statement error
        payload = {"problem": ""}
        result = await debate_orchestrator(payload, {})
        
        assert result["status"] == "error"
        assert "actor_id" in result
        assert result["actor_id"] == "orchestrator"
        assert "session_id" in result
        assert result["session_id"] is None
        assert "error" in result
        
        # Test 2: Invalid problem ID error
        payload = {"problemId": "nonexistent_id"}
        result = await debate_orchestrator(payload, {})
        
        assert result["status"] == "error"
        assert "actor_id" in result
        assert result["actor_id"] == "orchestrator"
        assert "session_id" in result
        assert result["session_id"] is None
        assert "error" in result
        
        # Test 3: Session creation failure error
        mock_memory.create_session.side_effect = Exception("Session creation failed")
        payload = {"problem": "Test problem"}
        result = await debate_orchestrator(payload, {})
        
        assert result["status"] == "error"
        assert "actor_id" in result
        assert result["actor_id"] == "orchestrator"
        assert "session_id" in result
        assert result["session_id"] is None
        assert "error" in result
        assert "Session creation failed" in result["error"]


@pytest.mark.asyncio
async def test_synthesis_error_response_includes_all_fields():
    """Test that synthesis error responses include all required fields"""
    
    with patch('orchestrator.app.memory') as mock_memory, \
         patch('orchestrator.app.jeff_barr_agent') as mock_jeff, \
         patch('orchestrator.app.swami_agent') as mock_swami, \
         patch('orchestrator.app.werner_agent') as mock_werner, \
         patch('orchestrator.app.synthesis_agent') as mock_synthesis:
        
        from orchestrator.app import debate_orchestrator
        
        # Setup mocks
        mock_memory.create_session.return_value = "test-session-12345678901234567890123456789012"
        mock_memory.get_context.return_value = "Previous context"
        mock_memory.get_full_context.return_value = "Full debate context"
        
        # Mock agent responses
        mock_response = MagicMock()
        mock_response.message = {"content": [{"text": "Agent response"}]}
        mock_jeff.return_value = mock_response
        mock_jeff.name = "jeff_barr"
        mock_swami.return_value = mock_response
        mock_swami.name = "swami"
        mock_werner.return_value = mock_response
        mock_werner.name = "werner_vogels"
        
        # Make synthesis fail with invalid response structure
        mock_synthesis_response = MagicMock()
        mock_synthesis_response.message = {"invalid": "structure"}
        mock_synthesis.return_value = mock_synthesis_response
        
        payload = {"problem": "Test problem", "actor_id": "test_actor"}
        result = await debate_orchestrator(payload, {})
        
        assert result["status"] == "error"
        assert "actor_id" in result
        assert result["actor_id"] == "test_actor"
        assert "session_id" in result
        assert result["session_id"] == "test-session-12345678901234567890123456789012"
        assert "sessionId" in result
        assert result["sessionId"] == "test-session-12345678901234567890123456789012"
        assert "error" in result
        assert "synthesis" in result
        assert result["synthesis"] is None
        assert "mermaidDiagram" in result
        assert result["mermaidDiagram"] is None


@pytest.mark.asyncio
async def test_success_response_includes_all_fields():
    """Test that success responses include all required fields"""
    
    with patch('orchestrator.app.memory') as mock_memory, \
         patch('orchestrator.app.jeff_barr_agent') as mock_jeff, \
         patch('orchestrator.app.swami_agent') as mock_swami, \
         patch('orchestrator.app.werner_agent') as mock_werner, \
         patch('orchestrator.app.synthesis_agent') as mock_synthesis, \
         patch('orchestrator.app.extract_mermaid') as mock_extract:
        
        from orchestrator.app import debate_orchestrator
        
        # Setup mocks
        mock_memory.create_session.return_value = "test-session-12345678901234567890123456789012"
        mock_memory.get_context.return_value = "Previous context"
        mock_memory.get_full_context.return_value = "Full debate context"
        
        # Mock agent responses
        mock_response = MagicMock()
        mock_response.message = {"content": [{"text": "Agent response"}]}
        mock_jeff.return_value = mock_response
        mock_jeff.name = "jeff_barr"
        mock_swami.return_value = mock_response
        mock_swami.name = "swami"
        mock_werner.return_value = mock_response
        mock_werner.name = "werner_vogels"
        
        # Mock synthesis response
        mock_synthesis_response = MagicMock()
        mock_synthesis_response.message = {"content": [{"text": "Synthesis text with architecture"}]}
        mock_synthesis.return_value = mock_synthesis_response
        mock_extract.return_value = "graph TD\n  A --> B"
        
        payload = {"problem": "Test problem", "actor_id": "test_actor"}
        result = await debate_orchestrator(payload, {})
        
        assert result["status"] == "complete"
        assert "actor_id" in result
        assert result["actor_id"] == "test_actor"
        assert "session_id" in result
        assert result["session_id"] == "test-session-12345678901234567890123456789012"
        assert "sessionId" in result
        assert result["sessionId"] == "test-session-12345678901234567890123456789012"
        assert "synthesis" in result
        assert result["synthesis"] == "Synthesis text with architecture"
        assert "mermaidDiagram" in result
        assert result["mermaidDiagram"] == "graph TD\n  A --> B"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
