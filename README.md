 AI Voice Interview Agent (Thrisha Karkera)

An interactive **voice-based AI interview assistant** that listens to interviewer questions and responds with **intelligent answers in both text and speech**.

This project combines **speech recognition, predefined logic, and LLM fallback** to simulate a structured technical interview.

---

## 🚀 Live Demo

👉 Deployed on Hugging Face: https://huggingface.co/spaces/Thrisha2005/voicebot

---

## ✨ Features

* 🎤 **Voice Input** — Ask questions using your microphone
* 🧠 **Smart Question Matching** — Detects intent using keyword-based matching
* 📚 **Predefined Answers** — High-quality, structured responses for common interview questions
* 🤖 **LLM Fallback (Groq + LLaMA)** — Handles unexpected questions dynamically
* 🔊 **Voice Output (TTS)** — Converts answers into speech using gTTS
* 💬 **Text Output** — Displays conversation clearly
* 🧾 **Conversation Memory** — Maintains chat history for context

---

## 🛠️ Tech Stack

* **Python**
* **Gradio** — UI interface
* **Groq API**

  * Whisper (`whisper-large-v3`) for speech-to-text
  * LLaMA (`llama-3.3-70b-versatile`) for fallback responses
* **gTTS** — Text-to-speech
* **pydub** — Audio processing

---

## 🧩 How It Works

1. 🎤 User records a question
2. 🔄 Audio is converted to `.wav` format
3. 🧠 Whisper (via Groq) transcribes speech → text
4. 🔍 System checks for a **predefined answer** using smart keyword matching
5. 🤖 If no match → fallback to LLaMA model
6. 🔊 Response is converted to speech (gTTS)
7. 💬 Output is shown as both **text + audio**

---

## 🧠 Smart Answer System

The assistant prioritizes **scripted, high-quality answers** for common interview questions like:

* "Tell me about yourself"
* "What are your strengths?"
* "Why should we hire you?"
* "What are your weaknesses?"
* "Where do you see yourself in 5 years?"

If a question doesn't match → it uses **LLM fallback** to generate a response.

---

## 📂 Project Structure

```
├── app.py              # Main application (Gradio UI + logic)
├── requirements.txt   # Dependencies
└── README.md          # Documentation
```

---

## ▶️ Run Locally

### 1. Clone the repository

```bash
git clone https://github.com/your-username/ai-voice-interview-agent.git
cd ai-voice-interview-agent
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Set API Key

```bash
export GROQ_API_KEY=your_api_key_here
```

### 4. Run the app

```bash
python app.py
```

---

## 🔑 Environment Variables

| Variable     | Description      |
| ------------ | ---------------- |
| GROQ_API_KEY | API key for Groq |

---

## ⚠️ Limitations

* Works best with **clear voice input**
* Scripted answers rely on keyword matching (not full NLP intent detection)
* Internet required for Groq API calls
* gTTS may introduce slight latency

---

## 🔮 Future Improvements

* ✅ Replace keyword matching with semantic search / embeddings
* ✅ Add multilingual support
* ✅ Improve voice quality with advanced TTS models
* ✅ Add real-time streaming responses
* ✅ Expand interview question coverage

---

## 📸 UI Preview

*(Add screenshots from your Hugging Face app here)*

---

## 🤝 Contributing

Contributions are welcome! Feel free to fork the repo and improve the system.

---

## 📜 License

MIT License 

---

## 🙌 Acknowledgements

* Groq for ultra-fast inference
* Open-source speech & audio libraries
* Gradio for rapid UI development

---

## 👤 Author

**Thrisha Karkera**

---
