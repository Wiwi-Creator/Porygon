docker build -t porygon-api-service .

docker run -d --rm -p 8080:8080 --name porygon-api porygon-api-service

docker run -d --name porygon-api --network mlflow-tracking_default -p 8080:8080 \
  -e MLFLOW_TRACKING_URI=http://mlflow:5000 \
  -e MODEL_URI=runs:/6390ffad485b425c848553ba47d184d0/porygon_chain \
  porygon-api-service