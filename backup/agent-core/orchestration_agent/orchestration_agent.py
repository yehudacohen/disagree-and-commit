from strands import Agent, tool
import json
from bedrock_agentcore.runtime import BedrockAgentCoreApp
from strands.models import BedrockModel
import boto3
import re

app = BedrockAgentCoreApp()

# Initialize AgentCore client
agentcore_client = boto3.client('bedrock-agentcore')

# Agent runtime ARNs - these are set from deployment
JEFF_BARR_ARN = "arn:aws:bedrock-agentcore:us-east-1:383661100299:runtime/ac_jeff_barr_agent-gGYnGD7zXv"
WERNER_VOGELS_ARN = "arn:aws:bedrock-agentcore:us-east-1:383661100299:runtime/ac_werner_vogels_agent-kpbwiD6QZy"
SWAMI_ARN = "arn:aws:bedrock-agentcore:us-east-1:383661100299:runtime/ac_swami_agent-23wHa3348R"

@tool
def call_jeff_barr(problem_description: str, round_number: int) -> str:
    """Call Jeff Barr agent to get his AWS solution proposal
    
    Args:
        problem_description: The engineering problem to solve
        round_number: Which round of discussion (1, 2, or 3)
    """
    try:
        payload = {
            "problem": problem_description,
            "round": round_number,
            "instruction": "Propose an AWS solution for this problem. Make it more complex than the previous round."
        }
        
        response = agentcore_client.invoke_agent_runtime(
            agentRuntimeArn=JEFF_BARR_ARN,
            payload=json.dumps(payload).encode('utf-8')
        )
        
        result = response['response'].read().decode('utf-8')
        return {"result": result}
    except Exception as e:
        return {"result": f"Jeff Barr is currently unavailable: {str(e)}"}

@tool
def call_werner_vogels(problem_description: str, round_number: int, previous_context: str) -> str:
    """Call Werner Vogels agent to critique and add distributed systems complexity
    
    Args:
        problem_description: The engineering problem to solve
        round_number: Which round of discussion (1, 2, or 3)
        previous_context: What Jeff said before
    """
    try:
        payload = {
            "problem": problem_description,
            "round": round_number,
            "previous_proposal": previous_context,
            "instruction": "Critique the previous proposal and add distributed systems complexity, resilience, and multi-region architecture."
        }
        
        response = agentcore_client.invoke_agent_runtime(
            agentRuntimeArn=WERNER_VOGELS_ARN,
            payload=json.dumps(payload).encode('utf-8')
        )
        
        result = response['response'].read().decode('utf-8')
        return {"result": result}
    except Exception as e:
        return {"result": f"Werner Vogels is currently unavailable: {str(e)}"}

@tool
def call_swami(problem_description: str, round_number: int, previous_context: str) -> str:
    """Call Swami agent to add AI/ML capabilities to the solution
    
    Args:
        problem_description: The engineering problem to solve
        round_number: Which round of discussion (1, 2, or 3)
        previous_context: What Werner said before
    """
    try:
        payload = {
            "problem": problem_description,
            "round": round_number,
            "previous_proposal": previous_context,
            "instruction": "Add AI/ML capabilities to make this solution 'intelligent' and 'AI-powered'."
        }
        
        response = agentcore_client.invoke_agent_runtime(
            agentRuntimeArn=SWAMI_ARN,
            payload=json.dumps(payload).encode('utf-8')
        )
        
        result = response['response'].read().decode('utf-8')
        return {"result": result}
    except Exception as e:
        return {"result": f"Swami is currently unavailable: {str(e)}"}

# Specify Bedrock LLM for the Agent
bedrock_model = BedrockModel(
    model_id="amazon.nova-lite-v1:0",
)

# System prompt - Orchestration Agent
system_prompt = '''
You are the Orchestration Agent for the "Disagree and Commit" panel discussion.

Your job is to:
1. Receive an engineering problem from the user
2. Orchestrate a 3-round discussion between Jeff Barr, Werner Vogels, and Swami Sivasubramanian
3. Each round, call the agents in sequence: Jeff → Werner → Swami
4. Each agent builds on the previous agent's proposal, making it MORE complex
5. After 3 rounds, summarize the hilariously over-engineered solution

## Process:
Round 1: Initial proposals (somewhat reasonable)
Round 2: Adding complexity (getting impractical)
Round 3: Maximum complexity (completely unfeasible)

## Your Response Format:
After running all 3 rounds, create a humorous summary that includes:
- A brief recap of the original problem
- Key highlights from each expert's contributions
- A sarcastic comment about the final architecture's complexity
- The conclusion: "They disagreed, but committed to this beautiful disaster"

Use the tools to call each agent in sequence. Pass the previous agent's response as context to the next agent.

Keep your final summary entertaining, sarcastic, and highlighting the absurdity of the over-engineered solution.
Include your response in <response></response> tags.
'''

agent = Agent(
    tools=[call_jeff_barr, call_werner_vogels, call_swami], 
    model=bedrock_model,
    system_prompt=system_prompt
)

@app.entrypoint
def orchestration_agent(payload):
    """
    Main entry point for the orchestration agent.
    Receives a problem description and orchestrates the panel discussion.
    """
    response = agent(json.dumps(payload))
    output = response.message['content'][0]['text']
    if "<response>" in output and "</response>" in output:
        match = re.search(r"<response>(.*?)</response>", output, re.DOTALL)
        if match:
            output = match.group(1).strip()
    return output
    
if __name__ == "__main__":
    app.run()
