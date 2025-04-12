#!/bin/bash
NAME=porygon-api-service
PROJECT_ID=wiwikuo-1989
IMAGE=asia.gcr.io/wiwikuo-1989/wiwikuo-1989
VPC_CONNECTOR=projects/datapool-1806/locations/asia-east1/connectors/migo-cloudrun-vpc
CPU=4
CONCURRENCY=4
MAX_INSTANCES=10
MEMORY=8Gi
TIMEOUT=3600

gcloud beta run deploy ${NAME} \
    --project ${PROJECT_ID} \
    --image ${IMAGE} \
    --concurrency ${CONCURRENCY} \
    --cpu ${CPU}\
    --max-instances ${MAX_INSTANCES} \
    --memory ${MEMORY} \
    --timeout ${TIMEOUT} \
    --vpc-connector ${VPC_CONNECTOR} \
    --service-account digdag-server@datapool-1806.iam.gserviceaccount.com \
    --region asia-east1 \
    --allow-unauthenticated \
    --platform managed \
    --vpc-egress all-traffic
