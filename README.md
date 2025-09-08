# 🧠 Jarvis – Local Voice-Controlled AI Assistant

**Jarvis** is a voice-activated, conversational AI assistant powered by a local LLM (Qwen via Ollama). It listens for a wake word, processes spoken commands using a local language model with LangChain, and responds out loud via TTS. It supports tool-calling for dynamic functions like checking the current time.

---

## 🚀 Features

- 🗣 Voice-activated with wake word **"Jarvis"**
- 🧠 Local language model (Qwen 3 via Ollama)
- 🔧 Tool-calling with LangChain
- 🔊 Text-to-speech responses via `pyttsx3`
- 🌍 Example tool: Get the current time in a given city
- 🔐 Optional support for OpenAI API integration

---


## ▶️ How It Works (`main.py`)

1. **Startup & local LLM Setup**
   - Initializes a local Ollama model (`qwen3:1.7b`) via `ChatOllama`
   - Registers tools (`get_time`) using LangChain

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

## 🤖 How To Start Jarvis

> **Note for Windows Users:** This project uses `make`. If you don't have it, you can install it easily with a package manager like [Chocolatey](https://chocolatey.org/) by running `choco install make`.

1. **Install Dependencies**  
   Use the provided Makefile to install dependencies with uv:
   ```bash
   make install
   ```
   This will automatically install uv if not present and install all dependencies.

2. **Set Up the Local Model**  
   Ensure you have the `qwen3:1.7b` model available in Ollama.

3. **Run Jarvis**  
   Start the assistant by running:
   ```bash
   make run
   ```
---

