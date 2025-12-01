#!/usr/bin/env python3
import boto3

def condense_text(text, max_chars=250):
    """Condense text to ~30 seconds"""
    sentences = text.split('. ')
    condensed = []
    char_count = 0
    
    for sentence in sentences:
        if char_count + len(sentence) < max_chars:
            condensed.append(sentence)
            char_count += len(sentence)
        else:
            break
    
    return '. '.join(condensed) + '.'

def extract_and_condense(md_file):
    """Extract and condense all three experts"""
    with open(md_file, 'r') as f:
        content = f.read()
    
    # Jeff Barr
    jeff_start = content.find("### Jeff Barr (The Simplifier)")
    swami_start = content.find("### Swami (The Shipper)")
    jeff_text = content[jeff_start:swami_start].split('\n', 1)[1].strip()
    
    # Swami
    werner_start = content.find("### Werner Vogels (The Scale Architect)")
    swami_text = content[swami_start:werner_start].split('\n', 1)[1].strip()
    
    # Werner
    werner_end = content.find("---", werner_start + 100)
    werner_text = content[werner_start:werner_end].split('\n', 1)[1].strip()
    
    return [
        ('Jeff Barr', condense_text(jeff_text)),
        ('Swami', condense_text(swami_text)),
        ('Werner Vogels', condense_text(werner_text))
    ]

def generate_combined_audio(experts, output_file):
    """Generate single audio with all speakers using SSML"""
    client = boto3.client('polly', region_name='us-east-1')
    
    # Build SSML with voice changes
    ssml = '<speak>'
    
    voices = {'Jeff Barr': 'Matthew', 'Swami': 'Stephen', 'Werner Vogels': 'Brian'}
    
    for name, text in experts:
        ssml += f'<voice name="{voices[name]}">'
        ssml += f'<prosody rate="medium">{text}</prosody>'
        ssml += '</voice>'
        ssml += '<break time="500ms"/>'
    
    ssml += '</speak>'
    
    response = client.synthesize_speech(
        Text=ssml,
        OutputFormat='mp3',
        VoiceId='Matthew',
        Engine='neural',
        TextType='ssml'
    )
    
    with open(output_file, 'wb') as f:
        f.write(response['AudioStream'].read())

if __name__ == "__main__":
    print("Creating 2-minute debate with all speakers...\n")
    
    experts = extract_and_condense("conversation_mars_currency.md")
    
    for name, text in experts:
        print(f"{name}: {len(text)} chars (~30 sec)")
    
    print("\nGenerating combined audio...")
    generate_combined_audio(experts, "debate_full_2min.mp3")
    
    print("\n" + "=" * 60)
    print("✓ Complete: debate_full_2min.mp3")
    print("  Duration: ~2 minutes")
    print("  All 3 speakers in sequence")
    print("\nPlay: open debate_full_2min.mp3")
