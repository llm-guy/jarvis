#!/usr/bin/env python3
"""
Test script for Coqui TTS functionality
"""

import logging
import tempfile
import os
import pygame
from TTS.api import TTS

logging.basicConfig(level=logging.INFO)

def test_coqui_tts():
    """Test Coqui TTS functionality"""
    try:
        # Initialize TTS
        print("Initializing Coqui TTS...")
        tts = TTS(model_name="tts_models/en/ljspeech/tacotron2-DDC", progress_bar=False)
        print("✅ TTS initialized successfully")
        
        # Initialize pygame for audio playback
        pygame.mixer.init()
        print("✅ Pygame mixer initialized")
        
        # Test text
        test_text = "Hello! I am Jarvis, your AI assistant. Coqui TTS is working perfectly!"
        
        # Create temporary file
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp_file:
            audio_path = tmp_file.name
        
        # Generate speech
        print(f"Generating speech: {test_text}")
        tts.tts_to_file(text=test_text, file_path=audio_path)
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
        print("✅ TTS test completed successfully!")
        
    except Exception as e:
        print(f"❌ TTS test failed: {e}")
        return False
    
    return True

if __name__ == "__main__":
    test_coqui_tts()
