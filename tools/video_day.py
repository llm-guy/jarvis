# tools/video_day.py

from langchain.tools import tool

@tool
def video_day() -> str:
    """Returns information about today being a good day for video content."""
    return "Today is a great day for creating video content! The lighting and energy are perfect."
