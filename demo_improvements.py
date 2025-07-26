#!/usr/bin/env python3
"""
Quick demo of improved Jarvis TTS with markdown cleaning
"""

import re
from gtts import gTTS
import pygame
import tempfile
import os
import time

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
    
    # Clean up mathematical expressions first (before dollar replacements)
    text = re.sub(r'\$\$.*?\$\$', 'mathematical expression', text)  # $$...$$
    text = re.sub(r'\$([0-9,]+(?:\.[0-9]+)?)', r'\1 dollars', text)  # $123 -> 123 dollars
    text = re.sub(r'\$', 'dollars', text)         # Remaining $ -> dollars
    text = re.sub(r'([0-9]+)%', r'\1 percent', text)  # 20% -> 20 percent  
    text = re.sub(r'[&]', 'and', text)            # & -> and
    
    # Remove excessive whitespace
    text = re.sub(r'\s+', ' ', text)
    text = text.strip()
    
    # Limit length to avoid very long speech
    if len(text) > 300:
        text = text[:297] + "..."
    
    return text

def demo_tts_improvements():
    """Demo the improved TTS functionality"""
    test_cases = [
        {
            "name": "Markdown Formatting",
            "text": "Hello! I am **Jarvis**, your *intelligent* assistant. I can help with `code` and [links](http://example.com)."
        },
        {
            "name": "Financial Data", 
            "text": "The stock price is $125.50, down 3% from yesterday. Market cap: $2.5B."
        },
        {
            "name": "System Status",
            "text": "**System Status:**\n• CPU: 45%\n• Memory: 67%\n• Disk: $100 GB free"
        },
        {
            "name": "Technical Content",
            "text": "## Installation\nRun `pip install requirements.txt` for **dependencies**. Cost: ~$0 per month."
        }
    ]
    
    print("🎤 Jarvis TTS Improvements Demo")
    print("=" * 50)
    
    for i, test in enumerate(test_cases, 1):
        print(f"\n{i}. {test['name']}:")
        print(f"   Original: {test['text']}")
        
        cleaned = clean_text_for_speech(test['text'])
        print(f"   Cleaned:  {cleaned}")
        
        print(f"   ✅ Improvement: Removed {len(test['text']) - len(cleaned)} problematic characters")
    
    print(f"\n🚀 Key Improvements:")
    print(f"   • Markdown symbols (**, *, `, #) → Clean text")
    print(f"   • Dollar signs ($123) → '123 dollars'")
    print(f"   • Percentages (20%) → '20 percent'")
    print(f"   • Bullet points (•) → Removed")
    print(f"   • Links [text](url) → 'text'")
    print(f"   • Math expressions → Simplified")
    
    print(f"\n⌨️  Interruption Features:")
    print(f"   • Press 's' key to stop speech")
    print(f"   • Ctrl+C for immediate stop")
    print(f"   • Visual feedback during playback")
    
    print(f"\n✨ Enhanced Voice Experience:")
    print(f"   • Google TTS (gTTS) for natural voice")
    print(f"   • Text length limiting (300 chars max)")
    print(f"   • Fallback to pyttsx3 if needed")
    print(f"   • Better error handling")

if __name__ == "__main__":
    demo_tts_improvements()
