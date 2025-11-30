"""Test script to verify expert agents are properly configured."""
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


if __name__ == "__main__":
    test_agent_configuration()
