#!/usr/bin/env python3
"""Jarvis Sistem Kurulum Script"""

import os
import sys
from pathlib import Path

def setup_jarvis():
    print("🚀 Jarvis Sistemi Kuruluyor...")
    
    # Dizinleri oluştur
    dirs = [
        "agents/jarvis",
        "agents/pmba",
        "agents/ikba",
        "agents/cikta",
        "core/tools",
        "core/router",
        "core/policy",
        "apps/jarvis_ui",
        "tests"
    ]
    
    for dir_path in dirs:
        Path(dir_path).mkdir(parents=True, exist_ok=True)
        print(f"✅ {dir_path} oluşturuldu")
    
    print("\n✅ Jarvis kurulumu tamamlandı!")
    print("🎯 Şimdi: python jarvis_setup.py çalıştırın")

if __name__ == "__main__":
    setup_jarvis()