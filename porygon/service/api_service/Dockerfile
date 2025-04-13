FROM python:3.9-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . ./

ENV PYTHONPATH="${PYTHONPATH}:/app" \
    MLFLOW_TRACKING_URI="" \
    MLFLOW_REGISTRY_URI="" \
    MLFLOW_ARTIFACT_URI="" \
    MODEL_URI=""

HEALTHCHECK --interval=30s --timeout=5s --start-period=30s --retries=3 \
    CMD curl -f http://localhost:8080/health || exit 1

CMD ["gunicorn", "api.main:app", "-k", "uvicorn.workers.UvicornWorker", "--preload", "--workers", "4", "--bind", "0.0.0.0:8080"]