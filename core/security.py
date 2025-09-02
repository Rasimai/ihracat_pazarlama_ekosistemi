"""Security Module"""
from pathlib import Path
from typing import Dict, Any

class SecurityManager:
    def __init__(self):
        self.allowed_paths = [
            Path.home() / "Desktop",
            Path.home() / "Downloads",
            Path.home() / "Documents"
        ]
        
        self.dangerous_patterns = [
            "rm -rf", "delete", "format", 
            "sudo", "admin", "password"
        ]
    
    def validate_path(self, path: Path) -> bool:
        """Check if path is in whitelist"""
        path = Path(path).resolve()
        return any(
            str(path).startswith(str(allowed))
            for allowed in self.allowed_paths
        )
    
    def validate_command(self, command: str) -> Dict[str, Any]:
        """Validate user command"""
        command_lower = command.lower()
        
        for pattern in self.dangerous_patterns:
            if pattern in command_lower:
                return {
                    "valid": False,
                    "reason": f"Güvenlik: '{pattern}' komutu engellenmiştir"
                }
        
        return {"valid": True, "reason": None}
