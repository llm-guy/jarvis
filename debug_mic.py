#!/usr/bin/env python3
"""
Debug mode for Jarvis - shows what the microphone is hearing
"""

import logging
import speech_recognition as sr
import time

logging.basicConfig(level=logging.INFO)

def debug_microphone():
    """Debug what the microphone is hearing"""
    recognizer = sr.Recognizer()
    
    # Adjust settings
    recognizer.energy_threshold = 300
    recognizer.dynamic_energy_threshold = True
    recognizer.pause_threshold = 0.8
    
    try:
        # Try using the default microphone
        mic = sr.Microphone()
        
        print("🎤 Available microphones:")
        for i, name in enumerate(sr.Microphone.list_microphone_names()):
            print(f"  {i}: {name}")
        
        print(f"\n🎤 Using default microphone")
        
        with mic as source:
            print("Adjusting for ambient noise... (be quiet for a moment)")
            recognizer.adjust_for_ambient_noise(source, duration=2)
            print(f"Energy threshold set to: {recognizer.energy_threshold}")
            print("🎤 Listening for 'jarvis' or any speech... (Press Ctrl+C to stop)")
            
        while True:
            try:
                with mic as source:
                    print("\n🎤 Listening...")
                    audio = recognizer.listen(source, timeout=5, phrase_time_limit=3)
                    print("📡 Processing audio...")
                    
                try:
                    transcript = recognizer.recognize_google(audio)
                    print(f"🗣 Heard: '{transcript}'")
                    
                    if "jarvis" in transcript.lower():
                        print("🎯 WAKE WORD DETECTED!")
                        
                except sr.UnknownValueError:
                    print("❌ Could not understand audio")
                    
            except sr.WaitTimeoutError:
                print("⏰ Timeout - no audio detected")
            except KeyboardInterrupt:
                print("\n👋 Stopping debug mode")
                break
                
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    debug_microphone()
