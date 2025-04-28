View this example in the Dagster docs at https://docs.dagster.io/deployment/guides/kubernetes/deploying-with-helm

```bash
docker build . -t iris_analysis:1
docker tag iris_analysis:1 gsarapura/k8s-dagster:latest
docker push gsarapura/k8s-dagster:latest 

eksctl create cluster -f cluster-config.yaml

helm repo add dagster https://dagster-io.github.io/helm
helm repo update
helm show values dagster/dagster > values.yaml
helm upgrade --install dagster dagster/dagster -f values.yaml
kubectl logs <pod-name>

eksctl delete cluster -f ./cluster-config.yaml
```