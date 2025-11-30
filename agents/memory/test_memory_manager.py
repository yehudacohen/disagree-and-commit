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
            assert manager.max_retries == 3
            assert manager.base_delay == 1.0
            assert manager.max_delay == 10.0
    
    def test_init_custom_memory_id(self):
        """Test MemoryManager initialization with custom memory_id."""
        with patch('boto3.client'):
            manager = MemoryManager(memory_id='custom-memory')
            assert manager.memory_id == 'custom-memory'
    
    def test_create_session_format(self):
        """Test that create_session generates correct session ID format."""
        with patch('boto3.client') as mock_boto:
            mock_client = Mock()
            mock_boto.return_value = mock_client
            
            manager = MemoryManager()
            problem = "Test problem statement"
            
            session_id = manager.create_session(problem)
            
            # Verify format: debate_{8-char-hash}_{timestamp}
            parts = session_id.split('_')
            assert parts[0] == 'debate'
            assert len(parts[1]) == 8  # 8-char hash
            # parts[2] should be ISO8601 timestamp
            assert 'T' in parts[2]  # ISO8601 contains 'T'
            
            # Verify hash is correct
            expected_hash = hashlib.md5(problem.encode()).hexdigest()[:8]
            assert parts[1] == expected_hash
    
    def test_create_session_calls_api(self):
        """Test that create_session calls the AgentCore Memory API."""
        with patch('boto3.client') as mock_boto:
            mock_client = Mock()
            mock_boto.return_value = mock_client
            
            manager = MemoryManager()
            problem = "Test problem"
            
            session_id = manager.create_session(problem)
            
            # Verify API was called
            mock_client.create_memory_session.assert_called_once()
            call_args = mock_client.create_memory_session.call_args
            assert call_args[1]['memoryId'] == 'debate-memory'
            assert call_args[1]['sessionId'] == session_id
    
    def test_store_response_with_metadata(self):
        """Test that store_response stores correct metadata."""
        with patch('boto3.client') as mock_boto:
            mock_client = Mock()
            mock_boto.return_value = mock_client
            
            manager = MemoryManager()
            session_id = "debate_abc12345_2025-11-30T12:00:00"
            agent_name = "jeff_barr"
            round_num = 2
            content = "Test response content"
            
            manager.store_response(session_id, agent_name, round_num, content)
            
            # Verify API was called with correct parameters
            mock_client.put_memory.assert_called_once()
            call_args = mock_client.put_memory.call_args
            
            assert call_args[1]['memoryId'] == 'debate-memory'
            assert call_args[1]['sessionId'] == session_id
            
            memory_content = call_args[1]['memoryContent']
            assert memory_content['userId'] == agent_name
            assert memory_content['round'] == round_num
            assert memory_content['content'] == content
            assert 'timestamp' in memory_content
    
    def test_get_context_formats_correctly(self):
        """Test that get_context formats memories correctly."""
        with patch('boto3.client') as mock_boto:
            mock_client = Mock()
            mock_boto.return_value = mock_client
            
            # Mock response from get_memory
            mock_client.get_memory.return_value = {
                'memories': [
                    {
                        'userId': 'jeff_barr',
                        'round': 1,
                        'content': 'First response'
                    },
                    {
                        'userId': 'swami',
                        'round': 1,
                        'content': 'Second response'
                    }
                ]
            }
            
            manager = MemoryManager()
            session_id = "debate_abc12345_2025-11-30T12:00:00"
            
            context = manager.get_context(session_id)
            
            # Verify format
            expected = "[jeff_barr - Round 1]: First response\n\n[swami - Round 1]: Second response"
            assert context == expected
            
            # Verify API was called
            mock_client.get_memory.assert_called_once()
            call_args = mock_client.get_memory.call_args
            assert call_args[1]['memoryId'] == 'debate-memory'
            assert call_args[1]['sessionId'] == session_id
            assert call_args[1]['maxResults'] == 50
    
    def test_get_context_empty_memories(self):
        """Test that get_context handles empty memories."""
        with patch('boto3.client') as mock_boto:
            mock_client = Mock()
            mock_boto.return_value = mock_client
            
            mock_client.get_memory.return_value = {'memories': []}
            
            manager = MemoryManager()
            context = manager.get_context("test_session")
            
            assert context == ""
    
    def test_get_full_context_calls_get_context(self):
        """Test that get_full_context delegates to get_context."""
        with patch('boto3.client') as mock_boto:
            mock_client = Mock()
            mock_boto.return_value = mock_client
            
            mock_client.get_memory.return_value = {
                'memories': [
                    {'userId': 'jeff_barr', 'round': 1, 'content': 'Test'}
                ]
            }
            
            manager = MemoryManager()
            session_id = "test_session"
            
            full_context = manager.get_full_context(session_id)
            context = manager.get_context(session_id)
            
            assert full_context == context
    
    def test_retry_logic_success_on_second_attempt(self):
        """Test that retry logic succeeds on second attempt."""
        with patch('boto3.client') as mock_boto:
            mock_client = Mock()
            mock_boto.return_value = mock_client
            
            # Fail first time, succeed second time
            mock_client.create_memory_session.side_effect = [
                Exception("Transient error"),
                None
            ]
            
            manager = MemoryManager()
            
            # Should succeed after retry
            with patch('time.sleep'):  # Mock sleep to speed up test
                session_id = manager.create_session("Test problem")
            
            assert session_id.startswith('debate_')
            assert mock_client.create_memory_session.call_count == 2
    
    def test_retry_logic_fails_after_max_retries(self):
        """Test that retry logic raises exception after max retries."""
        with patch('boto3.client') as mock_boto:
            mock_client = Mock()
            mock_boto.return_value = mock_client
            
            # Always fail
            mock_client.create_memory_session.side_effect = Exception("Persistent error")
            
            manager = MemoryManager()
            
            # Should raise exception after 3 retries
            with patch('time.sleep'):  # Mock sleep to speed up test
                with pytest.raises(Exception, match="Persistent error"):
                    manager.create_session("Test problem")
            
            assert mock_client.create_memory_session.call_count == 3
    
    def test_store_response_retry_logic(self):
        """Test that store_response has retry logic."""
        with patch('boto3.client') as mock_boto:
            mock_client = Mock()
            mock_boto.return_value = mock_client
            
            # Fail first time, succeed second time
            mock_client.put_memory.side_effect = [
                Exception("Transient error"),
                None
            ]
            
            manager = MemoryManager()
            
            # Should succeed after retry
            with patch('time.sleep'):
                manager.store_response("session", "jeff_barr", 1, "content")
            
            assert mock_client.put_memory.call_count == 2
    
    def test_get_context_retry_logic(self):
        """Test that get_context has retry logic."""
        with patch('boto3.client') as mock_boto:
            mock_client = Mock()
            mock_boto.return_value = mock_client
            
            # Fail first time, succeed second time
            mock_client.get_memory.side_effect = [
                Exception("Transient error"),
                {'memories': []}
            ]
            
            manager = MemoryManager()
            
            # Should succeed after retry
            with patch('time.sleep'):
                context = manager.get_context("session")
            
            assert context == ""
            assert mock_client.get_memory.call_count == 2


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
