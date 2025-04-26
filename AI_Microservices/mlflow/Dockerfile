FROM python:3.11-slim

WORKDIR /app

# 安裝基本系統依賴
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    ca-certificates \
    git \
    && rm -rf /var/lib/apt/lists/*

# 複製依賴文件
COPY requirements.txt .

# 安裝依賴，特別指定 MLflow 需要 GCS 支援
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --no-cache-dir mlflow[gcs]

# 複製應用程式代碼
COPY . .

# 設置環境變數
ENV PYTHONUNBUFFERED=1
ENV MLFLOW_TRACKING_URI="https://mlflow-931091704211.asia-east1.run.app"

# 暴露端口
EXPOSE 5000

# 啟動命令
CMD ["mlflow", "models", "serve", "-m", "gs://wiwi-bucket/1/15a6b7e29ad34d3fa1484ee9e0621774/artifacts/porygon_chain", "-p", "5000", "--host", "0.0.0.0"]