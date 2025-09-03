#!/usr/bin/env python3
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import sys
from pathlib import Path

# Path setup
sys.path.append(str(Path.cwd()))

app = FastAPI(title="JARVIS Enhanced API v2.5", version="2.5.0")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"])

@app.get("/enhanced/health")
async def health():
    return {
        "status": "healthy",
        "version": "2.5.0",
        "system": "enhanced",
        "message": "Enhanced API is running!"
    }

@app.get("/enhanced/system/info")
async def system_info():
    return {
        "system_name": "JARVIS Enhanced System",
        "version": "2.5.0",
        "phase": "5 - Production Ready",
        "features": ["Vision", "Web Scraping", "Auto-Sync", "21 Skills"]
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8007)
