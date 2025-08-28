#!/usr/bin/env bash
set -euo pipefail

python - <<'PY'
import os, time, sys
import psycopg
url = os.getenv("DATABASE_URL", "sqlite:///state/db.sqlite")
if url.startswith("postgres"):
    for i in range(60):
        try:
            with psycopg.connect(os.getenv("DATABASE_URL").replace("+psycopg",""), connect_timeout=3) as _:
                break
        except Exception:
            time.sleep(1)
    else:
        sys.exit("DB not ready")
PY

alembic -c alembic.ini upgrade head

uvicorn api.server:app --host 0.0.0.0 --port 8000 &
exec streamlit run apps/jarvis_ui/app.py --server.port 8501 --server.address 0.0.0.0
