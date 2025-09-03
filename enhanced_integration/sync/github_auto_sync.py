#!/usr/bin/env python3
"""GitHub Auto-Sync Daemon - Real-time Repository Synchronization"""

import os
import time
import subprocess
import json
import requests
from datetime import datetime
from pathlib import Path
import threading

class GitHubAutoSync:
    """GitHub otomatik senkronizasyon sistemi"""
    
    def __init__(self):
        self.repo_path = Path.cwd()
        self.branch = "hybrid-unified-system"
        self.remote = "origin"
        self.sync_interval = 300  # 5 dakika
        self.running = False
        self.last_sync = None
        
    def start_daemon(self):
        """Auto-sync daemon'ı başlat"""
        self.running = True
        print(f"🚀 GitHub Auto-Sync Daemon başlatıldı")
        print(f"📋 Branch: {self.branch}")
        print(f"⏱️ Sync Interval: {self.sync_interval} saniye")
        
        # Daemon thread'i başlat
        sync_thread = threading.Thread(target=self._sync_loop, daemon=True)
        sync_thread.start()
        
        return sync_thread
    
    def stop_daemon(self):
        """Daemon'ı durdur"""
        self.running = False
        print("🛑 GitHub Auto-Sync Daemon durduruldu")
    
    def _sync_loop(self):
        """Ana senkronizasyon döngüsü"""
        while self.running:
            try:
                self.perform_sync()
                time.sleep(self.sync_interval)
            except Exception as e:
                print(f"❌ Sync error: {e}")
                time.sleep(60)  # Hata durumunda 1 dakika bekle
    
    def perform_sync(self):
        """Senkronizasyon işlemini gerçekleştir"""
        try:
            os.chdir(self.repo_path)
            
            # Git durumunu kontrol et
            result = subprocess.run(['git', 'status', '--porcelain'], 
                                  capture_output=True, text=True)
            
            has_changes = len(result.stdout.strip()) > 0
            
            # Uzak repository'den değişiklikleri çek
            print("🔄 GitHub'dan değişiklikler kontrol ediliyor...")
            fetch_result = subprocess.run(['git', 'fetch', self.remote], 
                                        capture_output=True, text=True)
            
            if fetch_result.returncode == 0:
                # Uzaktan değişiklik var mı kontrol et
                behind_result = subprocess.run([
                    'git', 'rev-list', '--count', f'HEAD..{self.remote}/{self.branch}'
                ], capture_output=True, text=True)
                
                commits_behind = int(behind_result.stdout.strip() or "0")
                
                if commits_behind > 0:
                    print(f"📥 {commits_behind} yeni commit bulundu, pull yapılıyor...")
                    self.pull_changes()
                
                # Lokal değişiklikler varsa push et
                if has_changes:
                    print("📤 Lokal değişiklikler push ediliyor...")
                    self.push_changes()
                
                self.last_sync = datetime.now()
                print(f"✅ Sync tamamlandı: {self.last_sync.strftime('%H:%M:%S')}")
                
            else:
                print("⚠️ GitHub fetch başarısız")
                
        except Exception as e:
            print(f"❌ Sync işlemi başarısız: {e}")
    
    def pull_changes(self):
        """GitHub'dan değişiklikleri çek"""
        try:
            result = subprocess.run(['git', 'pull', self.remote, self.branch], 
                                  capture_output=True, text=True)
            
            if result.returncode == 0:
                print("✅ GitHub'dan değişiklikler başarıyla çekildi")
                
                # Pull sonrası sistem restart gerekebilir
                if self.requires_restart(result.stdout):
                    print("🔄 Sistem restart gerekiyor...")
                    self.restart_services()
                
            else:
                print(f"❌ Pull başarısız: {result.stderr}")
                
        except Exception as e:
            print(f"❌ Pull error: {e}")
    
    def push_changes(self):
        """Lokal değişiklikleri GitHub'a gönder"""
        try:
            # Add all changes
            subprocess.run(['git', 'add', '.'])
            
            # Commit with timestamp
            commit_msg = f"auto-sync: System update {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
            commit_result = subprocess.run(['git', 'commit', '-m', commit_msg], 
                                         capture_output=True, text=True)
            
            if commit_result.returncode == 0:
                # Push to remote
                push_result = subprocess.run(['git', 'push', self.remote, self.branch], 
                                           capture_output=True, text=True)
                
                if push_result.returncode == 0:
                    print("✅ Değişiklikler GitHub'a başarıyla gönderildi")
                else:
                    print(f"❌ Push başarısız: {push_result.stderr}")
            
        except Exception as e:
            print(f"❌ Push error: {e}")
    
    def requires_restart(self, pull_output):
        """Pull sonrası restart gerekip gerekmediğini kontrol et"""
        restart_keywords = [
            'requirements.txt',
            'docker-compose.yml',
            'enhanced_orchestrator.py',
            '.env'
        ]
        
        return any(keyword in pull_output for keyword in restart_keywords)
    
    def restart_services(self):
        """Servisleri yeniden başlat"""
        try:
            print("🔄 Container'lar yeniden başlatılıyor...")
            subprocess.run(['docker', 'compose', 'restart'])
            
            # Kısa bir bekleme
            time.sleep(10)
            
            print("✅ Servisler yeniden başlatıldı")
            
        except Exception as e:
            print(f"❌ Restart error: {e}")
    
    def get_status(self):
        """Daemon durumunu getir"""
        return {
            'running': self.running,
            'last_sync': self.last_sync.isoformat() if self.last_sync else None,
            'repo_path': str(self.repo_path),
            'branch': self.branch,
            'sync_interval': self.sync_interval
        }

# Global auto-sync instance
github_auto_sync = GitHubAutoSync()

if __name__ == "__main__":
    print("🎯 GitHub Auto-Sync Daemon")
    print("=" * 40)
    
    try:
        # Daemon'ı başlat
        sync_thread = github_auto_sync.start_daemon()
        
        print("🔄 Daemon çalışıyor... Durdurmak için Ctrl+C basın")
        
        # Ana thread'i alive tut
        while github_auto_sync.running:
            time.sleep(1)
            
    except KeyboardInterrupt:
        print("\n🛑 Daemon durduruluyor...")
        github_auto_sync.stop_daemon()
        print("✅ Daemon durduruldu")
