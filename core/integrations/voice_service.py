"""Voice Service"""
from config.settings import config
import tempfile

class VoiceService:
    def __init__(self):
        self.enabled = config.FEATURES["voice"]
    
    async def speech_to_text(self, audio_file=None):
        if not self.enabled:
            return {"error": "Voice servisi devre dışı"}
        
        # Speech recognition implementation
        return {"text": "Örnek metin", "confidence": 0.95}
    
    async def text_to_speech(self, text, lang="tr"):
        if not self.enabled:
            return {"error": "Voice servisi devre dışı"}
        
        # TTS implementation
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
        return {"audio_file": temp_file.name, "duration": "2.5s"}
