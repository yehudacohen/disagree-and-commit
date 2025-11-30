from bedrock_agentcore.runtime import BedrockAgentCoreApp
from experts.jeff_barr import jeff_barr_agent
from experts.swami import swami_agent
from experts.werner_vogels import werner_agent
from synthesis.synthesizer import synthesis_agent
from memory.session_manager import MemoryManager
import asyncio
import json

app = BedrockAgentCoreApp()
memory = MemoryManager()

@app.entrypoint
async def debate_orchestrator(payload, context):
    problem = payload['problem']
    session_id = memory.create_session(problem)
    
    agents = [jeff_barr_agent, swami_agent, werner_agent]
    
    # 3 rounds: 2 debate + 1 consensus
    for round_num in range(1, 4):
        round_type = "consensus" if round_num == 3 else "debate"
        
        for agent in agents:
            mem_context = memory.get_context(session_id)
            
            response = agent.run(
                f"Problem: {problem}\n\nRound {round_num} ({round_type})\n\nPrevious context:\n{mem_context}"
            )
            
            memory.store_response(
                session_id=session_id,
                agent_name=agent.name,
                round_num=round_num,
                content=response.message
            )
            
            await asyncio.sleep(60)  # 1 minute per turn
    
    # Synthesis
    full_context = memory.get_full_context(session_id)
    synthesis_result = synthesis_agent.run(full_context)
    
    return {
        "sessionId": session_id,
        "synthesis": synthesis_result.message,
        "status": "complete"
    }

if __name__ == "__main__":
    app.run()
