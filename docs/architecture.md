# System Architecture & 10-Stage Production CI/CD Pipeline

**Course:** Master's Degree in Cloud Computing  
**Author:** Chamroeun Saran (GitHub: [Chamroeun12](https://github.com/Chamroeun12))  
**Target Environment:** Amazon Web Services (EKS & ECR) with Argo CD GitOps  

---

## 1. End-to-End Architectural Flow Diagram

The following Mermaid diagram visualizes the complete **10-Stage Production CI/CD Flow**, mapping the developer commit on the left to live reconciliation on Amazon EKS on the right:

```mermaid
flowchart TD
    subgraph STAGE1 ["Stage 1: Code"]
        A[Developer Commit & Push] --> B[GitHub Repository Chamroeun12/Assignment]
    end

    subgraph STAGE2 ["Stage 2: Build & Test"]
        B --> C[CI Engine: GitHub Actions / Jenkins]
        C --> D[Run Flake8 PEP8 Linter]
        C --> E[Run Pytest Automated Unit Suite]
        D --> F{Tests Passed?}
        E --> F
    end

    subgraph STAGE3 ["Stage 3: Security & Quality"]
        F -- Yes --> G[SonarQube Code Quality Analysis]
        F -- Yes --> H[Trivy Vulnerability Scan: Container & K8s]
        G --> I{Security Gate OK?}
        H --> I
    end

    subgraph STAGE4 ["Stage 4: Container Registry"]
        I -- Yes --> J[Build Multi-Stage Docker Image]
        J --> K[Tag with Git SHA & Semantic Version]
        K --> L[Authenticate & Push to Amazon ECR]
    end

    subgraph STAGE5 ["Stage 5: GitOps Manifest"]
        L --> M[Update k8s/deployment.yaml with new SHA]
        M --> N[Commit & Push [skip ci] to GitHub]
    end

    subgraph STAGE6 ["Stage 6: Argo CD Sync"]
        N --> O[Argo CD Application Controller]
        O --> P[Detect GitOps Desired State Change]
        P --> Q[Reconcile with Amazon EKS Cluster]
    end

    subgraph STAGE7_8 ["Stage 7 & 8: EKS Deployment"]
        Q --> R[Amazon EKS Namespace: cicd-production]
        R --> S[Deployment Strategy: Rolling Update / Blue-Green]
        S --> T[Health Probes Validate /health API]
        T --> U[New Pods Enter Ready State]
    end

    subgraph STAGE9 ["Stage 9: Observability"]
        U --> V[Prometheus ServiceMonitor Scrapes Pods]
        U --> W[Grafana Visualizes CPU, Mem & Restarts]
        U --> X[AWS CloudWatch Container Insights Logs]
    end

    subgraph STAGE10 ["Stage 10: Safe Rollback"]
        U -. Incident Detected .-> Y[Git-Authoritative Revert]
        Y -. Sync .-> O
        U -. Emergency .-> Z[kubectl rollout undo Hotfix]
    end

    F -- No --> FAIL[Pipeline Halts & Alerts Developer]
    I -- Critical CVE --> FAIL
```

---

## 2. Comprehensive 10-Stage Technical Breakdown

### Stage 1: Commit & Push Code (Git)
- **Role:** Secure source code version control.
- **Implementation:** Developers push code to feature branches or open pull requests to `main`.
- **Branch Strategy:** Trunk-based development with feature branches (`feature/*`) protected by pull request reviews and status checks.
- **Protection:** `.gitignore` excludes all local credentials (`.aws/`, `*.pem`, `*.key`, `.env`, terraform states).

### Stage 2: Build & Test (GitHub Actions / Jenkins)
- **Role:** Automated continuous integration gatekeeper.
- **Implementation:** GitHub Actions workflow `.github/workflows/ci-cd.yml` (and enterprise `Jenkinsfile`).
- **Tests Executed:**
  - `flake8`: Strict PEP8 formatting and syntax checks.
  - `pytest`: Automated test suite covering `/` template rendering, `/health` JSON structure, status checks, and 404 handlers.
  - Test coverage generated as `coverage.xml`.

### Stage 3: Code Quality & Security Scan (SonarQube & Trivy)
- **Role:** Static Application Security Testing (SAST) and Container Vulnerability Scanning.
- **Implementation:**
  - `sonar-project.properties`: Configures SonarQube scanner for Python code quality, duplication, and coverage.
  - `aquasecurity/trivy`: Scans the built container image for CVEs (focusing on `CRITICAL` and `HIGH` severity) across OS and Python packages.

### Stage 4: Build & Push Docker Image (Amazon ECR)
- **Role:** Private, secure artifact storage.
- **Implementation:**
  - Lightweight multi-stage Docker build (`Dockerfile`) running as unprivileged user `appuser:1000`.
  - Immutable image tagging: `${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com/cicd-assignment:${GIT_COMMIT_SHA}` plus `:latest`.
  - Authentication via IAM OIDC federation (`aws-actions/configure-aws-credentials`).

### Stage 5: Update Kubernetes Configuration (GitOps Manifest)
- **Role:** Declarative desired state management.
- **Implementation:**
  - The CI workflow updates `k8s/deployment.yaml` with the new immutable ECR image tag.
  - Commits changes using `[skip ci]` in the commit message to prevent an infinite CI trigger loop.

### Stage 6: Sync with Amazon EKS (Argo CD)
- **Role:** GitOps pull-based continuous delivery operator.
- **Implementation:**
  - Argo CD Application (`k8s/argocd/application.yaml`) continuously monitors `k8s/` in the GitHub repository.
  - Compares the desired state in Git against the live cluster state on Amazon EKS.
  - Automatically reconciles differences (`selfHeal: true`, `prune: true`).

### Stage 7: Deploy to Pods (Kubernetes EKS)
- **Role:** Container orchestration runtime.
- **Implementation:**
  - Deploys 2 replicas in namespace `cicd-production`.
  - Enforces `runAsNonRoot: true` security context.
  - Configures CPU and memory requests (`100m`, `128Mi`) and limits (`250m`, `256Mi`).
  - Liveness and readiness HTTP probes on `/health`.

### Stage 8: Deployment Strategy (Rolling Update & Blue-Green)
- **Role:** Zero-downtime application releases.
- **Implementation:**
  - **Default:** Kubernetes `RollingUpdate` with `maxSurge: 1` and `maxUnavailable: 0`, ensuring continuous availability.
  - **Blue-Green Option:** Documented manifests in `k8s/blue-green/` with active `blue` deployment and candidate `green` deployment, switched via `switch-traffic.ps1` / `switch-traffic.sh`.

### Stage 9: Monitoring & Observability (Prometheus, Grafana, CloudWatch)
- **Role:** Real-time health, metrics, and log aggregation.
- **Implementation:**
  - Prometheus Operator `ServiceMonitor` scraping pod health endpoints every 15s.
  - Grafana dashboard (`monitoring/grafana/dashboard-cicd.json`) tracking pod readiness, CPU/memory usage, and restarts.
  - CloudWatch Container Insights DaemonSet forwarding stdout/stderr container logs to CloudWatch Log Groups.

### Stage 10: Safe Rollback Procedure
- **Role:** Rapid incident mitigation without data loss.
- **Implementation:**
  - **GitOps Authoritative:** Reverting the Git commit triggers Argo CD to roll back cluster state without configuration drift conflicts.
  - **Emergency Hotfix:** Break-glass procedure pauses Argo CD auto-sync and triggers `kubectl rollout undo`.

---

## 3. Mapping of Reference Diagram to Project Files

| Stage # | Stage Name | Config / Manifest Files | Verification Tool / Command |
| :---: | :--- | :--- | :--- |
| **1** | Commit & Push | `.gitignore`, `git branch` | `git status`, `git log -n 5` |
| **2** | Build & Test | `tests/test_app.py`, `requirements-dev.txt`, `.github/workflows/ci-cd.yml` | `pytest -v --cov=app`, `flake8` |
| **3** | Quality & Security | `sonar-project.properties`, `.github/workflows/ci-cd.yml` | `docker run aquasec/trivy:latest image` |
| **4** | Build & Push Docker | `Dockerfile`, `.dockerignore`, `.github/workflows/ci-cd.yml` | `docker build`, `aws ecr describe-images` |
| **5** | Update K8s Manifest | `k8s/kustomization.yaml`, `k8s/deployment.yaml` | `git diff k8s/deployment.yaml` |
| **6** | Sync with EKS | `k8s/argocd/application.yaml` | `argocd app get cicd-assignment` |
| **7** | Deploy to Pods | `k8s/namespace.yaml`, `k8s/deployment.yaml`, `k8s/service.yaml` | `kubectl get pods -n cicd-production` |
| **8** | Deployment Strategy | `k8s/deployment.yaml`, `k8s/blue-green/` | `kubectl rollout status`, `switch-traffic.ps1` |
| **9** | Monitoring | `monitoring/prometheus/`, `monitoring/grafana/`, `monitoring/cloudwatch/` | Prometheus targets, Grafana dashboard, CloudWatch logs |
| **10** | Safe Rollback | `docs/rollback-runbook.md`, `k8s/blue-green/switch-traffic.ps1` | `git revert`, `kubectl rollout undo` |
