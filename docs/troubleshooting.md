# Troubleshooting Guide: Common Incidents & Verified Solutions

**Course:** Master's in Cloud Computing  
**Author:** Chamroeun Saran (GitHub: [Chamroeun12](https://github.com/Chamroeun12))  
**Scope:** Docker, Pytest, Trivy, Amazon ECR, Amazon EKS, Argo CD, and GitOps  

---

## 1. Local Development & Docker Issues

### 1.1 "Failed to connect to the docker API at npipe:////./pipe/dockerDesktopLinuxEngine"
- **Root Cause:** Docker Desktop application is installed but the background Linux container engine service is not running or still booting up.
- **Solution:**
  1. Start Docker Desktop executable:
     ```powershell
     Start-Process "C:\Users\ahroe\AppData\Local\Programs\DockerDesktop\Docker Desktop.exe"
     ```
  2. Wait 15–30 seconds for the backend daemon to initialize.
  3. Verify with:
     ```powershell
     docker version
     ```

### 1.2 Flake8 Linting Failure in CI
- **Root Cause:** PEP8 spacing violations (e.g. `E302 expected 2 blank lines, found 1`).
- **Solution:**
  Ensure two blank lines precede top-level functions and classes in Python files (`app.py`, `tests/test_app.py`). Run locally before pushing:
  ```powershell
  flake8 --max-line-length=120 --exclude=venv,.venv,build_submission_report.py,generate_evidence_screens.py app.py tests/
  ```

---

## 2. Container Security & Trivy Issues

### 2.1 Trivy Detects HIGH/CRITICAL Vulnerabilities in Image
- **Root Cause:** Base operating system packages or third-party Python packages have reported CVEs.
- **Solution:**
  1. For Python libraries: Inspect `pip list` or Trivy report, update package version in `requirements.txt` to the patched version.
  2. For OS packages: In `Dockerfile`, add `RUN apt-get update && apt-get upgrade -y && rm -rf /var/lib/apt/lists/*` to pull latest patched Debian security updates.
  3. In CI: The workflow uses `exit-code: "0"` in audit mode for logging; switch to `exit-code: "1"` only once all team dependencies are vetted.

---

## 3. Amazon ECR & Authentication Issues

### 3.1 "no basic auth credentials" or "denied: Your authorization token has expired"
- **Root Cause:** AWS ECR authentication tokens expire after 12 hours.
- **Solution:**
  Re-authenticate Docker against your regional ECR registry:
  ```powershell
  aws ecr get-login-password --region ap-southeast-2 | docker login --username AWS --password-stdin 399311815210.dkr.ecr.ap-southeast-2.amazonaws.com
  ```

### 3.2 GitHub Actions Cannot Push to ECR
- **Root Cause:** Missing or invalid `AWS_ROLE_TO_ASSUME` or AWS access keys in repository secrets.
- **Solution:**
  Verify that GitHub Actions has permissions to assume your IAM role via OIDC trust policy. The repository name in the OIDC Subject must match `repo:Chamroeun12/Assignment:*`.

---

## 4. Kubernetes (EKS) & Pod Health Issues

### 4.1 Pod Status `ImagePullBackOff` or `ErrImagePull`
- **Root Cause:** EKS worker nodes cannot authenticate with private Amazon ECR.
- **Solution:**
  1. Ensure the EKS Node Group IAM role (`aws_iam_role.node_role`) has the managed policy `arn:aws:iam::aws:policy/AmazonEC2ContainerRegistryReadOnly` attached.
  2. Check the exact image URI and tag:
     ```bash
     kubectl describe pod -n cicd-production -l app=cicd-assignment
     ```
  3. Confirm that the image tag actually exists in the ECR repository:
     ```bash
     aws ecr describe-images --repository-name cicd-assignment --region ap-southeast-2
     ```

### 4.2 Pod Status `CrashLoopBackOff`
- **Root Cause:** Container process is failing immediately upon startup (e.g. syntax error or missing environment variable).
- **Solution:**
  Inspect the previous container logs:
  ```bash
  kubectl logs -n cicd-production -l app=cicd-assignment --previous
  ```

### 4.3 Readiness Probe Failing (Traffic Not Routing to Pod)
- **Root Cause:** HTTP GET `/health` returns non-2xx status code or times out.
- **Solution:**
  Test the endpoint locally or exec into the pod:
  ```bash
  kubectl exec -it -n cicd-production <POD_NAME> -- python -c "import urllib.request; print(urllib.request.urlopen('http://localhost:5000/health').read())"
  ```

---

## 5. Argo CD & GitOps Issues

### 5.1 Argo CD Overwrites Manual `kubectl` Changes (Self-Heal Conflict)
- **Root Cause:** When `selfHeal: true` is configured in Argo CD, any live change made via `kubectl` is viewed as unauthorized configuration drift.
- **Solution:**
  - Make Git the authoritative control point: commit changes to `k8s/deployment.yaml` and let Argo CD sync.
  - Or temporarily disable self-healing during an emergency:
    ```bash
    kubectl patch application cicd-assignment -n argocd --type merge -p '{"spec":{"syncPolicy":{"automated":null}}}'
    ```

### 5.2 Argo CD Application Shows "ComparisonError" or "Unknown Repo"
- **Root Cause:** The Git repository is private, or network access to GitHub is restricted.
- **Solution:**
  In Argo CD UI or CLI, add repository credentials:
  ```bash
  argocd repo add https://github.com/Chamroeun12/Assignment.git --username Chamroeun12 --password <GITHUB_PERSONAL_ACCESS_TOKEN>
  ```
