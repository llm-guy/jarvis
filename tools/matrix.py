from langchain.tools import tool
import subprocess
import platform
import tempfile
import sys
import shutil

@tool("matrix_mode", return_direct=True)
def matrix_mode() -> str:
    """
    Opens a new terminal window and runs the cmatrix command to enter 'Matrix Mode'.
    Use this tool when the user says something like:
    - "Enter matrix mode"
    - "Activate matrix mode"
    - "Go into matrix mode"
    """
    system = platform.system()

    try:
        if system == "Linux":
            if shutil.which("cmatrix") is None:
                return "Matrix mode requires 'cmatrix'. Please install it using your package manager."
            subprocess.Popen(["gnome-terminal", "--", "cmatrix"])
            return "Matrix mode activated! Enjoy the rain, Neo."

        elif system == "Darwin":
            if shutil.which("cmatrix") is None:
                return "Matrix mode requires 'cmatrix'. You can install it via Homebrew: brew install cmatrix"
            subprocess.Popen([
                "osascript", "-e",
                'tell application "Terminal" to do script "cmatrix"',
                "-e", 'tell application "Terminal" to activate'
            ])
            return "Matrix mode has been activated, sir!"

        elif system == "Windows":
            python_script = '''
import random
import time
import os
import sys

os.system("color 0A")  # Green text on black background
chars = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz!@#$%^&*"

def get_terminal_size():
    try:
        import shutil
        return shutil.get_terminal_size()
    except:
        return (80, 25)

width, height = get_terminal_size()
width = min(width, 120)
height = min(height, 30)

drops = [random.randint(0, height) for _ in range(width)]

print("\\033[32m")
print("Welcome to the Matrix. Press Ctrl+C to exit...")
time.sleep(2)

try:
    while True:
        os.system("cls")
        screen = [[" " for _ in range(width)] for _ in range(height)]
        for i in range(width):
            if drops[i] < height:
                screen[drops[i]][i] = random.choice(chars)
            drops[i] += 1
            if drops[i] > height and random.random() > 0.95:
                drops[i] = 0
        for row in screen:
            print("".join(row))
        time.sleep(0.1)
except KeyboardInterrupt:
    print("\\n\\033[32mExiting Matrix...\\033[0m")
    time.sleep(1)
'''

            with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False, encoding='utf-8') as f:
                f.write(python_script)
                script_path = f.name

            subprocess.Popen([sys.executable, script_path], creationflags=subprocess.CREATE_NEW_CONSOLE)
            return "Matrix mode activated! Welcome to the Matrix, Neo. Press Ctrl+C to exit."

        else:
            return f"Matrix mode is not supported on {system}."
    except Exception as e:
        return f"Failed to activate matrix mode: {str(e)}"

