import os
import logging
import time
import hashlib
import json
from pathlib import Path
from datetime import datetime, timedelta
from elevenlabs.client import ElevenLabs
from dotenv import load_dotenv
import speech_recognition as sr
from langchain_ollama import ChatOllama, OllamaLLM
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_core.prompts import ChatPromptTemplate
from tools.time import get_time 

load_dotenv()

MIC_INDEX = 0
TRIGGER_WORD = "friday"
CONVERSATION_TIMEOUT = 15  # seconds of inactivity before exiting conversation mode

logging.basicConfig(level=logging.DEBUG) # logging

# api_key = os.getenv("OPENAI_API_KEY") removed because it's not needed for ollama
# org_id = os.getenv("OPENAI_ORG_ID") removed because it's not needed for ollama

recognizer = sr.Recognizer()
mic = sr.Microphone(device_index=MIC_INDEX)

# Initialize Friday AI persona (LLM) based on environment configuration
use_openrouter = os.getenv("USE_OPENROUTER", "false").lower() == "true"

if use_openrouter:
    # Use OpenRouter configuration
    openrouter_api_key = os.getenv("OPENROUTER_API_KEY")
    openrouter_model = os.getenv("OPENROUTER_MODEL", "anthropic/claude-3-haiku")
    openrouter_base_url = os.getenv("OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1")
    
    if openrouter_api_key:
        llm = ChatOpenAI(
            model=openrouter_model,
            api_key=openrouter_api_key,
            base_url=openrouter_base_url
        )
        logging.info(f"🌐 Using OpenRouter model: {openrouter_model}")
    else:
        logging.error("❌ OpenRouter enabled but API key not found, falling back to local Ollama")
        llm = ChatOllama(model="qwen3:1.7b", reasoning=False)
        logging.info("🤖 Using fallback local Ollama model: qwen3:1.7b")
else:
    # Use local Ollama model
    ollama_model = os.getenv("OLLAMA_MODEL", "qwen3:1.7b")
    llm = ChatOllama(model=ollama_model, reasoning=False)
    logging.info(f"🤖 Using local Ollama model: {ollama_model}")

# Tool list
tools = [get_time]

# Tool-calling prompt
system_prompt = os.getenv("SYSTEM_PROMPT", "You are Friday, an intelligent, conversational AI assistant. Your goal is to be helpful, friendly, and informative. You can respond in natural, human-like language and use tools when needed to answer questions more accurately. Always explain your reasoning simply when appropriate, and keep your responses conversational and concise.")

prompt = ChatPromptTemplate.from_messages([
    ("system", system_prompt),
    ("human", "{input}"),
    ("placeholder", "{agent_scratchpad}")
])

# Agent + executor
agent = create_tool_calling_agent(llm=llm, tools=tools, prompt=prompt)
executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

# Audio Cache Management
def get_cache_key(text: str, voice_id: str, model_id: str, stability: float, similarity_boost: float) -> str:
    """Generate a unique cache key for the given TTS parameters"""
    cache_data = f"{text}|{voice_id}|{model_id}|{stability}|{similarity_boost}"
    return hashlib.md5(cache_data.encode()).hexdigest()

def ensure_cache_dir() -> Path:
    """Ensure cache directory exists and return Path object"""
    cache_dir = Path(os.getenv("AUDIO_CACHE_DIR", "./audio_cache"))
    cache_dir.mkdir(exist_ok=True)
    return cache_dir

def cleanup_expired_cache():
    """Remove expired cache files based on TTL"""
    try:
        cache_enabled = os.getenv("AUDIO_CACHE_ENABLED", "true").lower() == "true"
        if not cache_enabled:
            return
            
        cache_dir = ensure_cache_dir()
        ttl_days = int(os.getenv("AUDIO_CACHE_TTL_DAYS", "5"))
        cutoff_time = datetime.now() - timedelta(days=ttl_days)
        
        for cache_file in cache_dir.glob("*.json"):
            if cache_file.stat().st_mtime < cutoff_time.timestamp():
                # Remove both metadata and audio file
                audio_file = cache_file.with_suffix(".mp3")
                cache_file.unlink(missing_ok=True)
                audio_file.unlink(missing_ok=True)
                logging.debug(f"🗑️ Removed expired cache: {cache_file.name}")
    except Exception as e:
        logging.warning(f"⚠️ Cache cleanup failed: {e}")

