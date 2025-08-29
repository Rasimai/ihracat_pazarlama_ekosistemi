import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .terminal.routes import router as term_router

app = FastAPI(title="Artis Terminal Bridge", version="0.1.0")

# Simple CORS for local dev
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(term_router, prefix="/terminal")

@app.get("/")
def root():
    return {"status": "ok", "terminal": "/terminal"}

# For uvicorn: uvicorn app.main:app --reload
