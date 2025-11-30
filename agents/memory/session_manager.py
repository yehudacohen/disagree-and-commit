import boto3
import json
from datetime import datetime
import hashlib
import time
from typing import Optional, Callable, Any


class MemoryManager:
    """
    Manages AgentCore Memory operations for debate sessions.
    
    Provides session creation, response storage, and context retrieval
    with automatic retry logic for resilience against transient failures.
    """
    
    def __init__(self, memory_id: Optional[str] = None):
        """
        Initialize the MemoryManager.
        
        Args:
            memory_id: The AgentCore Memory resource ID. Defaults to 'debate-memory'.
        """
        self.client = boto3.client('bedrock-agent-runtime')
        self.memory_id = memory_id or 'debate-memory'
        self.max_retries = 3
        self.base_delay = 1.0
        self.max_delay = 10.0
    
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
    
    def create_session(self, problem: str) -> str:
        """
        Create a new memory session for a debate.
        
        Args:
            problem: The problem statement
        
        Returns:
            Session ID in format: debate_{8-char-hash}_{ISO8601-timestamp}
        
        Raises:
            Exception: If session creation fails after all retries
        """
        timestamp = datetime.utcnow().isoformat()
        problem_hash = hashlib.md5(problem.encode()).hexdigest()[:8]
        session_id = f"debate_{problem_hash}_{timestamp}"
        
        def _create():
            return self.client.create_memory_session(
                memoryId=self.memory_id,
                sessionId=session_id
            )
        
        self._retry_with_backoff(_create)
        
        return session_id
    
    def store_response(
        self, 
        session_id: str, 
        agent_name: str, 
        round_num: int, 
        content: str
    ) -> None:
        """
        Store an expert's response to memory with retry logic.
        
        Args:
            session_id: The debate session ID
            agent_name: Expert identifier (jeff_barr, swami, werner_vogels)
            round_num: Round number (1-3)
            content: The expert's response text
        
        Raises:
            Exception: If storage fails after all retries
        """
        def _store():
            return self.client.put_memory(
                memoryId=self.memory_id,
                sessionId=session_id,
                memoryContent={
                    'userId': agent_name,
                    'round': round_num,
                    'content': content,
                    'timestamp': datetime.utcnow().isoformat()
                }
            )
        
        self._retry_with_backoff(_store)
    
    def get_context(self, session_id: str) -> str:
        """
        Retrieve all previous responses for context with retry logic.
        
        Args:
            session_id: The debate session ID
        
        Returns:
            Formatted string with all previous responses in chronological order
        
        Raises:
            Exception: If retrieval fails after all retries
        """
        def _get():
            return self.client.get_memory(
                memoryId=self.memory_id,
                sessionId=session_id,
                maxResults=50
            )
        
        response = self._retry_with_backoff(_get)
        
        memories = response.get('memories', [])
        context = "\n\n".join([
            f"[{m['userId']} - Round {m['round']}]: {m['content']}"
            for m in memories
        ])
        
        return context
    
    def get_full_context(self, session_id: str) -> str:
        """
        Retrieve complete debate history for synthesis.
        
        Args:
            session_id: The debate session ID
        
        Returns:
            Complete formatted debate transcript
        
        Raises:
            Exception: If retrieval fails after all retries
        """
        return self.get_context(session_id)
