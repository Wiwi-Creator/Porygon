PROJECT_ID="genibuilder"
CLUSTER_NAME="multi-agent-system"
REGION_NAME="asia-east1"
VPC_NAME="porygon-vpc"
SUBNETWORK_NAME="vpn-asia-east1"
SUBNET_NAME=porygon-subnet

echo "Creating GKE Autopilot Cluster(Private) : ${CLUSTER_NAME} , VPC : ${VPC_NAME} , Subnetwork: ${SUBNETWORK_NAME} "
gcloud container clusters create porygon-cluster \
  --project=$PROJECT_ID \
  --region=$REGION \
  --network=$VPC_NAME \
  --subnetwork=$SUBNET_NAME \
  --enable-ip-alias
