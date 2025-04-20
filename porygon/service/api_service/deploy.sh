#!/usr/bin/env bash

set -e

make docker-auth
make build-m1 && make tag && make push

### -------- CONFIGURATION --------
PROJECT_ID="genibuilder"
REGION="asia-east1"
SERVICE_NAME="porygon-api"
MODEL_URI="gs://wiwi-bucket/1/15a6b7e29ad34d3fa1484ee9e0621774/artifacts/porygon_chain"
MLFLOW_TRACKING_URI="https://mlflow-931091704211.asia-east1.run.app"
MLFLOW_REGISTRY_URI="https://mlflow-931091704211.asia-east1.run.app"
IMAGE="asia-east1-docker.pkg.dev/genibuilder/api/porygon-api:latest"
PORT=8000
MEMORY="4Gi"
CPU=4
SERVICE_ACCOUNT="931091704211-compute@developer.gserviceaccount.com"
CLOUD_SQL="genibuilder:asia-east1:mlflow"

### -------- DEPLOY TO CLOUD RUN --------
echo "Deploying Porygon API to Cloud Run..."

gcloud run deploy "$SERVICE_NAME" \
  --project="$PROJECT_ID" \
  --image="$IMAGE" \
  --platform=managed \
  --region="$REGION" \
  --allow-unauthenticated \
  --port=$PORT \
  --memory="$MEMORY" \
  --cpu="$CPU" \
  --set-env-vars="GCP_PROJECT=$PROJECT_ID,PYTHONPATH=/app, MODEL_URI=$MODEL_URI, MLFLOW_TRACKING_URI=$MLFLOW_TRACKING_URI, MLFLOW_REGISTRY_URI=$MLFLOW_REGISTRY_URI" \
  --add-cloudsql-instances=$CLOUD_SQL \
  --service-account=$SERVICE_ACCOUNT
