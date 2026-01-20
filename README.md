# Voice Assistant Web App

A complete Voice Assistant application using Transformer architectures with Whisper (speech-to-text), BERT (intent classification), and GPT (response generation). Now available as a modern web application!

## 🌟 Features

✅ **Voice Input Recording** - Record audio directly in your browser  
✅ **Speech-to-Text** - Using OpenAI Whisper model  
✅ **Intent Classification** - Using BERT model  
✅ **Context-aware Responses** - Using GPT model  
✅ **Text-to-Speech** - Audio responses with gTTS  
✅ **Text Input Alternative** - Type messages if preferred  
✅ **Beautiful Modern UI** - Responsive web interface  
✅ **Real-time Status Indicators** - Visual feedback  
✅ **Error Handling** - Graceful error management  

## 🏗️ Architecture

- **Backend (Python)**: FastAPI server with Transformer models
  - **Whisper**: Speech-to-text transcription
  - **BERT**: Intent classification and understanding
  - **GPT**: Natural language response generation
  - **TTS**: Text-to-speech for audio responses

- **Frontend (Web)**: Modern web interface
  - HTML5/CSS3/JavaScript
  - Web Audio API for voice recording
  - Responsive design
  - Real-time updates

## 📁 Project Structure

```
.
├── backend/
│   ├── app/
│   │   ├── main.py              # FastAPI server with web routes
│   │   └── services/
│   │       ├── whisper_service.py
│   │       ├── bert_service.py
│   │       ├── gpt_service.py
│   │       └── tts_service.py
│   ├── requirements.txt
│   ├── run.py
│   └── generated_audio/        # Generated TTS audio files
│
└── web/
    ├── templates/
    │   └── index.html           # Main web interface
    └── static/
        ├── css/
        │   └── style.css       # Styling
        └── js/
            └── app.js          # Frontend logic
```

## 🚀 Quick Start

### Prerequisites

- Python 3.10+ (Python 3.14 recommended for Whisper)
- pip
- Git (for installing Whisper)
- **ffmpeg** (required for audio processing)
  - macOS: `brew install ffmpeg`
  - Linux: `sudo apt-get install ffmpeg` (Ubuntu/Debian) or `sudo yum install ffmpeg` (CentOS/RHEL)
  - Windows: Download from [ffmpeg.org](https://ffmpeg.org/download.html)

### Setup Instructions

1. **Navigate to backend directory:**
   ```bash
   cd backend
   ```

2. **Create virtual environment:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Install Whisper (if not already installed):**
   ```bash
   pip install git+https://github.com/openai/whisper.git
   ```

5. **Create .env file (optional):**
   ```bash
   cp .env.example .env
   ```
   Edit `.env` and add your OpenAI API key if you want to use GPT-4 instead of local GPT-2:
   ```
   OPENAI_API_KEY=your_api_key_here
   ```

6. **Start the backend server:**
   ```bash
   python run.py
   ```
   Or:
   ```bash
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```
   The backend will run on port 8000.

7. **Start the web frontend (in a new terminal):**
   ```bash
   # From project root
   python web_server.py
   ```
   The web frontend will run on port 3000 by default.
   
   You can customize ports using environment variables:
   ```bash
   WEB_PORT=3000 BACKEND_PORT=8000 python web_server.py
   ```

8. **Open your browser:**
   Navigate to `http://localhost:3000` (or the port you configured)

## 🎯 Usage

### Voice Input
1. Click the microphone button
2. Speak your message
3. Click again to stop recording
4. Wait for transcription and response

### Text Input
1. Type your message in the text field
2. Press Enter or click Send
3. Receive AI-generated response

### Audio Response
- Click "🔊 Play Response" to hear the audio version of the assistant's reply

## 🔌 API Endpoints

- `GET /` - Web interface
- `GET /health` - Service status check
- `POST /api/voice/transcribe` - Process voice input
- `POST /api/text/process` - Process text input
- `GET /api/voice/audio/{filename}` - Get generated audio file

## 🧠 Model Information

### Whisper
- Model: `base` (default, ~150 MB)
- Supports multiple languages
- Handles various audio formats (WAV, WebM, MP3)

### BERT
- Model: `bert-base-uncased`
- Intent classification
- ~440 MB (first download)

### GPT
- Primary: OpenAI GPT-4 (if API key provided)
- Fallback: Local GPT-2 (~500 MB)
- Context-aware response generation

### TTS
- Service: Google Text-to-Speech (gTTS)
- Generates MP3 audio files
- Multiple language support

## 🛠️ Technologies Used

### Backend
- **FastAPI** - Modern web framework
- **Whisper** - Speech-to-text
- **Transformers (Hugging Face)** - BERT, GPT-2
- **gTTS** - Text-to-speech
- **PyTorch** - Deep learning framework

### Frontend
- **HTML5** - Structure
- **CSS3** - Styling with modern design
- **JavaScript (ES6+)** - Interactivity
- **Web Audio API** - Browser-based recording

## 🌐 Browser Compatibility

- ✅ Chrome/Edge (recommended)
- ✅ Firefox
- ✅ Safari
- ✅ Opera

**Note**: Microphone permissions are required for voice recording.

## 📝 Environment Variables

Create a `.env` file in the `backend` directory:

```env
# Optional: OpenAI API key for GPT-4
OPENAI_API_KEY=your_api_key_here

# Server configuration (optional)
PORT=8000
HOST=0.0.0.0
```

## 🐛 Troubleshooting

### Microphone Not Working
- Ensure browser has microphone permissions
- Check browser settings for site permissions
- Try a different browser

### Models Not Loading
- Check internet connection (first-time download)
- Verify sufficient disk space (~1.1 GB for all models)
- Check Python version (3.10+ recommended)

### Audio Playback Issues
- Check browser audio settings
- Verify audio file was generated successfully
- Try refreshing the page

## 📊 Performance

- **First Request**: ~10-30 seconds (model loading)
- **Subsequent Requests**: ~2-5 seconds
- **Voice Recording**: Real-time in browser
- **Audio Generation**: ~1-2 seconds

## 🔒 Security Notes

- CORS is enabled for development (adjust for production)
- API keys should be kept secure
- Consider rate limiting for production use

## 📄 License

This project is for educational purposes.

## 🤝 Contributing

Feel free to submit issues and enhancement requests!

## 📚 Additional Resources

- [Whisper Documentation](https://github.com/openai/whisper)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Transformers Documentation](https://huggingface.co/docs/transformers)

---

**Enjoy your AI-powered voice assistant! 🎉**
