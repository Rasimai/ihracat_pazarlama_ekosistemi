# İhracat Pazarlama Ekosistemi

## Jarvis Orchestrator Sistemi

### Kurulum

1. Gereksinimleri yükle:
```bash
pip install -r requirements.txt
```

2. FastAPI başlat:
```bash
uvicorn app.main:app --reload
```

3. Streamlit UI başlat:
```bash
streamlit run apps/jarvis_ui.py
```

### Docker ile Çalıştırma

```bash
docker-compose up -d
```

### Özellikler

- Jarvis Orchestrator
- Alt Asistanlar (PMBA, IKBA, CIKTA)
- FastAPI Backend
- Streamlit Frontend
- Docker Support