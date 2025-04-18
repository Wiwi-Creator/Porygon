FROM python:3.9-slim

WORKDIR /app

COPY . ./

RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

RUN pip install poetry==1.8.3
RUN poetry install

ENV PYTHONPATH="${PYTHONPATH}:/app" \
    MLFLOW_TRACKING_URI="" \
    MLFLOW_REGISTRY_URI="" \
    MLFLOW_ARTIFACT_URI="" \
    MODEL_URI=""

CMD ["poetry", "run", "gunicorn", "api.main:app", "-k", "uvicorn.workers.UvicornWorker", "--preload", "--workers", "4", "--bind", "0.0.0.0:8080"]