#!/usr/bin/env python3
# enhanced_system_launcher.py - Hybrid sistem başlatıcısı
import subprocess
import time
import sys
import os
from pathlib import Path

def print_banner():
    print("="*60)
    print("🚀 JARVIS HYBRID ENHANCED SYSTEM")
    print("Mevcut Sistem + Enhanced Features")
    print("="*60)

def start_services():
    """Tüm servisleri başlat"""
    print_banner()
    
    processes = []
    
    # 1. Bridge API (Port 9999) - Mevcut sistem
    print("🔗 Bridge API başlatılıyor (Port 9999)...")
    
    # 2. Enhanced API (Port 8007) - Yeni
    print("⚡ Enhanced API başlatılıyor (Port 8007)...")
    enhanced_api = subprocess.Popen([
        sys.executable, "-c", 
        "import uvicorn; import sys; sys.path.append('.'); "
        "from enhanced_integration.api.enhanced_api import app; "
        "uvicorn.run(app, host='0.0.0.0', port=8007)"
    ], env=dict(os.environ, PYTHONPATH="."))
    processes.append(enhanced_api)
    time.sleep(3)
    
    # 3. Enhanced Dashboard (Port 8508) - Yeni
    print("🖥️ Enhanced Dashboard başlatılıyor (Port 8508)...")
    enhanced_dashboard = subprocess.Popen([
        sys.executable, "-m", "streamlit", "run",
        "enhanced_integration/apps/enhanced_dashboard.py",
        "--server.port", "8508",
        "--server.headless", "true"
    ], env=dict(os.environ, PYTHONPATH="."))
    processes.append(enhanced_dashboard)
    time.sleep(3)
    
    print("\n" + "="*60)
    print("🎉 HYBRID SYSTEM BAŞLATILDI!")
    print("="*60)
    print("🔗 Bridge API (Mevcut): http://localhost:9999")
    print("🌐 Jarvis API (Mevcut): http://localhost:8005")  
    print("🖥️ Streamlit (Mevcut): http://localhost:8506")
    print("⚡ Enhanced API: http://localhost:8007")
    print("🚀 Enhanced Dashboard: http://localhost:8508")
    print("="*60)
    print("Durdurmak için Ctrl+C basın")
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n🛑 Sistem kapatılıyor...")
        for process in processes:
            process.terminate()
        print("✅ Hybrid sistem kapatıldı")

if __name__ == "__main__":
    start_services()
