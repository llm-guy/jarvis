# 📚 **Jarvis API Documentation**

## 🔧 **Tool Functions Reference**

### ⏰ **Time & Date Functions**

#### `get_time(timezone: str = "local") -> str`
Get current time in specified timezone.

**Parameters:**
- `timezone` (str): Timezone name (default: "local")

**Returns:**
- Current time string

**Example:**
```python
result = get_time("America/New_York")
# Returns: "Current time: 3:45 PM EST on Friday, July 25, 2025"
```

---

### 🌤️ **Weather Functions**

#### `get_weather(location: str) -> str`
Get current weather conditions for a location.

**Parameters:**
- `location` (str): City name or coordinates

**Returns:**
- Weather information string

**Example:**
```python
result = get_weather("New York")
# Returns: "Weather in New York: 72°F, partly cloudy. Humidity: 65%"
```

---

### 💻 **System Information Functions**

#### `get_system_info() -> str`
Get comprehensive system status including CPU, memory, and disk usage.

**Returns:**
- System status report

**Example:**
```python
result = get_system_info()
# Returns: 
# "System Status:
# - OS: Linux 6.2.0
# - CPU: 23.4% usage (8 cores)
# - Memory: 47.3% used (7.6GB / 16GB)
# - Disk: 65.2% used (125GB free of 500GB)"
```

#### `get_battery_status() -> str`
Get battery status for laptops.

**Returns:**
- Battery status string

**Example:**
```python
result = get_battery_status()
# Returns: "Battery: 85% (plugged in)"
```

---

### 📁 **File Management Functions**

#### `list_files(directory: str = ".") -> str`
List contents of a directory.

**Parameters:**
- `directory` (str): Path to directory (default: current directory)

**Returns:**
- Directory contents listing

**Example:**
```python
result = list_files("/home/user")
# Returns: "Contents: Documents/, Downloads/, Pictures/, file.txt"
```

#### `create_directory(path: str) -> str`
Create a new directory.

**Parameters:**
- `path` (str): Path for new directory

**Returns:**
- Success/failure message

**Example:**
```python
result = create_directory("/home/user/projects")
# Returns: "Directory created successfully: /home/user/projects"
```

#### `get_file_info(file_path: str) -> str`
Get information about a file.

**Parameters:**
- `file_path` (str): Path to file

**Returns:**
- File information

**Example:**
```python
result = get_file_info("/home/user/document.txt")
# Returns: "File: document.txt, Size: 1.5KB, Modified: 2025-07-25 15:30"
```

---

### 🧮 **Calculator Functions**

#### `calculate(expression: str) -> str`
Perform mathematical calculations.

**Parameters:**
- `expression` (str): Mathematical expression

**Returns:**
- Calculation result

**Example:**
```python
result = calculate("15% of 2500")
# Returns: "15% of 2500 = 375"
```

#### `convert_units(value: float, from_unit: str, to_unit: str) -> str`
Convert between different units.

**Parameters:**
- `value` (float): Value to convert
- `from_unit` (str): Source unit
- `to_unit` (str): Target unit

**Returns:**
- Conversion result

**Example:**
```python
result = convert_units(100, "fahrenheit", "celsius")
# Returns: "100°F = 37.78°C"
```

---

## 🎤 **Voice Interface Functions**

### `speak_text(text: str)`
Convert text to speech with smart cleaning.

**Parameters:**
- `text` (str): Text to speak

**Features:**
- Automatic markdown removal
- Symbol-to-word conversion
- Speech interruption support
- Length limiting (300 chars)

**Example:**
```python
speak_text("The price is **$125.50** with a 20% discount")
# Speaks: "The price is 125.50 dollars with a 20 percent discount"
```

### `clean_text_for_speech(text: str) -> str`
Clean text for better speech synthesis.

**Parameters:**
- `text` (str): Raw text input

**Returns:**
- Cleaned text suitable for TTS

**Cleaning Rules:**
- `**bold**` → "bold"
- `*italic*` → "italic" 
- `$123` → "123 dollars"
- `20%` → "20 percent"
- `Company & Co` → "Company and Co"

---

## 🔌 **Configuration API**

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `OPENWEATHER_API_KEY` | Weather API key | None |
| `OLLAMA_MODEL` | AI model name | "qwen3:1.7b" |
| `SPEECH_RATE` | TTS speed | 180 |
| `TTS_LANGUAGE` | Speech language | "en" |

### Audio Configuration

| Setting | Description | Default |
|---------|-------------|---------|
| `MICROPHONE_INDEX` | Mic device index | None (auto) |
| `ENERGY_THRESHOLD` | Voice detection threshold | 4000 |
| `PAUSE_THRESHOLD` | Silence detection (seconds) | 1.0 |

---

## 🛠️ **Custom Tool Development**

### Creating a New Tool

1. **Create tool file:** `tools/my_tool.py`
2. **Define function:**
```python
from langchain.tools import tool

@tool
def my_custom_tool(parameter: str) -> str:
    """Description of what this tool does."""
    # Implementation here
    return "Result"
```

3. **Import in main.py:**
```python
from tools.my_tool import my_custom_tool
tools.append(my_custom_tool)
```

### Tool Best Practices

- **Clear descriptions**: Help AI understand when to use the tool
- **Type hints**: Use proper Python typing
- **Error handling**: Graceful failure with informative messages
- **Return strings**: Always return string results
- **Parameter validation**: Check inputs before processing

---

## 🧪 **Testing Functions**

### `test_microphone() -> bool`
Test microphone functionality.

**Returns:**
- True if microphone works, False otherwise

### `test_tts() -> bool`
Test text-to-speech system.

**Returns:**
- True if TTS works, False otherwise

### `test_ollama_connection() -> bool`
Test connection to Ollama AI model.

**Returns:**
- True if connected, False otherwise

---

## 🎯 **Error Handling**

### Common Error Types

| Error | Cause | Solution |
|-------|-------|----------|
| `MicrophoneError` | Audio device issues | Check `debug_mic.py` |
| `TTSError` | Speech synthesis failure | Fallback to pyttsx3 |
| `OllamaError` | AI model unavailable | Check Ollama service |
| `ToolError` | Tool execution failure | Check tool parameters |

### Error Recovery

- **Automatic fallbacks**: TTS → pyttsx3, network tools → offline mode
- **Graceful degradation**: Continue operation with reduced functionality
- **User feedback**: Clear error messages and suggested actions
- **Logging**: Comprehensive error tracking for debugging

---

## 🔄 **Integration Examples**

### Voice Command Flow
```
1. User speaks: "What's the weather and my battery status?"
2. Speech recognition → text
3. AI processes request → identifies tools needed
4. Calls: get_weather() and get_battery_status()
5. Combines results → response text
6. Text cleaning → speech synthesis
7. Audio output to user
```

### Text Mode Flow
```
1. User types: "Calculate 15% of $2,500 and create a directory called 'projects'"
2. AI processes → identifies: calculate() and create_directory()
3. Executes tools → gets results
4. Formats response → displays to user
```

---

*Complete API reference for Jarvis AI Voice Assistant*
