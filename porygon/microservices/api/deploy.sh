#!/usr/bin/env bash

set -e -x

# 創建 GKE 集群
gcloud container clusters create porygon-cluster \
  --zone=asia-east1-a \
  --num-nodes=3 \
  --machine-type=e2-standard-4

# 獲取集群憑證
gcloud container clusters get-credentials porygon-cluster --zone=asia-east1-a

# 創建服務帳戶
kubectl create serviceaccount porygon-api-sa

# 賦予權限
kubectl create clusterrolebinding porygon-api-sa-binding \
  --clusterrole=cluster-admin \
  --serviceaccount=default:porygon-api-sa

# 部署應用
kubectl apply -f porygon-api-deployment.yaml
kubectl apply -f porygon-api-service.yaml
