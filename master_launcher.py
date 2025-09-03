#!/usr/bin/env python3
"""Master Launcher - All Services in One Command"""

import subprocess
import time
import signal
import sys
from pathlib import Path
import threading

class MasterLauncher:
    """Tüm servisleri tek komutla başlatan ana launcher"""
    
    def __init__(self):
        self.processes = {}
        self.running = True
    
    def start_all_services(self):
        """Tüm servisleri başlat"""
        print("🚀 JARVIS UNIFIED SYSTEM v3.0 - MASTER LAUNCHER")
        print("=" * 60)
        
        # 1. Docker containers
        self.start_docker_services()
        
        # 2. Enhanced API (port 8007)
        self.start_enhanced_api()
        
        # 3. Unified Dashboard (port 8508)  
        self.start_unified_dashboard()
        
        # 4. Auto-sync daemon
        self.start_auto_sync()
        
        print("\n" + "=" * 60)
        print("🎉 ALL SERVICES STARTED!")
        print("🔗 Enhanced API: http://localhost:8007/docs")
        print("📊 Unified Dashboard: http://localhost:8508")
        print("📧 MailHog: http://localhost:8025")
        print("🐳 App Container: http://localhost:8000")
        print("🔄 Auto-Sync: Background daemon running")
        print("=" * 60)
        print("🛑 Press Ctrl+C to stop all services")
    
    def start_docker_services(self):
        """Docker container'larını başlat"""
        print("🐳 Starting Docker services...")
        try:
            process = subprocess.Popen(['docker', 'compose', 'up', '-d'])
            process.wait()
            print("✅ Docker services started")
            time.sleep(5)  # Container'ların başlaması için bekle
        except Exception as e:
            print(f"⚠️ Docker start warning: {e}")
    
    def start_enhanced_api(self):
        """Enhanced API'yi başlat"""
        print("⚡ Starting Enhanced API (port 8007)...")
        try:
            process = subprocess.Popen([
                'python', 'enhanced_integration/api/enhanced_api.py'
            ])
            self.processes['enhanced_api'] = process
            print("✅ Enhanced API started")
        except Exception as e:
            print(f"⚠️ Enhanced API warning: {e}")
    
    def start_unified_dashboard(self):
        """Unified Dashboard'ı başlat"""
        print("📊 Starting Unified Dashboard (port 8508)...")
        try:
            process = subprocess.Popen([
                'python', 'start_unified_dashboard.py'
            ])
            self.processes['unified_dashboard'] = process
            print("✅ Unified Dashboard started")
        except Exception as e:
            print(f"⚠️ Dashboard warning: {e}")
    
    def start_auto_sync(self):
        """Auto-sync daemon'ı başlat"""
        print("🔄 Starting Auto-Sync Daemon...")
        try:
            process = subprocess.Popen([
                'python', 'start_auto_sync.py'
            ])
            self.processes['auto_sync'] = process
            print("✅ Auto-Sync Daemon started")
        except Exception as e:
            print(f"⚠️ Auto-sync warning: {e}")
    
    def stop_all_services(self):
        """Tüm servisleri durdur"""
        print("\n🛑 Stopping all services...")
        self.running = False
        
        # Python process'lerini durdur
        for service_name, process in self.processes.items():
            try:
                print(f"🔄 Stopping {service_name}...")
                process.terminate()
                process.wait(timeout=10)
                print(f"✅ {service_name} stopped")
            except Exception as e:
                print(f"⚠️ {service_name} stop warning: {e}")
                try:
                    process.kill()
                except:
                    pass
        
        # Docker container'ları durdur (opsiyonel)
        try:
            print("🐳 Stopping Docker containers...")
            subprocess.run(['docker', 'compose', 'down'], timeout=30)
            print("✅ Docker containers stopped")
        except Exception as e:
            print(f"⚠️ Docker stop warning: {e}")
        
        print("✅ All services stopped")

def signal_handler(signum, frame, launcher):
    """Signal handler"""
    launcher.stop_all_services()
    sys.exit(0)

def main():
    launcher = MasterLauncher()
    
    # Signal handler setup
    signal.signal(signal.SIGINT, lambda s, f: signal_handler(s, f, launcher))
    signal.signal(signal.SIGTERM, lambda s, f: signal_handler(s, f, launcher))
    
    try:
        launcher.start_all_services()
        
        # Keep main thread alive
        while launcher.running:
            time.sleep(5)
            
    except KeyboardInterrupt:
        launcher.stop_all_services()

if __name__ == "__main__":
    main()
