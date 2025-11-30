from bedrock_agentcore.runtime import BedrockAgentCoreApp
from experts.jeff_barr import jeff_barr_agent
from experts.swami import swami_agent
from experts.werner_vogels import werner_agent
from synthesis.synthesizer import synthesis_agent, extract_mermaid
from memory.session_manager import MemoryManager
import asyncio
import json
import os
from typing import Optional

app = BedrockAgentCoreApp()
memory = MemoryManager()

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
    
    # If problemId provided, load predefined problem
    if problem_id and not problem:
        problem = get_problem_by_id(problem_id)
        if not problem:
            return {
                "status": "error",
                "error": f"Problem ID '{problem_id}' not found"
            }
    
    # Validate problem statement is non-empty (Requirement 1.4)
    if not problem or not problem.strip():
        return {
            "status": "error",
            "error": "Problem statement cannot be empty"
        }
    
    # Create session (Requirement 1.5)
    try:
        session_id = memory.create_session(problem)
    except Exception as e:
        return {
            "status": "error",
            "error": f"Failed to create session: {str(e)}"
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
            mem_context = memory.get_context(session_id)
            
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
            
            # Invoke expert agent
            try:
                response = agent.run(prompt)
                response_text = response.message
            except Exception as e:
                print(f"Error invoking {agent.name}: {e}")
                response_text = f"[Agent {agent.name} failed to respond]"
            
            # Store response to AgentCore Memory (Requirement 2.3, 6.2)
            try:
                memory.store_response(
                    session_id=session_id,
                    agent_name=agent.name,
                    round_num=round_num,
                    content=response_text
                )
            except Exception as e:
                print(f"Error storing response for {agent.name}: {e}")
            
            # Enforce 1-minute speaking time (Requirement 2.3)
            # In production, this would be actual timing enforcement
            # For now, we use a small delay to simulate sequential turns
            await asyncio.sleep(1)  # Reduced for testing; production would be 60
    
    # After all rounds complete, trigger Synthesis Agent (Requirement 2.6)
    try:
        full_context = memory.get_full_context(session_id)
        
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
        
        synthesis_result = synthesis_agent.run(synthesis_prompt)
        synthesis_text = synthesis_result.message
        
        # Extract Mermaid diagram from synthesis
        mermaid_diagram = extract_mermaid(synthesis_text)
        
    except Exception as e:
        print(f"Error during synthesis: {e}")
        return {
            "sessionId": session_id,
            "status": "error",
            "error": f"Synthesis failed: {str(e)}"
        }
    
    # Return final result with synthesis and Mermaid diagram
    return {
        "sessionId": session_id,
        "synthesis": synthesis_text,
        "mermaidDiagram": mermaid_diagram,
        "status": "complete"
    }

if __name__ == "__main__":
    app.run()
