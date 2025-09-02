"""İhracat Pazarlama Ekosistemi - FastAPI Ana Uygulama"""

from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, Dict, Any
import os
import sys
from pathlib import Path

# Add parent to path
sys.path.append(str(Path(__file__).parent.parent))

from agents.jarvis_orchestrator import JarvisOrchestrator

app = FastAPI(
    title="İhracat Pazarlama Ekosistemi API",
    description="Jarvis Orchestrator ile güçlendirilmiş sistem",
    version="1.0.0"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize Jarvis
orchestrator = JarvisOrchestrator()

class CommandRequest(BaseModel):
    message: str
    context: Optional[Dict[str, Any]] = None

class CommandResponse(BaseModel):
    success: bool
    message: str
    data: Optional[Any] = None

@app.get("/")
async def root():
    return {
        "status": "active",
        "service": "İhracat Pazarlama Ekosistemi",
        "version": "1.0.0",
        "endpoints": ["/health", "/execute", "/docs"]
    }

@app.get("/health")
async def health():
    return {
        "status": "healthy",
        "jarvis": "active",
        "agents": len(orchestrator.agents),
        "tools": len(orchestrator.tools)
    }

@app.post("/execute", response_model=CommandResponse)
async def execute_command(request: CommandRequest):
    try:
        result = await orchestrator.process(request.message, request.context)
        return CommandResponse(
            success=result.success,
            message=result.message,
            data=result.data
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/history")
async def get_history():
    return {"history": orchestrator.history[-10:]}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)