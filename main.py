import os
import sys
import logging
import time
import pyttsx3
from dotenv import load_dotenv
import speech_recognition as sr
from langchain_ollama import ChatOllama, OllamaLLM
from langchain_core.messages import HumanMessage
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.tools import tool
from tools.time import get_time
from tools.screenshot import take_screenshot
from tools.matrix import matrix_mode
from tools.web_search import google_search
from tools.shutdown import shutdown
from tools.app_launcher import app_launcher
from tools.changelog import changelog
from tools.Pc_Controller import PCController

load_dotenv()

MIC_INDEX = 0
TRIGGER_WORD = "jarvis"
CONVERSATION_TIMEOUT = 30  # seconds of inactivity before exiting conversation mode

# Configure logging with UTF-8 encoding
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('jarvis.log', encoding='utf-8'),
        logging.StreamHandler(sys.stdout)
    ]
)

# Fix encoding for Windows console
if sys.platform == "win32":
    try:
        import codecs
        sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
        sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')
    except:
        pass  # Fallback if encoding fix fails

recognizer = sr.Recognizer()
mic = sr.Microphone(device_index=MIC_INDEX)

# Initialize LLM
llm = ChatOllama(model="qwen3:1.7b", reasoning=False)

# Initialize PC Controller
pc_controller = PCController()

@tool
def pc_control(action: str, path: str = None, filename: str = None, command: str = None, power_action: str = None, target: str = None):
    """Control PC operations using the PC Controller. Available actions: system_info, process_list, file_list, screenshot, run_command, power_control, network_ping, install_deps"""
    try:
        if action == "system_info":
            return str(pc_controller.get_system_info())
        elif action == "process_list":
            result = pc_controller.process_control("list")
            return str(result)
        elif action == "file_list":
            result = pc_controller.file_operations("list", path or ".")
            return str(result)
        elif action == "screenshot":
            result = pc_controller.screenshot(filename)
            return str(result)
        elif action == "run_command":
            result = pc_controller.run_command(command)
            return str(result)
        elif action == "power_control":
            result = pc_controller.power_control(power_action)
            return str(result)
        elif action == "network_ping":
            result = pc_controller.network_operations("ping", target)
            return str(result)
        elif action == "install_deps":
            result = pc_controller.install_dependencies()
            return str(result)
        else:
            return f"Unknown action: {action}"
    except Exception as e:
        return f"Error: {str(e)}"

# Tool list
tools = [get_time, matrix_mode, take_screenshot, google_search, shutdown, app_launcher, changelog, pc_control]

# Tool-calling prompt
prompt = ChatPromptTemplate.from_messages([
    ("system", """You are Jarvis, an intelligent, conversational AI assistant, currently in version 1.4.0. Your goal is to be helpful, friendly, and informative. 
    
You now have access to a comprehensive PC Controller tool that can:
- Get system information
- Control processes and services
- Manage files and directories
- Perform network operations
- Take screenshots
- Execute system commands
- Control system power
- Monitor system resources
- Install missing dependencies

When asked about your version, updates, or changes, use the changelog tool to tell users about YOUR OWN updates and features - not about the computer's updates. You should be proud of your features and openly share what's new in your latest versions.

You can use the pc_control tool to help users with system management tasks. Always explain your reasoning simply when appropriate, and keep your responses conversational and concise."""),
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
        preferred_voices = ['david', 'james', 'mark']
        
        for voice in voices:
            if any(preferred in voice.name.lower() for preferred in preferred_voices):
                selected_voice = voice
                break
        
        if not selected_voice:
            for voice in voices:
                if 'en' in voice.languages[0].lower():
                    selected_voice = voice
                    break
        
        if not selected_voice and voices:
            selected_voice = voices[0]
        
        if selected_voice:
            engine.setProperty('voice', selected_voice.id)
            
        engine.setProperty('rate', 150)
        engine.setProperty('volume', 1.0)
        
        # Restore all logging levels
        logging.getLogger().setLevel(loggers_state['root'])
        comtypes_logger.setLevel(loggers_state['comtypes'])
        pyttsx3_logger.setLevel(loggers_state['pyttsx3'])
        
        # Clean text for speech
        text = text.replace(',', ', ')
        text = text.replace('.', '. ')
        text = text.replace('!', '! ')
        text = text.replace('?', '? ')
        
        try:
            engine.say(text)
            engine.runAndWait()
            time.sleep(0.5)
        except KeyboardInterrupt:
            if engine:
                engine.stop()
            raise
        except Exception as e:
            logging.error(f"TTS failed: {e}")
            print(f"Jarvis (text only): {text}")
    finally:
        if engine:
            engine.stop()
            del engine

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
                        logging.info("Listening for wake word...")
                        audio = recognizer.listen(source, timeout=10)
                        transcript = recognizer.recognize_google(audio)
                        logging.info(f"Heard: {transcript}")

                        if TRIGGER_WORD.lower() in transcript.lower():
                            logging.info(f"Triggered by: {transcript}")
                            speak_text("Yes sir?")
                            conversation_mode = True
                            last_interaction_time = time.time()
                        else:
                            logging.debug("Wake word not detected, continuing...")
                    else:
                        logging.info("Listening for next command...")
                        audio = recognizer.listen(source, timeout=10)
                        command = recognizer.recognize_google(audio)
                        logging.info(f"Command: {command}")

                        # Check for direct shutdown command first
                        if "shut down" in command.lower():
                            logging.info("Shutdown command received. Terminating...")
                            sys.exit(0)
                            
                        logging.info("Sending command to agent...")
                        response = executor.invoke({"input": command})
                        content = response["output"]
                        logging.info(f"Agent responded: {content}")

                        print("Jarvis:", content)
                        speak_text(content)
                        last_interaction_time = time.time()

                        if time.time() - last_interaction_time > CONVERSATION_TIMEOUT:
                            logging.info("Timeout: Returning to wake word mode.")
                            conversation_mode = False

                except sr.WaitTimeoutError:
                    logging.warning("Timeout waiting for audio.")
                    if conversation_mode and time.time() - last_interaction_time > CONVERSATION_TIMEOUT:
                        logging.info("No input in conversation mode. Returning to wake word mode.")
                        conversation_mode = False
                except sr.UnknownValueError:
                    logging.warning("Could not understand audio.")
                except Exception as e:
                    logging.error(f"Error during recognition or tool call: {e}")
                    time.sleep(1)

    except Exception as e:
        logging.critical(f"Critical error in main loop: {e}")

if __name__ == "__main__":
    write()
