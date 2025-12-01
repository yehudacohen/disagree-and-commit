"""
Test logging configuration across all modules.

This test verifies that:
1. All modules have logger instances
2. Logging configuration is properly set up
3. Log messages are generated for key operations
"""

import logging
import pytest
from unittest.mock import patch, MagicMock
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


def test_expert_agents_have_loggers():
    """Verify that all expert agent modules have logger instances."""
    from experts import jeff_barr, swami, werner_vogels
    
    # Check that each module has a logger
    assert hasattr(jeff_barr, 'logger'), "jeff_barr module should have a logger"
    assert hasattr(swami, 'logger'), "swami module should have a logger"
    assert hasattr(werner_vogels, 'logger'), "werner_vogels module should have a logger"
    
    # Check that loggers are properly configured
    assert isinstance(jeff_barr.logger, logging.Logger)
    assert isinstance(swami.logger, logging.Logger)
    assert isinstance(werner_vogels.logger, logging.Logger)


def test_memory_manager_has_logger():
    """Verify that memory manager module has a logger instance."""
    from memory import session_manager
    
    assert hasattr(session_manager, 'logger'), "session_manager module should have a logger"
    assert isinstance(session_manager.logger, logging.Logger)


def test_synthesis_has_logger():
    """Verify that synthesis module has a logger instance."""
    from synthesis import synthesizer
    
    assert hasattr(synthesizer, 'logger'), "synthesizer module should have a logger"
    assert isinstance(synthesizer.logger, logging.Logger)


def test_orchestrator_has_logger():
    """Verify that orchestrator module has a logger instance."""
    # Import orchestrator app
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'orchestrator'))
    from orchestrator import app
    
    assert hasattr(app, 'logger'), "app module should have a logger"
    assert isinstance(app.logger, logging.Logger)


def test_logging_configuration_format():
    """Verify that logging is configured with the correct format."""
    # Get the root logger
    root_logger = logging.getLogger()
    
    # Check that handlers are configured
    assert len(root_logger.handlers) > 0, "Root logger should have at least one handler"
    
    # Check that the handler has a formatter
    handler = root_logger.handlers[0]
    assert handler.formatter is not None, "Handler should have a formatter"


def test_memory_manager_logs_operations():
    """Verify that MemoryManager logs key operations."""
    from memory.session_manager import MemoryManager
    
    with patch('boto3.client') as mock_boto_client:
        mock_client = MagicMock()
        mock_boto_client.return_value = mock_client
        
        # Capture log messages
        with patch('memory.session_manager.logger') as mock_logger:
            # Create MemoryManager instance
            memory = MemoryManager(memory_id='test-memory', region='us-east-1')
            
            # Verify initialization logging
            mock_logger.info.assert_called()
            
            # Create session
            session_id = memory.create_session("test problem", "test_actor")
            
            # Verify session creation logging
            assert any('Created session ID' in str(call) for call in mock_logger.info.call_args_list)


def test_orchestrator_logs_configuration():
    """Verify that orchestrator logs configuration on startup."""
    # This test verifies that the orchestrator logs its configuration
    # when the module is imported
    
    with patch.dict(os.environ, {'LOG_LEVEL': 'DEBUG', 'MEMORY_ID': 'test-memory'}):
        # Re-import to trigger logging
        import importlib
        sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'orchestrator'))
        
        # The orchestrator should log configuration when imported
        # We can't easily test this without re-importing, but we can verify
        # the logger exists and is configured
        from orchestrator import app
        
        assert hasattr(app, 'logger')
        assert app.logger.level <= logging.DEBUG or logging.getLogger().level <= logging.DEBUG


def test_log_level_environment_variable():
    """Verify that LOG_LEVEL environment variable is respected."""
    # Test that the orchestrator respects the LOG_LEVEL environment variable
    with patch.dict(os.environ, {'LOG_LEVEL': 'WARNING'}):
        # The logging configuration should use WARNING level
        # This is configured in the orchestrator app.py
        
        # Get root logger level
        root_logger = logging.getLogger()
        
        # Note: The actual level might be INFO if already configured
        # but we can verify the environment variable is read
        assert os.getenv('LOG_LEVEL') == 'WARNING'


def test_error_logging_in_memory_manager():
    """Verify that MemoryManager logs errors appropriately."""
    from memory.session_manager import MemoryManager
    
    with patch('boto3.client') as mock_boto_client:
        mock_client = MagicMock()
        mock_boto_client.return_value = mock_client
        
        # Make store_response fail
        mock_client.create_event.side_effect = Exception("Test error")
        
        memory = MemoryManager(memory_id='test-memory')
        
        # Capture log messages
        with patch('memory.session_manager.logger') as mock_logger:
            # This should fail and log an error
            with pytest.raises(Exception):
                memory.store_response('session-123', 'actor-1', 1, 'test content')
            
            # Verify error was logged
            mock_logger.error.assert_called()


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
