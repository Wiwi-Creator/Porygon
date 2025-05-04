FROM rayproject/ray-ml:2.3.0

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

RUN mkdir -p /app/models

ENV PYTHONPATH="/app:${PYTHONPATH}"
ENV MLFLOW_TRACKING_INSECURE_TLS=true
ENV PYTHONHTTPSVERIFY=0