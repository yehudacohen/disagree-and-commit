#!/usr/bin/env python3
import boto3

def extract_expert_responses(md_file, round_num=1):
    """Extract all three expert responses from a specific round"""
    with open(md_file, 'r') as f:
        content = f.read()
    
    experts = {
        'jeff_barr': {'voice': 'Matthew', 'text': ''},
        'swami': {'voice': 'Stephen', 'text': ''},
        'werner_vogels': {'voice': 'Brian', 'text': ''}
    }
    
    # Find Round section
    round_marker = f"## Round {round_num}:"
    round_start = content.find(round_marker)
    if round_start == -1:
        return experts
    
    # Find next round or end
    next_round = content.find(f"## Round {round_num + 1}:", round_start + 1)
    if next_round == -1:
        next_round = content.find("## Final Synthesis", round_start + 1)
    if next_round == -1:
        next_round = len(content)
    
    round_content = content[round_start:next_round]
    
    # Extract Jeff Barr
    jeff_start = round_content.find("### Jeff Barr")
    swami_start = round_content.find("### Swami")
    if jeff_start != -1 and swami_start != -1:
        experts['jeff_barr']['text'] = round_content[jeff_start:swami_start].split('\n', 1)[1].strip()
    
    # Extract Swami
    werner_start = round_content.find("### Werner Vogels")
    if swami_start != -1 and werner_start != -1:
        experts['swami']['text'] = round_content[swami_start:werner_start].split('\n', 1)[1].strip()
    
    # Extract Werner
    if werner_start != -1:
        werner_text = round_content[werner_start:].split('\n', 1)[1].strip()
        # Remove trailing separators
        werner_text = werner_text.split('---')[0].strip()
        experts['werner_vogels']['text'] = werner_text
    
    return experts

def generate_audio(text, voice_id, output_file):
    """Generate audio using Amazon Polly Neural voices"""
    client = boto3.client('polly', region_name='us-east-1')
    
    try:
        response = client.synthesize_speech(
            Text=text,
            OutputFormat='mp3',
            VoiceId=voice_id,
            Engine='neural'
        )
        
        with open(output_file, 'wb') as f:
            f.write(response['AudioStream'].read())
        
        return True
    except Exception as e:
        print(f"Error: {e}")
        return False

if __name__ == "__main__":
    round_num = 1
    
    print(f"Extracting Round {round_num} responses...\n")
    experts = extract_expert_responses("conversation_mars_currency.md", round_num)
    
    for expert_id, data in experts.items():
        if data['text']:
            output_file = f"{expert_id}_round{round_num}.mp3"
            print(f"{expert_id.replace('_', ' ').title()}: {data['voice']} ({len(data['text'])} chars)")
            
            if generate_audio(data['text'], data['voice'], output_file):
                print(f"  ✓ {output_file}\n")
    
    print("=" * 60)
    print("Play debate:")
    print(f"  open jeff_barr_round{round_num}.mp3 && sleep 60 && open swami_round{round_num}.mp3 && sleep 60 && open werner_vogels_round{round_num}.mp3")
