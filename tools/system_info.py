# tools/system_info.py

from langchain.tools import tool
import psutil
import platform
import os
from datetime import datetime

@tool
def get_system_info() -> str:
    """Get system information including CPU, memory, and disk usage."""
    try:
        # CPU info
        cpu_percent = psutil.cpu_percent(interval=1)
        cpu_count = psutil.cpu_count()
        
        # Memory info
        memory = psutil.virtual_memory()
        memory_percent = memory.percent
        memory_total = round(memory.total / (1024**3), 2)  # GB
        memory_used = round(memory.used / (1024**3), 2)  # GB
        
        # Disk info
        disk = psutil.disk_usage('/')
        disk_percent = round((disk.used / disk.total) * 100, 2)
        disk_total = round(disk.total / (1024**3), 2)  # GB
        disk_free = round(disk.free / (1024**3), 2)  # GB
        
        # System info
        system = platform.system()
        release = platform.release()
        
        return f"""System Status:
- OS: {system} {release}
- CPU: {cpu_percent}% usage ({cpu_count} cores)
- Memory: {memory_percent}% used ({memory_used}GB / {memory_total}GB)
- Disk: {disk_percent}% used ({disk_free}GB free of {disk_total}GB)"""

    except Exception as e:
        return f"Error getting system info: {e}"

@tool
def get_battery_status() -> str:
    """Get battery status if available."""
    try:
        battery = psutil.sensors_battery()
        if battery:
            percent = battery.percent
            plugged = "plugged in" if battery.power_plugged else "not plugged in"
            return f"Battery: {percent}% ({plugged})"
        else:
            return "No battery information available (desktop system)"
    except Exception as e:
        return f"Error getting battery info: {e}"
