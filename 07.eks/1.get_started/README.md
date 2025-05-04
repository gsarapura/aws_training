# QuickStart: Auto Mode Cluster
https://docs.aws.amazon.com/eks/latest/userguide/quickstart.html

```bash
# Configure the cluster
eksctl create cluster -f 1.cluster-config.yaml
# Create IngressClass
kubectl apply -f 2.ingressclass.yaml


# Deploy the 2048 game sample application
kubectl create namespace game-2048 --save-config
kubectl apply -n game-2048 -f https://raw.githubusercontent.com/kubernetes-sigs/aws-load-balancer-controller/v2.8.0/docs/examples/2048/2048_full.yaml
kubectl apply -n game-2048 -f 3.20248_full.yaml

# Persist Data using Amazon EKS Auto Mode
kubectl apply -f 4.storage-class.yaml
kubectl apply -f 5.ebs-pvc.yaml
# Update your 2048 game deployment to use this PVC for storing data
kubectl apply -f 6.ebs-deployment.yaml
```