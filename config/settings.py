"""Merkezi Konfigürasyon Sistemi"""
import os
from pathlib import Path
import json

class Config:
    BASE_DIR = Path(__file__).parent.parent
    DATA_DIR = BASE_DIR / "data"
    LOGS_DIR = BASE_DIR / "logs"
    TEMP_DIR = BASE_DIR / "temp"
    
    # API Keys
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
    ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")
    GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY", "")
    GITHUB_TOKEN = os.getenv("GITHUB_TOKEN", "")
    
    # Email
    GMAIL_CLIENT_ID = os.getenv("GMAIL_CLIENT_ID", "")
    GMAIL_CLIENT_SECRET = os.getenv("GMAIL_CLIENT_SECRET", "")
    SMTP_HOST = os.getenv("SMTP_HOST", "smtp.gmail.com")
    SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
    
    # WhatsApp
    WHATSAPP_API_KEY = os.getenv("WHATSAPP_API_KEY", "")
    WHATSAPP_PHONE_ID = os.getenv("WHATSAPP_PHONE_ID", "")
    
    # Calendar
    GOOGLE_CALENDAR_ID = os.getenv("GOOGLE_CALENDAR_ID", "primary")
    
    # Database
    DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///jarvis.db")
    REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379")
    
    # Ports
    API_PORT = int(os.getenv("API_PORT", "8000"))
    UI_PORT = int(os.getenv("UI_PORT", "8501"))
    BRIDGE_PORT = int(os.getenv("BRIDGE_PORT", "9999"))
    
    # Features
    FEATURES = {
        "email": os.getenv("ENABLE_EMAIL", "true").lower() == "true",
        "whatsapp": os.getenv("ENABLE_WHATSAPP", "false").lower() == "true",
        "calendar": os.getenv("ENABLE_CALENDAR", "true").lower() == "true",
        "voice": os.getenv("ENABLE_VOICE", "false").lower() == "true",
        "database": os.getenv("ENABLE_DATABASE", "true").lower() == "true",
    }
    
    @classmethod
    def validate(cls):
        validation = {}
        validation["github"] = bool(cls.GITHUB_TOKEN)
        validation["openai"] = bool(cls.OPENAI_API_KEY)
        validation["paths"] = cls.BASE_DIR.exists()
        return validation

config = Config()
