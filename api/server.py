from fastapi import FastAPI
from pydantic import BaseModel
import os
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

app = FastAPI(title="ipe API", version="0.1.0")

DB_URL = os.getenv("DATABASE_URL") or "sqlite:///state/db.sqlite"
IS_SQLITE = DB_URL.startswith("sqlite")
connect_args = {"check_same_thread": False} if IS_SQLITE else {}
engine = create_engine(DB_URL, echo=False, future=True, connect_args=connect_args)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, future=True)

with engine.begin() as conn:
    ddl_sqlite = """
    CREATE TABLE IF NOT EXISTS companies(
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      name TEXT NOT NULL,
      website TEXT,
      country TEXT,
      city TEXT,
      source TEXT,
      created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """
    ddl_pg = """
    CREATE TABLE IF NOT EXISTS companies(
      id SERIAL PRIMARY KEY,
      name TEXT NOT NULL,
      website TEXT,
      country TEXT,
      city TEXT,
      source TEXT,
      created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """
    conn.execute(text(ddl_sqlite if IS_SQLITE else ddl_pg))

class Directive(BaseModel):
    text: str

@app.post("/api/directive")
def submit_directive(d: Directive):
    return {"message": f"Alındı: {d.text}", "intent_guess": "maps.search.radius"}

@app.get("/api/companies")
def list_companies():
    with engine.begin() as conn:
        rows = conn.execute(text("SELECT id,name,website,country,city FROM companies ORDER BY id DESC")).mappings().all()
        return [dict(r) for r in rows]

class CompanyIn(BaseModel):
    name: str
    website: str | None = None
    country: str | None = None
    city: str | None = None
    source: str | None = "manual"

@app.post("/api/companies")
def add_company(c: CompanyIn):
    with engine.begin() as conn:
        conn.execute(text("""
            INSERT INTO companies(name,website,country,city,source)
            VALUES(:name,:website,:country,:city,:source)
        """), c.model_dump())
    return {"ok": True}

@app.get("/api/reports/daily")
def daily_report():
    with engine.begin() as conn:
        if IS_SQLITE:
            q = "SELECT COUNT(*) FROM companies WHERE created_at > datetime('now','-1 day')"
        else:
            q = "SELECT COUNT(*) FROM companies WHERE created_at > now() - INTERVAL '1 day'"
        count = conn.execute(text(q)).scalar_one_or_none()
    return {"companies_last_24h": int(count or 0)}

@app.get("/manifest.json")
def manifest():
    return {"name": "ipe","version": "0.1.0","assets": []}
