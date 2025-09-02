"""Database Service"""
from datetime import datetime
from config.settings import config
import json
from pathlib import Path

class DatabaseService:
    def __init__(self):
        self.enabled = config.FEATURES["database"]
        self.db_file = Path("data/commands.json")
        self.db_file.parent.mkdir(exist_ok=True)
        
        if self.db_file.exists():
            with open(self.db_file) as f:
                self.commands = json.load(f)
        else:
            self.commands = []
    
    async def save_command(self, user_input, response, duration=0):
        if not self.enabled:
            return
        
        command = {
            "input": user_input,
            "response": response[:500],  # Truncate long responses
            "timestamp": datetime.now().isoformat(),
            "duration_ms": duration
        }
        
        self.commands.append(command)
        
        # Save to file
        with open(self.db_file, "w") as f:
            json.dump(self.commands, f, indent=2)
    
    async def get_history(self, limit=10):
        if not self.enabled:
            return []
        
        return self.commands[-limit:] if self.commands else []
    
    async def get_stats(self):
        if not self.enabled:
            return {}
        
        total = len(self.commands)
        avg_duration = sum(c.get("duration_ms", 0) for c in self.commands) / total if total > 0 else 0
        
        return {
            "total_commands": total,
            "avg_duration_ms": avg_duration,
            "last_command": self.commands[-1] if self.commands else None
        }
