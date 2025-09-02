# enhanced_integration/core/key_manager.py - Mevcut sisteme entegre edilmiş key manager
import json
import os
from pathlib import Path
from typing import Dict, Optional, List

class EnhancedKeyManager:
    """Mevcut .env sistemi ile uyumlu Enhanced Key Manager"""
    
    def __init__(self, env_file: str = ".env", config_file: str = "config/api_keys.json"):
        self.env_file = Path(env_file)
        self.config_file = Path(config_file)
        self.keys = {}
        
        # Önce .env dosyasından yükle (mevcut sistem)
        self.load_from_env()
        
        # Sonra config dosyasından yükle (enhanced özellikler)
        self.load_from_config()
    
    def load_from_env(self):
        """Mevcut .env dosyasından key'leri yükle"""
        if self.env_file.exists():
            with open(self.env_file, 'r') as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#') and '=' in line:
                        key, value = line.split('=', 1)
                        self.keys[key.strip()] = value.strip().strip('"').strip("'")
        
        print(f"Loaded {len(self.keys)} keys from .env file")
    
    def load_from_config(self):
        """Enhanced config dosyasından ek key'leri yükle"""
        if self.config_file.exists():
            try:
                with open(self.config_file, 'r') as f:
                    config_keys = json.load(f)
                    # Config'deki key'leri de ekle (mevcut olanları geçersiz kılma)
                    for key, value in config_keys.items():
                        if not key.startswith('_') and value:  # _ ile başlayanlar notlar
                            if key not in self.keys or not self.keys[key]:
                                self.keys[key] = value
            except Exception as e:
                print(f"Config file yükleme hatası: {e}")
        else:
            self.create_config_template()
    
    def create_config_template(self):
        """Enhanced özellikler için config template oluştur"""
        os.makedirs(self.config_file.parent, exist_ok=True)
        
        template = {
            "_INFO": {
                "description": "Enhanced Key Manager - Ek API keys",
                "note": "Bu dosyadaki key'ler .env dosyasındakileri tamamlar"
            },
            "hunter_io_api_key": "",
            "google_vision_credentials_path": "",
            "redis_url": "redis://localhost:6379",
            "performance_cache_ttl": "3600",
            "enhanced_features_enabled": "true"
        }
        
        with open(self.config_file, 'w') as f:
            json.dump(template, f, indent=4)
        
        print(f"Config template created: {self.config_file}")
    
    def get_key(self, key_name: str, default: str = "") -> str:
        """Key al - hem .env hem config'den"""
        return self.keys.get(key_name, default)
    
    def get_github_token(self) -> Optional[str]:
        """GitHub token al"""
        return self.get_key('GITHUB_TOKEN')
    
    def get_hunter_io_key(self) -> Optional[str]:
        """Hunter.io API key al"""
        return self.get_key('HUNTER_API_KEY') or self.get_key('hunter_io_api_key')
    
    def get_gmail_credentials(self) -> Dict[str, str]:
        """Gmail credentials al"""
        return {
            'client_id': self.get_key('GMAIL_CLIENT_ID'),
            'client_secret': self.get_key('GMAIL_CLIENT_SECRET'),
            'smtp_username': self.get_key('smtp_username'),
            'smtp_password': self.get_key('smtp_password')
        }
    
    def get_database_url(self) -> str:
        """Database URL al"""
        return self.get_key('DATABASE_URL', 'sqlite:///jarvis_enhanced.db')
    
    def get_redis_url(self) -> str:
        """Redis URL al"""
        return self.get_key('REDIS_URL', 'redis://localhost:6379')
    
    def validate_keys(self) -> Dict[str, bool]:
        """Key'lerin doluluğunu kontrol et"""
        critical_keys = [
            'GITHUB_TOKEN',
            'GMAIL_CLIENT_ID', 
            'GMAIL_CLIENT_SECRET'
        ]
        
        validation = {}
        for key in critical_keys:
            value = self.get_key(key)
            validation[key] = bool(value and value.strip() and value != 'your_key_here')
        
        return validation
    
    def get_missing_keys(self) -> List[str]:
        """Eksik key'leri listele"""
        validation = self.validate_keys()
        return [key for key, is_valid in validation.items() if not is_valid]
    
    def is_ready(self) -> bool:
        """Sistem hazır mı?"""
        missing = self.get_missing_keys()
        return len(missing) == 0
    
    def get_all_keys(self) -> Dict[str, str]:
        """Tüm key'leri döndür (debug için)"""
        return {k: ('***' + v[-4:] if len(v) > 4 else '***') for k, v in self.keys.items() if v}
    
    def sync_with_env(self, new_keys: Dict[str, str]):
        """Yeni key'leri .env dosyasına yaz"""
        env_content = []
        
        # Mevcut .env içeriğini oku
        if self.env_file.exists():
            with open(self.env_file, 'r') as f:
                env_content = f.readlines()
        
        # Yeni key'leri ekle veya güncelle
        for key, value in new_keys.items():
            found = False
            for i, line in enumerate(env_content):
                if line.strip().startswith(f"{key}="):
                    env_content[i] = f"{key}={value}\n"
                    found = True
                    break
            
            if not found:
                env_content.append(f"{key}={value}\n")
        
        # .env dosyasına yaz
        with open(self.env_file, 'w') as f:
            f.writelines(env_content)
        
        # Hafızayı güncelle
        self.keys.update(new_keys)
        
        print(f"Updated {len(new_keys)} keys in .env file")

# Global instance - mevcut sistemle uyumlu
enhanced_key_manager = EnhancedKeyManager()
