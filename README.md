# Production-Grade CI/CD Pipeline: Commit to Production on Amazon EKS with Argo CD GitOps

[![CI/CD Pipeline](https://github.com/Chamroeun12/cicd-homework2/actions/workflows/ci-cd.yml/badge.svg)](https://github.com/Chamroeun12/cicd-homework2/actions/workflows/ci-cd.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python: 3.10](https://img.shields.io/badge/Python-3.10-blue.svg)](https://www.python.org/)
[![Docker](https://img.shields.io/badge/Docker-Multi--stage-2496ED.svg)](https://www.docker.com/)
[![Kubernetes: EKS](https://img.shields.io/badge/Kubernetes-EKS-326CE5.svg)](https://aws.amazon.com/eks/)
[![GitOps: Argo CD](https://img.shields.io/badge/GitOps-Argo%20CD-EF7B4D.svg)](https://argo-cd.readthedocs.io/)

**Course:** Master's Degree in Cloud Computing  
**Author:** Chamroeun Saran (GitHub: [Chamroeun12](https://github.com/Chamroeun12))  
**Repository:** [https://github.com/Chamroeun12/cicd-homework2](https://github.com/Chamroeun12/cicd-homework2)  
**Target Architecture:** Amazon EKS & Amazon ECR (Sydney `ap-southeast-2`)  

---

## 1. Executive Summary & The 10-Step Architecture

This repository contains the complete implementation of a production-grade, automated **Continuous Integration and Continuous Deployment (CI/CD) Pipeline** following the reference architectural diagram:

```
[1. Commit & Push Code] 
       │ (Feature Branch / PR)
       ▼
[2. Build & Test] ──────────► Automated Pytest & Flake8 Linter
       │
       ▼
[3. Code Quality & Scan] ───► SonarQube & Trivy Vulnerability Scanner
       │
       ▼
[4. Build & Push Image] ────► Amazon Elastic Container Registry (ECR)
       │
       ▼
[5. Update K8s Manifest] ───► GitOps Automation with Immutable Commit SHA
       │
       ▼
[6. Sync with EKS] ─────────► Argo CD Pull-Based Reconciliation Engine
       │
       ▼
[7. Deploy to Pods] ────────► Kubernetes Pods with HTTP Health Probes
       │
       ▼
[8. Deployment Strategy] ───► Zero-Downtime Rolling Update & Blue-Green Option
       │
       ▼
[9. Monitoring & Logs] ─────► Prometheus, Grafana & AWS CloudWatch Insights
       │
       ▼
[10. Rollback if Needed] ───► Authoritative GitOps Revert & Emergency Undo
```

---

## 2. Mapping of Reference Diagram Stages to Implemented Artifacts

| Stage # | Stage Name | Target Tooling | Project Files | Status |
| :---: | :--- | :--- | :--- | :---: |
| **1** | **Commit & Push Code** | Git & GitHub | `.gitignore`, branch `feature/eks-argocd-cicd` | **PASS** |
| **2** | **Build & Test** | GitHub Actions / Pytest | `tests/test_app.py`, `requirements-dev.txt`, `.github/workflows/ci-cd.yml` | **PASS** |
| **3** | **Code Quality & Security** | SonarQube & Trivy | `sonar-project.properties`, Trivy scan in `.github/workflows/ci-cd.yml` | **PASS** |
| **4** | **Build & Push Image** | Docker & Amazon ECR | `Dockerfile`, `.dockerignore`, ECR workflow | **PASS** |
| **5** | **Update K8s Manifest** | GitOps Manifests | `k8s/kustomization.yaml`, `k8s/deployment.yaml` | **PASS** |
| **6** | **Sync with EKS** | Argo CD | `k8s/argocd/application.yaml` | **PASS** |
| **7** | **Deploy to Pods** | Amazon EKS | `k8s/namespace.yaml`, `k8s/service.yaml`, `k8s/configmap.yaml` | **PASS** |
| **8** | **Deployment Strategy** | Rolling & Blue-Green | `k8s/deployment.yaml`, `k8s/blue-green/switch-traffic.ps1` | **PASS** |
| **9** | **Monitoring & Logs** | Prometheus & CloudWatch | `monitoring/prometheus/`, `monitoring/grafana/`, `monitoring/cloudwatch/` | **PASS** |
| **10** | **Safe Rollback** | GitOps Revert / K8s Undo | `docs/rollback-runbook.md`, `k8s/blue-green/` | **PASS** |

---

## 3. Project Structure

```
.
├── .github/
│   └── workflows/
│       └── ci-cd.yml                     # Unified 10-stage GitHub Actions pipeline
├── docs/
│   ├── architecture.md                   # Complete architectural breakdown & Mermaid diagram
│   ├── deployment-guide.md               # End-to-end setup and provisioning guide
│   ├── implementation-plan.md            # Phase 0 environmental inspection & decisions
│   ├── monitoring-guide.md               # Prometheus, Grafana & CloudWatch setup
│   ├── rollback-runbook.md               # GitOps and Kubernetes recovery runbook
│   └── troubleshooting.md                # Incident resolution guide with verified solutions
├── k8s/
│   ├── argocd/
│   │   └── application.yaml              # Argo CD GitOps Application custom resource
│   ├── blue-green/
│   │   ├── deployment-blue.yaml          # Blue active deployment
│   │   ├── deployment-green.yaml         # Green candidate deployment
│   │   ├── service-preview.yaml          # Test/candidate preview service
│   │   ├── service-production.yaml       # Live production service
│   │   ├── switch-traffic.ps1            # PowerShell traffic switching automation
│   │   └── switch-traffic.sh             # Bash traffic switching automation
│   ├── configmap.yaml                    # Environment configuration
│   ├── deployment.yaml                   # Production Deployment with RollingUpdate
│   ├── kustomization.yaml                # GitOps image tag automation
│   ├── namespace.yaml                    # Production namespace (cicd-production)
│   └── service.yaml                      # LoadBalancer service for AWS EKS
├── monitoring/
│   ├── cloudwatch/
│   │   └── container-insights.yaml       # AWS CloudWatch Container Insights DaemonSet config
│   ├── grafana/
│   │   └── dashboard-cicd.json           # Real-time pod telemetry dashboard
│   └── prometheus/
│       ├── alert-rules.yaml              # Deployment failure & high CPU alert rules
│       └── servicemonitor.yaml           # Prometheus Operator scraper definition
├── terraform/
│   ├── main.tf                           # Reproducible AWS EKS cluster and VPC definition
│   ├── outputs.tf                        # EKS endpoint and kubeconfig outputs
│   └── variables.tf                      # Configurable node groups and region
├── tests/
│   ├── __init__.py                       # Test package initializer
│   └── test_app.py                       # Automated Pytest suite for / and /health
├── .dockerignore                         # Docker build context exclusions
├── .gitignore                            # Secret, credential, and cache exclusions
├── Dockerfile                            # Multi-stage, non-root, security-hardened container
├── Jenkinsfile                           # Enterprise declarative Jenkins pipeline alternative
├── app.py                                # Python Flask application
├── requirements.txt                      # Runtime dependencies (Flask 3.x)
├── requirements-dev.txt                  # Dev dependencies (pytest, pytest-cov, flake8)
├── sonar-project.properties              # SonarQube static code quality configuration
└── templates/
    └── index.html                        # Modern, dynamic UI displaying the 10 pipeline steps
```

---

## 4. Local Quickstart & Verification

### Step 4.1: Automated Tests and Linting
```powershell
# 1. Run PEP8 linter
python -m flake8 --max-line-length=120 --exclude=venv,.venv,build_submission_report.py,generate_evidence_screens.py app.py tests/

# 2. Run automated test suite with coverage
python -m pytest -v --cov=app --cov-report=term-missing tests/
```
**Verified Result:**
```
tests/test_app.py::test_index_route_success PASSED                       [ 25%]
tests/test_app.py::test_health_endpoint_structure PASSED                 [ 50%]
tests/test_app.py::test_health_endpoint_values PASSED                    [ 75%]
tests/test_app.py::test_404_not_found PASSED                             [100%]
TOTAL: 87% coverage (0 errors)
```

### Step 4.2: Build & Run Docker Container
```powershell
# 1. Build production image locally
docker build -t cicd-homework2:local .

# 2. Run container in background
docker run -d --name cicd-test-app -p 5001:5000 -e APP_VERSION=2.0.0 cicd-homework2:local

# 3. Test HTTP Health API
curl.exe http://127.0.0.1:5001/health
# Output: {"hostname":"bbc58ac46e38","status":"healthy","version":"2.0.0"}

# 4. Clean up
docker rm -f cicd-test-app
```

### Step 4.3: Run Trivy Vulnerability Scan
```powershell
docker run --rm -v //var/run/docker.sock:/var/run/docker.sock aquasec/trivy:latest image --severity HIGH,CRITICAL cicd-homework2:local
```

### Step 4.4: Validate Kubernetes Manifests
```powershell
kubectl kustomize k8s/
```
**Verified Result:** Output renders valid `Namespace`, `ConfigMap`, `Service`, and `Deployment` definitions.

---

## 5. Deployment Strategies

### 5.1 Rolling Updates (Default Strategy)
Configured inside `k8s/deployment.yaml`:
```yaml
strategy:
  type: RollingUpdate
  rollingUpdate:
    maxSurge: 1
    maxUnavailable: 0
```
- **Zero Downtime:** `maxUnavailable: 0` ensures existing pods continue serving traffic until new pods pass their HTTP readiness probes on `/health`.

### 5.2 Blue-Green Deployment Strategy
Located under `k8s/blue-green/`:
- **Blue Deployment:** Stable live environment (`version: blue`).
- **Green Deployment:** Candidate release (`version: green`).
- **Preview Service:** Points to candidate for integration testing.
- **Production Service:** Routes public traffic to active color.

**Switching Traffic Instantly:**
```powershell
# Switch traffic to green
.\k8s\blue-green\switch-traffic.ps1 -TargetVersion green

# Roll back instantly to blue
.\k8s\blue-green\switch-traffic.ps1 -TargetVersion blue
```

---

## 6. How to Demonstrate to Your Lecturer

Follow this sequence during your presentation:

1. **Explain the 10-Stage Pipeline Architecture:**
   - Open [`docs/architecture.md`](docs/architecture.md) and show the Mermaid diagram and mapping table.
2. **Demonstrate Automated Testing & Code Quality (Stages 2 & 3):**
   - Run `python -m pytest -v` in the terminal to show all tests passing.
   - Show `sonar-project.properties` and the Trivy container scanning output.
3. **Show Containerization & Security Best Practices (Stage 4):**
   - Open [`Dockerfile`](Dockerfile) and explain the multi-stage build, unprivileged non-root user (`appuser:1000`), and native Docker `HEALTHCHECK`.
4. **Show Kubernetes & GitOps Configuration (Stages 5, 6 & 7):**
   - Open [`k8s/deployment.yaml`](k8s/deployment.yaml) and [`k8s/argocd/application.yaml`](k8s/argocd/application.yaml).
   - Explain how Argo CD detects commits to Git and reconciles them onto Amazon EKS.
5. **Demonstrate Deployment Strategies & Rollback (Stages 8 & 10):**
   - Open [`docs/rollback-runbook.md`](docs/rollback-runbook.md).
   - Demonstrate `.\k8s\blue-green\switch-traffic.ps1` to showcase controlled, zero-downtime traffic switching.
6. **Show Full-Stack Observability (Stage 9):**
   - Open [`monitoring/grafana/dashboard-cicd.json`](monitoring/grafana/dashboard-cicd.json) and [`monitoring/prometheus/alert-rules.yaml`](monitoring/prometheus/alert-rules.yaml).
