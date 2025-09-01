#!/bin/bash

echo Starting Jarvis System...

# API başlat
uvicorn app.main:app --reload --port 8000 &

# UI başlat
streamlit run apps/jarvis_ui.py &

echo Jarvis System Started!
echo API: http://localhost:8000
echo UI: http://localhost:8501