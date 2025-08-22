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

## 🤖 Getting Started: A Step-by-Step Guide

This guide will walk you through setting up Jarvis from scratch on your local machine.

### Step 1: Set Up Your Project Folder

First, create a dedicated folder on your computer for this project. You can name it something like `Jarvis-AI`.

### Step 2: Download the Code

Download the project code as a `.zip` file from the repository. Once downloaded, move the `.zip` file into the `Jarvis-AI` folder you just created. Right-click on the `.zip` file and select "Extract All" to unzip the contents.

### Step 3: Set Up a Python Virtual Environment

It's a best practice to use a virtual environment to manage dependencies for your project.

1.  Open your terminal or command prompt.
2.  Navigate to your project folder:
    ```bash
    cd path/to/Jarvis-AI
    ```
3.  Create a virtual environment:
    ```bash
    python -m venv venv
    ```
4.  Activate the virtual environment:
    * **On Windows:**
        ```bash
        .\venv\Scripts\activate
        ```
    * **On macOS/Linux:**
        ```bash
        source venv/bin/activate
        ```
    You should now see `(venv)` at the beginning of your terminal prompt, indicating the virtual environment is active.

### Step 4: Install Dependencies

With your virtual environment activated, install all the required Python libraries using the `requirements.txt` file.

```bash
pip install -r requirements.txt

### Step 5: Install and Configure Ollama
Jarvis uses Ollama to run the language model locally.

Download Ollama: Go to the official Ollama website and download the installer for your operating system.

Install Ollama: Run the installer and follow the on-screen instructions.

Download the Qwen Model: Open a new terminal or command prompt and run the following command to download the qwen3:1.7b model.

ollama run qwen3:1.7b

This will download the model to your local machine. You can then exit the Ollama session by typing /bye


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

1. **Install Dependencies**  
   Make sure you have installed all required dependencies listed in `requirements.txt`:
   ```bash
   pip install -r requirements.txt
   ```

2. **Set Up the Local Model**  
   Ensure you have the `qwen3:1.7b` model available in Ollama.

3. **Run Jarvis**  
   Start the assistant by running:
   ```bash
   python main.py
   ```
---

