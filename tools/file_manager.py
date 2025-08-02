# tools/file_manager.py

from langchain.tools import tool
import os
import shutil
from pathlib import Path
from datetime import datetime

@tool
def list_files(directory: str = ".") -> str:
    """List files and directories in the specified path."""
    try:
        path = Path(directory).expanduser()
        if not path.exists():
            return f"Directory {directory} does not exist."
        
        if not path.is_dir():
            return f"{directory} is not a directory."
        
        items = []
        for item in sorted(path.iterdir()):
            if item.is_dir():
                items.append(f"📁 {item.name}/")
            else:
                size = item.stat().st_size
                if size > 1024**3:  # GB
                    size_str = f"{size / (1024**3):.1f}GB"
                elif size > 1024**2:  # MB
                    size_str = f"{size / (1024**2):.1f}MB"
                elif size > 1024:  # KB
                    size_str = f"{size / 1024:.1f}KB"
                else:
                    size_str = f"{size}B"
                items.append(f"📄 {item.name} ({size_str})")
        
        if not items:
            return f"Directory {directory} is empty."
        
        return f"Contents of {directory}:\n" + "\n".join(items[:20])  # Limit to 20 items
        
    except Exception as e:
        return f"Error listing files: {e}"

@tool
def create_directory(directory: str) -> str:
    """Create a new directory."""
    try:
        path = Path(directory).expanduser()
        path.mkdir(parents=True, exist_ok=True)
        return f"Directory {directory} created successfully."
    except Exception as e:
        return f"Error creating directory: {e}"

@tool
def get_file_info(file_path: str) -> str:
    """Get information about a specific file."""
    try:
        path = Path(file_path).expanduser()
        if not path.exists():
            return f"File {file_path} does not exist."
        
        stat = path.stat()
        size = stat.st_size
        modified = datetime.fromtimestamp(stat.st_mtime).strftime("%Y-%m-%d %H:%M:%S")
        
        if size > 1024**3:  # GB
            size_str = f"{size / (1024**3):.2f} GB"
        elif size > 1024**2:  # MB
            size_str = f"{size / (1024**2):.2f} MB"
        elif size > 1024:  # KB
            size_str = f"{size / 1024:.2f} KB"
        else:
            size_str = f"{size} bytes"
        
        file_type = "Directory" if path.is_dir() else "File"
        
        return f"{file_type}: {file_path}\nSize: {size_str}\nModified: {modified}"
        
    except Exception as e:
        return f"Error getting file info: {e}"
