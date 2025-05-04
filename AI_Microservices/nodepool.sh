gcloud container node-pools create ray-nodepool \
  --cluster=YOUR_CLUSTER_NAME \
  --zone=asia-east1-a \
  --machine-type=e2-standard-4 \  # 4vCPU / 16Gi memory
  --num-nodes=2 \
  --enable-autoscaling --min-nodes=1 --max-nodes=5 \
  --node-labels=ray-pool=default \
  --node-taints=ray-node=true:NoSchedule