#!/usr/bin/env python3
"""System Verification Script"""

import requests
import subprocess
import json
from pathlib import Path

def verify_system():
    """Complete system verification"""
    print("🔍 SYSTEM VERIFICATION STARTED")
    print("=" * 50)
    
    results = {
        'docker': False,
        'git': False, 
        'ports': {},
        'files': {},
        'services': {}
    }
    
    # Docker verification
    try:
        result = subprocess.run(['docker', 'compose', 'ps'], 
                              capture_output=True, text=True)
        results['docker'] = result.returncode == 0
        print(f"🐳 Docker: {'✅ OK' if results['docker'] else '❌ FAIL'}")
    except:
        print("🐳 Docker: ❌ NOT AVAILABLE")
    
    # Git verification
    try:
        result = subprocess.run(['git', 'status'], 
                              capture_output=True, text=True)
        results['git'] = result.returncode == 0
        print(f"📦 Git: {'✅ OK' if results['git'] else '❌ FAIL'}")
        
        # Current branch
        branch_result = subprocess.run(['git', 'branch', '--show-current'], 
                                     capture_output=True, text=True)
        current_branch = branch_result.stdout.strip()
        print(f"🌿 Current Branch: {current_branch}")
        
    except:
        print("📦 Git: ❌ NOT AVAILABLE")
    
    # Port verification
    ports_to_check = [8000, 8007, 8025, 8501, 8508]
    
    for port in ports_to_check:
        try:
            response = requests.get(f"http://localhost:{port}", timeout=2)
            results['ports'][port] = response.status_code < 400
            status = "✅ OK" if results['ports'][port] else "⚠️ ISSUES"
        except:
            results['ports'][port] = False
            status = "❌ OFFLINE"
        
        print(f"🌐 Port {port}: {status}")
    
    # File verification
    critical_files = [
        'docker-compose.yml',
        'master_launcher.py',
        'start_auto_sync.py',
        'enhanced_integration/sync/github_auto_sync.py',
        'core/enhanced_orchestrator.py',
        'core/enhanced_skill_registry.py'
    ]
    
    for file_path in critical_files:
        exists = Path(file_path).exists()
        results['files'][file_path] = exists
        status = "✅ EXISTS" if exists else "❌ MISSING"
        print(f"📄 {file_path}: {status}")
    
    # Overall system health
    docker_ok = results['docker']
    git_ok = results['git']
    files_ok = all(results['files'].values())
    ports_partial = sum(results['ports'].values()) >= 2
    
    overall_health = docker_ok and git_ok and files_ok and ports_partial
    
    print("\n" + "=" * 50)
    print(f"🎯 OVERALL SYSTEM HEALTH: {'✅ READY' if overall_health else '⚠️ PARTIAL'}")
    print("=" * 50)
    
    return results

if __name__ == "__main__":
    verify_system()
