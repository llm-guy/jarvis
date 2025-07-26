# 🚀 **Jarvis Installation Guide**

## 📋 **System Requirements**

- **Operating System**: Linux (Ubuntu 20.04+ recommended)
- **Python**: 3.12 or higher
- **Memory**: 4GB RAM minimum, 8GB recommended
- **Storage**: 2GB free space
- **Audio**: Microphone and speakers/headphones
- **Network**: Internet connection for weather/search features

---

## ⚡ **Quick Install (5 Minutes)**

### 1. **Install System Dependencies**
```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install audio dependencies
sudo apt install -y portaudio19-dev python3-pyaudio alsa-utils

# Install build tools
sudo apt install -y build-essential python3-dev

# Install Ollama
curl -fsSL https://ollama.ai/install.sh | sh
```

### 2. **Setup Ollama AI Model**
```bash
# Start Ollama service
ollama serve &

# Download AI model (this may take a few minutes)
ollama pull qwen3:1.7b

# Test model
ollama run qwen3:1.7b "Hello, test message"
```

### 3. **Setup Jarvis**
```bash
# Navigate to Jarvis directory
cd /home/lpch/doc-ai/jarvis/jarvis

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install Python dependencies
pip install --upgrade pip
pip install -r requirements.txt
```

### 4. **Configure Environment**
```bash
# Create environment file
cat > .env << EOF
OPENWEATHER_API_KEY=get_from_openweathermap.org
OLLAMA_MODEL=qwen3:1.7b
SPEECH_RATE=180
TTS_LANGUAGE=en
EOF

# Make scripts executable
chmod +x *.py
```

### 5. **Test Installation**
```bash
# Test microphone
python debug_mic.py

# Test TTS
python test_improved_tts.py

# Test tools
python test_tools.py

# Run text mode (safest first test)
python text_jarvis.py
```

---

## 🔧 **Detailed Installation Steps**

### **Step 1: Prepare System**

#### Update Ubuntu
```bash
sudo apt update
sudo apt upgrade -y
sudo apt autoremove -y
```

#### Install Python 3.12
```bash
# Add Python PPA
sudo add-apt-repository ppa:deadsnakes/ppa -y
sudo apt update

# Install Python 3.12
sudo apt install python3.12 python3.12-venv python3.12-dev -y

# Set as default (optional)
sudo update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.12 1
```

### **Step 2: Audio System Setup**

#### Install Audio Libraries
```bash
# Core audio libraries
sudo apt install -y \
    libasound2-dev \
    portaudio19-dev \
    python3-pyaudio \
    alsa-utils \
    pulseaudio \
    pavucontrol

# Test audio system
speaker-test -t wav -c 2
```

#### Configure Audio Permissions
```bash
# Add user to audio group
sudo usermod -a -G audio $USER

# Restart audio services
systemctl --user restart pulseaudio
```

### **Step 3: Install Ollama**

#### Download and Install
```bash
# Install Ollama
curl -fsSL https://ollama.ai/install.sh | sh

# Verify installation
ollama --version
```

#### Setup as Service
```bash
# Create systemd service
sudo tee /etc/systemd/system/ollama.service > /dev/null <<EOF
[Unit]
Description=Ollama Server
After=network-online.target

[Service]
ExecStart=/usr/local/bin/ollama serve
User=ollama
Group=ollama
Restart=always
RestartSec=3

[Install]
WantedBy=default.target
EOF

# Enable and start service
sudo systemctl enable ollama
sudo systemctl start ollama
```

#### Download AI Model
```bash
# Download qwen3:1.7b model (small, fast)
ollama pull qwen3:1.7b

# Alternative models (optional):
# ollama pull llama3.2:1b     # Faster, less capable
# ollama pull qwen3:3b        # Slower, more capable
# ollama pull codellama:7b    # Better for code tasks
```

### **Step 4: Python Environment**

#### Create Virtual Environment
```bash
cd /home/lpch/doc-ai/jarvis/jarvis

# Create venv with Python 3.12
python3.12 -m venv venv

# Activate environment
source venv/bin/activate

# Verify Python version
python --version  # Should show 3.12+
```

#### Install Dependencies
```bash
# Upgrade pip
pip install --upgrade pip setuptools wheel

# Install PyAudio (may need compilation)
pip install pyaudio

# Install remaining packages
pip install \
    langchain==0.3.9 \
    langchain-ollama==0.2.1 \
    langchain-core==0.3.21 \
    speech-recognition==3.12.0 \
    gtts==2.5.4 \
    pygame==2.6.1 \
    psutil==6.1.0 \
    requests==2.32.3 \
    python-dotenv==1.0.1 \
    keyboard==0.13.5

# Verify installation
pip list | grep -E "(langchain|gtts|pygame|speech|psutil)"
```

### **Step 5: Configuration**

