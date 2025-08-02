#!/usr/bin/env python3
"""
Quick text-only test of Jarvis - no microphone needed
"""

from langchain_ollama import ChatOllama
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_core.prompts import ChatPromptTemplate
from tools.time import get_time
from tools.system_info import get_system_info
from tools.calculator import calculate

# Initialize LLM
llm = ChatOllama(model="qwen3:1.7b", reasoning=False)

# Tools
tools = [get_time, get_system_info, calculate]

# Simple direct prompt
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are Jarvis. When users ask for time, use get_time tool. When they ask about system info, use get_system_info tool. When they ask calculations, use calculate tool. Always use the appropriate tools."),
    ("human", "{input}"),
    ("placeholder", "{agent_scratchpad}")
])

# Create agent
agent = create_tool_calling_agent(llm=llm, tools=tools, prompt=prompt)
executor = AgentExecutor(agent=agent, tools=tools, verbose=False)

print("🤖 Jarvis Text Mode - Type your commands:")
print("Try: 'what time is it in new york', 'check system status', 'calculate 25*4'")
print("Type 'quit' to exit\n")

while True:
    try:
        user_input = input("You: ").strip()
        if user_input.lower() in ['quit', 'exit']:
            break
        
        if user_input:
            response = executor.invoke({"input": user_input})
            print(f"Jarvis: {response['output']}\n")
            
    except KeyboardInterrupt:
        print("\nGoodbye!")
        break
    except Exception as e:
        print(f"Error: {e}\n")