def manage_cache_size():
    """Ensure cache doesn't exceed maximum size"""
    try:
        cache_enabled = os.getenv("AUDIO_CACHE_ENABLED", "true").lower() == "true"
        if not cache_enabled:
            return
            
        cache_dir = ensure_cache_dir()
        max_size_mb = int(os.getenv("AUDIO_CACHE_MAX_SIZE_MB", "100"))
        max_size_bytes = max_size_mb * 1024 * 1024
        
        # Calculate current cache size
        total_size = sum(f.stat().st_size for f in cache_dir.iterdir() if f.is_file())
        
        if total_size > max_size_bytes:
            # Remove oldest files until under limit
            files = [(f, f.stat().st_mtime) for f in cache_dir.iterdir() if f.is_file()]
            files.sort(key=lambda x: x[1])  # Sort by modification time
            
            for file_path, _ in files:
                if total_size <= max_size_bytes:
                    break
                    
                file_size = file_path.stat().st_size
                file_path.unlink(missing_ok=True)
                total_size -= file_size
                logging.debug(f"🗑️ Removed cache file for size limit: {file_path.name}")
    except Exception as e:
        logging.warning(f"⚠️ Cache size management failed: {e}")

def get_cached_audio(cache_key: str) -> bytes:
    """Retrieve cached audio if available and valid"""
    try:
        cache_enabled = os.getenv("AUDIO_CACHE_ENABLED", "true").lower() == "true"
        if not cache_enabled:
            return None
            
        cache_dir = ensure_cache_dir()
        metadata_file = cache_dir / f"{cache_key}.json"
        audio_file = cache_dir / f"{cache_key}.mp3"
        
        if not (metadata_file.exists() and audio_file.exists()):
            return None
            
        # Check if cache is still valid (TTL)
        ttl_days = int(os.getenv("AUDIO_CACHE_TTL_DAYS", "5"))
        cutoff_time = datetime.now() - timedelta(days=ttl_days)
        
        if metadata_file.stat().st_mtime < cutoff_time.timestamp():
            return None
            
        # Read cached audio
        with open(audio_file, 'rb') as f:
            return f.read()
            
    except Exception as e:
        logging.debug(f"⚠️ Cache retrieval failed: {e}")
        return None

def save_audio_to_cache(cache_key: str, audio_data: bytes, text: str, voice_id: str, model_id: str):
    """Save audio data to cache with metadata"""
    try:
        cache_enabled = os.getenv("AUDIO_CACHE_ENABLED", "true").lower() == "true"
        if not cache_enabled:
            return
            
        cache_dir = ensure_cache_dir()
        metadata_file = cache_dir / f"{cache_key}.json"
        audio_file = cache_dir / f"{cache_key}.mp3"
        
        # Save metadata
        metadata = {
            "text": text,
            "voice_id": voice_id,
            "model_id": model_id,
            "created_at": datetime.now().isoformat(),
            "cache_key": cache_key
        }
        
        with open(metadata_file, 'w') as f:
            json.dump(metadata, f, indent=2)
            
        # Save audio data
        with open(audio_file, 'wb') as f:
            f.write(audio_data)
            
        logging.debug(f"💾 Cached audio: {cache_key}")
        
        # Manage cache size after adding new file
        manage_cache_size()
        
    except Exception as e:
        logging.warning(f"⚠️ Cache save failed: {e}")

