# enhanced_integration/api/enhanced_api.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import sys
from pathlib import Path

# Path'i düzelt
current_dir = Path(__file__).parent.parent.parent
sys.path.append(str(current_dir))
sys.path.append(str(current_dir / 'enhanced_integration'))

from enhanced_integration.core.key_manager import enhanced_key_manager
from enhanced_integration.core.database_service import enhanced_db_service

app = FastAPI(title="JARVIS Enhanced API", version="2.0.0")

app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"])

@app.on_event("startup")
async def startup():
    enhanced_db_service.initialize()

@app.get("/enhanced/health")
async def health():
    return {
        "status": "healthy",
        "keys_loaded": len(enhanced_key_manager.keys),
        "missing_keys": enhanced_key_manager.get_missing_keys()
    }

@app.get("/enhanced/dashboard")  
async def dashboard():
    return {
        "metrics": enhanced_db_service.get_dashboard_data(),
        "key_status": enhanced_key_manager.validate_keys()
    }
