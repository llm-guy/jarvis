import sys
from typing import Type
from langchain.tools import BaseTool

def shutdown_assistant() -> str:
    sys.exit(0)
    return ""  # This won't be reached due to exit

class ShutdownTool(BaseTool):
    name: str = "shutdown"
    description: str = "Shuts down Jarvis immediately when user says shut down"
    
    def _run(self) -> str:
        return shutdown_assistant()
    
    def _arun(self) -> str:
        raise NotImplementedError("Async not implemented")

shutdown = ShutdownTool()
