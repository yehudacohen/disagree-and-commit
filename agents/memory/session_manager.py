import boto3
import json
import logging
from datetime import datetime
import hashlib
import time
from typing import Optional, Callable, Any

# Get logger instance for this module
logger = logging.getLogger(__name__)


class MemoryManager:
    """
    Manages AgentCore Memory operations for debate sessions.
    
    Provides session creation, response storage, and context retrieval
    with automatic retry logic for resilience against transient failures.
    """
    
    def __init__(self, memory_id: Optional[str] = None, region: str = 'us-east-1'):
        """
        Initialize the MemoryManager.
        
        Args:
            memory_id: The AgentCore Memory resource ID. Defaults to 'debate-memory'.
            region: AWS region for the bedrock-agent-runtime client. Defaults to 'us-east-1'.
        """
        self.client = boto3.client('bedrock-agent-runtime', region_name=region)
        self.memory_id = memory_id or 'debate-memory'
        self.region = region
        self.max_retries = 3
        self.base_delay = 1.0
        self.max_delay = 10.0
        logger.info(f"MemoryManager initialized with memory_id={self.memory_id}, region={region}")
    
    def _retry_with_backoff(self, func: Callable, *args, **kwargs) -> Any:
        """
        Execute a function with exponential backoff retry logic.
        
        Args:
            func: The function to execute
            *args: Positional arguments for the function
            **kwargs: Keyword arguments for the function
        
        Returns:
            The result of the function call
        
        Raises:
            Exception: If all retry attempts fail
        """
        last_exception = None
        
        for attempt in range(self.max_retries):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                last_exception = e
                if attempt == self.max_retries - 1:
                    raise
                
                # Calculate exponential backoff delay
                delay = min(
                    self.base_delay * (2 ** attempt),
                    self.max_delay
                )
                time.sleep(delay)
        
        # This should never be reached, but just in case
        if last_exception:
            raise last_exception
    
    def create_session(self, problem: str, actor_id: str) -> str:
        """
        Create a new memory session for a debate.
        
        Sessions in AgentCore Memory are implicit - they are created automatically
        when the first event is stored. This method generates a valid session ID
        that meets the minimum length requirement (33 characters).
        
        Args:
            problem: The problem statement
            actor_id: The actor identifier for this session
        
        Returns:
            Session ID in format: debate_{8-char-hash}_{ISO8601-timestamp}
            Guaranteed to be at least 33 characters long.
        
        Raises:
            Exception: If session ID generation fails
        """
        timestamp = datetime.utcnow().isoformat()
        problem_hash = hashlib.md5(problem.encode()).hexdigest()[:8]
        session_id = f"debate_{problem_hash}_{timestamp}"
        
        # Ensure minimum 33 character length for AgentCore Memory
        if len(session_id) < 33:
            # Pad with additional hash characters if needed
            padding = hashlib.md5(f"{problem}{timestamp}".encode()).hexdigest()
            session_id = f"{session_id}_{padding}"[:33]
        
        logger.info(f"Created session ID: {session_id} (length: {len(session_id)}) for actor: {actor_id}")
        
        # Sessions are implicit in AgentCore Memory - no API call needed
        return session_id
    
    def store_response(
        self, 
        session_id: str, 
        actor_id: str, 
        round_num: int, 
        content: str
    ) -> None:
        """
        Store an expert's response to memory using create_event API with retry logic.
        
        Args:
            session_id: The debate session ID
            actor_id: Expert identifier (jeff_barr, swami, werner_vogels)
            round_num: Round number (1-3)
            content: The expert's response text
        
        Raises:
            Exception: If storage fails after all retries
        """
        def _store():
            try:
                # Format messages as required by create_event API
                messages = [
                    {
                        "role": "USER",
                        "text": f"Round {round_num} prompt"
                    },
                    {
                        "role": "ASSISTANT",
                        "text": content
                    }
                ]
                
                response = self.client.create_event(
                    memoryId=self.memory_id,
                    actorId=actor_id,
                    sessionId=session_id,
                    messages=messages
                )
                
                logger.info(f"Stored response for actor={actor_id}, session={session_id}, round={round_num}")
                return response
                
            except Exception as e:
                logger.error(f"Error storing response for actor={actor_id}, session={session_id}: {e}")
                raise
        
        self._retry_with_backoff(_store)
    
    def get_context(self, session_id: str, actor_id: str) -> str:
        """
        Retrieve all previous responses for context using retrieve_memory API with retry logic.
        
        Args:
            session_id: The debate session ID
            actor_id: The actor identifier for filtering memories
        
        Returns:
            Formatted string with all previous responses in chronological order
        
        Raises:
            Exception: If retrieval fails after all retries
        """
        def _get():
            try:
                response = self.client.retrieve_memory(
                    memoryId=self.memory_id,
                    actorId=actor_id,
                    sessionId=session_id,
                    maxResults=50
                )
                
                logger.info(f"Retrieved context for actor={actor_id}, session={session_id}")
                return response
                
            except Exception as e:
                logger.error(f"Error retrieving context for actor={actor_id}, session={session_id}: {e}")
                raise
        
        response = self._retry_with_backoff(_get)
        
        # Extract text from the content structure
        memories = response.get('memories', [])
        context_parts = []
        
        for memory in memories:
            try:
                # Extract text from content structure
                content = memory.get('content', {})
                if isinstance(content, dict):
                    text = content.get('text', '')
                else:
                    text = str(content)
                
                if text:
                    context_parts.append(text)
            except Exception as e:
                logger.warning(f"Error parsing memory content: {e}")
                continue
        
        context = "\n\n".join(context_parts)
        return context
    
    def get_full_context(self, session_id: str, actor_id: str) -> str:
        """
        Retrieve complete debate history for synthesis using retrieve_memory API.
        
        This method retrieves all memories for the session to provide a complete
        debate transcript for synthesis.
        
        Args:
            session_id: The debate session ID
            actor_id: The actor identifier for filtering memories
        
        Returns:
            Complete formatted debate transcript
        
        Raises:
            Exception: If retrieval fails after all retries
        """
        def _get_all():
            try:
                # Retrieve all memories for the session
                response = self.client.retrieve_memory(
                    memoryId=self.memory_id,
                    actorId=actor_id,
                    sessionId=session_id,
                    maxResults=100  # Increased limit for complete context
                )
                
                logger.info(f"Retrieved full context for actor={actor_id}, session={session_id}")
                return response
                
            except Exception as e:
                logger.error(f"Error retrieving full context for actor={actor_id}, session={session_id}: {e}")
                raise
        
        response = self._retry_with_backoff(_get_all)
        
        # Extract and format complete debate transcript
        memories = response.get('memories', [])
        transcript_parts = []
        
        for memory in memories:
            try:
                # Extract text from content structure
                content = memory.get('content', {})
                if isinstance(content, dict):
                    text = content.get('text', '')
                else:
                    text = str(content)
                
                if text:
                    transcript_parts.append(text)
            except Exception as e:
                logger.warning(f"Error parsing memory content in full context: {e}")
                continue
        
        transcript = "\n\n".join(transcript_parts)
        return transcript
