import json
import asyncio
from orchestrator.app import debate_orchestrator

async def test_debate():
    with open('problem_statements.json') as f:
        problems = json.load(f)
    
    # Test with Mars currency problem
    problem = problems['problems'][0]['statement']
    
    payload = {
        'problem': problem
    }
    
    result = await debate_orchestrator(payload, None)
    
    print("=" * 80)
    print("DEBATE COMPLETE")
    print("=" * 80)
    print(f"\nSession ID: {result['sessionId']}")
    print(f"\nSynthesis:\n{result['synthesis']}")

if __name__ == "__main__":
    asyncio.run(test_debate())
