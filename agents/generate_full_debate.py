#!/usr/bin/env python3
import boto3
import os

def extract_round(content, round_num):
    """Extract all expert responses from a round"""
    round_marker = f"## Round {round_num}:"
    round_start = content.find(round_marker)
    if round_start == -1:
        return []
    
    next_round = content.find(f"## Round {round_num + 1}:", round_start + 1)
    if next_round == -1:
        next_round = content.find("## Final Synthesis", round_start + 1)
    if next_round == -1:
        next_round = len(content)
    
    round_content = content[round_start:next_round]
    
    experts = []
    
    # Jeff
    jeff_start = round_content.find("### Jeff Barr")
    swami_start = round_content.find("### Swami")
    if jeff_start != -1 and swami_start != -1:
        text = round_content[jeff_start:swami_start].split('\n', 1)[1].strip()
        experts.append(('Jeff Barr', 'Matthew', text[:600]))  # ~45 sec
    
    # Swami
    werner_start = round_content.find("### Werner")
    if swami_start != -1 and werner_start != -1:
        text = round_content[swami_start:werner_start].split('\n', 1)[1].strip()
        experts.append(('Swami', 'Stephen', text[:600]))
    
    # Werner
    if werner_start != -1:
        text = round_content[werner_start:].split('\n', 1)[1].strip().split('---')[0].strip()
        experts.append(('Werner Vogels', 'Brian', text[:600]))
    
    return experts

def extract_synthesis(content):
    """Extract final synthesis"""
    synth_start = content.find("## Final Synthesis")
    if synth_start == -1:
        return None
    
    synth_content = content[synth_start:]
    
    # Get architecture overview and core components
    arch_start = synth_content.find("**Architecture Overview:**")
    core_start = synth_content.find("**Core Components:**")
    trade_start = synth_content.find("**Trade-offs:**")
    
    if arch_start != -1 and trade_start != -1:
        text = synth_content[arch_start:trade_start]
        # Condense to key points
        text = text.replace("**Architecture Overview:**", "Final Architecture: ")
        text = text.replace("**Core Components:**", "Key Components: ")
        return text[:800]  # ~60 sec
    
    return None

def generate_audio(text, voice_id, output_file):
    """Generate audio using Polly"""
    client = boto3.client('polly', region_name='us-east-1')
    
    response = client.synthesize_speech(
        Text=text,
        OutputFormat='mp3',
        VoiceId=voice_id,
        Engine='neural'
    )
    
    with open(output_file, 'wb') as f:
        f.write(response['AudioStream'].read())

if __name__ == "__main__":
    with open("conversation_mars_currency.md", 'r') as f:
        content = f.read()
    
    all_files = []
    
    print("Generating Complete Debate Audio\n" + "=" * 60)
    
    # Generate all 3 rounds
    for round_num in range(1, 4):
        round_name = ["Initial Positions", "Debate & Refinement", "Consensus Building"][round_num - 1]
        print(f"\nRound {round_num}: {round_name}")
        
        experts = extract_round(content, round_num)
        
        for name, voice, text in experts:
            filename = f"r{round_num}_{name.replace(' ', '_').lower()}.mp3"
            print(f"  {name} ({voice}): {len(text)} chars")
            generate_audio(text, voice, filename)
            all_files.append(filename)
    
    # Generate synthesis
    print(f"\nFinal Synthesis")
    synth_text = extract_synthesis(content)
    if synth_text:
        filename = "r4_synthesis.mp3"
        print(f"  Architecture Summary: {len(synth_text)} chars")
        generate_audio(synth_text, 'Matthew', filename)
        all_files.append(filename)
    
    # Combine all
    print("\nCombining all audio files...")
    os.system(f"cat {' '.join(all_files)} > debate_complete.mp3")
    
    print("\n" + "=" * 60)
    print("✓ Complete debate: debate_complete.mp3")
    print(f"  Total segments: {len(all_files)}")
    print(f"  Estimated duration: ~{len(all_files) * 45 // 60} minutes")
    print("\nPlay: open debate_complete.mp3")
