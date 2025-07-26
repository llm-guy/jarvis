#!/usr/bin/env python3
"""
Test script for gTTS functionality
"""

import logging
import tempfile
import os
import pygame
from gtts import gTTS

logging.basicConfig(level=logging.INFO)

def test_gtts():
    """Test gTTS functionality"""
    try:
        # Initialize pygame mixer
        pygame.mixer.init()
        print("✅ Pygame mixer initialized")
        
        # Test text
        test_text = "Hello! I am Jarvis, your AI assistant. Google Text to Speech is working perfectly!"
        
        # Create temporary file
        with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as tmp_file:
            audio_path = tmp_file.name
        
        # Generate speech
        print(f"Generating speech: {test_text}")
        tts = gTTS(text=test_text, lang='en', slow=False)
        tts.save(audio_path)
        print("✅ Speech generated successfully")
        
        # Play audio
        print("Playing audio...")
        pygame.mixer.music.load(audio_path)
        pygame.mixer.music.play()
        
        # Wait for playback to finish
        while pygame.mixer.music.get_busy():
            pygame.time.wait(100)
        
        # Clean up
        os.unlink(audio_path)
        print("✅ gTTS test completed successfully!")
        
    except Exception as e:
        print(f"❌ gTTS test failed: {e}")
        return False
    
    return True

if __name__ == "__main__":
    test_gtts()
