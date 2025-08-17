import os
import sys
import logging
import time
import pyttsx3
from dotenv import load_dotenv
import speech_recognition as sr
from langchain_ollama import ChatOllama, OllamaLLM
# from langchain_openai import ChatOpenAI # if you want to use openai
from langchain_core.messages import HumanMessage
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_core.prompts import ChatPromptTemplate
from tools.time import get_time
from tools.screenshot import take_screenshot
from tools.matrix import matrix_mode
from tools.web_search import google_search
from tools.shutdown import shutdown
from tools.app_launcher import app_launcher
from tools.changelog import changelog


load_dotenv()

MIC_INDEX = 0
TRIGGER_WORD = "jarvis"
CONVERSATION_TIMEOUT = 30  # seconds of inactivity before exiting conversation mode

logging.basicConfig(level=logging.DEBUG) # logging

# api_key = os.getenv("OPENAI_API_KEY") removed because it's not needed for ollama
# org_id = os.getenv("OPENAI_ORG_ID") removed because it's not needed for ollama

recognizer = sr.Recognizer()
mic = sr.Microphone(device_index=MIC_INDEX)

# Initialize LLM
llm = ChatOllama(model="qwen3:1.7b", reasoning=False)

# llm = ChatOpenAI(model="gpt-4o-mini", api_key=api_key, organization=org_id) for openai

# Tool list
tools = [get_time, matrix_mode, take_screenshot, google_search, shutdown, app_launcher, changelog]

# Tool-calling prompt
prompt = ChatPromptTemplate.from_messages([
    ("system", """You are Jarvis, an intelligent, conversational AI assistant, currently in version 1.4.0. Your goal is to be helpful, friendly, and informative. 
    
When asked about your version, updates, or changes, use the changelog tool to tell users about YOUR OWN updates and features - not about the computer's updates. You should be proud of your features and openly share what's new in your latest versions.

For example:
- If someone asks "what version are you?", use the changelog tool to tell them about your current version
- If someone asks "what's new?", tell them about your latest features and updates
- If someone asks about changes, tell them about your own development progress

Always explain your reasoning simply when appropriate, and keep your responses conversational and concise."""),
    ("human", "{input}"),
    ("placeholder", "{agent_scratchpad}")
])

# Agent + executor
agent = create_tool_calling_agent(llm=llm, tools=tools, prompt=prompt)
executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

# TTS setup
def speak_text(text: str):
    engine = None
    try:
        # Temporarily reduce logging level for pyttsx3 and comtypes
        logging_level = logging.getLogger().getEffectiveLevel()
        comtypes_logger = logging.getLogger('comtypes')
        pyttsx3_logger = logging.getLogger('pyttsx3')
        loggers_state = {
            'root': logging_level,
            'comtypes': comtypes_logger.level,
            'pyttsx3': pyttsx3_logger.level
        }
        
        # Set all relevant loggers to ERROR level
        logging.getLogger().setLevel(logging.ERROR)
        comtypes_logger.setLevel(logging.ERROR)
        pyttsx3_logger.setLevel(logging.ERROR)
        
        engine = pyttsx3.init()
        voices = engine.getProperty('voices')
        
        # Try to find the best voice for clear speech
        selected_voice = None
        preferred_voices = ['david', 'james', 'mark']  # List of preferred voice names
        
        # First try to find one of our preferred voices
        for voice in voices:
            if any(preferred in voice.name.lower() for preferred in preferred_voices):
                selected_voice = voice
                break
        
        # If no preferred voice found, try to find any English voice
        if not selected_voice:
            for voice in voices:
                if 'en' in voice.languages[0].lower():
                    selected_voice = voice
                    break
        
        # If still no voice found, use the first available voice
        if not selected_voice and voices:
            selected_voice = voices[0]
        
        if selected_voice:
            engine.setProperty('voice', selected_voice.id)
            
        # Optimize speech settings for clarity
        engine.setProperty('rate', 150)  # Slower rate for better clarity
        engine.setProperty('volume', 1.0)
        
        # Restore all logging levels
        logging.getLogger().setLevel(loggers_state['root'])
        comtypes_logger.setLevel(loggers_state['comtypes'])
        pyttsx3_logger.setLevel(loggers_state['pyttsx3'])
        
        # Add slight pauses around punctuation for better speech rhythm
        # Add pauses around punctuation for better speech rhythm
        text = text.replace(',', ', ')
        text = text.replace('.', '. ')
        text = text.replace('!', '! ')
        text = text.replace('?', '? ')
        
        try:
            engine.say(text)
            engine.runAndWait()
            time.sleep(0.5)  # Slightly longer pause between sentences
        except KeyboardInterrupt:
            # Handle ctrl+c gracefully
            if engine:
                engine.stop()
            raise
        except Exception as e:
            logging.error(f"❌ TTS failed: {e}")
            print(f"Jarvis (text only): {text}")  # Fallback to text if speech fails
    finally:
        if engine:
            engine.stop()  # Ensure engine is properly stopped
            del engine    # Clean up the engine object

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
                            speak_text("Yes sir?")
                            conversation_mode = True
                            last_interaction_time = time.time()
                        else:
                            logging.debug("Wake word not detected, continuing...")
                    else:
                        logging.info("🎤 Listening for next command...")
                        audio = recognizer.listen(source, timeout=10)
                        command = recognizer.recognize_google(audio)
                        logging.info(f"📥 Command: {command}")

                        # Check for direct shutdown command first
                        if "shut down" in command.lower():
                            logging.info("🔌 Shutdown command received. Terminating...")
                            sys.exit(0)
                            
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
