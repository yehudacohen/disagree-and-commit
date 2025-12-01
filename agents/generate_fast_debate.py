#!/usr/bin/env python3
import boto3
import os

def extract_round(content, round_num):
    """Extract condensed expert responses"""
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
        experts.append(('Jeff Barr', 'Matthew', text[:250]))  # ~15 sec at fast rate
    
    # Swami
    werner_start = round_content.find("### Werner")
    if swami_start != -1 and werner_start != -1:
        text = round_content[swami_start:werner_start].split('\n', 1)[1].strip()
        experts.append(('Swami', 'Stephen', text[:250]))
    
    # Werner
    if werner_start != -1:
        text = round_content[werner_start:].split('\n', 1)[1].strip().split('---')[0].strip()
        experts.append(('Werner Vogels', 'Brian', text[:250]))
    
    return experts

def extract_synthesis(content):
    """Extract condensed synthesis"""
    synth_start = content.find("## Final Synthesis")
    if synth_start == -1:
        return None
    
    synth_content = content[synth_start:]
    arch_start = synth_content.find("**Architecture Overview:**")
    core_start = synth_content.find("**Core Components:**")
    
    if arch_start != -1 and core_start != -1:
        text = synth_content[arch_start:core_start].replace("**Architecture Overview:**", "Final Architecture: ")
        return text[:300]  # ~20 sec
    
    return None

def generate_audio(text, voice_id, output_file):
    """Generate audio with fast speech rate"""
    client = boto3.client('polly', region_name='us-east-1')
    
    # Use SSML for faster speech
    ssml = f'<speak><prosody rate="fast">{text}</prosody></speak>'
    
    response = client.synthesize_speech(
        Text=ssml,
        OutputFormat='mp3',
        VoiceId=voice_id,
        Engine='neural',
        TextType='ssml'
    )
    
    with open(output_file, 'wb') as f:
        f.write(response['AudioStream'].read())

if __name__ == "__main__":
    with open("conversation_mars_currency.md", 'r') as f:
        content = f.read()
    
    all_files = []
    
    print("Generating Fast 3-Minute Debate\n" + "=" * 60)
    
    # All 3 rounds
    for round_num in range(1, 4):
        round_name = ["Round 1: Initial", "Round 2: Debate", "Round 3: Consensus"][round_num - 1]
        print(f"\n{round_name}")
        
        experts = extract_round(content, round_num)
        
        for name, voice, text in experts:
            filename = f"fast_r{round_num}_{name.replace(' ', '_').lower()}.mp3"
            print(f"  {name}: {len(text)} chars")
            generate_audio(text, voice, filename)
            all_files.append(filename)
    
    # Synthesis
    print(f"\nFinal Synthesis")
    synth_text = extract_synthesis(content)
    if synth_text:
        filename = "fast_synthesis.mp3"
        print(f"  Architecture: {len(synth_text)} chars")
        generate_audio(synth_text, 'Matthew', filename)
        all_files.append(filename)
    
    # Combine
    print("\nCombining...")
    os.system(f"cat {' '.join(all_files)} > debate_fast_3min.mp3")
    
    print("\n" + "=" * 60)
    print("✓ Fast debate: debate_fast_3min.mp3")
    print(f"  Duration: ~3 minutes")
    print(f"  Speech rate: Fast (2x)")
    print("\nPlay: open debate_fast_3min.mp3")
