#!/usr/bin/env python3
"""
Simple text-based Jarvis for testing - bypasses voice recognition issues
"""

import os
import logging
from dotenv import load_dotenv
from langchain_ollama import ChatOllama
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_core.prompts import ChatPromptTemplate

# Import tools
from tools.time import get_time
from tools.weather import get_weather
from tools.system_info import get_system_info, get_battery_status
from tools.file_manager import list_files, create_directory, get_file_info
from tools.calculator import calculate, convert_units
from tools.search import search_web, get_news_headlines

load_dotenv()

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

print("🤖 Jarvis Text Mode - Testing Agent & Tools")
print("=" * 50)
print("This bypasses voice recognition to test if the AI agent works properly.")
print("Type your commands directly. Type 'exit' to quit.")
print()

# Initialize LLM
llm = ChatOllama(model="qwen3:1.7b", reasoning=False)

# Tool list
tools = [
    get_time,
    get_weather, 
    get_system_info,
    get_battery_status,
    list_files,
    create_directory,
    get_file_info,
    calculate,
    convert_units,
    search_web,
    get_news_headlines
]

# Tool-calling prompt
prompt = ChatPromptTemplate.from_messages([
    ("system", """You are Jarvis, an intelligent AI assistant with access to specialized tools. 

CRITICAL INSTRUCTIONS:
1. When users ask for specific information (time, weather, system status, calculations, etc.), YOU MUST use the appropriate tools
2. DO NOT provide generic responses like "Hello! I'm Jarvis" repeatedly 
3. Actually PROCESS user requests and use tools to get real information
4. If asked about time, use get_time tool
5. If asked about weather, use get_weather tool  
6. If asked about system status, use get_system_info tool
7. If asked calculations, use calculate tool
8. Always try to fulfill the user's specific request with available tools

Available tools: get_time, get_weather, get_system_info, get_battery_status, list_files, create_directory, get_file_info, calculate, convert_units, search_web, get_news_headlines

Respond helpfully and use tools when the user asks for specific information."""),
    ("human", "{input}"),
    ("placeholder", "{agent_scratchpad}")
])

# Create agent
agent = create_tool_calling_agent(llm=llm, tools=tools, prompt=prompt)
executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

def main():
    print("🎯 Ready! Try these test commands:")
    print("   - 'What time is it in New York?'")
    print("   - 'Check my system status'")
    print("   - 'Calculate 25 * 4 + 10'")
    print("   - 'List files in current directory'")
    print()
    
    while True:
        try:
            user_input = input("You: ").strip()
            
            if user_input.lower() in ['exit', 'quit', 'bye', 'stop']:
                print("👋 Goodbye!")
                break
                
            if not user_input:
                continue
                
            print("\n🤖 Processing your request...")
            print("-" * 30)
            
            try:
                response = executor.invoke({"input": user_input})
                content = response["output"]
                print(f"\nJarvis: {content}")
                
            except Exception as agent_error:
                print(f"❌ Agent error: {agent_error}")
                print("Jarvis: I'm having trouble processing that request. Could you try again?")
                
            print()
            
        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()
