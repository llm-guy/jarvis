# 🧠 Jarvis – Local Voice-Controlled AI Assistant

<div align="center">

![Jarvis Logo](https://img.shields.io/badge/Jarvis-AI%20Assistant-blue?style=for-the-badge&logo=robot)
![Version](https:- 🚀 **New App Launcher Tool**:
  - Launch applications with voice commands
  - Support for common Windows apps and shortcuts
  - Automatic app detection in Start Menu and Program Files
  - Smart path detection for .exe and .lnk files
  - Simple voice commands: "open [app]" or "launch [app]".shields.io/badge/Version-1.1.0-green?style=for-the-badge)
![Python](https://img.shields.io/badge/Python-3.8+-blue?style=for-the-badge&logo=python)
![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20macOS-lightgrey?style=for-the-badge)

**Your Personal AI Assistant - Powered by Local LLM Technology**

*Voice-activated, privacy-focused, and completely offline*

</div>

---

## 🎯 **What is Jarvis?**

**Jarvis** is an intelligent, voice-controlled AI assistant that runs entirely on your local machine. Built with cutting-edge local language models (Qwen via Ollama), it provides a seamless conversational experience while maintaining complete privacy and data sovereignty.

### ✨ **Key Features**
- 🗣 **Voice-Activated**: Wake with "Jarvis" and speak naturally
- 🧠 **Local AI**: Powered by Qwen 3.1.7B model via Ollama
- 🔒 **Privacy-First**: All processing happens locally on your device
- 🔧 **Tool Integration**: Extensible with custom tools and functions
- 🔊 **Natural Speech**: High-quality text-to-speech responses
- ⚡ **Real-Time**: Instant voice recognition and response

---

## � **Complete Command List**

Start any interaction by saying **"Jarvis"** and waiting for the "Yes sir?" response. Then use any of these commands:

### 🕐 **Time Commands**
```bash
"What time is it?"
"What's the current time?"
"Time in Berlin"
"Time in Munich"
"Time in Hamburg"
"What's the weather in Germany?"  # Returns time instead
```

### 📸 **Screenshot Commands**
```bash
"Take a screenshot"
"Capture the screen"
"Save a screenshot"
"Screenshot this"
```

### 🔍 **Web Search Commands**
```bash
"Search for [your topic]"
"Google [your topic]"
"Find information about [your topic]"
"Open browser and search for [your topic]"
"Search the web for [your topic]"
```

### 🌟 **Matrix Mode Commands**
```bash
"Enter matrix mode"
"Start matrix"
"Show matrix"
"Matrix mode"
"Activate matrix"
```

### 🔌 **Shutdown Commands**
```bash
"Shut down"
"Turn off"
"Shutdown"
```

### � **Version & Update Commands**
```bash
"What version are you?"
"Show me the changelog"
"What's new?"
"Tell me about recent updates"
"What changed in the latest version?"
"Show version history"
```

### �🚀 **App Launcher Commands**
```bash
"Open steam"
"Launch discord"
"Start spotify"
"Open cursor"
"Launch calculator"
"Open notepad"
```

Supported Applications:
- Steam (Steam gaming platform)
- Discord (Chat & communication)
- Spotify (Music streaming)
- Cursor (Code editor)
- Calculator (Windows calculator)
- Notepad (Text editor)
- Other applications will be searched automatically in common installation folders

---

## �🛠 **Built-in Tools**

Jarvis comes with powerful built-in tools that enhance its capabilities:

### 🕐 **Smart Time Assistant**
- **Weather-to-Time Conversion**: Ask about weather in Germany, get current time instead
- **Multi-City Support**: Get time for any German city (Berlin, Munich, Hamburg, etc.)
- **German Language**: Full German language support with localized responses
- **Date & Time**: Complete date and time information in German format

### 📸 **Screenshot and OCR Tools**
- **Instant Capture**: Take screenshots with voice commands
- **Auto-Save**: Automatically saves to designated folder
- **Text Recognition**: Extract text from screenshots (OCR)
- **Multi-Platform**: Works on both Windows and macOS
- **Smart Detection**: Finds screenshots in common system locations

**Screenshot Commands:**
```bash
"Take a screenshot"
"Capture the screen"
"Save a screenshot"
```

**OCR Commands:**
```bash
"Read the screen"
"What does the screenshot say?"
"Extract text from the image"
"Read the screenshot"
```

📝 **Note for Windows Users:**
- Requires Tesseract OCR to be installed
- Install from: https://github.com/UB-Mannheim/tesseract/wiki
- Default installation path: C:\Program Files\Tesseract-OCR\

### 🔍 **Web Search**
- **Google Integration**: Search the web with voice commands
- **Browser Support**: Open searches directly in your default browser
- **Natural Queries**: Use natural language to search
- **Quick Access**: Get instant search results

**Example Commands:**
```bash
"Search for artificial intelligence news"
"Open browser and search for weather forecast"
"Google quantum computing basics"
```

### 🌟 **Matrix Mode**
- **Matrix Rain Effect**: Classic Matrix-style falling characters
- **Windows & macOS**: Optimized for Windows Terminal and macOS Terminal
- **Python-Based**: No external dependencies required
- **Auto-Cleanup**: Automatically removes temporary files when closed

**Example Commands:**
```bash
"Enter matrix mode"
"Activate matrix mode"
"Go into matrix mode"
"Matrix mode"
```

### � **Shutdown Control**
- **Voice Command**: Simple "shut down" command
- **Graceful Exit**: Clean termination of the program
- **Confirmation**: Verbal confirmation before shutting down
- **Safe State**: Ensures proper cleanup before exit

**Example Commands:**
```bash
"Shut down"
"Turn off"
"Exit program"
```

### �🔧 **Extensible Architecture**
- **Custom Tools**: Easy to add new tools and functions
- **LangChain Integration**: Built on robust LangChain framework
- **Plugin System**: Modular design for easy expansion
- **Platform Support**: Optimized for Windows and macOS

---


## 🔬 **How It Works**

1. **Startup & local LLM Setup**
   - Initializes a local Ollama model (`qwen3:1.7b`) via `ChatOllama`
   - Registers tools (`get_time`, `take_screenshot`, `matrix_mode`) using LangChain

2. **Wake Word Listening**
   - Listens via microphone (e.g., `device_index=0`)
   - If it hears the word **"Jarvis"**, it enters "conversation mode"

3. **Voice Command Handling**
   - Records the user’s spoken command
   - Passes the command to the LLM, which may invoke tools
   - Responds using `pyttsx3` text-to-speech (with optional custom voice)

4. **Timeout**
   - If the user is inactive for more than 30 seconds in conversation mode, it resets to wait for the wake word again.

---

## 📋 Changelog

### Version 1.4.0 (August 17, 2025)
- 📋 **New Changelog Integration**:
  - Added version history access through voice commands
  - Smart changelog parsing and retrieval
  - Current version information on demand
  - Complete update history access

### Version 1.3.0 (August 17, 2025)
- 📝 **New OCR Capability**:
  - Added text recognition from screenshots
  - Multi-platform support (Windows & macOS)
  - Automatic screenshot detection
  - Smart path handling for different OS locations
  - Custom screenshot folder support (C:\Users\maxsc\Pictures\Jarvis)

### Version 1.2.0 (August 17, 2025)
- � **New App Launcher Tool**:
  - Launch applications with voice commands
  - Support for common apps (Steam, Discord, browsers, etc.)
  - Automatic app detection and launching
  - Simple "open [app]" command structure
- �🔍 **New Web Search Tool**:
  - Added Google search functionality
  - Voice-activated web searches
  - Browser integration for direct search results
  - Natural language search commands
- 🔌 **Shutdown Command**:
  - Added ability to shut down Jarvis with voice command
  - Immediate termination without confirmation
  - Simple "shut down" voice command

### Version 1.1.0 (August 16, 2025)
- ✨ **Enhanced Time Tool**: 
  - Now responds to weather queries about Germany with current time
  - Added German language support for responses
  - Improved city detection for German cities
  - Added date display in German format
- 📸 **New Screenshot Tool**: 
  - Added `take_screenshot` tool for capturing screen shots
  - Integrated into main application
- 🌟 **New Matrix Mode**: 
  - Added `matrix_mode` tool for Matrix rain effect
  - Windows and macOS optimized implementation
  - Auto-cleanup of temporary files
- 🔧 **Tool Integration**: 
  - All three tools (time, screenshot, matrix) now available in main application
  - Improved tool detection and response handling

---

## 🚀 **Quick Start Guide**

### 📋 **Prerequisites**
- **Python 3.8+** installed on your system
- **Ollama** installed and running
- **Microphone** for voice input
- **Speakers** for voice output
- **Tesseract OCR** for text recognition:
  - Windows: Install from UB-Mannheim's repository
  - macOS: Install via `brew install tesseract`

### 🔧 **Installation Steps**

#### 1. **Clone the Repository**
```bash
git clone https://github.com/yourusername/jarvis.git
cd jarvis
```

#### 2. **Set Up Virtual Environment**
```bash
# Windows
py -m venv venv
.\venv\Scripts\Activate.ps1

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

#### 3. **Install Dependencies**
```bash
# Windows
pip install -r requirements-windows.txt

# macOS/Linux
pip install -r requirements.txt
```

#### 4. **Install Ollama Model**
```bash
ollama pull qwen3:1.7b
```

#### 5. **Run Jarvis**
```bash
python main.py
```

### 🎯 **First Interaction**
1. Say **"Jarvis"** to wake the assistant
2. Wait for **"Yes sir?"** response
3. Use any command from the **Complete Command List** above
4. Enjoy the conversation!

💡 **Pro Tips:**
- Speak clearly and naturally
- Wait for the "Yes sir?" response before giving commands
- You have 30 seconds to give a command before Jarvis returns to wake word mode
- You can use variations of the commands - Jarvis understands natural language
- For web searches, be as specific as possible
- For immediate shutdown, just say "shut down"

### 🔧 **Configuration Options**
- **Microphone Index**: Modify `MIC_INDEX` in `main.py` if needed
- **Wake Word**: Change `TRIGGER_WORD` to customize wake phrase
- **Timeout**: Adjust `CONVERSATION_TIMEOUT` for session duration
- **Voice**: Customize TTS voice settings in the `speak_text` function

---

## 🛠 **Troubleshooting**

### ❌ **Common Issues & Solutions**

#### **Microphone Not Working**
```bash
# Check available audio devices
python -c "import speech_recognition as sr; print(sr.Microphone.list_microphone_names())"
```
- Update `MIC_INDEX` in `main.py` to match your microphone
- Ensure microphone permissions are granted

#### **Ollama Model Issues**
```bash
# Check installed models
ollama list

# Pull model if missing
ollama pull qwen3:1.7b
```

#### **Python Dependencies**
```bash
# Reinstall dependencies
pip install --upgrade -r requirements-windows.txt

# Install missing packages
pip install mss pyttsx3 SpeechRecognition
```

#### **Audio Output Problems**
- Check system volume and speaker connections
- Verify TTS voice availability on your system
- Try different voice settings in `main.py`

### 🔧 **Performance Optimization**
- **Reduce Model Size**: Use smaller models for faster responses
- **Adjust Timeout**: Modify `CONVERSATION_TIMEOUT` for longer sessions
- **Voice Quality**: Customize TTS settings for better audio output

---

## ❓ **FAQ**

### **Q: Can I use Jarvis without internet?**
**A:** Yes! Jarvis runs completely offline using local models and processing.

### **Q: How do I add new tools?**
**A:** Create new tool files in the `tools/` directory and import them in `main.py`.

### **Q: Can I change the wake word?**
**A:** Yes, modify the `TRIGGER_WORD` variable in `main.py`.

### **Q: Is my data private?**
**A:** Absolutely! All processing happens locally on your device.

### **Q: What languages does Jarvis support?**
**A:** Currently optimized for English and German, with extensible language support.

### **Q: Can I run Jarvis on mobile?**
**A:** Currently designed for desktop systems, but mobile support is planned.

---

## 🤝 **Contributing**

We welcome contributions! Here's how you can help:

### 🐛 **Reporting Issues**
- Use GitHub Issues for bug reports
- Include system information and error logs
- Provide steps to reproduce the issue

### 💡 **Feature Requests**
- Suggest new tools and capabilities
- Propose UI/UX improvements
- Request language support additions

### 🔧 **Code Contributions**
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

### 📝 **Documentation**
- Improve README sections
- Add code comments
- Create tutorials and guides

---

## 📄 **License**

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 **Acknowledgments**

- **Ollama** for local LLM infrastructure
- **LangChain** for tool orchestration framework
- **Google Speech Recognition** for voice processing
- **pyttsx3** for text-to-speech capabilities
- **Qwen** for the language model

---

## 📞 **Support**

- **GitHub Issues**: [Report bugs and request features](https://github.com/yourusername/jarvis/issues)
- **Discussions**: [Join the community](https://github.com/yourusername/jarvis/discussions)
- **Email**: your.email@example.com

---

*Made with ❤️ for the open-source community*