#### Environment Variables
```bash
# Create .env file
cat > .env << EOF
# Weather API (get free key from openweathermap.org)
OPENWEATHER_API_KEY=your_api_key_here

# AI Model Configuration
OLLAMA_MODEL=qwen3:1.7b
OLLAMA_BASE_URL=http://localhost:11434

# Speech Configuration
SPEECH_RATE=180
TTS_LANGUAGE=en
MAX_SPEECH_LENGTH=300

# Audio Configuration
MICROPHONE_INDEX=0
ENERGY_THRESHOLD=4000
PAUSE_THRESHOLD=1.0

# Debug Settings
LOG_LEVEL=INFO
DEBUG_MODE=False
EOF
```

#### Get Weather API Key
1. Visit [OpenWeatherMap](https://openweathermap.org/api)
2. Sign up for free account
3. Get API key from account dashboard
4. Replace `your_api_key_here` in `.env` file

---

## 🧪 **Testing Your Installation**

### **Test 1: System Dependencies**
```bash
# Test Python
python --version

# Test audio libraries
python -c "import pyaudio; print('PyAudio OK')"
python -c "import pygame; pygame.mixer.init(); print('Pygame OK')"

# Test Ollama
ollama list
curl http://localhost:11434/api/tags
```

### **Test 2: Microphone**
```bash
# Run microphone test
python debug_mic.py

# Expected output:
# ✅ Microphone detected: USB Audio Device
# 🎤 Recording test... (speak now)
# ✅ Recording successful
```

### **Test 3: Text-to-Speech**
```bash
# Run TTS test
python test_improved_tts.py

# Should play audio samples with clean speech
```

### **Test 4: AI Model**
```bash
# Test Ollama connection
python -c "
from langchain_ollama import ChatOllama
llm = ChatOllama(model='qwen3:1.7b')
print(llm.invoke('Hello world'))
"
```

### **Test 5: Full System**
```bash
# Test text mode first (safer)
python text_jarvis.py

# Type: "What time is it?"
# Expected: AI response with current time

# Test voice mode (if text mode works)
python main.py
```

---

## 🔧 **Troubleshooting**

### **Common Issues & Solutions**

#### ❌ **"ModuleNotFoundError: No module named 'pyaudio'"**
```bash
# Install system dependencies first
sudo apt install portaudio19-dev python3-dev

# Then reinstall PyAudio
pip uninstall pyaudio
pip install pyaudio
```

#### ❌ **"ALSA lib pcm_dmix.c: unable to open slave"**
```bash
# Fix audio permissions
sudo usermod -a -G audio $USER
logout  # Log out and back in

# Or restart audio
systemctl --user restart pulseaudio
```

#### ❌ **"Connection error: Could not connect to Ollama"**
```bash
# Check Ollama service
sudo systemctl status ollama

# Restart if needed
sudo systemctl restart ollama

# Check port
netstat -tlnp | grep 11434
```

#### ❌ **"gTTS requires internet connection"**
```bash
# Test internet
ping google.com

# For offline use, will fallback to pyttsx3
pip install pyttsx3
```

#### ❌ **"Microphone not detected"**
```bash
# List audio devices
arecord -l

# Test microphone
arecord -d 5 test.wav && aplay test.wav

# Set specific microphone in debug_mic.py
```

### **Performance Issues**

#### **Slow AI responses**
- Use smaller model: `ollama pull qwen3:1b`
- Increase RAM allocation
- Close other applications

#### **Audio dropouts**
- Check audio buffer settings
- Use wired headphones instead of Bluetooth
- Reduce system load

#### **High CPU usage**
- Use lighter AI model
- Reduce TTS quality settings
- Limit background processes

---

## 🔄 **Updating Jarvis**

### **Update Python Packages**
```bash
source venv/bin/activate
pip install --upgrade -r requirements.txt
```

### **Update AI Model**
```bash
ollama pull qwen3:1.7b  # Re-download latest version
```

### **Update System Dependencies**
```bash
sudo apt update && sudo apt upgrade
```

---

## 📋 **Verification Checklist**

Before considering installation complete, verify:

- [ ] Python 3.12+ installed and working
- [ ] Virtual environment created and activated  
- [ ] All Python packages installed without errors
- [ ] Ollama service running and model downloaded
- [ ] Microphone detected and working
- [ ] TTS system producing audio
- [ ] AI model responding to test queries
- [ ] Environment variables configured
- [ ] Text mode working correctly
- [ ] Voice mode functioning (if applicable)

---

## 🎉 **You're Ready!**

If all tests pass, your Jarvis installation is complete! 

**Next steps:**
1. Read the [README.md](README.md) for usage instructions
2. Check [API_DOCUMENTATION.md](API_DOCUMENTATION.md) for advanced features
3. Run `python main.py` for full voice experience
4. Run `python text_jarvis.py` for text-only mode

**Get help:**
- Test individual components with provided scripts
- Check logs for detailed error information
- Refer to troubleshooting section above

---

*Installation complete! Welcome to Jarvis AI Assistant! 🤖*
