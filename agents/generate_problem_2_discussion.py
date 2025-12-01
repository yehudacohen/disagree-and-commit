#!/usr/bin/env python3
from strands import Agent
from strands.models import BedrockModel
from experts.jeff_barr import jeff_barr_agent
from experts.swami import swami_agent
from experts.werner_vogels import werner_agent

problem = """How to use AWS technology to build a movable air device like clear-air taxi to bring down air pollution? Consider: real-time air quality monitoring, route optimization for minimal emissions, fleet management at scale, predictive maintenance, and AWS IoT and analytics services."""

def run_round(round_num, round_type, context=""):
    """Run one round of discussion"""
    agents = [
        ('Jeff Barr', jeff_barr_agent),
        ('Swami Sivasubramanian', swami_agent),
        ('Werner Vogels', werner_agent)
    ]
    
    responses = []
    
    for name, agent in agents:
        prompt = f"""Problem: {problem}

Round {round_num}: {round_type}

{context}

Provide your response (keep to ~200 words, 1 minute speaking time)."""
        
        result = agent.run(prompt)
        responses.append((name, result.message))
        context += f"\n\n{name}: {result.message}"
    
    return responses, context

def generate_discussion():
    """Generate full 4-round discussion"""
    output = f"""# AWS Executive Panel Discussion - Problem Statement 2

**Problem:** {problem}

**Panelists:**
- Jeff Barr
- Swami Sivasubramanian
- Werner Vogels

---

"""
    
    context = ""
    
    # Round 1: Initial Opinions
    print("Generating Round 1: Initial Opinions...")
    responses, context = run_round(1, "Initial Opinions", context)
    output += "## Round 1: Initial Opinions\n\n"
    for name, response in responses:
        output += f"### {name}\n\n{response}\n\n---\n\n"
    
    # Round 2: Disagreements
    print("Generating Round 2: Disagreements...")
    responses, context = run_round(2, "Disagreements - Challenge each other's approaches", context)
    output += "## Round 2: Disagreements\n\n"
    for name, response in responses:
        output += f"### {name}\n\n{response}\n\n---\n\n"
    
    # Round 3: Personal Callouts
    print("Generating Round 3: Personal Callouts...")
    responses, context = run_round(3, "Personal Callouts - Directly address other panelists' points", context)
    output += "## Round 3: Personal Callouts\n\n"
    for name, response in responses:
        output += f"### {name}\n\n{response}\n\n---\n\n"
    
    # Round 4: Disagree and Commit
    print("Generating Round 4: Disagree and Commit...")
    responses, context = run_round(4, "Disagree and Commit - Find consensus and commit to a solution", context)
    output += "## Round 4: Disagree and Commit\n\n"
    for name, response in responses:
        output += f"### {name}\n\n{response}\n\n---\n\n"
    
    return output

if __name__ == "__main__":
    print("Generating panel discussion for Problem Statement 2...")
    print("=" * 60)
    
    discussion = generate_discussion()
    
    with open("problem_statement_2.md", "w") as f:
        f.write(discussion)
    
    print("\n" + "=" * 60)
    print("✓ Discussion saved to problem_statement_2.md")
