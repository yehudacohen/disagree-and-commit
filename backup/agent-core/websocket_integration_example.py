"""
Example integration of Disagree and Commit panel with WebSocket server

This shows how to integrate the orchestration agent with your Nova Sonic WebSocket server.
"""

import boto3
import json
from typing import Dict, Any

class DisagreeAndCommitPanel:
    """
    Handler for the Disagree and Commit panel discussion
    """
    
    def __init__(self, region: str = "us-east-1"):
        """
        Initialize the panel handler
        
        Args:
            region: AWS region where agents are deployed
        """
        self.agentcore_client = boto3.client('bedrock-agent-runtime', region_name=region)
        self.orchestration_agent_name = 'ac_orchestration_agent'
    
    def start_discussion(self, problem: str) -> str:
        """
        Start a panel discussion about the given problem
        
        Args:
            problem: The engineering problem to solve
            
        Returns:
            The panel's discussion summary
        """
        payload = {
            "problem": problem,
            "instruction": "Have the panel discuss this problem and propose an AWS solution. Run 3 rounds of discussion."
        }
        
        try:
            response = self.agentcore_client.invoke_agent(
                agentName=self.orchestration_agent_name,
                inputText=json.dumps(payload)
            )
            
            return response.get('output', 'Panel discussion failed to generate output')
            
        except Exception as e:
            return f"Error starting panel discussion: {str(e)}"
    
    def format_for_voice(self, discussion_result: str) -> str:
        """
        Format the panel discussion result for voice output
        
        Args:
            discussion_result: The raw discussion result
            
        Returns:
            A voice-friendly version of the result
        """
        # For voice, we might want to shorten or summarize the result
        # This is a simple example - you can make it more sophisticated
        
        if len(discussion_result) > 500:
            # Truncate long responses for voice
            return discussion_result[:500] + "... The panel had much more to say, but I'll spare you the details!"
        
        return discussion_result


# Example usage in your WebSocket server
def handle_nova_sonic_message(message: Dict[str, Any]) -> str:
    """
    Example handler for Nova Sonic messages
    
    Args:
        message: The message from Nova Sonic
        
    Returns:
        Response to send back to Nova Sonic
    """
    # Initialize the panel
    panel = DisagreeAndCommitPanel(region="us-east-1")
    
    # Extract the problem from the message
    # This depends on your message format
    problem = message.get('problem') or message.get('text') or message.get('query')
    
    if not problem:
        return "Please provide an engineering problem for the panel to discuss."
    
    # Start the discussion
    print(f"Starting panel discussion for: {problem}")
    result = panel.start_discussion(problem)
    
    # Format for voice if needed
    voice_result = panel.format_for_voice(result)
    
    return voice_result


# Example WebSocket event handler
async def on_nova_sonic_tool_use(event: Dict[str, Any]):
    """
    Example handler for Nova Sonic tool use events
    
    This would be integrated into your existing WebSocket server
    """
    tool_name = event.get('toolName')
    
    if tool_name == 'disagree_and_commit_panel':
        # Extract parameters
        tool_input = event.get('toolInput', {})
        problem = tool_input.get('problem')
        
        # Initialize panel
        panel = DisagreeAndCommitPanel()
        
        # Get discussion result
        result = panel.start_discussion(problem)
        
        # Return tool result
        return {
            'toolUseId': event.get('toolUseId'),
            'content': [
                {
                    'text': result
                }
            ]
        }


# Example tool definition for Nova Sonic
DISAGREE_AND_COMMIT_TOOL = {
    "toolSpec": {
        "name": "disagree_and_commit_panel",
        "description": "Consult a panel of AWS experts (Jeff Barr, Werner Vogels, and Swami Sivasubramanian) who will debate how to solve an engineering problem in increasingly complex ways. Use this when the user wants creative (and humorous) AWS architecture suggestions.",
        "inputSchema": {
            "json": {
                "type": "object",
                "properties": {
                    "problem": {
                        "type": "string",
                        "description": "The engineering problem or project idea to discuss"
                    }
                },
                "required": ["problem"]
            }
        }
    }
}


if __name__ == "__main__":
    # Simple test
    panel = DisagreeAndCommitPanel()
    
    test_problem = "How can we build a simple to-do list app?"
    print(f"Testing with problem: {test_problem}\n")
    
    result = panel.start_discussion(test_problem)
    print("Panel Discussion Result:")
    print("=" * 60)
    print(result)
    print("=" * 60)
