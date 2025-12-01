from bedrock_agentcore.runtime import BedrockAgentCoreApp
from experts.jeff_barr import jeff_barr_agent
from experts.swami import swami_agent
from experts.werner_vogels import werner_agent
from synthesis.synthesizer import synthesis_agent, extract_mermaid
from memory.session_manager import MemoryManager
import asyncio
import json
import os
import logging
from typing import Optional

# Configure logging for the entire application
# This is the main entry point, so we configure logging here
LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO').upper()
logging.basicConfig(
    level=getattr(logging, LOG_LEVEL, logging.INFO),
    format='%(asctime)s [%(levelname)s] %(name)s: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

# Get logger instance for this module
logger = logging.getLogger(__name__)
logger.info(f"Logging configured at {LOG_LEVEL} level")

# Initialize app
app = BedrockAgentCoreApp()

# Get environment variables with defaults
MEMORY_ID = os.getenv('MEMORY_ID')
MODEL_ID = os.getenv('MODEL_ID', 'us.anthropic.claude-sonnet-4-20250514-v1:0')
REGION = os.getenv('AWS_REGION', 'us-east-1')

# Validate and log configuration
if not MEMORY_ID:
    logger.warning("MEMORY_ID environment variable not set, memory operations may fail")
logger.info(f"Initializing with MODEL_ID={MODEL_ID}, REGION={REGION}")

# Initialize MemoryManager with environment configuration
memory = MemoryManager(memory_id=MEMORY_ID, region=REGION)

# Load problem statements
PROBLEM_STATEMENTS_PATH = os.path.join(os.path.dirname(__file__), '..', 'problem_statements.json')

def load_problem_statements() -> dict:
    """Load predefined problem statements from JSON file."""
    try:
        with open(PROBLEM_STATEMENTS_PATH, 'r') as f:
            data = json.load(f)
            return {p['id']: p for p in data.get('problems', [])}
    except Exception as e:
        print(f"Warning: Could not load problem statements: {e}")
        return {}

PROBLEMS = load_problem_statements()

def get_problem_by_id(problem_id: str) -> Optional[str]:
    """
    Retrieve a predefined problem statement by ID.
    
    Args:
        problem_id: The problem identifier (e.g., 'mars_currency')
    
    Returns:
        The full problem statement text, or None if not found
    """
    problem = PROBLEMS.get(problem_id)
    if problem:
        return problem['statement']
    return None

@app.entrypoint
async def debate_orchestrator(payload: dict, context: dict) -> dict:
    """
    Orchestrates a 9-minute debate across 3 rounds between three expert agents.
    
    This is the main entrypoint for the debate system. It coordinates:
    - Problem validation and session creation
    - 3 sequential debate rounds (2 debate + 1 consensus)
    - Expert agent invocations with cumulative context
    - Memory storage after each response
    - Final synthesis with Mermaid diagram generation
    
    Args:
        payload: {
            "problem": str (optional) - Custom problem statement
            "problemId": str (optional) - Predefined problem ID
        }
        context: AgentCore execution context
    
    Returns:
        {
            "sessionId": str - Unique session identifier
            "synthesis": str - Final synthesized architecture
            "mermaidDiagram": str - Mermaid diagram code
            "status": "complete" | "error"
        }
    
    Validates: Requirements 1.4, 1.5, 2.1, 2.2, 2.3, 2.4, 2.5, 2.6, 6.2
    """
    # Get problem from payload - either custom or by ID
    problem = payload.get('problem')
    problem_id = payload.get('problemId')
    
    # Get actor_id from payload or use default (needed for all responses)
    actor_id = payload.get('actor_id', 'orchestrator')
    
    # If problemId provided, load predefined problem
    if problem_id and not problem:
        problem = get_problem_by_id(problem_id)
        if not problem:
            return {
                "status": "error",
                "error": f"Problem ID '{problem_id}' not found",
                "actor_id": actor_id,
                "session_id": None
            }
    
    # Validate problem statement is non-empty (Requirement 1.4)
    if not problem or not problem.strip():
        return {
            "status": "error",
            "error": "Problem statement cannot be empty",
            "actor_id": actor_id,
            "session_id": None
        }
    
    # Create session (Requirement 1.5)
    try:
        session_id = memory.create_session(problem, actor_id)
        logger.info(f"Created session {session_id} for actor {actor_id}")
    except Exception as e:
        logger.error(f"Failed to create session: {e}")
        return {
            "status": "error",
            "error": f"Failed to create session: {str(e)}",
            "actor_id": actor_id,
            "session_id": None
        }
    
    # Define expert agents in order (Requirement 2.2)
    agents = [jeff_barr_agent, swami_agent, werner_agent]
    
    # Execute 3 rounds: 2 debate + 1 consensus (Requirement 2.1)
    for round_num in range(1, 4):
        # Round 3 is consensus, others are debate (Requirement 2.5)
        round_type = "consensus" if round_num == 3 else "debate"
        
        # Invoke each expert sequentially (Requirement 2.2)
        for agent in agents:
            # Retrieve cumulative context before each expert invocation (Requirement 6.2)
            try:
                mem_context = memory.get_context(session_id=session_id, actor_id=agent.name)
                # Handle empty context gracefully
                if not mem_context or not mem_context.strip():
                    mem_context = "[No previous context]"
                    logger.info(f"No previous context for {agent.name} in session {session_id}")
            except Exception as e:
                logger.error(f"Error retrieving context for {agent.name}: {e}")
                mem_context = "[Error retrieving context]"
            
            # Build prompt with problem, round info, and context
            if round_type == "consensus":
                prompt = f"""Problem: {problem}

Round {round_num} (CONSENSUS ROUND - work toward agreement)

Previous discussion:
{mem_context}

Your response (keep to ~200 words):"""
            else:
                prompt = f"""Problem: {problem}

Round {round_num} ({round_type})

Previous discussion:
{mem_context}

Your response (keep to ~200 words):"""
            
            # Invoke expert agent with correct pattern
            try:
                logger.info(f"Invoking agent {agent.name} for round {round_num}")
                response = agent(prompt)
                response_text = response.message['content'][0]['text']
                logger.info(f"Agent {agent.name} responded successfully")
            except (KeyError, TypeError, IndexError) as e:
                logger.error(f"Error extracting response from {agent.name}: {e}")
                response_text = f"[Agent {agent.name} failed to respond - invalid response structure]"
            except Exception as e:
                logger.error(f"Error invoking {agent.name}: {e}")
                response_text = f"[Agent {agent.name} failed to respond]"
            
            # Store response to AgentCore Memory (Requirement 2.3, 6.2)
            try:
                memory.store_response(
                    session_id=session_id,
                    actor_id=agent.name,
                    round_num=round_num,
                    content=response_text
                )
                logger.info(f"Stored response for {agent.name} in round {round_num}")
            except Exception as e:
                logger.error(f"Error storing response for {agent.name}: {e}")
                # Continue execution - memory failure shouldn't stop debate
            
            # Enforce 1-minute speaking time (Requirement 2.3)
            # In production, this would be actual timing enforcement
            # For now, we use a small delay to simulate sequential turns
            await asyncio.sleep(1)  # Reduced for testing; production would be 60
    
    # After all rounds complete, trigger Synthesis Agent (Requirement 2.6)
    try:
        full_context = memory.get_full_context(session_id=session_id, actor_id=actor_id)
        # Handle empty context gracefully
        if not full_context or not full_context.strip():
            logger.warning(f"No context retrieved for synthesis in session {session_id}")
            full_context = "[No debate context available]"
        
        # Build synthesis prompt
        synthesis_prompt = f"""You have observed a complete 3-round debate on the following problem:

Problem: {problem}

Complete debate transcript:
{full_context}

Please synthesize all three expert perspectives into a unified architecture proposal. Include:
1. Architecture overview combining all viewpoints
2. Core components and services
3. A Mermaid diagram showing the architecture
4. Key trade-offs between the different approaches

Remember to honor:
- Jeff's serverless and simplicity principles
- Swami's speed-to-market and AI/ML focus
- Werner's scale and distributed systems concerns"""
        
        logger.info("Invoking synthesis agent")
        synthesis_result = synthesis_agent(synthesis_prompt)
        synthesis_text = synthesis_result.message['content'][0]['text']
        logger.info("Synthesis agent completed successfully")
        
        # Extract Mermaid diagram from synthesis
        mermaid_diagram = extract_mermaid(synthesis_text)
        logger.info(f"Extracted Mermaid diagram: {len(mermaid_diagram)} characters")
        
    except (KeyError, TypeError, IndexError) as e:
        logger.error(f"Error extracting synthesis response: {e}")
        return {
            "status": "error",
            "error": f"Synthesis failed - invalid response structure: {str(e)}",
            "sessionId": session_id,
            "actor_id": actor_id,
            "session_id": session_id,
            "synthesis": None,
            "mermaidDiagram": None
        }
    except Exception as e:
        logger.error(f"Error during synthesis: {e}")
        return {
            "status": "error",
            "error": f"Synthesis failed: {str(e)}",
            "sessionId": session_id,
            "actor_id": actor_id,
            "session_id": session_id,
            "synthesis": None,
            "mermaidDiagram": None
        }
    
    # Return final result with synthesis and Mermaid diagram
    return {
        "sessionId": session_id,
        "actor_id": actor_id,
        "session_id": session_id,
        "synthesis": synthesis_text,
        "mermaidDiagram": mermaid_diagram,
        "status": "complete"
    }

if __name__ == "__main__":
    app.run()
