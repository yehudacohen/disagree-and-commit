import boto3
import json
from datetime import datetime
import hashlib

class MemoryManager:
    def __init__(self):
        self.client = boto3.client('bedrock-agent-runtime')
        self.memory_id = 'debate-memory'
    
    def create_session(self, problem):
        timestamp = datetime.utcnow().isoformat()
        problem_hash = hashlib.md5(problem.encode()).hexdigest()[:8]
        session_id = f"debate_{problem_hash}_{timestamp}"
        
        self.client.create_memory_session(
            memoryId=self.memory_id,
            sessionId=session_id
        )
        
        return session_id
    
    def store_response(self, session_id, agent_name, round_num, content):
        self.client.put_memory(
            memoryId=self.memory_id,
            sessionId=session_id,
            memoryContent={
                'userId': agent_name,
                'round': round_num,
                'content': content,
                'timestamp': datetime.utcnow().isoformat()
            }
        )
    
    def get_context(self, session_id):
        response = self.client.get_memory(
            memoryId=self.memory_id,
            sessionId=session_id,
            maxResults=50
        )
        
        memories = response.get('memories', [])
        context = "\n\n".join([
            f"[{m['userId']} - Round {m['round']}]: {m['content']}"
            for m in memories
        ])
        
        return context
    
    def get_full_context(self, session_id):
        return self.get_context(session_id)
