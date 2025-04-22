#!/usr/bin/env bash

set -e

### -------- CONFIGURATION --------
PROJECT_ID="genibuilder"
REGION="asia-east1"
SERVICE_NAME="mlflow"
IMAGE="asia-east1-docker.pkg.dev/genibuilder/mlflow-gcp/mlflow-gcp@sha256:440721510c8541052a4d834490463801db1a00439a92cba7066ec0216fcb68dd"
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
  --timeout=300 \
  --set-env-vars=GCP_PROJECT=$PROJECT_ID \
  --add-cloudsql-instances=$CLOUD_SQL \
  --service-account=$SERVICE_ACCOUNT
