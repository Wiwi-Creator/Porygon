# 設定環境變數（用你的專案 ID）
PROJECT_ID="genibuilder"
IMAGE_NAME="mlflow-wikipedia-agent"
REGION="asia-east1"  # 可選 region

# 設定 tag 為 GCR or GAR 格式（以下是 GCR）
docker tag $IMAGE_NAME gcr.io/$PROJECT_ID/$IMAGE_NAME

# 登入 GCP 並推送
gcloud auth configure-docker
docker push gcr.io/$PROJECT_ID/$IMAGE_NAME