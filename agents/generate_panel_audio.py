#!/usr/bin/env python3
import boto3
import re

def parse_panel_file(filename):
    """Parse panel.txt and extract all responses by person and round"""
    with open(filename, 'r') as f:
        content = f.read()
    
    rounds = {}
    
    for round_num in range(1, 5):
        round_marker = f"ROUND {round_num}:"
        round_start = content.find(round_marker)
        if round_start == -1:
            continue
        
        next_round = content.find(f"ROUND {round_num + 1}:", round_start + 1)
        if next_round == -1:
            next_round = content.find("DISCUSSION COMPLETE", round_start + 1)
        if next_round == -1:
            next_round = len(content)
        
        round_content = content[round_start:next_round]
        rounds[round_num] = {}
        
        # Jeff Barr
        jeff_start = round_content.find("Jeff Barr:")
        swami_start = round_content.find("Swami Sivasubramanian:")
        if jeff_start != -1 and swami_start != -1:
            text = round_content[jeff_start:swami_start]
            text = text.replace("Jeff Barr:", "").strip()
            text = re.sub(r'\*[^*]+\*', '', text).strip()
            rounds[round_num]['jeff'] = text[:600]
        
        # Swami
        werner_start = round_content.find("Werner Vogels:")
        if swami_start != -1 and werner_start != -1:
            text = round_content[swami_start:werner_start]
            text = text.replace("Swami Sivasubramanian:", "").strip()
            text = re.sub(r'\*[^*]+\*', '', text).strip()
            rounds[round_num]['swami'] = text[:600]
        
        # Werner
        if werner_start != -1:
            text = round_content[werner_start:]
            next_section = text.find("────────────────", 100)
            if next_section != -1:
                text = text[:next_section]
            text = text.replace("Werner Vogels:", "").strip()
            text = re.sub(r'\*[^*]+\*', '', text).strip()
            rounds[round_num]['werner'] = text[:600]
    
    return rounds

def generate_audio(text, voice_id, output_file, language_code='en-US'):
    """Generate audio with fast speech rate"""
    client = boto3.client('polly', region_name='us-east-1')
    
    ssml = f'<speak><prosody rate="fast">{text}</prosody></speak>'
    
    response = client.synthesize_speech(
        Text=ssml,
        OutputFormat='mp3',
        VoiceId=voice_id,
        Engine='neural',
        TextType='ssml',
        LanguageCode=language_code
    )
    
    with open(output_file, 'wb') as f:
        f.write(response['AudioStream'].read())

if __name__ == "__main__":
    voices = {
        'jeff': {'voice': 'Matthew', 'lang': 'en-US', 'desc': 'US English Male'},
        'swami': {'voice': 'Stephen', 'lang': 'en-US', 'desc': 'US English Male (warm tone)'},
        'werner': {'voice': 'Arthur', 'lang': 'en-GB', 'desc': 'British English Male (European)'}
    }
    
    round_names = {
        1: "Initial Opinions",
        2: "Disagreements",
        3: "Personal Callouts",
        4: "Disagree and Commit"
    }
    
    print("Parsing panel.txt...")
    rounds = parse_panel_file("panel.txt")
    
    print("\nGenerating 12 audio files - All Male Voices\n" + "=" * 60)
    
    files_generated = []
    
    for round_num in range(1, 5):
        print(f"\nRound {round_num}: {round_names[round_num]}")
        
        for person, voice_config in voices.items():
            if round_num in rounds and person in rounds[round_num]:
                text = rounds[round_num][person]
                filename = f"r{round_num}_{person}.mp3"
                
                print(f"  {person.title()}: {voice_config['voice']} ({voice_config['desc']}) → {filename}")
                generate_audio(text, voice_config['voice'], filename, voice_config['lang'])
                files_generated.append(filename)
    
    print("\n" + "=" * 60)
    print(f"✓ Generated {len(files_generated)} audio files")
    print("\nVoice assignments (All Male):")
    print("  Jeff Barr: Matthew (US English)")
    print("  Swami: Stephen (US English - warm tone)")
    print("  Werner: Arthur (British English - European)")
