"""
Orchestration Agent Client for WebSocket Server
Calls the deployed Orchestration Agent on AgentCore Runtime
"""

import boto3
import json
import os
import logging

logger = logging.getLogger(__name__)


class OrchestrationClient:
    """Client for calling Orchestration Agent (Disagree and Commit Panel)"""
    
    def __init__(self, runtime_arn: str = None):
        """
        Initialize Orchestration Client.
        
        Args:
            runtime_arn: AgentCore Runtime ARN for orchestration agent
        """
        self.runtime_arn = runtime_arn or os.getenv("ORCHESTRATION_RUNTIME_ARN")
        self.region = os.getenv("AWS_REGION", "us-east-1")
        
        if not self.runtime_arn:
            logger.warning("ORCHESTRATION_RUNTIME_ARN not set - orchestration agent will not be available")
            self.client = None
        else:
            logger.info(f"Using AgentCore Runtime ARN: {self.runtime_arn}")
            self.client = boto3.client("bedrock-agentcore", region_name=self.region)
    
    async def process_problem(
        self,
        problem_description: str,
        instruction: str = None
    ) -> dict:
        """
        Process engineering problem through Orchestration Agent.
        
        Args:
            problem_description: The engineering problem to solve
            instruction: Optional instruction for the panel
            
        Returns:
            Response with the panel discussion result
        """
        if not self.client:
            return {
                "result": "Orchestration agent not available. Please set ORCHESTRATION_RUNTIME_ARN environment variable.",
                "error": True
            }
        
        try:
            payload = {
                "problem": problem_description,
                "instruction": instruction or "Have the panel discuss this problem and propose an AWS solution"
            }
            
            logger.info(f"Invoking orchestration agent with problem: {problem_description[:100]}...")
            
            response = self.client.invoke_agent_runtime(
                agentRuntimeArn=self.runtime_arn,
                payload=json.dumps(payload, ensure_ascii=False).encode('utf-8')
            )
            
            # Parse response
            if 'response' in response:
                streaming_body = response['response']
                output_bytes = streaming_body.read()
                output = output_bytes.decode('utf-8')
                
                logger.info("Successfully received response from orchestration agent")
                
                return {
                    "result": output,
                    "error": False
                }
            else:
                logger.error(f"Unexpected response format: {response}")
                return {
                    "result": "Unexpected response format from orchestration agent",
                    "error": True
                }
                
        except Exception as e:
            logger.error(f"Failed to call orchestration agent: {e}")
            import traceback
            traceback.print_exc()
            return {
                "result": f"Error calling orchestration agent: {str(e)}",
                "error": True
            }
    
    def process_problem_sync(
        self,
        problem_description: str,
        instruction: str = None
    ) -> dict:
        """
        Synchronous version of process_problem for non-async contexts.
        
        Args:
            problem_description: The engineering problem to solve
            instruction: Optional instruction for the panel
            
        Returns:
            Response with the panel discussion result
        """
        import asyncio
        
        # Create new event loop for sync call
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        try:
            result = loop.run_until_complete(
                self.process_problem(problem_description, instruction)
            )
            return result
        finally:
            loop.close()
