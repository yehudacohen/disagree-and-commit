#!/usr/bin/env env python3
"""
AWS Executive Panel Discussion POC
Orchestrates a multi-round debate between Jeff Barr, Swami Sivasubramanian, and Werner Vogels
"""

import boto3
import json
import sys
from typing import List, Dict
from dataclasses import dataclass


@dataclass
class Panelist:
    name: str
    prompt_file: str
    persona_prompt: str


class PanelDiscussion:
    def __init__(self, aws_profile: str = "chrismiller"):
        """Initialize the panel discussion with AWS Bedrock client"""
        self.session = boto3.Session(profile_name=aws_profile)
        self.bedrock = self.session.client('bedrock-runtime', region_name='us-west-2')
        self.model_id = "anthropic.claude-3-5-sonnet-20241022-v2:0"
        
        # Load persona prompts
        self.panelists = self._load_panelists()
        self.discussion_history = []
        
    def _load_panelists(self) -> List[Panelist]:
        """Load the persona prompts for each panelist"""
        panelist_configs = [
            ("Jeff Barr", "jeff-barr-agent-prompt.md"),
            ("Swami Sivasubramanian", "swami-sivasubramanian-agent-prompt.md"),
            ("Werner Vogels", "werner_vogels_agent_prompt.md")
        ]
        
        panelists = []
        for name, filename in panelist_configs:
            with open(filename, 'r') as f:
                persona_prompt = f.read()
            panelists.append(Panelist(name, filename, persona_prompt))
        
        return panelists
    
    def _call_claude(self, system_prompt: str, user_message: str) -> str:
        """Call Claude Sonnet 4.5 via Bedrock"""
        request_body = {
            "anthropic_version": "bedrock-2023-05-31",
            "max_tokens": 2000,
            "temperature": 0.7,
            "system": system_prompt,
            "messages": [
                {
                    "role": "user",
                    "content": user_message
                }
            ]
        }
        
        response = self.bedrock.invoke_model(
            modelId=self.model_id,
            body=json.dumps(request_body)
        )
        
        response_body = json.loads(response['body'].read())
        return response_body['content'][0]['text']

    def _format_discussion_context(self, round_num: int, round_name: str) -> str:
        """Format the discussion history for context"""
        if not self.discussion_history:
            return ""
        
        context = f"\n\n=== PREVIOUS ROUNDS ===\n"
        for entry in self.discussion_history:
            context += f"\n[{entry['round']}] {entry['panelist']}:\n{entry['response']}\n"
        return context
    
    def round_1_initial_opinions(self, problem: str):
        """Round 1: Each panelist shares their opinion on solving the problem"""
        print("\n" + "="*80)
        print("ROUND 1: INITIAL OPINIONS")
        print("="*80)
        print(f"\nPROBLEM: {problem}\n")
        
        for panelist in self.panelists:
            user_message = f"""You are participating in a panel discussion about the following problem:

PROBLEM: {problem}

This is ROUND 1 of the discussion. Please share your initial opinion on how to solve this problem. 
Stay true to your personality and expertise. Keep your response to 2-3 paragraphs."""
            
            response = self._call_claude(panelist.persona_prompt, user_message)
            
            print(f"\n{'─'*80}")
            print(f"{panelist.name}:")
            print(f"{'─'*80}")
            print(response)
            
            self.discussion_history.append({
                "round": "Round 1",
                "panelist": panelist.name,
                "response": response
            })
    
    def round_2_disagreements(self):
        """Round 2: Each panelist disagrees with others based on their worldview"""
        print("\n" + "="*80)
        print("ROUND 2: DISAGREEMENTS")
        print("="*80)
        
        context = self._format_discussion_context(2, "Disagreements")
        
        for panelist in self.panelists:
            other_panelists = [p for p in self.panelists if p.name != panelist.name]
            
            user_message = f"""You are continuing the panel discussion. Here's what has been said so far:
{context}

This is ROUND 2. Now you need to DISAGREE with the other panelists' approaches based on your own worldview and expertise.

Specifically address what {other_panelists[0].name} and {other_panelists[1].name} said, and explain why their approaches are problematic from your perspective.

Stay true to your personality. Keep your response to 2-3 paragraphs."""
            
            response = self._call_claude(panelist.persona_prompt, user_message)
            
            print(f"\n{'─'*80}")
            print(f"{panelist.name}:")
            print(f"{'─'*80}")
            print(response)
            
            self.discussion_history.append({
                "round": "Round 2",
                "panelist": panelist.name,
                "response": response
            })
    
    def round_3_personal_callouts(self):
        """Round 3: Panelists call out solutions in a personal way based on personality"""
        print("\n" + "="*80)
        print("ROUND 3: PERSONAL CALLOUTS")
        print("="*80)
        
        context = self._format_discussion_context(3, "Personal Callouts")
        
        for panelist in self.panelists:
            other_panelists = [p for p in self.panelists if p.name != panelist.name]
            
            user_message = f"""You are continuing the panel discussion. Here's what has been said so far:
{context}

This is ROUND 3. Now you need to call out the other panelists' solutions in a PERSONAL way that reflects your unique personality and communication style.

Be direct, use your characteristic phrases and mannerisms. Challenge {other_panelists[0].name} and {other_panelists[1].name} based on who they are and how they think.

This is where your personality really shines through. Keep your response to 2-3 paragraphs."""
            
            response = self._call_claude(panelist.persona_prompt, user_message)
            
            print(f"\n{'─'*80}")
            print(f"{panelist.name}:")
            print(f"{'─'*80}")
            print(response)
            
            self.discussion_history.append({
                "round": "Round 3",
                "panelist": panelist.name,
                "response": response
            })
    
    def round_4_disagree_and_commit(self):
        """Round 4: Panelists disagree but commit to one solution"""
        print("\n" + "="*80)
        print("ROUND 4: DISAGREE AND COMMIT")
        print("="*80)
        
        context = self._format_discussion_context(4, "Disagree and Commit")
        
        for panelist in self.panelists:
            user_message = f"""You are in the final round of the panel discussion. Here's everything that has been said:
{context}

This is ROUND 4 - the final round. Following Amazon's "Disagree and Commit" principle, you need to:

1. Acknowledge where you still disagree with the other panelists
2. Commit to ONE specific solution that the team should move forward with
3. Explain why you're willing to commit despite your disagreements

Stay true to your personality, but show leadership by committing to a path forward. Keep your response to 2-3 paragraphs."""
            
            response = self._call_claude(panelist.persona_prompt, user_message)
            
            print(f"\n{'─'*80}")
            print(f"{panelist.name}:")
            print(f"{'─'*80}")
            print(response)
            
            self.discussion_history.append({
                "round": "Round 4",
                "panelist": panelist.name,
                "response": response
            })
    
    def run_discussion(self, problem: str):
        """Run the complete 4-round panel discussion"""
        print("\n" + "="*80)
        print("AWS EXECUTIVE PANEL DISCUSSION")
        print("="*80)
        print(f"\nPanelists:")
        for panelist in self.panelists:
            print(f"  • {panelist.name}")
        
        self.round_1_initial_opinions(problem)
        self.round_2_disagreements()
        self.round_3_personal_callouts()
        self.round_4_disagree_and_commit()
        
        print("\n" + "="*80)
        print("DISCUSSION COMPLETE")
        print("="*80)


def main():
    if len(sys.argv) < 2:
        print("Usage: python panel_discussion.py '<problem statement>'")
        print("\nExample:")
        print("  python panel_discussion.py 'How should we approach building a real-time data processing platform for IoT devices?'")
        sys.exit(1)
    
    problem = sys.argv[1]
    
    try:
        panel = PanelDiscussion(aws_profile="chrismiller")
        panel.run_discussion(problem)
    except Exception as e:
        print(f"\nError: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
