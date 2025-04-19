#!/usr/bin/env bash

set -e

# 驗證必要的環境變數
if [[ -z "${GCP_PROJECT}" ]]; then
    echo "Error: GCP_PROJECT not set"
    exit 1
fi

# 從 Secret Manager 獲取機密
export XAI_API_KEY="$(python3 /app/get_secret.py --project="${GCP_PROJECT}" --secret=xai_api_key)"
export XAI_DEPLOYMENT_NAME="$(python3 /app/get_secret.py --project="${GCP_PROJECT}" --secret=xai_deployment_name)"
export XAI_ENDPOINT="$(python3 /app/get_secret.py --project="${GCP_PROJECT}" --secret=xai_endpoint)"
export AZURE_OPENAI_API_KEY="$(python3 /app/get_secret.py --project="${GCP_PROJECT}" --secret=azure_openai_api_key)"
export AZURE_OPENAI_ENDPOINT="$(python3 /app/get_secret.py --project="${GCP_PROJECT}" --secret=azure_openai_endpoint)"
export AZURE_OPENAI_DEPLOYMENT_NAME="$(python3 /app/get_secret.py --project="${GCP_PROJECT}" --secret=azure_openai_deployment_name)"
export AZURE_OPENAI_API_VERSION="$(python3 /app/get_secret.py --project="${GCP_PROJECT}" --secret=azure_openai_api_version)"
export SERPAPI_API_KEY="$(python3 /app/get_secret.py --project="${GCP_PROJECT}" --secret=serpapi_api_key)"

# 獲取 MLflow 相關設定
if [[ -z "${MLFLOW_TRACKING_URI}" ]]; then
    export MLFLOW_TRACKING_URI="$(python3 /app/get_secret.py --project="${GCP_PROJECT}" --secret=mlflow_tracking_uri)"
fi

if [[ -z "${MLFLOW_REGISTRY_URI}" ]]; then
    export MLFLOW_REGISTRY_URI="${MLFLOW_TRACKING_URI}"
fi

if [[ -z "${MODEL_URI}" ]]; then
    export MODEL_URI="$(python3 /app/get_secret.py --project="${GCP_PROJECT}" --secret=model_uri)"
fi

# 檢查必要的環境變數
if [[ -z "${MLFLOW_TRACKING_URI}" ]]; then
    echo "Error: MLFLOW_TRACKING_URI not set"
    exit 1
fi

if [[ -z "${MODEL_URI}" ]]; then
    echo "Error: MODEL_URI not set"
    exit 1
fi

if [[ -z "${PORT}" ]]; then
    export PORT=8080
fi

if [[ -z "${HOST}" ]]; then
    export HOST=0.0.0.0
fi

# 顯示服務啟動信息
echo "Starting Porygon API Service..."
echo "MLflow Tracking URI: ${MLFLOW_TRACKING_URI}"
echo "Model URI: ${MODEL_URI}"

# 啟動 Gunicorn 服務器
exec gunicorn -b "${HOST}:${PORT}" -w 4 --timeout 300 --preload \
  --access-logfile=- --error-logfile=- --log-level=info \
  porygon_api.main:app -k uvicorn.workers.UvicornWorker
