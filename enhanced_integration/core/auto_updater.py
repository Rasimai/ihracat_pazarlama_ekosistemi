# enhanced_integration/core/auto_updater.py - GitHub otomatik güncelleme
import subprocess
import sys
import os
from pathlib import Path
from enhanced_integration.core.key_manager import enhanced_key_manager

class AutoUpdater:
    def __init__(self):
        self.repo_path = Path.cwd()
        self.github_token = enhanced_key_manager.get_github_token()
        
    def check_for_updates(self):
        """GitHub'da güncellemeler var mı kontrol et"""
        try:
            # Fetch latest
            result = subprocess.run(['git', 'fetch', 'origin'], 
                                  capture_output=True, text=True)
            
            # Check if current branch is behind
            result = subprocess.run(['git', 'status', '-uno'], 
                                  capture_output=True, text=True)
            
            return 'behind' in result.stdout.lower()
            
        except Exception as e:
            print(f"Update check error: {e}")
            return False
    
    def auto_update(self):
        """Otomatik güncelleme yap"""
        if not self.check_for_updates():
            print("No updates available")
            return False
            
        try:
            # Pull latest changes
            subprocess.run(['git', 'pull', 'origin', 'hybrid-enhanced-system'], check=True)
            print("System updated successfully!")
            return True
            
        except subprocess.CalledProcessError as e:
            print(f"Update failed: {e}")
            return False
    
    def restart_system(self):
        """Sistemi yeniden başlat"""
        print("Restarting system...")
        os.execv(sys.executable, ['python'] + sys.argv)

auto_updater = AutoUpdater()
