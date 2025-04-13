FROM python:3.9-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

COPY . ./

RUN pip install --no-cache-dir -r requirements.txt

ENV PYTHONPATH="${PYTHONPATH}:/app" \
    GOOGLE_APPLICATION_CREDENTIALS="/app/configs/credentials.json" \
    MLFLOW_TRACKING_URI="http://localhost:5000" \
    MLFLOW_REGISTRY_URI="http://localhost:5000"

CMD ["gunicorn", "app.main:app", "-k", "uvicorn.workers.UvicornWorker", "--preload", "--workers", "4", "--bind", "0.0.0.0:8080"]