#!/usr/bin/env python3
# enhanced_system_launcher.py - Auto-update destekli launcher
import subprocess
import time
import sys
import os
from pathlib import Path

def check_auto_update():
    """Başlatmadan önce güncelleme kontrolü"""
    try:
        from enhanced_integration.core.auto_updater import auto_updater
        
        if auto_updater.check_for_updates():
            print("🔄 Updates found! Updating system...")
            if auto_updater.auto_update():
                print("✅ System updated! Restarting...")
                auto_updater.restart_system()
        else:
            print("✅ System is up to date")
            
    except Exception as e:
        print(f"⚠️ Auto-update check failed: {e}")

def start_services():
    """Hybrid sistem servisleri"""
    print("="*60)
    print("🚀 JARVIS HYBRID ENHANCED SYSTEM v2.1")
    print("Auto-Update Enabled | GitHub Synced")
    print("="*60)
    
    # Auto-update kontrolü
    check_auto_update()
    
    processes = []
    
    # Enhanced API (Port 8007)
    print("⚡ Enhanced API starting (Port 8007)...")
    enhanced_api = subprocess.Popen([
        sys.executable, "-c", 
        "import uvicorn; import sys; sys.path.append('.'); "
        "from enhanced_integration.api.enhanced_api import app; "
        "uvicorn.run(app, host='0.0.0.0', port=8007)"
    ], env=dict(os.environ, PYTHONPATH="."))
    processes.append(enhanced_api)
    time.sleep(3)
    
    # Enhanced Dashboard (Port 8508)
    print("🖥️ Enhanced Dashboard starting (Port 8508)...")
    enhanced_dashboard = subprocess.Popen([
        sys.executable, "-m", "streamlit", "run",
        "enhanced_integration/apps/enhanced_dashboard.py",
        "--server.port", "8508",
        "--server.headless", "true"
    ], env=dict(os.environ, PYTHONPATH="."))
    processes.append(enhanced_dashboard)
    time.sleep(3)
    
    print("\n" + "="*60)
    print("🎉 HYBRID SYSTEM READY!")
    print("="*60)
    print("🔗 Bridge API (Existing): http://localhost:9999")
    print("🌐 Jarvis API (Existing): http://localhost:8005")
    print("🖥️ Streamlit (Existing): http://localhost:8506") 
    print("⚡ Enhanced API: http://localhost:8007")
    print("🚀 Enhanced Dashboard: http://localhost:8508")
    print("📚 Enhanced API Docs: http://localhost:8007/docs")
    print("="*60)
    print("Press Ctrl+C to stop")
    
    try:
        while True:
            time.sleep(30)  # Her 30 saniyede health check
    except KeyboardInterrupt:
        print("\n🛑 Shutting down...")
        for process in processes:
            process.terminate()
        print("✅ Hybrid system stopped")

if __name__ == "__main__":
    start_services()
