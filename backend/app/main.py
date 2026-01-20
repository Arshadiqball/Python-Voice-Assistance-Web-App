from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, FileResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import Optional
import uvicorn
import os
from dotenv import load_dotenv
import tempfile
import io
from pathlib import Path

from app.services.whisper_service import WhisperService
from app.services.bert_service import BertService
from app.services.gpt_service import GPTService
from app.services.tts_service import TTSService

load_dotenv()

# Get the project root directory (parent of backend)
BASE_DIR = Path(__file__).resolve().parent.parent.parent
WEB_DIR = BASE_DIR / "web"

app = FastAPI(title="Voice Assistant Web App", version="2.0.0")

# CORS middleware for web app
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files (CSS, JS, images)
if WEB_DIR.exists():
    app.mount("/static", StaticFiles(directory=str(WEB_DIR / "static")), name="static")

# Initialize services
whisper_service = WhisperService()
bert_service = BertService()
gpt_service = GPTService()
tts_service = TTSService()


class TextRequest(BaseModel):
    text: str


class VoiceResponse(BaseModel):
    text: str
    intent: str
    response: str
    audio_url: Optional[str] = None


@app.get("/", response_class=HTMLResponse)
async def root():
    """Serve the web interface"""
    html_file = WEB_DIR / "templates" / "index.html"
    if html_file.exists():
        with open(html_file, "r") as f:
            return HTMLResponse(content=f.read())
    return HTMLResponse(content="<h1>Web interface not found</h1>", status_code=404)


@app.get("/health")
async def health_check():
    return {"status": "healthy", "services": {
        "whisper": whisper_service.is_loaded(),
        "bert": bert_service.is_loaded(),
        "gpt": gpt_service.is_ready()
    }}


@app.post("/api/voice/transcribe", response_model=VoiceResponse)
async def process_voice(audio_file: UploadFile = File(...)):
    """
    Process voice input: transcribe, understand intent, generate response, and create TTS
    Supports WAV, WebM, MP3, and other audio formats
    """
    try:
        # Get file extension from content type or filename
        file_ext = ".wav"
        if audio_file.content_type:
            if "webm" in audio_file.content_type.lower():
                file_ext = ".webm"
            elif "mp3" in audio_file.content_type.lower():
                file_ext = ".mp3"
        elif audio_file.filename:
            file_ext = os.path.splitext(audio_file.filename)[1] or ".wav"
        
        # Save uploaded file temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix=file_ext) as tmp_file:
            content = await audio_file.read()
            tmp_file.write(content)
            tmp_path = tmp_file.name

        try:
            # Step 1: Transcribe audio using Whisper
            transcribed_text = await whisper_service.transcribe(tmp_path)
            
            if not transcribed_text or transcribed_text.strip() == "":
                raise HTTPException(status_code=400, detail="No speech detected in audio")

            # Step 2: Understand intent using BERT
            intent = await bert_service.classify_intent(transcribed_text)
            
            # Step 3: Generate response using GPT
            response_text = await gpt_service.generate_response(transcribed_text, intent)
            
            # Step 4: Generate TTS audio
            audio_path = await tts_service.text_to_speech(response_text)
            
            return VoiceResponse(
                text=transcribed_text,
                intent=intent,
                response=response_text,
                audio_url=f"/api/voice/audio/{os.path.basename(audio_path)}"
            )
        finally:
            # Clean up temporary file
            if os.path.exists(tmp_path):
                os.unlink(tmp_path)

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing voice: {str(e)}")


@app.post("/api/text/process")
async def process_text(request: TextRequest):
    """
    Process text input: understand intent and generate response
    """
    try:
        # Step 1: Understand intent using BERT
        intent = await bert_service.classify_intent(request.text)
        
        # Step 2: Generate response using GPT
        response_text = await gpt_service.generate_response(request.text, intent)
        
        # Step 3: Generate TTS audio
        audio_path = await tts_service.text_to_speech(response_text)
        
        return VoiceResponse(
            text=request.text,
            intent=intent,
            response=response_text,
            audio_url=f"/api/voice/audio/{os.path.basename(audio_path)}"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing text: {str(e)}")


@app.get("/api/voice/audio/{filename}")
async def get_audio(filename: str):
    """
    Serve generated audio files
    """
    audio_dir = "generated_audio"
    file_path = os.path.join(audio_dir, filename)
    
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="Audio file not found")
    
    return FileResponse(file_path, media_type="audio/mpeg")


if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    host = os.getenv("HOST", "0.0.0.0")
    uvicorn.run(app, host=host, port=port)

