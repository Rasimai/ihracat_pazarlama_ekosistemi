"""Manifest-based Auto Updater System"""
import requests
import zipfile
import json
import shutil
from pathlib import Path
from datetime import datetime
from config.settings import config

class ManifestUpdater:
    """Otomatik güncelleme sistemi"""
    
    def __init__(self):
        self.current_version = "1.0.0"
        self.manifest_url = None
        self.protected_dirs = [".venv", "venv", "state", ".streamlit", ".git", "data"]
        self.backup_dir = Path("backups")
    
    def check_updates(self, manifest_url: str) -> dict:
        """Güncelleme kontrolü"""
        try:
            response = requests.get(manifest_url, timeout=10)
            manifest = response.json()
            
            if self._compare_versions(manifest["version"], self.current_version) > 0:
                return {
                    "available": True,
                    "current": self.current_version,
                    "new": manifest["version"],
                    "notes": manifest.get("notes", ""),
                    "zip_url": manifest["zip_url"],
                    "size": manifest.get("size", "Unknown")
                }
            
            return {"available": False, "current": self.current_version}
            
        except Exception as e:
            return {"error": str(e)}
    
    def apply_update(self, zip_url: str) -> dict:
        """Güncellemeyi uygula"""
        try:
            # 1. Backup oluştur
            backup_path = self._create_backup()
            
            # 2. ZIP indir
            temp_zip = Path("temp_update.zip")
            response = requests.get(zip_url, stream=True)
            
            with open(temp_zip, "wb") as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            
            # 3. Extract et (korunan dizinler hariç)
            with zipfile.ZipFile(temp_zip, "r") as zip_ref:
                for file in zip_ref.namelist():
                    if not any(file.startswith(p) for p in self.protected_dirs):
                        zip_ref.extract(file, ".")
            
            # 4. Temizlik
            temp_zip.unlink()
            
            return {
                "status": "success",
                "message": "Güncelleme başarıyla uygulandı",
                "backup": str(backup_path),
                "restart_required": True
            }
            
        except Exception as e:
            return {"status": "error", "message": str(e)}
    
    def _compare_versions(self, v1: str, v2: str) -> int:
        """Versiyon karşılaştırma"""
        v1_parts = [int(x) for x in v1.split(".")]
        v2_parts = [int(x) for x in v2.split(".")]
        
        for i in range(max(len(v1_parts), len(v2_parts))):
            p1 = v1_parts[i] if i < len(v1_parts) else 0
            p2 = v2_parts[i] if i < len(v2_parts) else 0
            
            if p1 > p2:
                return 1
            elif p1 < p2:
                return -1
        
        return 0
    
    def _create_backup(self) -> Path:
        """Güncelleme öncesi backup"""
        self.backup_dir.mkdir(exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_path = self.backup_dir / f"backup_{timestamp}.zip"
        
        with zipfile.ZipFile(backup_path, "w") as zip_ref:
            for path in Path(".").rglob("*"):
                if not any(p in str(path) for p in self.protected_dirs):
                    zip_ref.write(path)
        
        return backup_path
    
    def rollback(self, backup_path: str) -> dict:
        """Güncellemeyi geri al"""
        try:
            with zipfile.ZipFile(backup_path, "r") as zip_ref:
                zip_ref.extractall(".")
            
            return {"status": "success", "message": "Rollback tamamlandı"}
            
        except Exception as e:
            return {"status": "error", "message": str(e)}

# Global updater instance
updater = ManifestUpdater()
