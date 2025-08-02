# 🤖 Jarvis AI Voice Assistant

> **A powerful, intelligent voice assistant with natural language processing, advanced TTS, and 11 specialized tools**

[![Python 3.12+](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Status: Active](https://img.shields.io/badge/Status-Active-green.svg)]()

## 🌟 **Overview**

Jarvis is an advanced AI voice assistant built with modern technologies, featuring natural speech synthesis, intelligent text processing, and comprehensive system integration. It combines the power of Ollama LLM with Google Text-to-Speech for a seamless conversational experience.

### ✨ **Key Features**

- 🎙️ **Natural Voice Interface** - High-quality Google TTS with speech interruption
- 🧠 **AI-Powered Responses** - Ollama integration with qwen3:1.7b model  
- 🛠️ **11 Specialized Tools** - Time, weather, system monitoring, file management, and more
- 🎯 **Smart Text Processing** - Automatic markdown cleaning for better speech
- ⌨️ **Interrupt Control** - Press 's' to stop speech anytime
- 🔄 **Dual Modes** - Voice and text-only interfaces
- 📊 **System Integration** - Deep system monitoring and control

---

## 🚀 **Quick Start**

### Prerequisites

- Python 3.12+
- Linux/Ubuntu system
- Microphone and speakers
- Ollama installed with qwen3:1.7b model

### Installation

1. **Clone and setup environment:**
```bash
cd /home/lpch/doc-ai/jarvis/jarvis
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

2. **Install system dependencies:**
```bash
sudo apt update
sudo apt install portaudio19-dev python3-pyaudio alsa-utils
```

3. **Configure environment:**
```bash
# Create .env file with API keys
echo "OPENWEATHER_API_KEY=your_api_key_here" > .env
```

4. **Run Jarvis:**
```bash
# Voice mode with Google TTS (default, requires internet)
python main.py

# Voice mode with offline TTS
python main.py --tts pyttsx3

# Text mode with Google TTS (type commands, hear responses)
python main.py --text-mode --tts gtts

# Silent text mode (no speech)
python main.py --text-mode --tts none

# Linux espeak (lightweight offline)
python main.py --tts espeak --voice-rate 150

# Custom settings
python main.py --tts pyttsx3 --voice-rate 200 --volume 0.8
```

### 🎛️ **Command Line Options**

```bash
# TTS Engine Selection
--tts gtts          # Google Text-to-Speech (high quality, needs internet)
--tts pyttsx3       # Python TTS (offline, cross-platform)
--tts espeak        # Linux espeak (lightweight, offline)
--tts none          # No speech, text-only display

# Voice Settings
--voice-rate 180    # Speech speed (50-300, default: 180)
--volume 1.0        # Volume level (0.0-1.0, default: 1.0)

# Mode Options
--text-mode         # Type commands instead of speaking
--debug             # Enable detailed logging

# Examples
python main.py --help                           # Show all options
python main.py --tts gtts --voice-rate 200     # Fast Google TTS
python main.py --text-mode --tts none          # Silent text mode
python main.py --debug --tts pyttsx3           # Debug with offline TTS
```

---

## 🎯 **Core Capabilities**

### 🎤 **Voice Interface**

| Feature | Description | Example |
|---------|-------------|---------|
| **Natural TTS** | Google Text-to-Speech with clean output | "Hello, I am Jarvis" |
| **Speech Interruption** | Press 's' key to stop speech | Press `s` during playback |
| **Markdown Cleaning** | Removes `**bold**`, `*italic*`, symbols | `**bold**` → "bold" |
| **Smart Formatting** | Converts `$123` → "123 dollars" | Financial data handling |

### 🧠 **AI Intelligence**

- **Conversational AI** powered by Ollama qwen3:1.7b
- **Context-aware responses** with memory
- **Tool integration** for extended capabilities
- **Error handling** with graceful fallbacks

---

## 🛠️ **Available Tools**

### ⏰ **Time & Date Tools**
```python
@tool get_current_time()    # Current local time
@tool get_world_time()      # Time in different timezones
```

### 🌤️ **Weather Tools**
```python
@tool get_current_weather() # Current weather conditions
@tool get_weather_forecast() # Weather forecast
```

### 💻 **System Monitoring**
```python
@tool get_system_info()     # CPU, memory, disk usage
@tool get_cpu_usage()       # Detailed CPU metrics
@tool get_memory_usage()    # Memory statistics
@tool get_disk_usage()      # Disk space information
@tool get_battery_info()    # Battery status (laptops)
```

### 📁 **File Management**
```python
@tool list_directory()      # List directory contents
@tool read_file_content()   # Read file contents
@tool write_file_content()  # Write to files
@tool create_directory()    # Create directories
@tool delete_file()         # Delete files
```

### 🧮 **Calculator & Conversion**
```python
@tool calculate()           # Mathematical operations
@tool convert_units()       # Unit conversions
```

### 🔍 **Web & Search**
```python
@tool search_web()          # Web search functionality
@tool get_news_headlines()  # Latest news headlines
```

---

## 💬 **Usage Examples**

### Basic Conversations
```
You: "What's the current time?"
Jarvis: "The current time is 3:45 PM on Friday, July 25th, 2025."

You: "Check my system status"
Jarvis: "System Status:
- OS: Linux 6.2.0
- CPU: 23.4% usage (8 cores)
- Memory: 47.3% used (7.6GB / 16GB)
- Disk: 65.2% used (125GB free of 500GB)"
```

### Advanced Queries
```
You: "What's the weather like and calculate 15% of $2,500"
Jarvis: "The current weather is 72°F and partly cloudy. 15% of $2,500 is $375."

You: "Create a directory called 'projects' and list my home directory"
Jarvis: "I've created the 'projects' directory. Your home directory contains: Documents, Downloads, Pictures, projects..."
```

---

## 🔧 **Configuration**

### Environment Variables
```bash
# .env file
OPENWEATHER_API_KEY=your_openweather_api_key
OLLAMA_MODEL=qwen3:1.7b
SPEECH_RATE=180
TTS_LANGUAGE=en
```

### Audio Settings
```python
# Microphone configuration
MICROPHONE_INDEX = None  # Auto-detect
ENERGY_THRESHOLD = 4000
DYNAMIC_ENERGY_THRESHOLD = True
PAUSE_THRESHOLD = 1.0
```

### TTS Configuration
```python
# Text-to-speech settings
TTS_ENGINE = "gtts"  # Google TTS
SPEECH_RATE = 180
VOLUME = 1.0
MAX_SPEECH_LENGTH = 300  # characters
```

---

## 🎨 **Text Processing Features**

### Markdown Cleaning
Jarvis automatically cleans text for better speech synthesis:

| Input | Output | Description |
|-------|--------|-------------|
| `**bold text**` | "bold text" | Removes bold formatting |
| `*italic text*` | "italic text" | Removes italic formatting |
| `` `code` `` | "code" | Removes code formatting |
| `# Header` | "Header" | Removes header symbols |
| `[link](url)` | "link" | Extracts link text |
| `$123.50` | "123.50 dollars" | Converts currency |
| `25%` | "25 percent" | Converts percentages |
| `Company & Co` | "Company and Co" | Converts symbols |

### Smart Features
- **Length limiting**: Speeches capped at 300 characters
- **Whitespace normalization**: Removes excessive spacing
- **Symbol replacement**: Converts symbols to words
- **Mathematical expressions**: Simplifies complex math notation

---

## 🎮 **Controls & Shortcuts**

### Voice Mode Controls
| Key/Action | Function |
|------------|----------|
| `s` | Stop current speech |
| `Ctrl+C` | Emergency exit |
| `Enter` | Submit voice input |
| Voice: "conversation mode" | Enter continuous conversation |
| Voice: "exit" or "quit" | Exit application |

### Text Mode Controls
| Command | Function |
|---------|----------|
| `quit` or `exit` | Exit application |
| Any text input | Send to AI |

---

## 📁 **Project Structure**

```
jarvis/
├── main.py                 # Main voice interface with TTS options
├── test_jarvis_text.py     # Clean text-only testing
├── jarvis_help.py          # Usage guide and examples
├── requirements.txt        # Python dependencies
├── .env                    # Environment configuration
├── README.md              # This documentation
├── demo_improvements.py   # Feature demonstration
├── test_improved_tts.py   # TTS testing utility
├── debug_mic.py           # Microphone debugging
├── test_tools.py          # Tools functionality test
└── tools/                 # Tool modules
    ├── __init__.py
    ├── time.py            # Time and date functions
    ├── weather.py         # Weather information
    ├── system_info.py     # System monitoring
    ├── file_manager.py    # File operations
    ├── calculator.py      # Math and conversions
    └── search.py          # Web search and news
```

---

## 🧪 **Testing & Debugging**

### Test Individual Components
```bash
# Test TTS improvements
python test_improved_tts.py

# Test all tools functionality
python test_tools.py

# Debug microphone issues
python debug_mic.py

# Demo improvements
python demo_improvements.py

# Quick help guide
python jarvis_help.py

# Test agent without voice issues
python test_jarvis_text.py
```

### Debugging Commands
```bash
# Check audio devices
arecord -l

# Test microphone
arecord -d 5 test.wav && aplay test.wav

# Check Ollama status
ollama list
ollama run qwen3:1.7b "Hello"
```

---

## 🔧 **Troubleshooting**

### Common Issues

#### 🎤 **Microphone Problems**
```bash
# Install audio dependencies
sudo apt install portaudio19-dev python3-pyaudio

# Check microphone permissions
ls -la /dev/snd/

# Test with debug script
python debug_mic.py

# Use text mode if microphone fails
python main.py --text-mode --tts gtts
```

#### 🔊 **Audio Playback Issues**
```bash
# Install ALSA utilities
sudo apt install alsa-utils

# Check audio devices
aplay -l

# Test pygame audio
python -c "import pygame; pygame.mixer.init(); print('Audio OK')"

# Try different TTS engines
python main.py --tts pyttsx3        # Offline alternative
python main.py --tts espeak         # Linux lightweight
python main.py --tts none           # Silent mode
```

#### 🌐 **Network Issues (Speech Recognition)**
```bash
# Check internet connection
ping google.com

# Use offline alternatives
python main.py --text-mode --tts pyttsx3  # Fully offline
python main.py --tts espeak               # Offline TTS with voice input

# Test speech recognition separately
python debug_mic.py
```

#### 🤖 **Ollama Connection**
```bash
# Start Ollama service
ollama serve

# Install model
ollama pull qwen3:1.7b

# Test connection
curl http://localhost:11434/api/tags
```

#### 🌐 **API Key Issues**
```bash
# Check environment file
cat .env

# Test weather API
curl "http://api.openweathermap.org/data/2.5/weather?q=London&appid=YOUR_API_KEY"
```

---

## 📋 **Requirements**

### Python Packages
```txt
langchain==0.3.9
langchain-ollama==0.2.1
langchain-core==0.3.21
speech-recognition==3.12.0
gtts==2.5.4
pygame==2.6.1
psutil==6.1.0
requests==2.32.3
python-dotenv==1.0.1
pyaudio==0.2.14
keyboard==0.13.5
```

### System Dependencies
```bash
# Ubuntu/Debian
sudo apt install portaudio19-dev python3-pyaudio alsa-utils

# Audio libraries
sudo apt install libasound2-dev

# Development tools
sudo apt install build-essential
```

---

## 🚀 **Performance Tips**

### Optimization Strategies
1. **TTS Caching**: Cache frequently used phrases
2. **Model Selection**: Use smaller models for faster responses
3. **Tool Filtering**: Only load needed tools
4. **Memory Management**: Regular cleanup of temporary files

### Best Practices
- Keep speeches under 300 characters for better user experience
- Use conversation mode for extended interactions
- Regularly update Ollama models for improved performance
- Monitor system resources during operation

---

## 📊 **Changelog**

### v2.0.0 (Latest) - July 25, 2025
#### 🚀 **Major Improvements**
- ✅ **Upgraded TTS**: Switched from pyttsx3 to Google TTS (gTTS)
- ✅ **Smart Text Cleaning**: Automatic markdown and symbol removal
- ✅ **Speech Interruption**: Press 's' key to stop speech
- ✅ **Enhanced Tools**: Added 11 comprehensive tools
- ✅ **Better Error Handling**: Graceful fallbacks and recovery
- ✅ **Improved Stability**: Fixed microphone initialization issues

#### 🔧 **Technical Changes**
- Enhanced audio system configuration
- Keyboard package integration for interruption
- Modular tool architecture
- Comprehensive logging system
- Better conversation flow management

#### 🐛 **Bug Fixes**
- Fixed NoneType microphone errors
- Resolved PyAudio installation issues
- Eliminated unwanted continuous responses
- Improved symbol handling in speech

---

## 🤝 **Contributing**

### Development Setup
```bash
git clone <repository>
cd jarvis
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Adding New Tools
1. Create tool file in `tools/` directory
2. Use `@tool` decorator
3. Add to imports in `main.py`
4. Test with `test_tools.py`

### Code Style
- Follow PEP 8 guidelines
- Use type hints
- Add comprehensive docstrings
- Include error handling

---

## 📄 **License**

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🆘 **Support**

### Getting Help
- 📖 **Documentation**: This README file
- 🐛 **Issues**: Create GitHub issues for bugs
- 💡 **Features**: Request new features via issues
- 🧪 **Testing**: Use provided test scripts

### Contact
- **Repository**: Project_n8n_System
- **Branch**: lowperry
- **Owner**: lamont703

---

## 🙏 **Acknowledgments**

- **Ollama** - Local LLM inference
- **Google TTS** - Natural voice synthesis
- **LangChain** - AI framework and tools
- **PyAudio** - Audio input/output
- **Pygame** - Audio playback

---

*Built with ❤️ for intelligent voice assistance*

