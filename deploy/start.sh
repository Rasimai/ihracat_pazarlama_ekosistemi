#!/usr/bin/env bash
set -e
APP=""
if [ -f "app/main.py" ]; then APP="app.main:app"; fi
if [ -z "$APP" ] && [ -f "main.py" ]; then APP="main:app"; fi
if [ -z "$APP" ]; then
python - <<'PY'
from fastapi import FastAPI
app = FastAPI()
@app.get("/")
def root():
    return {"status":"ok"}
import uvicorn
uvicorn.run(app, host="0.0.0.0", port=8000)
PY
else
  exec uvicorn "$APP" --host 0.0.0.0 --port 8000
fi
