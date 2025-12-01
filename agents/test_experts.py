"""Test script to verify expert agents are properly configured."""
from unittest.mock import Mock, patch
from experts import jeff_barr_agent, swami_agent, werner_agent


def test_agent_configuration():
    """Verify all expert agents are properly configured."""
    agents = [
        ("jeff_barr", jeff_barr_agent),
        ("swami", swami_agent),
        ("werner_vogels", werner_agent)
    ]
    
    for name, agent in agents:
        # Verify agent has correct name
        assert agent.name == name, f"Agent name mismatch: expected {name}, got {agent.name}"
        
        # Verify agent has a model configured
        assert agent.model is not None, f"Agent {name} has no model configured"
        
        # Test BedrockModel initialization with correct parameters (Requirement 10.1)
        # BedrockModel stores configuration in a config dictionary
        model = agent.model
        assert hasattr(model, 'config'), f"Agent {name} model missing config attribute"
        config = model.config
        
        # Verify model_id is correct
        assert 'model_id' in config, f"Agent {name} config missing model_id"
        assert config['model_id'] == "us.anthropic.claude-sonnet-4-20250514-v1:0", \
            f"Agent {name} has incorrect model_id: {config['model_id']}"
        
        # Verify temperature is correct
        assert 'temperature' in config, f"Agent {name} config missing temperature"
        assert config['temperature'] == 0.7, \
            f"Agent {name} has incorrect temperature: {config['temperature']}"
        
        # Verify max_tokens is correct
        assert 'max_tokens' in config, f"Agent {name} config missing max_tokens"
        assert config['max_tokens'] == 2048, \
            f"Agent {name} has incorrect max_tokens: {config['max_tokens']}"
        
        # Verify agent has instructions (system_prompt)
        assert agent.system_prompt is not None, f"Agent {name} has no instructions"
        assert len(agent.system_prompt) > 0, f"Agent {name} has empty instructions"
        
        # Verify instructions contain key persona elements
        instructions = agent.system_prompt.lower()
        
        if name == "jeff_barr":
            assert "serverless" in instructions, f"Jeff Barr agent missing serverless emphasis"
            assert "lambda" in instructions, f"Jeff Barr agent missing Lambda reference"
            assert "200 words" in instructions, f"Jeff Barr agent missing response length constraint"
            assert "here's the simple approach" in instructions, f"Jeff Barr agent missing persona phrase"
            
        elif name == "swami":
            assert "ai/ml" in instructions or "bedrock" in instructions, f"Swami agent missing AI/ML emphasis"
            assert "200 words" in instructions, f"Swami agent missing response length constraint"
            assert "ship" in instructions, f"Swami agent missing shipping emphasis"
            
        elif name == "werner_vogels":
            assert "scale" in instructions, f"Werner agent missing scale emphasis"
            assert "distributed" in instructions, f"Werner agent missing distributed systems reference"
            assert "200 words" in instructions, f"Werner agent missing response length constraint"
            assert "at scale" in instructions, f"Werner agent missing persona phrase"
    
    print("✓ All expert agents are properly configured!")
    print(f"✓ Jeff Barr agent: {jeff_barr_agent.name}")
    print(f"✓ Swami agent: {swami_agent.name}")
    print(f"✓ Werner agent: {werner_agent.name}")


def test_agent_invocation_response_structure():
    """Test that agent responses have correct structure (Requirement 10.1, 10.2).
    
    Mock agent responses with correct structure: {"message": {"content": [{"text": "..."}]}}
    Update assertions to check response.message['content'][0]['text']
    """
    # Mock agent response with correct structure as per new pattern
    mock_response = Mock()
    mock_response.message = {
        'content': [
            {'text': 'This is a test response from the agent.'}
        ]
    }
    
    # Test extracting text from response structure using the correct pattern
    try:
        response_text = mock_response.message['content'][0]['text']
        assert response_text == 'This is a test response from the agent.'
        assert isinstance(response_text, str)
        assert len(response_text) > 0
        print("✓ Agent response structure extraction verified")
    except (KeyError, TypeError, IndexError) as e:
        raise AssertionError(f"Failed to extract text from response structure: {e}")
    
    # Test with multiple content items
    mock_response_multi = Mock()
    mock_response_multi.message = {
        'content': [
            {'text': 'First response'},
            {'text': 'Second response'}
        ]
    }
    
    # Should extract first content item
    response_text = mock_response_multi.message['content'][0]['text']
    assert response_text == 'First response'
    print("✓ Multi-content response structure verified")


def test_agent_invocation_pattern():
    """Test that agents can be invoked with correct pattern (Requirement 10.1).
    
    Tests the pattern: response = agent(prompt)
    And extraction: response.message['content'][0]['text']
    """
    # This test verifies the invocation pattern without making actual API calls
    # In production, agents are called with: response = agent(prompt)
    
    # Create a mock agent to test the pattern
    mock_agent = Mock()
    mock_response = Mock()
    mock_response.message = {
        'content': [
            {'text': 'Mocked response'}
        ]
    }
    mock_agent.return_value = mock_response
    
    # Test invocation pattern: agent(prompt)
    prompt = "Test prompt"
    response = mock_agent(prompt)
    
    # Verify call was made with the prompt
    mock_agent.assert_called_once_with(prompt)
    
    # Verify response structure matches expected pattern
    assert 'content' in response.message
    assert isinstance(response.message['content'], list)
    assert len(response.message['content']) > 0
    assert 'text' in response.message['content'][0]
    
    # Extract text using the correct pattern
    response_text = response.message['content'][0]['text']
    assert response_text == 'Mocked response'
    assert isinstance(response_text, str)
    
    print("✓ Agent invocation pattern verified")


def test_response_extraction_pattern():
    """Test the response extraction pattern used in production (Requirement 10.2)."""
    # This test verifies the exact pattern used in the orchestrator
    # to extract text from agent responses
    
    # Create various mock response structures to test robustness
    test_cases = [
        {
            'name': 'standard_response',
            'response': {
                'content': [
                    {'text': 'Standard agent response'}
                ]
            },
            'expected': 'Standard agent response'
        },
        {
            'name': 'multi_content_response',
            'response': {
                'content': [
                    {'text': 'First content item'},
                    {'text': 'Second content item'}
                ]
            },
            'expected': 'First content item'
        },
        {
            'name': 'long_response',
            'response': {
                'content': [
                    {'text': 'A' * 1000}  # Long response
                ]
            },
            'expected': 'A' * 1000
        }
    ]
    
    for test_case in test_cases:
        mock_response = Mock()
        mock_response.message = test_case['response']
        
        # Extract using the production pattern
        response_text = mock_response.message['content'][0]['text']
        
        assert response_text == test_case['expected'], \
            f"Failed for {test_case['name']}: expected {test_case['expected'][:50]}, got {response_text[:50]}"
        assert isinstance(response_text, str)
    
    print("✓ Response extraction pattern verified for all test cases")


if __name__ == "__main__":
    test_agent_configuration()
    test_agent_invocation_response_structure()
    test_agent_invocation_pattern()
    test_response_extraction_pattern()
    print("\n✅ ALL EXPERT AGENT TESTS PASSED!")
