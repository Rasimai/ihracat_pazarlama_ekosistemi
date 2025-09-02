"""Google Calendar Service"""
from datetime import datetime
from config.settings import config

class CalendarService:
    def __init__(self):
        self.enabled = config.FEATURES["calendar"]
        self.calendar_id = config.GOOGLE_CALENDAR_ID
    
    async def create_event(self, title, start, end, description=""):
        if not self.enabled:
            return {"error": "Calendar servisi devre dışı"}
        
        event = {
            "summary": title,
            "description": description,
            "start": start.isoformat(),
            "end": end.isoformat()
        }
        
        return {"success": True, "event_id": "mock_event_123", "event": event}
    
    async def list_events(self, date=None):
        if not self.enabled:
            return {"error": "Calendar servisi devre dışı"}
        
        # Mock data for testing
        return [
            {"title": "Toplantı", "time": "14:00", "duration": "1 saat"},
            {"title": "Sunum", "time": "16:00", "duration": "30 dakika"}
        ]
