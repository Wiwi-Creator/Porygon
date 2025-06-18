kubectl get pods -o wide
NAME                               READY   STATUS    RESTARTS   AGE    IP           NODE                                                 NOMINATED NODE   READINESS GATES
curl-test-pod                      1/1     Running   0          15s    10.72.0.17   gke-multi-agent-cluster-default-pool-af7c477b-cnb2   <none>           <none>
kuberay-operator-975995b7d-6mnxt   1/1     Running   0          2d9h   10.72.0.13   gke-multi-agent-cluster-default-pool-af7c477b-cnb2   <none>           <none>
wikipedia                          1/1     Running   0          3h6m   10.72.1.19   gke-multi-agent-cluster-default-pool-af7c477b-s9j7   <none>           <none>

curl http://10.72.1.19:8000

