https://docs.aws.amazon.com/eks/latest/userguide/quickstart.html

```bash
eksctl create cluster -f cluster-config.yaml
kubectl apply -f ingressclass.yaml
kubectl create namespace game-2048 --save-config
kubectl apply -n game-2048 -f https://raw.githubusercontent.com/kubernetes-sigs/aws-load-balancer-controller/v2.8.0/docs/examples/2048/2048_full.yaml

```