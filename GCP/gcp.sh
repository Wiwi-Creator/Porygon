gcloud auth login

gcloud projects list

gcloud config set project genibuilder

gcloud auth activate-service-account --key-file=/Users/wiwi_kuo/Documents/GitHub/Porygon/gcp_credentials.json

## Create postrgresql instance
## Setup public IP access
## Setup SSL and enforce it
gcloud sql instances create mlflow-postgres \
  --database-version=POSTGRES_14 \
  --cpu=2 \
  --memory=4GB \
  --region=asia-east1 \
  --root-password=mlflow-password \
  --storage-type=SSD \
  --storage-size=20GB \
  --availability-type=REGIONAL \
  --backup-start-time=00:00 \
  --enable-bin-log \
  --database-flags=max_connections=100

gcloud sql databases create mlflow --instance=mlflow

gcloud sql users create mlflow --instance=mlflow-postgres --password=mlflow-user-password

## open your IP to Cloud SQL
MY_IP=(curl -s https://api.ipify.org) # 49.216.174.129%
gcloud sql instances patch mlflow --authorized-networks=$MY_IP/32
## connect to SQL
psql "sslmode=verify-ca sslrootcert=server-ca.pem sslcert=client-cert.pem sslkey=client-key.pem hostaddr=35.187.145.181 port=5432 user=postgres dbname=mlflow"

# Create Secret
echo -n "gs://wiwi-bucket" | \
gcloud secrets create mlflow_artifact_url \
  --data-file=- \
  --project=genibuilder

echo -n "postgresql+psycopg2://postgres:mlflow@/mlflow?host=/cloudsql/genibuilder:asia-east1:mlflow" | \
gcloud secrets create mlflow_database_url \
  --data-file=- \
  --project=genibuilder


echo -n "mlflow-admin" | \
gcloud secrets create mlflow_tracking_username \
  --data-file=- \
  --project=genibuilder

echo -n "mlflow" | \
gcloud secrets create mlflow_tracking_password \
  --data-file=- \
  --project=genibuilder


export GCP_PROJECT=genibuilder
make docker-auth
make build-m1 && make tag && make push

# Cloud Run UI 設定


# Get Your cloud run account
gcloud run services describe mlflow-gcp \
  --platform managed \
  --region asia-east1 \
  --format="value(spec.template.spec.serviceAccountName)"

# Set secret manager
gcloud projects add-iam-policy-binding genibuilder \
  --member="serviceAccount:931091704211-compute@developer.gserviceaccount.com" \
  --role="roles/secretmanager.secretAccessor"

# 為服務帳號授予 Storage Object Creator 權限
gsutil iam ch serviceAccount:wiwi-service-account@genibuilder.iam.gserviceaccount.com:roles/storage.objectCreator gs://wiwi-bucket

# 或者授予更全面的 Storage Object Admin 權限
gsutil iam ch serviceAccount:wiwi-service-account@genibuilder.iam.gserviceaccount.com:roles/storage.objectAdmin gs://wiwi-bucket


gcloud firestore databases create \
  --project=genibuilder \
  --database=member \
  --location=asia-east1

# 檢查 IAM 權限
gcloud projects get-iam-policy genibuilder --format=json
# admin 權限
gcloud projects add-iam-policy-binding genibuilder \
  --member="user:w22151500@gmail.com" \
  --role="roles/datastore.owner"

gcloud projects add-iam-policy-binding genibuilder \
  --member="user:w22151500@gmail.com" \
  --role="roles/datastore.user"

gsutil iam ch serviceAccount:931091704211-compute@developer.gserviceaccount.com:objectViewer gs://wiwi-bucket

gcloud projects add-iam-policy-binding genibuilder \
  --member="serviceAccount:931091704211-compute@developer.gserviceaccount.com" \
  --role="roles/storage.objectViewer"

  gcloud projects add-iam-policy-binding genibuilder \
  --member="serviceAccount:931091704211-compute@developer.gserviceaccount.com" \
  --role="roles/bigquery.dataEditor"

gcloud projects add-iam-policy-binding genibuilder \
  --member="user:w22151500@gmail.com" \
  --role="roles/bigquery.dataEditor"


gcloud projects get-iam-policy genibuilder \
  --flatten="bindings[].members" \
  --format="table(bindings.role,bindings.members)" \
  --filter="bindings.members:931091704211-compute@developer.gserviceaccount.com"

gcloud projects get-iam-policy genibuilder --flatten="bindings[].members" --format="table(bindings.role,bindings.members)" --filter="bindings.members:w22151500@gmail.com"

# 檢視 MLflow cloud run 權限
gcloud run services add-iam-policy-binding mlflow \
  --member="serviceAccount:931091704211-compute@developer.gserviceaccount.com" \
  --role="roles/run.invoker" \
  --region=asia-east1