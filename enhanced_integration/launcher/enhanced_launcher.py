#!/usr/bin/env python3
import subprocess
import os
from pathlib import Path

def main():
    print("🎉 JARVIS ENHANCED + GITHUB DOCKER SYNC")
    print("=" * 50)
    
    current_dir = Path.cwd()
    os.environ["PYTHONPATH"] = str(current_dir)
    
    # Check if Docker is available
    try:
        subprocess.run(["docker", "--version"], check=True, capture_output=True)
        print("🐳 Docker found - starting Docker compose system...")
        
        # Copy .env if not exists
        if not Path(".env").exists() and Path(".env.example").exists():
            subprocess.run(["cp", ".env.example", ".env"])
            print("📝 .env file created from example")
        
        # Start Docker compose
        process = subprocess.Popen(["docker", "compose", "up", "-d", "--build"], 
                                   stdout=subprocess.PIPE, 
                                   stderr=subprocess.PIPE)
        
        print("🚀 Docker containers starting...")
        print("📧 MailHog: http://localhost:8025")
        print("🔧 System API: http://localhost:8005")
        print("📊 Dashboard: http://localhost:8506")
        
        process.wait()
        
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("⚠️ Docker not available, trying Python fallback...")
        
        # Look for main Python file
        python_files = ["main.py", "app.py", "server.py", "run.py"]
        main_file = None
        
        for file in python_files:
            if Path(file).exists():
                main_file = file
                break
        
        if main_file:
            print(f"🐍 Starting Python system: {main_file}")
            process = subprocess.Popen(["python3", main_file])
            process.wait()
        else:
            print("❌ No main file found. Available Python files:")
            for py_file in Path(".").glob("*.py"):
                print(f"  - {py_file.name}")

if __name__ == "__main__":
    main()
