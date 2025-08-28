import json
import os
import smtplib
import time
from email.message import EmailMessage

import redis

r = redis.Redis(
    host=os.getenv("REDIS_HOST", "redis"),
    port=int(os.getenv("REDIS_PORT", "6379")),
    db=0,
)


def process_text(text: str) -> str:
    # Basit örnek: metni büyüt
    time.sleep(1)
    return text.upper()


def send_email(to_addr: str, subject: str, body: str):
    host = os.getenv("SMTP_HOST", "mailhog")
    port = int(os.getenv("SMTP_PORT", "1025"))
    sender = os.getenv("EMAIL_FROM", "no-reply@example.local")
    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = sender
    msg["To"] = to_addr
    msg.set_content(body)
    with smtplib.SMTP(host, port) as s:
        s.send_message(msg)


def main():
    print("worker: started")
    while True:
        _, raw = r.brpop("ipe:jobs")
        job = json.loads(raw)
        result = process_text(job["text"])
        if job.get("notify_email"):
            send_email(job["notify_email"], "Directive tamamlandı", f"Sonuç: {result}")


if __name__ == "__main__":
    main()
