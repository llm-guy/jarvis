#!/usr/bin/env python3
"""
Quick test of Jarvis agent with tools
"""

import os
import sys
from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain.agents import create_tool_calling_agent, AgentExecutor

# Add tools
sys.path.append('.')
from tools.time import get_time
from tools.system_info import get_system_info
from tools.calculator import calculate

def test_agent():
    print("🤖 Testing Jarvis Agent with Tools")
    print("=" * 50)
    
    # Initialize LLM
    llm = ChatOllama(model="qwen3:1.7b", reasoning=False)
    
    # Simple tools list
    tools = [get_time, get_system_info, calculate]
    
    # Simple prompt
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are Jarvis. When users ask for time, use get_time tool. When they ask about system info, use get_system_info tool. When they ask calculations, use calculate tool. Be direct and use the tools."),
        ("human", "{input}"),
        ("placeholder", "{agent_scratchpad}")
    ])
    
    # Create agent
    agent = create_tool_calling_agent(llm=llm, tools=tools, prompt=prompt)
    executor = AgentExecutor(agent=agent, tools=tools, verbose=True)
    
    # Test commands
    test_commands = [
        "What time is it in New York?",
        "Check my system status",
        "Calculate 25 * 4"
    ]
    
    for cmd in test_commands:
        print(f"\n🗣️ Testing: {cmd}")
        print("-" * 30)
        try:
            response = executor.invoke({"input": cmd})
            print(f"✅ Response: {response['output']}")
        except Exception as e:
            print(f"❌ Error: {e}")
        print()

if __name__ == "__main__":
    test_agent()
