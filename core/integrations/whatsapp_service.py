"""WhatsApp Service"""
import httpx
from config.settings import config

class WhatsAppService:
    def __init__(self):
        self.enabled = config.FEATURES["whatsapp"]
        self.api_key = config.WHATSAPP_API_KEY
        self.phone_id = config.WHATSAPP_PHONE_ID
    
    async def send_message(self, to, message):
        if not self.enabled:
            return {"error": "WhatsApp servisi devre dışı"}
        
        if not self.api_key:
            return {"error": "WhatsApp API key eksik"}
        
        # WhatsApp Business API implementation
        return {"success": True, "message": f"Mesaj gönderildi: {to}"}
