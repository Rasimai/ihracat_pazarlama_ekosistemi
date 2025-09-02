"""Complete Jarvis Orchestrator with All Features"""
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent.parent))

from datetime import datetime
from config.settings import config
from core.integrations.email_service import EmailService
from core.integrations.whatsapp_service import WhatsAppService
from core.integrations.calendar_service import CalendarService
from core.integrations.voice_service import VoiceService
from core.integrations.database_service import DatabaseService

class JarvisComplete:
    def __init__(self):
        # Initialize all services
        self.email = EmailService()
        self.whatsapp = WhatsAppService()
        self.calendar = CalendarService()
        self.voice = VoiceService()
        self.database = DatabaseService()
        
        # System state
        self.validation = config.validate()
        self.history = []
        
        print(f"Jarvis Complete initialized. Services: {self.get_status()}")
    
    async def process(self, message, context=None):
        """Ana işlem fonksiyonu"""
        start = datetime.now()
        
        # Mesajı küçük harfe çevir
        msg_lower = message.lower()
        
        # Komutu işle
        if "email" in msg_lower or "e-posta" in msg_lower:
            response = await self.handle_email(message)
        elif "whatsapp" in msg_lower or "mesaj" in msg_lower:
            response = await self.handle_whatsapp(message)
        elif "takvim" in msg_lower or "calendar" in msg_lower or "etkinlik" in msg_lower:
            response = await self.handle_calendar(message)
        elif "ses" in msg_lower or "konuş" in msg_lower:
            response = await self.handle_voice(message)
        elif "geçmiş" in msg_lower or "history" in msg_lower:
            response = await self.handle_history()
        elif "durum" in msg_lower or "status" in msg_lower:
            response = self.get_detailed_status()
        else:
            response = await self.handle_default(message)
        
        # Veritabanına kaydet
        duration = int((datetime.now() - start).total_seconds() * 1000)
        await self.database.save_command(message, response, duration)
        
        # History'ye ekle
        self.history.append({
            "message": message,
            "response": response,
            "timestamp": datetime.now().isoformat()
        })
        
        # Result object
        class Result:
            def __init__(self, msg):
                self.success = True
                self.message = msg
                self.data = {"duration_ms": duration}
        
        return Result(response)
    
    async def handle_email(self, message):
        """Email işlemleri"""
        if not self.email.enabled:
            return "Email servisi aktif değil. .env dosyasında ENABLE_EMAIL=true yapın."
        
        result = await self.email.send_email(
            to=["test@example.com"],
            subject="Jarvis Test Email",
            body=message
        )
        
        if "error" in result:
            return f"Email gönderilemedi: {result['error']}"
        
        return "✅ Email başarıyla gönderildi!"
    
    async def handle_whatsapp(self, message):
        """WhatsApp işlemleri"""
        if not self.whatsapp.enabled:
            return "WhatsApp servisi aktif değil. API anahtarını ekleyin."
        
        result = await self.whatsapp.send_message("+905551234567", message)
        
        if "error" in result:
            return f"WhatsApp mesajı gönderilemedi: {result['error']}"
        
        return "✅ WhatsApp mesajı gönderildi!"
    
    async def handle_calendar(self, message):
        """Takvim işlemleri"""
        if not self.calendar.enabled:
            return "Calendar servisi aktif değil."
        
        events = await self.calendar.list_events()
        
        if isinstance(events, dict) and "error" in events:
            return events["error"]
        
        if not events:
            return "Bugün etkinlik yok."
        
        response = "📅 Bugünkü Etkinlikler:\n"
        for event in events:
            response += f"• {event['time']}: {event['title']} ({event.get('duration', 'N/A')})\n"
        
        return response
    
    async def handle_voice(self, message):
        """Ses işlemleri"""
        if not self.voice.enabled:
            return "Ses servisi aktif değil. Gerekli modülleri yükleyin."
        
        result = await self.voice.text_to_speech(message)
        
        if "error" in result:
            return f"Ses oluşturulamadı: {result['error']}"
        
        return f"🔊 Ses dosyası oluşturuldu: {result['audio_file']}"
    
    async def handle_history(self):
        """Geçmiş komutları göster"""
        history = await self.database.get_history(5)
        
        if not history:
            return "Henüz komut geçmişi yok."
        
        response = "📜 Son 5 Komut:\n"
        for i, cmd in enumerate(history, 1):
            response += f"{i}. {cmd['input'][:50]}... ({cmd.get('duration_ms', 0)}ms)\n"
        
        return response
    
    async def handle_default(self, message):
        """Varsayılan işlemler"""
        # Basit komutlar için mevcut handler'ları kullan
        from core.tools.file_ops import FileOperations
        from core.tools.excel_pro import ExcelProcessor
        
        if "excel" in message.lower():
            excel = ExcelProcessor()
            return await excel.create_excel({})
        elif "dosya" in message.lower():
            file_ops = FileOperations()
            return await file_ops.list_files()
        
        return f"Komut alındı: {message}"
    
    def get_status(self):
        """Servis durumları"""
        return {
            "email": self.email.enabled,
            "whatsapp": self.whatsapp.enabled,
            "calendar": self.calendar.enabled,
            "voice": self.voice.enabled,
            "database": self.database.enabled
        }
    
    def get_detailed_status(self):
        """Detaylı sistem durumu"""
        status = self.get_status()
        validation = self.validation
        
        response = "🔧 Sistem Durumu:\n\n"
        response += "Servisler:\n"
        
        for service, enabled in status.items():
            emoji = "✅" if enabled else "❌"
            response += f"{emoji} {service.capitalize()}: {'Aktif' if enabled else 'Devre Dışı'}\n"
        
        response += "\nDoğrulama:\n"
        for key, valid in validation.items():
            emoji = "✅" if valid else "⚠️"
            response += f"{emoji} {key}: {'OK' if valid else 'Eksik'}\n"
        
        return response
