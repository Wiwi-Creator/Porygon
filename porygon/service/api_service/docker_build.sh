#!/bin/bash
docker build -t porygon-fastapi .

docker rm -f porygon-api 2>/dev/null || true


docker run --rm -d\
  --name porygon-fastapi \
  --network mlflow-tracking_mlflow-network \
  -p 8080:8080 \
  -e PYTHONPATH=/app \
  -e MLFLOW_TRACKING_URI=http://mlflow:5000 \
  -e MLFLOW_REGISTRY_URI=http://mlflow:5000 \
  -e MODEL_URI=runs:/fb67e9e648914f4a88afb205e80126f8/porygon_chain \
  -e XAI_API_KEY=${XAI_API_KEY} \
  -e XAI_DEPLOYMENT_NAME=${XAI_DEPLOYMENT_NAME} \
  -e XAI_ENDPOINT=${XAI_ENDPOINT} \
  -e AZURE_OPENAI_API_KEY=${AZURE_OPENAI_API_KEY} \
  -e AZURE_OPENAI_ENDPOINT=${AZURE_OPENAI_ENDPOINT} \
  -e AZURE_OPENAI_DEPLOYMENT_NAME=${AZURE_OPENAI_DEPLOYMENT_NAME} \
  -e AZURE_OPENAI_API_VERSION=${AZURE_OPENAI_API_VERSION} \
  -e SERPAPI_API_KEY=${SERPAPI_API_KEY} \

  porygon-fastapi

echo "Porygon API 服務已啟動，請訪問 http://localhost:8080/docs 查看 API 文檔"