#!/bin/bash

MODEL_URI="gs://wiwi-bucket/1/15a6b7e29ad34d3fa1484ee9e0621774/artifacts/porygon_chain"
IMAGE_NAME="mlflow-wikipedia-agent"

echo "✅ Generating Dockerfile from MLflow model..."
mlflow models generate-dockerfile -m "$MODEL_URI" --enable-mlserver

echo "🔨 Building Docker image..."
docker build -t "$IMAGE_NAME" .

echo "🎉 Done! You can now run:"
echo "    docker run -p 5000:8080 $IMAGE_NAME"

mlflow models serve -m gs://wiwi-bucket/1/15a6b7e29ad34d3fa1484ee9e0621774/artifacts/porygon_chain -p 5000


mlflow models serve -m gs://wiwi-bucket/1/15a6b7e29ad34d3fa1484ee9e0621774/artifacts/porygon_chain -p 5000


## Test External IP
curl http://35.201.255.108/invocations \
    -H "Content-Type: application/json" \
    --data '{"inputs": {"input": "What is the strongest pokemon?"}}'

curl http://127.0.0.1:5000/invocations \
    -H "Content-Type: application/json" \
    --data '{"inputs": {"input": "What is the strongest pokemon?"}}'
## Test Internal IP
curl http://wikipedia-service:80/invocations \
    -H "Content-Type: application/json" \
    --data '{"inputs": {"input": "What is the strongest pokemon?"}}'

