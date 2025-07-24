import os
import logging
import time
import pyttsx3
from dotenv import load_dotenv
import speech_recognition as sr
from langchain_ollama import ChatOllama, OllamaLLM
from langchain_core.messages import HumanMessage
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_core.prompts import ChatPromptTemplate
from tools.time import get_time 
from tools.video_day import video_day

load_dotenv()

MIC_INDEX = 0
TRIGGER_WORD = "jarvis"
CONVERSATION_TIMEOUT = 30  # seconds of inactivity before exiting conversation mode

logging.basicConfig(level=logging.INFO)

# Global variables
recognizer = sr.Recognizer()
mic = None
tts_engine = None

# Initialize LLM
llm = ChatOllama(model="qwen2.5:1.5b", reasoning=False)

# Tool list
tools = [get_time, video_day]

# Tool-calling prompt
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are Jarvis, an intelligent, conversational AI assistant. Your goal is to be helpful, friendly, and informative. You can respond in natural, human-like language and use tools when needed to answer questions more accurately. Always explain your reasoning simply when appropriate, and keep your responses conversational and concise."),
    ("human", "{input}"),
    ("placeholder", "{agent_scratchpad}")
])

# Agent + executor
agent = create_tool_calling_agent(llm=llm, tools=tools, prompt=prompt)
executor = AgentExecutor(agent=agent, tools=tools, verbose=False)

def safe_tts_init():
    """Safely initialize TTS engine"""
    global tts_engine
    try:
        if tts_engine is None:
            logging.info("🔊 Initializing TTS engine...")
            tts_engine = pyttsx3.init()
            if tts_engine:
                voices = tts_engine.getProperty('voices')
                if voices:
                    for voice in voices:
                        if "jamie" in voice.name.lower():
                            tts_engine.setProperty('voice', voice.id)
                            break
                tts_engine.setProperty('rate', 180)
                tts_engine.setProperty('volume', 1.0)
                logging.info("✅ TTS engine initialized")
                return True
            else:
                logging.error("❌ TTS engine is None after init")
                return False
    except Exception as e:
        logging.error(f"❌ TTS initialization failed: {e}")
        tts_engine = None
        return False
    return tts_engine is not None

def safe_speak(text: str):
    """Safely speak text"""
    global tts_engine
    try:
        if tts_engine is None:
            if not safe_tts_init():
                logging.error("❌ Cannot speak - TTS not available")
                return
        
        if tts_engine:
            tts_engine.say(text)
            tts_engine.runAndWait()
            time.sleep(0.3)
    except Exception as e:
        logging.error(f"❌ Speech failed: {e}")
        tts_engine = None

def list_microphones():
    """List available microphones"""
    try:
        logging.info("🎤 Available microphones:")
        for index, name in enumerate(sr.Microphone.list_microphone_names()):
            logging.info(f"  {index}: {name}")
    except Exception as e:
        logging.error(f"❌ Could not list microphones: {e}")

def safe_mic_init():
    """Safely initialize microphone with fallback options"""
    global mic
    
    list_microphones()
    
    # Try different microphone indices - prioritize MacBook Pro Microphone
    mic_indices_to_try = [2, 0, 1, None]  # MacBook Pro Microphone, C34H89x, Logitech BRIO, default
    
    for mic_index in mic_indices_to_try:
        try:
            logging.info(f"🎤 Trying microphone index: {mic_index}")
            
            # Create microphone object
            if mic_index is None:
                mic = sr.Microphone()
            else:
                mic = sr.Microphone(device_index=mic_index)
            
            # Test the microphone by using it briefly
            logging.info("🔧 Testing microphone...")
            with mic as source:
                recognizer.adjust_for_ambient_noise(source, duration=0.5)
            
            logging.info(f"✅ Microphone initialized successfully with index {mic_index}")
            return True
            
        except Exception as e:
            logging.warning(f"⚠️ Microphone index {mic_index} failed: {e}")
            mic = None
            continue
    
    logging.error("❌ All microphone initialization attempts failed")
    return False

def safe_cleanup():
    """Safely cleanup resources"""
    global tts_engine, mic
    try:
        if tts_engine:
            try:
                tts_engine.stop()
            except:
                pass
            tts_engine = None
        mic = None
        logging.info("🧹 Cleanup completed")
    except Exception as e:
        logging.error(f"❌ Cleanup error: {e}")

def main_loop():
    """Main interaction loop with better error handling"""
    conversation_mode = False
    last_interaction_time = None

    # Initialize components
    if not safe_mic_init():
        logging.critical("❌ Failed to initialize microphone. Exiting.")
        return
    
    if not safe_tts_init():
        logging.warning("⚠️ TTS not available, continuing without speech")

    try:
        if mic is None:
            logging.critical("❌ Microphone is None, cannot continue")
            return
            
        logging.info("🚀 Jarvis is ready! Say 'Jarvis' to activate.")
        
        with mic as source:
            while True:
                try:
                    if not conversation_mode:
                        logging.info("🎤 Listening for wake word...")
                        audio = recognizer.listen(source, timeout=10)
                        transcript = recognizer.recognize_google(audio)
                        logging.info(f"🗣 Heard: {transcript}")

                        if TRIGGER_WORD.lower() in transcript.lower():
                            logging.info(f"🗣 Triggered by: {transcript}")
                            safe_speak("Yes sir?")
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
                        safe_speak(content)
                        last_interaction_time = time.time()

                        if time.time() - last_interaction_time > CONVERSATION_TIMEOUT:
                            logging.info("⌛ Timeout: Returning to wake word mode.")
                            conversation_mode = False

                except sr.WaitTimeoutError:
                    logging.warning("⚠️ Timeout waiting for audio.")
                    if conversation_mode and last_interaction_time and time.time() - last_interaction_time > CONVERSATION_TIMEOUT:
                        logging.info("⌛ No input in conversation mode. Returning to wake word mode.")
                        conversation_mode = False
                except sr.UnknownValueError:
                    logging.warning("⚠️ Could not understand audio.")
                except Exception as e:
                    logging.error(f"❌ Error during recognition or tool call: {e}")
                    time.sleep(1)

    except KeyboardInterrupt:
        logging.info("🛑 Interrupted by user")
    except Exception as e:
        logging.critical(f"❌ Critical error in main loop: {e}")
        import traceback
        traceback.print_exc()
    finally:
        safe_cleanup()

if __name__ == "__main__":
    main_loop()
