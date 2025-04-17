#!/usr/bin/env bash

set -e

make docker-auth
make build-m1 && make tag && make push

### -------- CONFIGURATION --------
PROJECT_ID="genibuilder"
REGION="asia-east1"
SERVICE_NAME="mlflow"
IMAGE="asia-east1-docker.pkg.dev/genibuilder/mlflow-gcp/mlflow-gcp:latest"
PORT=8080
MEMORY="2Gi"
CPU=2
SERVICE_ACCOUNT="931091704211-compute@developer.gserviceaccount.com"
CLOUD_SQL="genibuilder:asia-east1:mlflow"

### -------- DEPLOY TO CLOUD RUN --------
echo "Deploying MLflow to Cloud Run..."

gcloud run deploy "$SERVICE_NAME" \
  --project="$PROJECT_ID" \
  --image="$IMAGE" \
  --platform=managed \
  --region="$REGION" \
  --allow-unauthenticated \
  --port=$PORT \
  --memory="$MEMORY" \
  --cpu="$CPU" \
  --set-env-vars=GCP_PROJECT=$PROJECT_ID \
  --add-cloudsql-instances=$CLOUD_SQL \
  --service-account=$SERVICE_ACCOUNT
