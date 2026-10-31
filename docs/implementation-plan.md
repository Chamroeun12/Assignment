# Implementation Plan: Production-Grade CI/CD Pipeline on Amazon EKS with GitOps (Argo CD)

**Course:** Master's Degree in Cloud Computing  
**Author:** Chamroeun Saran (GitHub: [Chamroeun12](https://github.com/Chamroeun12))  
**Project:** CI/CD Assignment & Assignment — Commit to Production  
**Date:** October 26, 2026  
**Status:** PHASE 0 COMPLETED — PROCEEDING TO IMPLEMENTATION  

---

## 1. Executive Summary & Objective

The objective of this assignment is to design, implement, document, and verify an end-to-end, production-grade CI/CD pipeline following the **10-step reference architecture diagram**:

```
[1. Commit & Push Code (Git)] 
       │
       ▼
[2. Build & Test (GitHub Actions / Jenkins)] 
       │
       ▼
[3. Code Quality & Security Scan (SonarQube & Trivy)] 
       │
       ▼
[4. Build & Push Docker Image (Amazon ECR)] 
       │
       ▼
[5. Update Kubernetes Configuration (GitOps Manifests)] 
       │
       ▼
[6. Sync with EKS (Argo CD)] 
       │
       ▼
[7. Deploy to Pods (Kubernetes EKS)] 
       │
       ▼
[8. Deployment Strategy (Rolling Update & Blue-Green)] 
       │
       ▼
[9. Monitoring (CloudWatch, Prometheus, Grafana, ALB, Logs)] 
       │
       ▼
[10. Rollback if Needed (Production EKS Reconciliation)]
```

---

## 2. Environment & Resource Baseline (Phase 0 Audit)

### 2.1 Local Environment
- **Operating System:** Windows 10/11
- **Development Tooling:** VS Code / Antigravity IDE
- **Git Version:** `2.52.0.windows.1`
- **Docker Engine:** Docker Desktop 4.90.0 (API v1.55, Linux container engine running)
- **Runtime & Language:** Python 3.10.0, Flask 3.1.3
- **Kubernetes CLI (`kubectl`):** Installed via Docker Desktop (`v1.32.1`)
- **AWS CLI:** `aws-cli/1.46.2` installed; no local credentials stored in `~/.aws/` (preventing accidental credential leaks).
- **Package Managers:** Winget, Pip, Npm

### 2.2 AWS Infrastructure Discovery
- **AWS Account ID (from prior assignment):** `399311815210`
- **Target AWS Region:** `ap-southeast-2` (Sydney)
- **Container Registry (ECR):** `399311815210.dkr.ecr.ap-southeast-2.amazonaws.com/cicd-assignment`
- **EC2 Instance:** User confirmed an EC2 instance is running; previous dynamic IP entries timed out over SSH port 22 (pending security group or fresh IP verification).
- **Target Kubernetes Cluster:** Amazon EKS. Per grading rules and financial safety guidelines, billable EKS clusters, NAT gateways, and Application Load Balancers will NOT be auto-created without explicit approval. Comprehensive, validated, and executable Terraform / manifests are provided.

---

## 3. Mapping of the 10 Pipeline Stages

| Stage # | Stage Name | Target Tooling | Implementation Artifacts | Verification Criteria |
| :---: | :--- | :--- | :--- | :--- |
| **1** | **Commit & Push Code** | Git & GitHub | Feature branch `feature/eks-argocd-cicd`, `.gitignore` | Commits pushed to remote with clear messages; clean tree. |
| **2** | **Build & Test** | GitHub Actions / Pytest | `tests/test_app.py`, `.github/workflows/ci.yml` | Unit tests execute and pass; dependencies verified. |
| **3** | **Code Quality & Security** | SonarQube & Trivy | `sonar-project.properties`, Trivy scan step | Static code analysis configured; container vulnerability report generated. |
| **4** | **Build & Push Docker Image** | Docker & Amazon ECR | Multi-stage `Dockerfile`, ECR push workflow | Multi-arch Docker image tagged with commit SHA and pushed to ECR. |
| **5** | **Update K8s Configuration** | GitOps Manifests | `k8s/deployment.yaml`, `k8s/kustomization.yaml` | Image tag updated in GitOps manifest automatically without loop. |
| **6** | **Sync with EKS** | Argo CD | `k8s/argocd/application.yaml` | Argo CD detects repository commit and reconciles cluster state. |
| **7** | **Deploy to Pods** | Kubernetes (EKS) | `k8s/service.yaml`, probes, resource limits | Pods transition to `Running` and `Ready` state; health checks pass. |
| **8** | **Deployment Strategy** | Rolling & Blue-Green | `k8s/deployment.yaml`, `k8s/blue-green/` | Zero-downtime rolling update verified; Blue-Green switch script provided. |
| **9** | **Monitoring & Logging** | Prometheus, Grafana, CloudWatch | `monitoring/`, metrics endpoints, dashboards | Pod metrics, health endpoints, logs routed to stdout, alerts specified. |
| **10** | **Rollback if Needed** | GitOps Revert / K8s Undo | `docs/rollback-runbook.md`, rollback scripts | Controlled Git revert triggers Argo CD roll back to previous healthy SHA. |

---

## 4. Implementation Phasing & Sequence

1. **Phase 1: Git & Repository Organization**
   - Create and checkout feature branch `feature/eks-argocd-cicd`.
   - Update `.gitignore` to protect all credentials, `.env`, reports, and test caches.
   - Update `README.md` with prerequisites and workflow instructions.

2. **Phase 2: Dockerfile & Container Optimization**
   - Enhance `Dockerfile` for multi-stage production caching and non-root user execution (`appuser:1000`).
   - Add container health check instruction and environment variable flexibility.
   - Build and verify the container locally using Docker Desktop.

3. **Phase 3: Automated Testing & Continuous Integration**
   - Create comprehensive unit and API integration tests in `tests/test_app.py` for `/` and `/health`.
   - Add test runner requirements (`pytest`, `pytest-cov`, `flake8`).
   - Create `.github/workflows/ci.yml` with automated test and lint execution.

4. **Phase 4: Code Quality & Vulnerability Scanning**
   - Add `sonar-project.properties` with clear exclusion and coverage paths.
   - Add Trivy container image scanning in GitHub Actions to detect CVEs.
   - Document vulnerability thresholds (FAIL on CRITICAL, WARN on HIGH).

5. **Phase 5: Amazon ECR Image Registry Integration**
   - Configure workflow to authenticate to Amazon ECR securely using GitHub OIDC / secrets.
   - Tag images immutably with `${{ github.sha }}` and semantic versioning.

6. **Phase 6: Kubernetes Manifests & GitOps Repository Structure**
   - Create structured `k8s/` directory:
     - `namespace.yaml` (`cicd-production`)
     - `deployment.yaml` (probes, security context, resource requests/limits, rolling update strategy)
     - `service.yaml` (ClusterIP / LoadBalancer)
     - `kustomization.yaml` (for programmatic GitOps image tagging)
     - `argocd/application.yaml` (Argo CD Application Custom Resource)

7. **Phase 7: Amazon EKS & Argo CD Integration**
   - Provide complete, verified Terraform configuration (`terraform/`) for provisioning EKS safely if approved.
   - Provide Argo CD installation and sync manifests.

8. **Phase 8: Deployment Strategies (Rolling & Blue-Green)**
   - Configure `maxSurge: 1`, `maxUnavailable: 0` for zero-downtime rolling updates.
   - Create `k8s/blue-green/` manifests with blue/green Services and traffic switching script.

9. **Phase 9: Monitoring, Logging, and Observability**
   - Configure Prometheus ServiceMonitor and Grafana dashboard definitions.
   - Configure CloudWatch Container Insights logging guidance.

10. **Phase 10: Rollback Runbook & Safety**
    - Authoritative GitOps rollback procedure (reverting git commit).
    - Emergency fallback (`kubectl rollout undo`).

11. **Phase 11: Final Integration Test & Verification**
    - Execute local container tests, lint tests, and manifest dry-run validations.
    - Run docker build and test suite.

12. **Phase 12: Documentation & Lecturer Presentation Deliverables**
    - Architecture guide (`docs/architecture.md`).
    - Deployment guide (`docs/deployment-guide.md`).
    - Troubleshooting guide (`docs/troubleshooting.md`).
    - Rollback runbook (`docs/rollback-runbook.md`).
    - Monitoring guide (`docs/monitoring-guide.md`).
    - Updated comprehensive `README.md`.

---

## 5. Risk Assessment & Mitigations

| Risk | Mitigation |
| :--- | :--- |
| **Unintended AWS Cloud Charges** | No billable AWS services (EKS, NAT Gateways, ALBs) will be provisioned without explicit user approval. All manifests and Terraform code are fully validated locally. |
| **Credential / Secret Leaking** | No passwords, tokens, or private keys will be committed. Secrets are managed via GitHub Actions Secrets, AWS IAM OIDC roles, and Kubernetes Secrets. |
| **CI/GitOps Infinite Loop** | GitOps updates target only manifest files (`k8s/kustomization.yaml`) with `[skip ci]` or distinct commit author/branch to prevent re-triggering CI. |
| **Container Downtime During Deploy** | Rolling update strategy guarantees `maxUnavailable: 0` with HTTP `/health` readiness probes. |
