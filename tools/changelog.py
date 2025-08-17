from langchain.tools import BaseTool
import os
import re
from typing import Optional

def get_changelog() -> str:
    """Read the changelog from README.md"""
    try:
        readme_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "README.md")
        with open(readme_path, 'r', encoding='utf-8') as f:
            content = f.read()
            # Find the changelog section
            changelog_match = re.search(r'## 📋 Changelog\n\n(.*?)(?=\n\n---)', content, re.DOTALL)
            if changelog_match:
                return changelog_match.group(1).strip()
            return "Changelog not found in README.md"
    except Exception as e:
        return f"Error reading changelog: {str(e)}"

def get_current_version() -> Optional[str]:
    """Get the current version number from the changelog"""
    changelog = get_changelog()
    version_match = re.search(r'### Version (\d+\.\d+\.\d+)', changelog)
    if version_match:
        return version_match.group(1)
    return None

class ChangelogTool(BaseTool):
    name: str = "changelog"
    description: str = "Retrieves information about my own version history and updates. Use this when someone asks what version I (Jarvis) am, what features I have, or what has changed in my recent updates. This is about my own changelog, not system or other program changes."
    
    def _run(self, query: str = "") -> str:
        changelog = get_changelog()
        current_version = get_current_version()
        
        response = f"Current version: {current_version}\n\n"
        response += "Recent changes:\n" + changelog
        return response
    
    def _arun(self, query: str = "") -> str:
        raise NotImplementedError("Async not implemented")

changelog = ChangelogTool()
