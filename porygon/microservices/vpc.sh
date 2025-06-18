# 設置環境變數
PROJECT_ID=genibuilder
REGION=asia-east1
VPC_NAME=porygon-vpc
SUBNET_NAME=porygon-subnet
SUBNET_RANGE=10.0.0.0/20

# 建立 VPC network
gcloud compute networks create $VPC_NAME \
  --project=$PROJECT_ID \
  --subnet-mode=custom

# 建立子網路(subnet)
gcloud compute networks subnets create $SUBNET_NAME \
  --project=$PROJECT_ID \
  --region=$REGION \
  --network=$VPC_NAME \
  --range=$SUBNET_RANGE \
  --enable-private-ip-google-access

# 允許 VPC 內部通信
gcloud compute firewall-rules create allow-internal-traffic \
  --network porygon-vpc \
  --allow tcp,udp,icmp \
  --source-ranges 10.0.0.0/20

# 允許 SSH 和其他管理服務
gcloud compute firewall-rules create allow-management \
  --network porygon-vpc \
  --allow tcp:22,tcp:3389,icmp

# 建立 Cloud Router
gcloud compute routers create porygon-router \
  --network=porygon-vpc \
  --region=asia-east1

# 配置 NAT 
gcloud compute routers nats create porygon-nat \
  --router=porygon-router \
  --auto-allocate-nat-external-ips \
  --nat-all-subnet-ip-ranges \
  --region=asia-east1

# Create VPC connector 確保 IP range 不重疊
gcloud compute networks vpc-access connectors create porygon-vpc-connector \
  --region=asia-east1 \
  --network=porygon-vpc \
  --range=10.8.0.0/28