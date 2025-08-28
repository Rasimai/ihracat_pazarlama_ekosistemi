#!/usr/bin/env bash
set -euo pipefail

# DB migrate
alembic upgrade head

# API
uvicorn api.server:app --host 0.0.0.0 --port 8000 &

# UI (Streamlit)
exec streamlit run apps/jarvis_ui/app.py --server.port 8501 --server.address 0.0.0.0
