#!/usr/bin/env bash
set -e
streamlit run apps/jarvis_ui/app.py --server.port 8501 --server.headless true &
uvicorn api.server:app --host 0.0.0.0 --port 8000
