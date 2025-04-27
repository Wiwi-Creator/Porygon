FROM python:3.11-slim

WORKDIR /app

# 安裝基本系統依賴
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    ca-certificates \
    git \
    tini \
    curl \
    && rm -rf /var/lib/apt/lists/*

# 複製依賴文件
COPY requirements.txt .

# 安裝依賴，確保 Pydantic 2.x 版本
RUN pip install --no-cache-dir pydantic==2.11.3
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --no-cache-dir mlflow[gcs]

# 複製應用程式代碼
COPY . .

# 設置環境變數
ENV PYTHONUNBUFFERED=1
ENV MLFLOW_TRACKING_URI="https://mlflow-931091704211.asia-east1.run.app"

# 暴露端口
EXPOSE 8080

# 使用 tini 作為 init 進程來正確處理信號
ENTRYPOINT ["/usr/bin/tini", "--"]

# 啟動命令
CMD ["mlflow", "models", "serve", "-m", "gs://wiwi-bucket/1/15a6b7e29ad34d3fa1484ee9e0621774/artifacts/porygon_chain", "-p", "8080", "--host", "0.0.0.0", "--no-conda", "--timeout-keep-alive", "120"]