FROM python:3.9


ENV XAI_API_KEY="xai-AbFqy5cxF1ZgS3LbhrLywjju7EKwaqMDAVKtjYnsuMgoJQjnjiiadmkZZR1CzVcjOsIF87qdfdKyygIT"
ENV XAI_DEPLOYMENT_NAME="grok-2-latest"
ENV XAI_ENDPOINT="https://api.x.ai/v1"

WORKDIR /app
COPY . .
RUN pip install -r requirements.txt