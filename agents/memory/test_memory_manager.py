"""Unit tests for MemoryManager class."""

import pytest
from unittest.mock import Mock, patch, MagicMock
from datetime import datetime
import hashlib
from memory.session_manager import MemoryManager


class TestMemoryManager:
    """Test suite for MemoryManager."""
    
    def test_init_default_memory_id(self):
        """Test MemoryManager initialization with default memory_id."""
        with patch('boto3.client'):
            manager = MemoryManager()
            assert manager.memory_id == 'debate-memory'
            assert manager.region == 'us-east-1'
            assert manager.max_retries == 3
            assert manager.base_delay == 1.0
            assert manager.max_delay == 10.0
    
    def test_init_custom_memory_id(self):
        """Test MemoryManager initialization with custom memory_id."""
        with patch('boto3.client'):
            manager = MemoryManager(memory_id='custom-memory')
            assert manager.memory_id == 'custom-memory'
    
    def test_init_custom_region(self):
        """Test MemoryManager initialization with custom region."""
        with patch('boto3.client') as mock_boto:
            manager = MemoryManager(region='us-west-2')
            assert manager.region == 'us-west-2'
            # Verify boto3 client was called with correct region
            mock_boto.assert_called_once_with('bedrock-agent-runtime', region_name='us-west-2')
    
    def test_create_session_format(self):
        """Test that create_session generates correct session ID format."""
        with patch('boto3.client') as mock_boto:
            mock_client = Mock()
            mock_boto.return_value = mock_client
            
            manager = MemoryManager()
            problem = "Test problem statement"
            actor_id = "test_actor"
            
            session_id = manager.create_session(problem, actor_id)
            
            # Verify format: debate_{8-char-hash}_{timestamp}
            assert session_id.startswith('debate_')
            
            # Verify minimum length requirement (33 characters)
            assert len(session_id) >= 33
    
    def test_create_session_no_api_call(self):
        """Test that create_session does not call API (sessions are implicit)."""
        with patch('boto3.client') as mock_boto:
            mock_client = Mock()
            mock_boto.return_value = mock_client
            
            manager = MemoryManager()
            problem = "Test problem"
            actor_id = "test_actor"
            
            session_id = manager.create_session(problem, actor_id)
            
            # Verify NO API was called (sessions are implicit)
            mock_client.create_memory_session.assert_not_called()
            assert session_id.startswith('debate_')
            assert len(session_id) >= 33
    
    def test_store_response_with_metadata(self):
        """Test that store_response uses create_event API correctly."""
        with patch('boto3.client') as mock_boto:
            mock_client = Mock()
            mock_boto.return_value = mock_client
            
            manager = MemoryManager()
            session_id = "debate_abc12345_2025-11-30T12:00:00123"
            actor_id = "jeff_barr"
            round_num = 2
            content = "Test response content"
            
            manager.store_response(session_id, actor_id, round_num, content)
            
            # Verify create_event API was called with correct parameters
            mock_client.create_event.assert_called_once()
            call_args = mock_client.create_event.call_args
            
            assert call_args[1]['memoryId'] == 'debate-memory'
            assert call_args[1]['sessionId'] == session_id
            assert call_args[1]['actorId'] == actor_id
            
            # Verify message format
            messages = call_args[1]['messages']
            assert len(messages) == 2
            assert messages[0]['role'] == 'USER'
            assert f'Round {round_num}' in messages[0]['text']
            assert messages[1]['role'] == 'ASSISTANT'
            assert messages[1]['text'] == content
    
    def test_get_context_formats_correctly(self):
        """Test that get_context uses retrieve_memory API and formats correctly."""
        with patch('boto3.client') as mock_boto:
            mock_client = Mock()
            mock_boto.return_value = mock_client
            
            # Mock response from retrieve_memory with new structure
            mock_client.retrieve_memory.return_value = {
                'memories': [
                    {
                        'content': {
                            'text': 'First response'
                        }
                    },
                    {
                        'content': {
                            'text': 'Second response'
                        }
                    }
                ]
            }
            
            manager = MemoryManager()
            session_id = "debate_abc12345_2025-11-30T12:00:00123"
            actor_id = "test_actor"
            
            context = manager.get_context(session_id, actor_id)
            
            # Verify format
            expected = "First response\n\nSecond response"
            assert context == expected
            
            # Verify retrieve_memory API was called
            mock_client.retrieve_memory.assert_called_once()
            call_args = mock_client.retrieve_memory.call_args
            assert call_args[1]['memoryId'] == 'debate-memory'
            assert call_args[1]['sessionId'] == session_id
            assert call_args[1]['actorId'] == actor_id
            assert call_args[1]['maxResults'] == 50
    
    def test_get_context_empty_memories(self):
        """Test that get_context handles empty memories."""
        with patch('boto3.client') as mock_boto:
            mock_client = Mock()
            mock_boto.return_value = mock_client
            
            mock_client.retrieve_memory.return_value = {'memories': []}
            
            manager = MemoryManager()
            context = manager.get_context("test_session", "test_actor")
            
            assert context == ""
    
    def test_get_full_context_retrieves_all_memories(self):
        """Test that get_full_context uses retrieve_memory with higher limit."""
        with patch('boto3.client') as mock_boto:
            mock_client = Mock()
            mock_boto.return_value = mock_client
            
            mock_client.retrieve_memory.return_value = {
                'memories': [
                    {'content': {'text': 'Test response'}}
                ]
            }
            
            manager = MemoryManager()
            session_id = "test_session_12345678901234567890123"
            actor_id = "test_actor"
            
            full_context = manager.get_full_context(session_id, actor_id)
            
            assert full_context == "Test response"
            
            # Verify retrieve_memory was called with maxResults=100
            mock_client.retrieve_memory.assert_called_once()
            call_args = mock_client.retrieve_memory.call_args
            assert call_args[1]['maxResults'] == 100
    
    def test_create_session_no_retry_needed(self):
        """Test that create_session generates ID without API calls."""
        with patch('boto3.client') as mock_boto:
            mock_client = Mock()
            mock_boto.return_value = mock_client
            
            manager = MemoryManager()
            
            # Should succeed immediately (no API call)
            session_id = manager.create_session("Test problem", "test_actor")
            
            assert session_id.startswith('debate_')
            assert len(session_id) >= 33
            # No API calls should be made
            mock_client.create_memory_session.assert_not_called()
    
    def test_store_response_retry_logic(self):
        """Test that store_response has retry logic."""
        with patch('boto3.client') as mock_boto:
            mock_client = Mock()
            mock_boto.return_value = mock_client
            
            # Fail first time, succeed second time
            mock_client.create_event.side_effect = [
                Exception("Transient error"),
                {}
            ]
            
            manager = MemoryManager()
            
            # Should succeed after retry
            with patch('time.sleep'):
                manager.store_response("session_12345678901234567890123", "jeff_barr", 1, "content")
            
            assert mock_client.create_event.call_count == 2
    
    def test_get_context_retry_logic(self):
        """Test that get_context has retry logic."""
        with patch('boto3.client') as mock_boto:
            mock_client = Mock()
            mock_boto.return_value = mock_client
            
            # Fail first time, succeed second time
            mock_client.retrieve_memory.side_effect = [
                Exception("Transient error"),
                {'memories': []}
            ]
            
            manager = MemoryManager()
            
            # Should succeed after retry
            with patch('time.sleep'):
                context = manager.get_context("session_12345678901234567890123", "test_actor")
            
            assert context == ""
            assert mock_client.retrieve_memory.call_count == 2


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
