"""File Operations"""
import os
from pathlib import Path

class FileOperations:
    def __init__(self):
        self.desktop = Path.home() / "Desktop"
    
    async def open_latest_image(self):
        images = list(self.desktop.glob("*.png")) + list(self.desktop.glob("*.jpg"))
        if images:
            latest = max(images, key=lambda p: p.stat().st_mtime)
            os.system(f"open '{latest}'")
            return f"✅ Açıldı: {latest.name}"
        return "❌ Görsel bulunamadı"
    
    async def list_files(self):
        files = list(self.desktop.iterdir())[:10]
        return "\n".join([f"📄 {f.name}" for f in files])
