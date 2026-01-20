import whisper
import os
from dotenv import load_dotenv
import asyncio
from concurrent.futures import ThreadPoolExecutor

load_dotenv()

class WhisperService:
    def __init__(self):
        self.model = None
        self.model_name = os.getenv("WHISPER_MODEL", "base")
        self.executor = ThreadPoolExecutor(max_workers=1)
        self._load_model()
    
    def _load_model(self):
        """Load Whisper model asynchronously"""
        print(f"Loading Whisper model: {self.model_name}")
        try:
            self.model = whisper.load_model(self.model_name)
            print("Whisper model loaded successfully")
        except Exception as e:
            print(f"Error loading Whisper model: {e}")
            # Fallback to smaller model if base fails
            try:
                self.model_name = "tiny"
                self.model = whisper.load_model(self.model_name)
                print("Loaded fallback Whisper model: tiny")
            except Exception as e2:
                print(f"Error loading fallback model: {e2}")
                raise
    
    def is_loaded(self):
        return self.model is not None
    
    async def transcribe(self, audio_path: str) -> str:
        """
        Transcribe audio file to text using Whisper
        """
        if not self.model:
            raise Exception("Whisper model not loaded")
        
        # Run transcription in thread pool to avoid blocking
        loop = asyncio.get_event_loop()
        result = await loop.run_in_executor(
            self.executor,
            self._transcribe_sync,
            audio_path
        )
        return result
    
    def _transcribe_sync(self, audio_path: str) -> str:
        """Synchronous transcription"""
        try:
            # Check if ffmpeg is available
            import subprocess
            try:
                subprocess.run(['ffmpeg', '-version'], capture_output=True, check=True)
            except (subprocess.CalledProcessError, FileNotFoundError):
                raise Exception("ffmpeg is not installed. Please install it using: brew install ffmpeg (macOS) or apt-get install ffmpeg (Linux)")
            
            # Transcribe audio
            result = self.model.transcribe(
                audio_path,
                language="en",
                task="transcribe",
                fp16=False  # Use fp32 for better compatibility
            )
            return result["text"].strip()
        except Exception as e:
            error_msg = str(e)
            if "ffmpeg" in error_msg.lower() or "no such file" in error_msg.lower():
                raise Exception("ffmpeg is not installed. Please install it using: brew install ffmpeg (macOS) or apt-get install ffmpeg (Linux)")
            raise Exception(f"Transcription error: {error_msg}")


