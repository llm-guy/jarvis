from langchain.tools import tool
import subprocess
import platform
import os
import sys
import time
import random
import threading

@tool("matrix_mode", return_direct=True)
def matrix_mode() -> str:
    """
    Activates Matrix Mode with a Python-based matrix rain effect.
    Use this tool when the user says something like:
    - "Enter matrix mode"
    - "Activate matrix mode"
    - "Go into matrix mode"
    - "Matrix mode"
    """
    system = platform.system()

    try:
        if system == "Windows":
            # Windows version - create Python-based matrix effect
            try:
                # Create matrix script
                matrix_script = create_matrix_script()
                script_path = os.path.join(os.getcwd(), "matrix_effect.py")
                
                with open(script_path, "w") as f:
                    f.write(matrix_script)
                
                # Try Windows Terminal first
                try:
                    subprocess.Popen(["wt", "new-tab", "--title", "Matrix Mode", "python", script_path])
                    return "Matrix mode activated in Windows Terminal! Welcome to the Matrix, Neo."
                except FileNotFoundError:
                    # Fallback to PowerShell
                    subprocess.Popen(["powershell", "-Command", f"python {script_path}"])
                    return "Matrix mode activated in PowerShell! The Matrix has you."
                    
            except Exception as e:
                return f"Matrix mode activation failed: {str(e)}."

        elif system == "Darwin":
            # macOS version - create Python-based matrix effect
            try:
                # Create matrix script
                matrix_script = create_matrix_script()
                script_path = os.path.join(os.getcwd(), "matrix_effect.py")
                
                with open(script_path, "w") as f:
                    f.write(matrix_script)
                
                # Open in macOS Terminal
                subprocess.Popen([
                    "osascript", "-e",
                    f'tell application "Terminal" to do script "python3 {script_path}"',
                    "-e", 'tell application "Terminal" to activate'
                ])
                return "Matrix mode activated in Terminal! Welcome to the Matrix, Neo."
                
            except Exception as e:
                return f"Matrix mode activation failed: {str(e)}."

        else:
            return f"Matrix mode is currently only supported on Windows and macOS. Your system: {system}"

    except Exception as e:
        return f"Failed to activate matrix mode: {str(e)}."

def create_matrix_script():
    """Creates a Python script for matrix rain effect"""
    return '''
import os
import sys
import time
import random
import threading
import atexit

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def cleanup_script():
    """Clean up the script file when exiting"""
    try:
        script_path = os.path.abspath(__file__)
        if os.path.exists(script_path):
            os.remove(script_path)
            print("\\033[32mMatrix script cleaned up.\\033[0m")
    except Exception as e:
        print(f"\\033[33mWarning: Could not clean up script file: {e}\\033[0m")

def matrix_rain():
    # Register cleanup function
    atexit.register(cleanup_script)
    
    # Matrix characters
    chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789@#$%^&*()_+-=[]{}|;:,.<>?"
    
    # Get terminal size
    try:
        import shutil
        cols, rows = shutil.get_terminal_size()
    except:
        cols, rows = 80, 24
    
    # Initialize matrix columns
    matrix = [0] * cols
    
    print("\\033[32m")  # Green color
    print("Welcome to the Matrix, Neo...")
    print("Press Ctrl+C to exit")
    print("\\033[0m")  # Reset color
    time.sleep(2)
    clear_screen()
    
    try:
        while True:
            # Update matrix columns
            for i in range(cols):
                if matrix[i] == 0:
                    if random.random() < 0.02:  # 2% chance to start new column
                        matrix[i] = 1
                else:
                    matrix[i] += 1
                    if matrix[i] > rows:
                        matrix[i] = 0
            
            # Print matrix
            output = ""
            for row in range(rows):
                line = ""
                for col in range(cols):
                    if matrix[col] > row:
                        char = random.choice(chars)
                        if row == matrix[col] - 1:
                            line += "\\033[37m" + char + "\\033[32m"  # White head
                        else:
                            line += char
                    else:
                        line += " "
                output += line + "\\n"
            
            print("\\033[H" + output, end="")
            time.sleep(0.1)
            
    except KeyboardInterrupt:
        print("\\033[0m\\nExiting the Matrix...")
        # Clean up immediately on Ctrl+C
        cleanup_script()
        sys.exit(0)

if __name__ == "__main__":
    matrix_rain()
'''
