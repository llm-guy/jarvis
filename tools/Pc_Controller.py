import os
import sys
import subprocess
import platform
import socket
import getpass
import shutil
import logging
from datetime import datetime

logging.basicConfig(level=logging.INFO)

class PCController:
    """Concise PC Controller for Windows systems"""
    
    def __init__(self):
        self.is_admin = self._check_admin()
        
    def _check_admin(self):
        try:
            import ctypes
            return ctypes.windll.shell32.IsUserAnAdmin() != 0
        except:
            return False
    
    def get_system_info(self):
        """Get brief system information"""
        return f"OS: {platform.platform()} | User: {getpass.getuser()} | Admin: {self.is_admin}"
    
    def process_list(self):
        """Get running processes (top 5)"""
        try:
            import psutil
            processes = []
            for proc in psutil.process_iter(['pid', 'name'])[:5]:
                processes.append(f"{proc.info['pid']}: {proc.info['name']}")
            return f"Top processes: {', '.join(processes)}"
        except:
            return "Process list not available"
    
    def file_list(self, path="."):
        """List directory contents"""
        try:
            items = os.listdir(path)[:5]
            files = [f for f in items if os.path.isfile(os.path.join(path, f))]
            dirs = [d for d in items if os.path.isdir(os.path.join(path, d))]
            return f"Files: {len(files)} | Dirs: {len(dirs)} | First: {', '.join(items[:3])}"
        except:
            return f"Cannot access {path}"
    
    def screenshot(self, filename=None):
        """Take screenshot"""
        try:
            from PIL import ImageGrab
            if not filename:
                filename = f"screenshot_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
            ImageGrab.grab().save(filename)
            return f"Screenshot saved: {filename}"
        except:
            return "Screenshot not available"
    
    def run_command(self, command):
        """Run system command"""
        try:
            result = subprocess.run(command, shell=True, capture_output=True, text=True, timeout=10)
            if result.returncode == 0:
                return f"Success: {result.stdout[:100]}..."
            else:
                return f"Error: {result.stderr[:100]}..."
        except:
            return "Command failed"
    
    def power_control(self, action):
        """Control system power"""
        actions = {"shutdown": "shutdown /s /t 0", "restart": "shutdown /r /t 0"}
        if action in actions:
            return f"Executing {action}..."
        return "Invalid action"
    
    def network_ping(self, target):
        """Ping network target"""
        try:
            result = subprocess.run(f"ping {target} -n 1", shell=True, capture_output=True, text=True)
            if "time=" in result.stdout:
                time_ms = result.stdout.split("time=")[1].split("ms")[0]
                return f"Ping {target}: {time_ms}ms"
            return f"Ping {target}: failed"
        except:
            return "Network error"
    
    def install_deps(self):
        """Install missing dependencies"""
        packages = ["psutil", "pillow"]
        installed = []
        for pkg in packages:
            try:
                subprocess.check_call([sys.executable, "-m", "pip", "install", pkg])
                installed.append(pkg)
            except:
                pass
        return f"Installed: {', '.join(installed)}" if installed else "No packages installed"

# Quick access functions
def quick_system_info():
    pc = PCController()
    return pc.get_system_info()

def quick_process_list():
    pc = PCController()
    return pc.process_list()

def quick_screenshot():
    pc = PCController()
    return pc.screenshot()
