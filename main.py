import os
import logging
import time
import pyttsx3
import re
from dotenv import load_dotenv
import speech_recognition as sr
from langchain_ollama import ChatOllama, OllamaLLM
# from langchain_openai import ChatOpenAI # if you want to use openai
from langchain_core.messages import HumanMessage
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_core.prompts import ChatPromptTemplate
from tools.time import get_time 

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
tools = [get_time]

# Tool-calling prompt
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are Jarvis, an intelligent, conversational AI assistant. Your goal is to be helpful, friendly, and informative. You can respond in natural, human-like language and use tools when needed to answer questions more accurately. Always explain your reasoning simply when appropriate, and keep your responses conversational and concise."),
    ("human", "{input}"),
    ("placeholder", "{agent_scratchpad}")
])

# Agent + executor
agent = create_tool_calling_agent(llm=llm, tools=tools, prompt=prompt)
executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

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

# TTS setup
def speak_text(text: str):
    try:
        # Clean text for speech
        clean_text = clean_text_for_speech(text)
        
        if not clean_text.strip():
            logging.warning("⚠️ No speakable text after cleaning")
            return
        
        engine = pyttsx3.init()
        for voice in engine.getProperty('voices'):
            if "jamie" in voice.name.lower():
                engine.setProperty('voice', voice.id)
                break
        engine.setProperty('rate', 180)
        engine.setProperty('volume', 1.0)
        engine.say(clean_text)
        engine.runAndWait()
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
