"""
Supervisor Agent Client for WebSocket Server
Calls the deployed Supervisor Agent on AgentCore Runtime
"""

import boto3
import json
import os
import logging

logger = logging.getLogger(__name__)


class SupervisorClient:
    """Client for calling Supervisor Agent"""
    
    def __init__(self, endpoint_url: str = None):
        """
        Initialize Supervisor Client.
        
        Args:
            endpoint_url: AgentCore Runtime endpoint URL for supervisor agent
        """
        self.endpoint_url = endpoint_url or os.getenv("SUPERVISOR_ENDPOINT")
        self.region = os.getenv("AWS_REGION", "us-east-1")
        
        # For local development, import directly
        self.local_mode = not self.endpoint_url
        
        if self.local_mode:
            logger.info("Running in local mode - importing supervisor directly")
            try:
                import sys
                sys.path.append(os.path.join(os.path.dirname(__file__), '../../agents'))
                from supervisor import supervisor_entrypoint
                self.supervisor_entrypoint = supervisor_entrypoint
            except ImportError as e:
                logger.error(f"Failed to import supervisor: {e}")
                self.supervisor_entrypoint = None
        else:
            logger.info(f"Using AgentCore endpoint: {self.endpoint_url}")
            self.client = boto3.client("bedrock-agentcore", region_name=self.region)
    
    async def process_input(
        self,
        user_input: str,
        session_id: str,
        user_profile: dict = None
    ) -> dict:
        """
        Process user input through Supervisor Agent.
        
        Args:
            user_input: User's message
            session_id: Session identifier
            user_profile: Current user profile
            
        Returns:
            Combined response with text, image, and gamification
        """
        if self.local_mode:
            # Local development mode
            if self.supervisor_entrypoint:
                payload = {
                    "prompt": user_input,
                    "session_id": session_id,
                    "user_profile": user_profile or {"total_xp": 0, "level": 1, "badges": []}
                }
                return self.supervisor_entrypoint(payload)
            else:
                return {
                    "text": "Supervisor agent not available",
                    "image": None,
                    "gamification": {
                        "xp_gained": 0,
                        "total_xp": 0,
                        "level": 1,
                        "message": "System initializing..."
                    }
                }
        else:
            # Production mode - call AgentCore endpoint
            try:
                payload = {
                    "prompt": user_input,
                    "session_id": session_id,
                    "user_profile": user_profile or {"total_xp": 0, "level": 1, "badges": []}
                }
                
                # Extract ARN from endpoint (endpoint format: arn:.../runtime-endpoint/DEFAULT)
                agent_runtime_arn = self.endpoint_url.rsplit('/runtime-endpoint/', 1)[0]
                
                response = self.client.invoke_agent_runtime(
                    agentRuntimeArn=agent_runtime_arn,
                    payload=json.dumps(payload).encode('utf-8'),
                    contentType="application/json"
                )
                
                # Parse response
                response_body = json.loads(response["body"].read())
                return response_body
                
            except Exception as e:
                logger.error(f"Failed to call supervisor agent: {e}")
                import traceback
                traceback.print_exc()
                return {
                    "text": "I'm having trouble processing that right now. Please try again.",
                    "image_url": None,
                    "gamification": {
                        "xp_gained": 0,
                        "total_xp": user_profile.get("total_xp", 0) if user_profile else 0,
                        "level": user_profile.get("level", 1) if user_profile else 1,
                        "message": "Connection issue"
                    }
                }
