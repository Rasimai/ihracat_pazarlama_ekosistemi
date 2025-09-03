import os
import json
from pathlib import Path
from typing import Dict, Optional

class EnhancedKeyManager:
    def __init__(self):
        self.keys = {}
        self.load_keys()
    
    def load_keys(self):
        if os.path.exists("config/api_keys.json"):
            with open("config/api_keys.json", "r") as f:
                self.keys = json.load(f)
        print(f"✅ Loaded {len(self.keys)} API keys")
    
    def get_key(self, key_name: str) -> Optional[str]:
        return self.keys.get(key_name)
    
    def is_ready(self) -> bool:
        return len(self.keys) > 0

enhanced_key_manager = EnhancedKeyManager()
