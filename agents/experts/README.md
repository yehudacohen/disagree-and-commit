# Expert Agents

This module contains three expert agents built using the Strands framework for the Disagree and Commit debate system.

## Agents

### Jeff Barr Agent (`jeff_barr.py`)
- **Name**: jeff_barr
- **Model**: Claude Sonnet 4.1 (anthropic.claude-sonnet-4-v1)
- **Persona**: AWS evangelist and simplicity advocate
- **Focus**: Serverless solutions (Lambda, Step Functions, EventBridge)
- **Signature Phrase**: "Here's the simple approach..."
- **Response Length**: ~200 words (1 minute speaking time)

### Swami Agent (`swami.py`)
- **Name**: swami
- **Model**: Claude Sonnet 4.1 (anthropic.claude-sonnet-4-v1)
- **Persona**: AWS AI/ML VP and shipping advocate
- **Focus**: AI/ML solutions (Bedrock, SageMaker), rapid deployment
- **Signature Phrase**: "We can ship this in weeks..."
- **Response Length**: ~200 words (1 minute speaking time)

### Werner Agent (`werner_vogels.py`)
- **Name**: werner_vogels
- **Model**: Claude Sonnet 4.1 (anthropic.claude-sonnet-4-v1)
- **Persona**: AWS CTO and scale architect
- **Focus**: Distributed systems, fault tolerance, scale
- **Signature Phrase**: "At scale, we need..."
- **Response Length**: ~200 words (1 minute speaking time)

## Usage

```python
from experts import jeff_barr_agent, swami_agent, werner_agent

# Invoke an agent with a prompt
result = jeff_barr_agent("How should we build a serverless API?")
print(result.message)
```

## Requirements Validation

All agents meet the following requirements:
- ✅ Built using Strands Agent framework
- ✅ Configured with Claude Sonnet 4.1 model
- ✅ Persona-specific instructions (~200 word responses)
- ✅ Designed to reference previous context in responses
- ✅ Distinct personality traits and technical biases
- ✅ Characteristic opening phrases for persona consistency

## Testing

Run the test suite to verify agent configuration:

```bash
python agents/test_experts.py
```

This validates:
- Agent names are correctly set
- Models are properly configured
- System prompts contain required persona elements
- Response length constraints are specified
- Signature phrases are present
