#!/usr/bin/env python3
"""Unified Dashboard Starter"""

import sys
import subprocess
from pathlib import Path

# Path setup
sys.path.append(str(Path.cwd()))
sys.path.append(str(Path.cwd() / 'enhanced_integration'))

def start_dashboard():
    """Start unified dashboard on port 8508"""
    print("🚀 Starting Unified Dashboard on port 8508...")
    try:
        subprocess.run([
            'streamlit', 'run', 
            'enhanced_integration/apps/unified_dashboard.py',
            '--server.port', '8508',
            '--server.address', '0.0.0.0'
        ])
    except Exception as e:
        print(f"❌ Dashboard start failed: {e}")

if __name__ == "__main__":
    start_dashboard()
