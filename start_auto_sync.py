#!/usr/bin/env python3
"""Auto-Sync Service Starter"""

import sys
import time
import signal
from pathlib import Path

# Path setup
sys.path.append(str(Path.cwd()))
sys.path.append(str(Path.cwd() / 'enhanced_integration'))

from enhanced_integration.sync.github_auto_sync import github_auto_sync

def signal_handler(signum, frame):
    """Signal handler for graceful shutdown"""
    print(f"\n🔔 Signal {signum} received, shutting down...")
    github_auto_sync.stop_daemon()
    sys.exit(0)

def main():
    """Main auto-sync service"""
    print("🚀 GitHub Auto-Sync Service Starting...")
    
    # Register signal handlers
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    try:
        # Start daemon
        sync_thread = github_auto_sync.start_daemon()
        
        # Keep main thread alive
        while github_auto_sync.running:
            time.sleep(5)
            
            # Show status every 60 seconds
            if int(time.time()) % 60 == 0:
                status = github_auto_sync.get_status()
                last_sync = status['last_sync'] or 'Never'
                print(f"📊 Status: Running | Last Sync: {last_sync}")
    
    except Exception as e:
        print(f"❌ Auto-sync service error: {e}")
        github_auto_sync.stop_daemon()

if __name__ == "__main__":
    main()
