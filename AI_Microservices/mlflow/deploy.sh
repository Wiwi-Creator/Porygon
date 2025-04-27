kubectl apply -f mlflow-deployment.yaml
kubectl apply -f mlflow-service.yaml

kubectl port-forward pod/wikipedia 8080:8080

35.201.255.108