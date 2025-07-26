#!/usr/bin/env python3
"""
Test improved TTS with markdown cleaning and interruption
"""

import os
import sys
import tempfile
import pygame
import re
from gtts import gTTS

# Global variable for speech interruption
speech_interrupted = False

def clean_text_for_speech(text: str) -> str:
    """Clean text for better speech synthesis"""
    # Remove markdown formatting
    text = re.sub(r'\*\*(.*?)\*\*', r'\1', text)  # **bold** -> bold
    text = re.sub(r'\*(.*?)\*', r'\1', text)      # *italic* -> italic
    text = re.sub(r'`(.*?)`', r'\1', text)        # `code` -> code
    text = re.sub(r'#{1,6}\s*', '', text)         # Remove # headers
    text = re.sub(r'\[(.*?)\]\(.*?\)', r'\1', text)  # [text](link) -> text
    
    # Remove special characters that sound bad
    text = re.sub(r'[•◦▪▫]', '', text)            # Remove bullet points
    text = re.sub(r'[-]{2,}', '', text)           # Remove multiple dashes
    text = re.sub(r'[=]{2,}', '', text)           # Remove equals signs
    text = re.sub(r'[\$]', 'dollars', text)       # $ -> dollars
    text = re.sub(r'[%]', 'percent', text)        # % -> percent
    text = re.sub(r'[&]', 'and', text)            # & -> and
    
    # Clean up mathematical expressions
    text = re.sub(r'\$\$.*?\$\$', 'mathematical expression', text)  # $$...$$
    text = re.sub(r'\$.*?\$', 'math', text)       # $...$
    
    # Remove excessive whitespace
    text = re.sub(r'\s+', ' ', text)
    text = text.strip()
    
    # Limit length to avoid very long speech
    if len(text) > 300:
        text = text[:297] + "..."
    
    return text

def speak_text(text: str):
    """Generate and play speech using gTTS with interrupt capability"""
    global speech_interrupted
    speech_interrupted = False
    
    # Clean text for speech
    clean_text = clean_text_for_speech(text)
    
    print(f"Original text: {text}")
    print(f"Cleaned text: {clean_text}")
    
    if not clean_text.strip():
        print("⚠️ No speakable text after cleaning")
        return
    
    try:
        # Initialize pygame mixer
        pygame.mixer.init()
        
        # Create a temporary file for the audio
        with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as tmp_file:
            audio_path = tmp_file.name
        
        # Generate speech using gTTS
        print("🎵 Generating speech...")
        tts = gTTS(text=clean_text, lang='en', slow=False)
        tts.save(audio_path)
        
        # Play the audio using pygame with interrupt capability
        print("🔊 Playing audio... (Press Ctrl+C to interrupt)")
        pygame.mixer.music.load(audio_path)
        pygame.mixer.music.play()
        
        # Wait for playback to finish with interrupt check
        while pygame.mixer.music.get_busy() and not speech_interrupted:
            pygame.time.wait(50)  # Check every 50ms for interruption
        
        # Stop if interrupted
        if speech_interrupted:
            pygame.mixer.music.stop()
            print("🛑 Speech interrupted")
        else:
            print("✅ Speech completed")
        
        # Clean up the temporary file
        os.unlink(audio_path)
        
    except KeyboardInterrupt:
        pygame.mixer.music.stop()
        print("🛑 Speech interrupted by user")
    except Exception as e:
        print(f"❌ TTS failed: {e}")

def test_tts():
    """Test TTS with various markdown texts"""
    test_texts = [
        "Hello! I am **Jarvis**, your *AI assistant*. This is `code` and here's a link [Google](https://google.com).",
        
        "**System Status:**\n- OS: Linux\n- CPU: 4.2% usage\n- Memory: 47.3% used\n• This has bullets\n• And more bullets",
        
        "The calculation is: $$45 \\times 23 + 67 = 1102$$. The result is $1102$.",
        
        "# This is a header\n## Subheader\n### Another header\nNormal text with *emphasis* and **bold**.",
        
        "Price: $100 | Discount: 20% | Company: AT&T"
    ]
    
    for i, text in enumerate(test_texts, 1):
        print(f"\n{'='*50}")
        print(f"Test {i}:")
        speak_text(text)
        
        response = input("\nContinue to next test? (y/n): ")
        if response.lower() != 'y':
            break
    
    print("\n✅ TTS testing completed!")

if __name__ == "__main__":
    try:
        test_tts()
    except KeyboardInterrupt:
        print("\n👋 Testing stopped by user")
