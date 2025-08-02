#!/usr/bin/env python3
"""
Simple text-based Jarvis for testing without microphone
"""

import os
import logging
from dotenv import load_dotenv
from langchain_ollama import ChatOllama
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_core.prompts import ChatPromptTemplate
from tools.time import get_time
from tools.weather import get_weather
from tools.system_info import get_system_info, get_battery_status
from tools.file_manager import list_files, create_directory, get_file_info
from tools.calculator import calculate, convert_units
from tools.search import search_web, get_news_headlines

load_dotenv()

logging.basicConfig(level=logging.INFO)

def main():
    """Run Jarvis in text-only mode"""
    print("🤖 Jarvis Text Mode")
    print("Type 'exit' to quit")
    print("-" * 40)
    
    # Initialize LLM
    try:
        llm = ChatOllama(model="qwen3:1.7b", reasoning=False)
        print("✅ AI model loaded successfully")
    except Exception as e:
        print(f"❌ Failed to load AI model: {e}")
        return
    
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
        ("system", "You are Jarvis, an intelligent, conversational AI assistant. Your goal is to be helpful, friendly, and informative. You can respond in natural, human-like language and use tools when needed to answer questions more accurately. Always explain your reasoning simply when appropriate, and keep your responses conversational and concise."),
        ("human", "{input}"),
        ("placeholder", "{agent_scratchpad}")
    ])
    
    # Agent + executor
    agent = create_tool_calling_agent(llm=llm, tools=tools, prompt=prompt)
    executor = AgentExecutor(agent=agent, tools=tools, verbose=False)
    
    while True:
        try:
            user_input = input("\nYou: ").strip()
            
            if user_input.lower() in ['exit', 'quit', 'bye', 'goodbye']:
                print("👋 Goodbye!")
                break
            
            if user_input:
                print("🤖 Thinking...")
                try:
                    response = executor.invoke({"input": user_input})
                    content = response["output"]
                    print(f"🤖 Jarvis: {content}")
                except Exception as e:
                    print(f"❌ Error: {e}")
                    
        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()