# Speech Markup Parsing for Enhanced Realism
def parse_speech_markup(text: str) -> str:
    """
    Parse AI response text for action descriptions and convert them to ElevenLabs SSML markup
    for more realistic speech synthesis.
    """
    import re
    
    # Dictionary mapping common actions to ElevenLabs SSML or pauses
    action_mappings = {
        # Throat clearing and breathing
        r'\*clears throat\*': '<break time="0.5s"/>',
        r'\*coughs\*': '<break time="0.3s"/>',
        r'\*sighs\*': '<break time="0.7s"/>',
        r'\*takes a breath\*': '<break time="0.4s"/>',
        r'\*breathes\*': '<break time="0.4s"/>',
        
        # Pauses and thinking
        r'\*pauses\*': '<break time="1.0s"/>',
        r'\*thinks\*': '<break time="0.8s"/>',
        r'\*considers\*': '<break time="0.6s"/>',
        r'\*hesitates\*': '<break time="0.5s"/>',
        
        # Emotional expressions
        r'\*chuckles\*': '<break time="0.3s"/>',
        r'\*laughs\*': '<break time="0.4s"/>',
        r'\*smiles\*': '',  # No audio break, just remove the text
        r'\*grins\*': '',
        
        # Professional sounds
        r'\*ahem\*': '<break time="0.3s"/>',
        r'\*hmm\*': '<prosody rate="slow">Hmm</prosody><break time="0.3s"/>',
        r'\*ah\*': '<prosody rate="slow">Ah</prosody><break time="0.2s"/>',
        r'\*oh\*': '<prosody rate="slow">Oh</prosody><break time="0.2s"/>',
        
        # Emphasis and tone changes
        r'\*whispers\*': '<prosody volume="soft">',
        r'\*/whispers\*': '</prosody>',
        r'\*speaks quietly\*': '<prosody volume="soft">',
        r'\*/speaks quietly\*': '</prosody>',
        r'\*emphasizes\*': '<prosody rate="slow" pitch="+5%">',
        r'\*/emphasizes\*': '</prosody>',
    }
    
    # Apply all mappings
    processed_text = text
    for pattern, replacement in action_mappings.items():
        processed_text = re.sub(pattern, replacement, processed_text, flags=re.IGNORECASE)
    
    # Clean up any remaining action descriptions in asterisks
    processed_text = re.sub(r'\*[^*]+\*', '', processed_text)
    
    # Clean up extra whitespace
    processed_text = re.sub(r'\s+', ' ', processed_text).strip()
    
    # Wrap in SSML speak tags if we have SSML markup
    if '<' in processed_text and '>' in processed_text:
        processed_text = f'<speak>{processed_text}</speak>'
    
    logging.debug(f"🎙️ Speech markup - Original: {text[:100]}...")
    logging.debug(f"🎙️ Speech markup - Processed: {processed_text[:100]}...")
    
    return processed_text

