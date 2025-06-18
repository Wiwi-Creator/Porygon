PROJECT_ID="genibuilder"
CLUSTER_NAME="multi-agent-cluster"
ZONE="asia-east1-b"
VPC_NAME="porygon-vpc"
SUBNET_NAME="porygon-subnet"

echo "🚀 建立 GKE Standard Cluster（節點自動擴展）..."

gcloud container clusters create ${CLUSTER_NAME} \
  --project=${PROJECT_ID} \
  --zone=${ZONE} \
  --enable-ip-alias \
  --network=${VPC_NAME} \
  --subnetwork=${SUBNET_NAME} \
  --num-nodes=1 \
  --enable-autoscaling \
  --min-nodes=1 \
  --max-nodes=5 \
  --machine-type=e2-standard-4 \
  --release-channel=regular \
  --scopes=https://www.googleapis.com/auth/cloud-platform

echo " 取得 GKE 認證 context"
gcloud container clusters get-credentials ${CLUSTER_NAME} --zone ${ZONE} --project=${PROJECT_ID}

echo "Helm Install KubeRay."
helm install kuberay-operator kuberay/kuberay-operator --version 1.2.2

kubectl port-forward pod/wikipedia 8080:8080
