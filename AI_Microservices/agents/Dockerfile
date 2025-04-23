# agents/Dockerfile
FROM rayproject/ray:2.7.0-py310

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app/

ENV MODEL_URI="models:/wikipedia-agent/production"
ENV MLFLOW_TRACKING_URI="http://mlflow-service:5000"

ENTRYPOINT ["python", "-m", "wikipedia_agent.job"]