# TTS setup
def speak_text(text: str):
    try:
        # Parse speech markup for enhanced realism
        processed_text = parse_speech_markup(text)
        
        # Get ElevenLabs configuration from environment variables
        elevenlabs_api_key = os.getenv("ELEVENLABS_API_KEY")
        elevenlabs_voice_id = os.getenv("ELEVENLABS_VOICE_ID")
        elevenlabs_model_id = os.getenv("ELEVENLABS_MODEL_ID", "eleven_monolingual_v1")  # Default fallback
        
        # Voice settings from environment variables
        elevenlabs_stability = float(os.getenv("ELEVENLABS_STABILITY", "0.5"))
        elevenlabs_similarity_boost = float(os.getenv("ELEVENLABS_SIMILARITY_BOOST", "0.5"))
        
        if not elevenlabs_api_key:
            logging.error("❌ ElevenLabs API key not found in environment variables")
            return
            
        if not elevenlabs_voice_id:
            logging.error("❌ ElevenLabs voice ID not found in environment variables")
            return
        
        logging.info(f"🎙️ Using ElevenLabs voice: {elevenlabs_voice_id}, model: {elevenlabs_model_id}")
        logging.debug(f"🎵 Voice settings - Stability: {elevenlabs_stability}, Similarity: {elevenlabs_similarity_boost}")
        
        # Cleanup expired cache periodically
        cleanup_expired_cache()
        
        # Generate cache key for this TTS request (use processed text for caching)
        cache_key = get_cache_key(processed_text, elevenlabs_voice_id, elevenlabs_model_id, elevenlabs_stability, elevenlabs_similarity_boost)
        
        # Try to get cached audio first
        cached_audio = get_cached_audio(cache_key)
        if cached_audio:
            logging.info(f"💾 Using cached audio for: {text[:50]}...")
            audio_data = cached_audio
        else:
            # Generate audio using ElevenLabs API with processed text
            logging.info(f"🌐 Generating new audio via API for: {text[:50]}...")
            client = ElevenLabs(api_key=elevenlabs_api_key)
            
            # Use processed text with SSML markup for more realistic speech
            audio = client.text_to_speech.convert(
                voice_id=elevenlabs_voice_id,  # Voice ID from environment variable
                text=processed_text,  # Use processed text with SSML markup
                model_id=elevenlabs_model_id  # Model ID from environment variable
            )
            
            # Convert audio generator to bytes
            audio_data = b''.join(audio)
            
            # Save to cache for future use (using processed text)
            save_audio_to_cache(cache_key, audio_data, processed_text, elevenlabs_voice_id, elevenlabs_model_id)
        
        # Play the audio (either cached or newly generated)
        import io
        import pygame
        
        # Initialize pygame mixer for audio playback
        pygame.mixer.init()
        
        # Convert audio bytes to a file-like object and play
        audio_io = io.BytesIO(audio_data)
        pygame.mixer.music.load(audio_io)
        pygame.mixer.music.play()
        
        # Wait for playback to finish
        while pygame.mixer.music.get_busy():
            time.sleep(0.1)
            
        time.sleep(0.3)
    except Exception as e:
        logging.error(f"❌ TTS failed: {e}")

# Main interaction loop
def write():
    conversation_mode = False
    last_interaction_time = None

    try:
        with mic as source:
            recognizer.adjust_for_ambient_noise(source)
            while True:
                try:
                    if not conversation_mode:
                        logging.info("🎤 Listening for wake word...")
                        audio = recognizer.listen(source, timeout=10)
                        transcript = recognizer.recognize_google(audio)
                        logging.info(f"🗣 Heard: {transcript}")

                        if TRIGGER_WORD.lower() in transcript.lower():
                            logging.info(f"🗣 Triggered by: {transcript}")
                            speak_text("Yes, boss?")
                            conversation_mode = True
                            last_interaction_time = time.time()
                        else:
                            logging.debug("Wake word not detected, continuing...")
                    else:
                        logging.info("🎤 Listening for next command...")
                        audio = recognizer.listen(source, timeout=10)
                        command = recognizer.recognize_google(audio)
                        logging.info(f"📥 Command: {command}")

                        logging.info("🤖 Sending command to agent...")
                        response = executor.invoke({"input": command})
                        content = response["output"]
                        logging.info(f"✅ Agent responded: {content}")

                        print("Jarvis:", content)
                        speak_text(content)
                        last_interaction_time = time.time()

                        if time.time() - last_interaction_time > CONVERSATION_TIMEOUT:
                            logging.info("⌛ Timeout: Returning to wake word mode.")
                            conversation_mode = False

                except sr.WaitTimeoutError:
                    logging.warning("⚠️ Timeout waiting for audio.")
                    if conversation_mode and time.time() - last_interaction_time > CONVERSATION_TIMEOUT:
                        logging.info("⌛ No input in conversation mode. Returning to wake word mode.")
                        conversation_mode = False
                except sr.UnknownValueError:
                    logging.warning("⚠️ Could not understand audio.")
                except Exception as e:
                    logging.error(f"❌ Error during recognition or tool call: {e}")
                    time.sleep(1)

    except Exception as e:
        logging.critical(f"❌ Critical error in main loop: {e}")

if __name__ == "__main__":
    write()
