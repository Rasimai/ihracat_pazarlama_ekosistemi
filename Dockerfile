FROM python:3.11-slim
WORKDIR /app
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1 PIP_DISABLE_PIP_VERSION_CHECK=1
RUN apt-get update && apt-get install -y build-essential curl && rm -rf /var/lib/apt/lists/*
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["bash","-lc","uvicorn api.server:app --host 0.0.0.0 --port 8000 & streamlit run apps/jarvis_ui/app.py --server.port=8501 --server.address=0.0.0.0"]
