from langchain.tools import tool
import os
import mss
import mss.tools

@tool("capture_screenshot", return_direct=True)
def take_screenshot() -> str:
    """
    Captures the current screen and saves it to '~/path/to/example.png' using the 'mss' library.
    
    Use this tool when the user says:
    - "Take a screenshot"
    - "Capture the screen"
    - "Save a screenshot"
    """
    try:
        # Create screenshots directory in user's Pictures folder
        screenshots_dir = os.path.expanduser("~/Pictures/Jarvis")
        os.makedirs(screenshots_dir, exist_ok=True)
        
        # Generate filename with timestamp
        from datetime import datetime
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"screenshot_{timestamp}.png"
        image_path = os.path.join(screenshots_dir, filename)

        with mss.mss() as sct:
            monitor = sct.monitors[1]  # [1] = main monitor; [0] = all monitors
            screenshot = sct.grab(monitor)
            mss.tools.to_png(screenshot.rgb, screenshot.size, output=image_path)

        return f"Screenshot captured and saved to {image_path} sir."
    except Exception as e:
        return f"Failed to capture screenshot: {str(e)}"
