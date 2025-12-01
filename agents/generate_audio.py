#!/usr/bin/env python3
import boto3

def extract_first_minute_text(md_file):
    """Extract Jeff Barr's first response (~1 minute of content)"""
    with open(md_file, 'r') as f:
        content = f.read()
    
    start = content.find("### Jeff Barr (The Simplifier)")
    end = content.find("### Swami (The Shipper)")
    
    if start != -1 and end != -1:
        text = content[start:end].strip()
        text = text.replace("### Jeff Barr (The Simplifier)", "").strip()
        return text
    
    return "Text extraction failed"

def generate_audio_polly(text, output_file="jeff_barr_round1.mp3"):
    """Generate audio using Amazon Polly"""
    client = boto3.client('polly', region_name='us-east-1')
    
    try:
        response = client.synthesize_speech(
            Text=text,
            OutputFormat='mp3',
            VoiceId='Matthew',
            Engine='neural'
        )
        
        with open(output_file, 'wb') as f:
            f.write(response['AudioStream'].read())
        
        print(f"✓ Audio generated: {output_file}")
        print(f"  Voice: Matthew (Neural)")
        return output_file
            
    except Exception as e:
        print(f"Error: {e}")
        return None

if __name__ == "__main__":
    text = extract_first_minute_text("conversation_mars_currency.md")
    print(f"Text ({len(text)} chars): {text[:100]}...")
    print("\nGenerating audio...")
    output = generate_audio_polly(text)
    if output:
        print(f"\n✓ Success! Play with: open {output}")
