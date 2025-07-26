#!/usr/bin/env python3
"""
Jarvis AI Assistant - Quick Start Guide
"""

print("""
🤖 Jarvis AI Voice Assistant - Usage Guide
=" * 50

📢 TTS Engine Options:
  --tts gtts      Google Text-to-Speech (requires internet, high quality)
  --tts pyttsx3   Python TTS (offline, cross-platform)
  --tts espeak    Linux espeak (offline, lightweight)
  --tts none      No speech, text-only display

🎛️ Voice Settings:
  --voice-rate 180    Speech speed (50-300, default: 180)
  --volume 1.0        Volume level (0.0-1.0, default: 1.0)

💬 Mode Options:
  --text-mode     Run in text-only mode (no microphone)
  --debug         Enable debug logging

🚀 Quick Examples:

1. Default (Google TTS with voice recognition):
   python main.py

2. Fast offline speech:
   python main.py --tts pyttsx3 --voice-rate 200

3. Text-only mode with speech output:
   python main.py --text-mode --tts gtts

4. Silent text-only mode:
   python main.py --text-mode --tts none

5. Linux espeak (lightweight):
   python main.py --tts espeak --voice-rate 150

6. Debug mode:
   python main.py --debug --tts pyttsx3

📋 Test Commands to Try:
  "What time is it in New York?"
  "Check my system status"
  "Calculate 25 * 4 + 10"
  "List files in current directory"
  "What's 15% of 2500?"

🔧 Troubleshooting:
  - No internet? Use: --tts pyttsx3 or --tts espeak
  - Microphone issues? Use: --text-mode
  - Need to install espeak? Run: sudo apt install espeak
  - Speech too fast/slow? Adjust: --voice-rate [number]

=" * 50
""")
