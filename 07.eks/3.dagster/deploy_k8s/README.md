# View this example in the Dagster docs at https://docs.dagster.io/deployment/guides/kubernetes/deploying-with-helm

- Build user code image
```bash
docker build . -t iris_analysis:1
docker tag iris_analysis:1 gsarapura/k8s-dagster:latest
docker push gsarapura/k8s-dagster:latest 

```
- Test
```bash
eksctl create cluster \
  --name k8s-dagster-test \
  --region us-east-1 \
  --nodegroup-name single-node \
  --node-type t3.medium \
  --nodes 1 \
  --nodes-min 1 \
  --nodes-max 1 \
  --managed \
  --with-oidc \
  --dry-run

# Storage class
kubectl get storageclass
# Add gp3
kubectl apply -f storage-class-gp3.yaml
# Set as default
kubectl patch storageclass gp3 -p '{"metadata": {"annotations":{"storageclass.kubernetes.io/is-default-class":"true"}}}'

eksctl get nodegroup --cluster k8s-dagster-test --region us-east-1 -o yaml
aws iam attach-role-policy \
    --role-name eksctl-k8s-dagster-test-nodegroup--NodeInstanceRole-bOoPs0nP6x18 \
    --policy-arn arn:aws:iam::992382742298:policy/EKSNodeEBSPolicy
aws iam list-attached-role-policies \
    --role-name eksctl-k8s-dagster-test-nodegroup--NodeInstanceRole-bOoPs0nP6x18
eksctl get nodegroup --cluster k8s-dagster-test --region us-east-1

# -----------------------------------------------------------------------------------------------
# https://docs.aws.amazon.com/eks/latest/userguide/ebs-csi.html
# Adding OIDC: OIDC (OpenID Connect) is a simple identity layer on top of the OAuth 2.0 protocol
eksctl utils associate-iam-oidc-provider --region us-east-1 --cluster dagster-test --approve
# -----------------------------------------------------------------------------------------------


kubectl create namespace dagster
helm install dagster dagster/dagster \
    --namespace dagster \
    -f values-test.yaml
helm upgrade dagster dagster/dagster \
    --namespace dagster \
    -f values-test.yaml

kubectl apply -f service-ui.yaml
```

- Dev

```bash
# Node managed
eksctl create cluster \
    --name k8s-dagster \
    --region us-east-1 \
    --node-type t3.medium \
    --nodes 2 \
    --nodes-min 2 \
    --nodes-max 3 \
    --managed

cat <<EOF > storage-class.yaml
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
  name: ebs-sc
provisioner: ebs.csi.aws.com
volumeBindingMode: WaitForFirstConsumer
EOF
# Apply the storage class
kubectl apply -f storage-class.yaml

# Add the AWS EBS CSI driver Helm repository
helm repo add aws-ebs-csi-driver https://kubernetes-sigs.github.io/aws-ebs-csi-driver
helm install aws-ebs-csi-driver aws-ebs-csi-driver/aws-ebs-csi-driver \
    --namespace kube-system

cat <<EOF > ebs-policy.json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "ec2:CreateVolume",
                "ec2:DeleteVolume",
                "ec2:AttachVolume",
                "ec2:DetachVolume",
                "ec2:DescribeVolumes",
                "ec2:DescribeVolumesModifications",
                "ec2:ModifyVolume",
                "ec2:CreateTags",
                "ec2:DeleteTags",
                "ec2:DescribeTags"
            ],
            "Resource": "*"
        }
    ]
}
EOF
aws iam create-policy \
    --policy-name EKSNodeEBSPolicy \
    --policy-document file://ebs-policy.json
eksctl get nodegroup --cluster k8s-dagster --region us-east-1 -o json | jq -r '.[0].NodeInstanceRoleARN'
aws iam attach-role-policy \
    --role-name eksctl-k8s-dagster-nodegroup-ng-8c-NodeInstanceRole-FBeEMqIaiGE0 \
    --policy-arn arn:aws:iam::992382742298:policy/EKSNodeEBSPolicy
aws iam list-attached-role-policies \
    --role-name eksctl-k8s-dagster-nodegroup-ng-8c-NodeInstanceRole-FBeEMqIaiGE0


kubectl create namespace dagster
helm install dagster dagster/dagster \
    --namespace dagster \
    -f values-dev.yaml

eksctl get nodegroup --cluster k8s-dagster --region us-east-1

# REMOVE
helm uninstall dagster -n dagster
kubectl delete namespace dagster
helm uninstall aws-ebs-csi-driver -n kube-system
kubectl delete storageclass ebs-sc
eksctl delete cluster --name k8s-dagster --region us-east-1
# Optional
aws iam delete-policy --policy-arn arn:aws:iam::992382742298:policy/EKSNodeEBSPolicy
```