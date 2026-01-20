# Project Structure

Complete Voice Assistant application with Transformer models.

## Directory Structure

```
.
├── backend/                          # Python FastAPI backend
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py                  # FastAPI server and routes
│   │   └── services/
│   │       ├── __init__.py
│   │       ├── whisper_service.py   # Whisper STT integration
│   │       ├── bert_service.py      # BERT intent classification
│   │       ├── gpt_service.py       # GPT response generation
│   │       └── tts_service.py       # Text-to-speech
│   ├── requirements.txt              # Python dependencies
│   ├── run.py                        # Server entry point
│   ├── .env.example                  # Environment variables template
│   └── .gitignore
│
├── flutter_app/                      # Flutter mobile app
│   ├── lib/
│   │   ├── main.dart                 # App entry point
│   │   ├── screens/
│   │   │   └── home_screen.dart      # Main UI screen
│   │   ├── providers/
│   │   │   └── voice_provider.dart  # State management
│   │   ├── services/
│   │   │   ├── api_service.dart     # Backend API client
│   │   │   └── audio_service.dart   # Audio recording
│   │   └── widgets/
│   │       ├── voice_button.dart    # Recording button
│   │       ├── conversation_card.dart
│   │       └── intent_badge.dart
│   ├── android/                      # Android configuration
│   │   └── app/
│   │       └── src/main/
│   │           ├── AndroidManifest.xml
│   │           └── kotlin/.../MainActivity.kt
│   ├── ios/                          # iOS configuration
│   │   └── Runner/
│   │       └── Info.plist
│   ├── pubspec.yaml                  # Flutter dependencies
│   └── analysis_options.yaml
│
├── README.md                         # Full documentation
├── QUICKSTART.md                     # Quick setup guide
├── setup_backend.sh                  # Backend setup script
├── setup_flutter.sh                  # Flutter setup script
└── .gitignore

```

## Key Components

### Backend Services

1. **WhisperService** (`whisper_service.py`)
   - Loads OpenAI Whisper model
   - Transcribes audio to text
   - Supports multiple model sizes

2. **BertService** (`bert_service.py`)
   - Loads BERT model for embeddings
   - Classifies user intent (greeting, question, command, etc.)
   - Uses keyword-based classification (can be fine-tuned)

3. **GPTService** (`gpt_service.py`)
   - Uses OpenAI API if key provided
   - Falls back to local GPT-2 model
   - Generates context-aware responses

4. **TTSService** (`tts_service.py`)
   - Converts text to speech using gTTS
   - Generates MP3 audio files
   - Returns audio file paths

### Flutter App

1. **HomeScreen** - Main UI with:
   - Voice recording button
   - Text input field
   - Status indicators
   - Conversation display

2. **VoiceProvider** - State management:
   - Recording state
   - API communication
   - Error handling

3. **ApiService** - Backend communication:
   - Voice processing endpoint
   - Text processing endpoint
   - Audio playback

4. **AudioService** - Audio recording:
   - Microphone access
   - WAV file recording
   - Permission handling

## API Endpoints

- `GET /` - API info
- `GET /health` - Service status
- `POST /api/voice/transcribe` - Process voice
- `POST /api/text/process` - Process text
- `GET /api/voice/audio/{filename}` - Get audio file

## Data Flow

1. **Voice Input**:
   ```
   User speaks → Flutter records → Upload to backend
   → Whisper transcribes → BERT classifies intent
   → GPT generates response → TTS creates audio
   → Response sent to Flutter → Audio played
   ```

2. **Text Input**:
   ```
   User types → Send to backend
   → BERT classifies intent → GPT generates response
   → TTS creates audio → Response sent to Flutter
   → Audio played
   ```

## Model Sizes

- Whisper base: ~150 MB
- BERT base: ~440 MB
- GPT-2: ~500 MB
- **Total**: ~1.1 GB (first download)

## Technologies Used

### Backend
- FastAPI - Web framework
- Whisper - Speech-to-text
- Transformers (Hugging Face) - BERT, GPT-2
- gTTS - Text-to-speech
- PyTorch - Deep learning framework

### Frontend
- Flutter - Cross-platform framework
- Provider - State management
- Record - Audio recording
- HTTP - API communication
- AudioPlayers - Audio playback

## Platform Support

- ✅ Android (API 21+)
- ✅ iOS (12.0+)
- ✅ Web (with limitations)
- ✅ macOS (with Flutter desktop)
- ✅ Windows (with Flutter desktop)
- ✅ Linux (with Flutter desktop)


