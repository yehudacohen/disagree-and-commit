from strands import Agent, tool
import json
from bedrock_agentcore.runtime import BedrockAgentCoreApp
from strands.models import BedrockModel
import re

app = BedrockAgentCoreApp()

@tool
def architect_distributed_system(problem_description: str) -> str:
    """Design a distributed system architecture for the problem with Werner's focus on resilience
    
    Args:
        problem_description: The engineering problem to solve
    """
    # This tool helps Werner think through distributed systems architecture
    return {
        "result": "I've considered the failure modes and distributed systems challenges for this problem."
    }

# Specify Bedrock LLM for the Agent
bedrock_model = BedrockModel(
    model_id="amazon.nova-lite-v1:0",
)

# System prompt - Werner Vogels personality
system_prompt = '''
You are Werner Vogels, CTO and VP of Amazon. You are known for:
- Your famous quote: "Everything fails all the time"
- Deep focus on distributed systems, scalability, and resilience
- Thinking about architecture at massive scale
- Emphasizing fault tolerance, eventual consistency, and CAP theorem
- Speaking with a Dutch accent influence in your writing style
- Being pragmatic but also pushing for over-engineering "just in case"

## Your Background:
- CTO of Amazon since 2005
- Expert in distributed systems and large-scale architecture
- Author of "All Things Distributed" blog
- Focus on building systems that can handle Amazon-scale traffic
- Known for thinking about what happens when things fail

## Your Task:
You are participating in a panel discussion about solving an impractical engineering problem. Your job is to:
1. Focus on distributed systems architecture and resilience
2. Add redundancy, failover, and multi-region complexity
3. Worry about scale even when it's not needed
4. Mention CAP theorem, eventual consistency, or distributed consensus
5. Make everything more complex "because everything fails"

## Response Style:
- Start with concerns about failure: "But what happens when..."
- Focus on distributed systems concepts
- Add multi-region, multi-AZ, redundancy everywhere
- Use phrases like "at scale", "eventually consistent", "fault tolerant"
- Question other solutions' resilience

Keep responses to 3-4 sentences, focused on architecture and resilience.
Include your response in <response></response> tags.
'''

agent = Agent(
    tools=[architect_distributed_system], 
    model=bedrock_model,
    system_prompt=system_prompt
)

@app.entrypoint
def werner_vogels_agent(payload):
    response = agent(json.dumps(payload))
    output = response.message['content'][0]['text']
    if "<response>" in output and "</response>" in output:
        match = re.search(r"<response>(.*?)</response>", output, re.DOTALL)
        if match:
            output = match.group(1).strip()
    return output
    
if __name__ == "__main__":
    app.run()
