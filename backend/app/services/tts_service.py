from gtts import gTTS
import os
import asyncio
from concurrent.futures import ThreadPoolExecutor
import uuid

class TTSService:
    def __init__(self):
        self.audio_dir = "generated_audio"
        self.executor = ThreadPoolExecutor(max_workers=2)
        self._ensure_audio_dir()
    
    def _ensure_audio_dir(self):
        """Create audio directory if it doesn't exist"""
        if not os.path.exists(self.audio_dir):
            os.makedirs(self.audio_dir)
    
    async def text_to_speech(self, text: str, language: str = "en") -> str:
        """
        Convert text to speech and save as MP3 file
        Returns path to the generated audio file
        """
        loop = asyncio.get_event_loop()
        audio_path = await loop.run_in_executor(
            self.executor,
            self._text_to_speech_sync,
            text,
            language
        )
        return audio_path
    
    def _text_to_speech_sync(self, text: str, language: str) -> str:
        """Synchronous text-to-speech conversion"""
        try:
            # Generate unique filename
            filename = f"{uuid.uuid4().hex}.mp3"
            filepath = os.path.join(self.audio_dir, filename)
            
            # Generate speech using gTTS
            tts = gTTS(text=text, lang=language, slow=False)
            tts.save(filepath)
            
            return filepath
        except Exception as e:
            raise Exception(f"TTS error: {str(e)}")


