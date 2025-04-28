https://www.youtube.com/watch?v=jUYNS90nq8U

```bash
#!/bin/bash
kubectl get all

minikube ip 

# Either
curl 192.168.49.2:31879
## Or set up LoadBalancer type in sevice.yaml to create tunnel
minikube tunnel

# Install first one
helm install mywebapp-devops webapp1/ --values webapp1/values.yaml

# Remove current implementation
helm uninstall $NAME

# Upgrade
helm upgrade mywebapp-devops webapp1/ --values webapp1/values.yaml


# Create DEV/PROD
kubectl create namespace dev
kubectl create namespace prod
helm install mywebapp-devops-dev webapp1/ --values webapp1/values.yaml -f webapp1/values-dev.yaml -n dev
helm install mywebapp-devops-prod webapp1/ --values webapp1/values.yaml -f webapp1/values-prod.yaml -n prod
helm ls --all-namespaces


```