#!/bin/bash
docker build -t porygon-fastapi .

docker rm -f porygon-api 2>/dev/null || true

# 使用 host.docker.internal 連接到本機 MLflow 服務
docker run --rm -d \
  --name porygon-fastapi \
  --network mlflow-network-v1 \
  -p 8080:8080 \
  -e PYTHONPATH=/app \
  -e MLFLOW_TRACKING_URI=http://mlflow-tracking-server:5010 \
  -e MLFLOW_REGISTRY_URI=http://mlflow-tracking-server:5010 \
  -e MLFLOW_ARTIFACT_URI=http://mlflow-artifact-server:5500/api/2.0/mlflow-artifacts/artifacts \
  -e MODEL_URI=runs:/e4b99fdeff71405aa3c78f5352b6308a/porygon_chain \
  porygon-fastapi

echo "Porygon API 服務已啟動，請訪問 http://localhost:8080/docs 查看 API 文檔"