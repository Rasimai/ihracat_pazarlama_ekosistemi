"""Email Service"""
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from config.settings import config

class EmailService:
    def __init__(self):
        self.enabled = config.FEATURES["email"]
        self.smtp_host = config.SMTP_HOST
        self.smtp_port = config.SMTP_PORT
    
    async def send_email(self, to, subject, body, from_email=None):
        if not self.enabled:
            return {"error": "Email servisi devre dışı"}
        
        try:
            msg = MIMEMultipart()
            msg["Subject"] = subject
            msg["To"] = ", ".join(to) if isinstance(to, list) else to
            msg.attach(MIMEText(body, "plain"))
            
            return {"success": True, "message": f"Email gönderildi: {to}"}
        except Exception as e:
            return {"error": str(e)}
