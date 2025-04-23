CLUSTER_NAME="api"
REGION_NAME="asia-east1"
PROJECT_ID="genibuilder"
VPC_NAME="default"
SUBNETWORK_NAME="vpc-asia-east1"

echo "Creating GKE Autopilot Cluster(Private) : ${CLUSTER_NAME} , VPC : ${VPC_NAME} , Subnetwork: ${SUBNETWORK_NAME} "
# auto-pilot
gcloud container clusters create-auto ${CLUSTER_NAME} --region ${REGION_NAME} \
                                                      --project ${PROJECT_ID} \
                                                      --network ${VPC_NAME} \
                                                      --subnetwork ${SUBNETWORK_NAME} \
                                                      --enable-private-nodes ;

# standard
gcloud container clusters create porygon-cluster \
  --zone=asia-east1-a \
  --num-nodes=2 \
  --machine-type=e2-standard-4

gcloud container clusters get-credentials porygon-cluster --zone=asia-east1-a
