import os
import subprocess
from typing import Optional, Dict
from langchain.tools import BaseTool

# Dictionary of common apps and their default paths
DEFAULT_APPS = {
    "steam": r"C:\Program Files (x86)\Steam\steam.exe",
    "discord": r"C:\Users\%USERNAME%\AppData\Local\Discord\app-1.0.9013\Discord.exe",
    "chrome": r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    "firefox": r"C:\Program Files\Mozilla Firefox\firefox.exe",
    "spotify": r"C:\Users\%USERNAME%\AppData\Roaming\Spotify\Spotify.exe",
    "vscode": r"C:\Users\%USERNAME%\AppData\Local\Programs\Microsoft VS Code\Code.exe",
    "notepad": r"C:\Windows\system32\notepad.exe",
    "calculator": r"C:\Windows\System32\calc.exe"
}

def open_app(app_name: str) -> str:
    """Opens an application based on the given name."""
    app_name = app_name.lower()
    
    # Expand environment variables in paths
    for key, path in DEFAULT_APPS.items():
        DEFAULT_APPS[key] = os.path.expandvars(path)
    
    # Check if app is in our default list
    if app_name in DEFAULT_APPS:
        app_path = DEFAULT_APPS[app_name]
        if os.path.exists(app_path):
            try:
                subprocess.Popen(app_path)
                return f"Opening {app_name}"
            except Exception as e:
                return f"Error opening {app_name}: {str(e)}"
        else:
            return f"Could not find {app_name} at {app_path}"
    
    # Try to find the app in common Program Files locations
    common_paths = [
        r"C:\Program Files",
        r"C:\Program Files (x86)",
        os.path.expandvars(r"%LOCALAPPDATA%"),
        os.path.expandvars(r"%APPDATA%")
    ]
    
    for base_path in common_paths:
        for root, dirs, files in os.walk(base_path):
            for file in files:
                if app_name.lower() in file.lower() and file.endswith('.exe'):
                    full_path = os.path.join(root, file)
                    try:
                        subprocess.Popen(full_path)
                        return f"Opening {file}"
                    except Exception:
                        continue
    
    return f"Could not find application: {app_name}"

class AppLauncherTool(BaseTool):
    name: str = "app_launcher"
    description: str = "Opens applications on the computer. Provide the name of the app to open (e.g., 'steam', 'chrome', 'discord', etc.)"
    
    def _run(self, app_name: str) -> str:
        return open_app(app_name)
    
    def _arun(self, app_name: str) -> str:
        raise NotImplementedError("Async not implemented")

app_launcher = AppLauncherTool()
