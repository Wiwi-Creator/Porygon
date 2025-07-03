#!/usr/bin/env bash

set -e -x

make docker-auth
make build-m1 && make tag && make push

### -------- CONFIGURATION --------
PROJECT_ID=$PROJECT_NAME
REGION="asia-east1"
SERVICE_NAME="porygon-api"
MODEL_URI=$MODEL_URI_ON_GCS
MLFLOW_TRACKING_URI="https://mlflow-931091704211.asia-east1.run.app"
MLFLOW_REGISTRY_URI="https://mlflow-931091704211.asia-east1.run.app"
IMAGE=$IMAGE_NAME
PORT=8000
MEMORY="16Gi"
CPU=8
SERVICE_ACCOUNT=$SERVICE_ACCOUNT
CLOUD_SQL=$CLOUD_SQL
### -------- DEPLOY TO CLOUD RUN --------
echo "Deploying Porygon API to Cloud Run..."

# 在 deploy.sh 中添加環境變數
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
  --set-env-vars="GCP_PROJECT=$PROJECT_ID,PYTHONPATH=/app,MODEL_URI=$MODEL_URI,MLFLOW_TRACKING_URI=$MLFLOW_TRACKING_URI,MLFLOW_REGISTRY_URI=$MLFLOW_REGISTRY_URI,MLFLOW_TRACKING_INSECURE_TLS=true,PYTHONHTTPSVERIFY=0,MLFLOW_TRACKING_USERNAME=mlflow-admin,MLFLOW_TRACKING_PASSWORD=mlflow" \
  --service-account=$SERVICE_ACCOUNT \
  --add-cloudsql-instances=$CLOUD_SQL
