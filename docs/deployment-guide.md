# Comprehensive Deployment & Operations Guide

**Course:** Master's in Cloud Computing  
**Author:** Chamroeun Saran (GitHub: [Chamroeun12](https://github.com/Chamroeun12))  
**Target Environment:** Local Workstation / Amazon EKS (Sydney `ap-southeast-2`) / Argo CD GitOps  

---

## 1. Prerequisites Checklist

Before executing the deployment workflow, ensure the following tools are available:
- **Git:** Version 2.40+ (`git --version`)
- **Docker Desktop:** Linux container engine running (`docker info`)
- **Python:** 3.10+ with pip (`python --version`)
- **AWS CLI:** 1.40+ or 2.x (`aws --version`)
- **Kubernetes CLI (`kubectl`):** v1.28+ (`kubectl version --client`)
- **Terraform (Optional for cluster creation):** v1.5.0+ (`terraform -version`)

---

## 2. Local Development & Verification

### 2.1 Running the Flask Application Locally
```powershell
# 1. Create and activate a Python virtual environment
python -m venv .venv
.\.venv\Scripts\Activate.ps1

# 2. Install dependencies
pip install -r requirements.txt
pip install -r requirements-dev.txt

# 3. Run automated tests and PEP8 lint check
pytest -v --cov=app --cov-report=term-missing
flake8 --max-line-length=120 --exclude=venv,.venv,build_submission_report.py,generate_evidence_screens.py app.py tests/

# 4. Start Flask web server locally
python app.py
```
Visit `http://localhost:5000/` in your browser, or verify via API:
```powershell
curl.exe http://127.0.0.1:5000/health
```

### 2.2 Building and Running with Docker Desktop
```powershell
# 1. Build the production multi-stage image
docker build -t cicd-assignment:local .

# 2. Run container as non-root user
docker run -d --name cicd-test-app -p 5001:5000 -e APP_VERSION=2.0.0 cicd-assignment:local

# 3. Test endpoints
curl.exe http://127.0.0.1:5001/health
curl.exe -I http://127.0.0.1:5001/

# 4. Run local Trivy vulnerability scan
docker run --rm -v //var/run/docker.sock:/var/run/docker.sock aquasec/trivy:latest image --severity HIGH,CRITICAL cicd-assignment:local

# 5. Clean up container
docker rm -f cicd-test-app
```

---

## 3. Amazon ECR Configuration

The repository uses the private Amazon ECR registry:
- **Registry URI:** `399311815210.dkr.ecr.ap-southeast-2.amazonaws.com/cicd-assignment`

### Authenticating and Pushing Manually (if testing from CLI):
```powershell
# Authenticate Docker client against Amazon ECR
aws ecr get-login-password --region ap-southeast-2 | docker login --username AWS --password-stdin 399311815210.dkr.ecr.ap-southeast-2.amazonaws.com

# Tag and push image
docker tag cicd-assignment:local 399311815210.dkr.ecr.ap-southeast-2.amazonaws.com/cicd-assignment:latest
docker push 399311815210.dkr.ecr.ap-southeast-2.amazonaws.com/cicd-assignment:latest
```

---

## 4. Amazon EKS Cluster Provisioning (When Approved)

To create the Amazon EKS cluster safely with reproducible infrastructure-as-code:

> [!IMPORTANT]
> Amazon EKS incurs AWS hourly charges (~$0.10/hour for the EKS control plane + EC2 worker nodes). Only execute `terraform apply` when you are ready to provision live cloud resources.

```bash
cd terraform

# 1. Initialize Terraform plugins
terraform init

# 2. Inspect the execution plan (Read-Only)
terraform plan

# 3. Apply infrastructure upon explicit approval
terraform apply

# 4. Update local kubeconfig to connect kubectl to EKS
aws eks update-kubeconfig --region ap-southeast-2 --name cicd-eks-cluster
```

Verify cluster node status:
```bash
kubectl get nodes -o wide
```

---

## 5. Argo CD Installation & GitOps Synchronization

### 5.1 Installing Argo CD on Amazon EKS
```bash
# 1. Create the argocd namespace
kubectl create namespace argocd

# 2. Install official Argo CD manifests
kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml

# 3. Wait for Argo CD pods to become Ready
kubectl wait --namespace argocd --for=condition=ready pod --selector=app.kubernetes.io/name=argocd-server --timeout=180s

# 4. Retrieve initial admin password (base64 decoded)
kubectl -n argocd get secret argocd-initial-admin-secret -o jsonpath="{.data.password}" | base64 -d
```

### 5.2 Accessing the Argo CD UI Safely
To keep the administrative interface secure from public exposure:
```powershell
kubectl port-forward svc/argocd-server -n argocd 8080:443
```
Open `https://localhost:8080` in your browser (Username: `admin`, Password: from step 4).

### 5.3 Deploying the GitOps Application
```bash
# Apply the GitOps Application Custom Resource
kubectl apply -f k8s/argocd/application.yaml
```

Argo CD will automatically create the `cicd-production` namespace, pull manifests from `k8s/` in the GitHub repository, deploy the pods, and continuously maintain the desired state!

---

## 6. GitHub Actions Secrets Setup

In your GitHub repository (`Chamroeun12/Assignment`), go to **Settings > Secrets and variables > Actions** and configure:

| Secret Name | Description | Example / Format |
| :--- | :--- | :--- |
| `AWS_ACCOUNT_ID` | Your AWS Account ID | `399311815210` |
| `AWS_ROLE_TO_ASSUME` | IAM Role ARN for OIDC federation *(Recommended)* | `arn:aws:iam::399311815210:role/github-actions-ecr-role` |
| `AWS_ACCESS_KEY_ID` | IAM User Access Key *(Alternative)* | `AKIA...` |
| `AWS_SECRET_ACCESS_KEY` | IAM User Secret Key *(Alternative)* | *(Kept secret)* |
| `SONAR_TOKEN` | SonarQube / SonarCloud API Token *(Optional)* | `squ_...` |
| `SONAR_HOST_URL` | SonarQube Server URL *(Optional)* | `https://sonarcloud.io` or internal server |
