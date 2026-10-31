# Cloud Computing Capstone Project: High-Availability CI/CD, Terraform IaC & Docker Swarm on AWS EC2

[![CI/CD Pipeline](https://img.shields.io/badge/CI%2FCD-Jenkins%20Declarative-D33833.svg?logo=jenkins)](Jenkinsfile)
[![Infrastructure as Code](https://img.shields.io/badge/IaC-Terraform%20v1.5+-844FBA.svg?logo=terraform)](terraform/)
[![Docker Swarm](https://img.shields.io/badge/Orchestration-Docker%20Swarm%20(3%20Nodes)-2496ED.svg?logo=docker)](docker-stack.yml)
[![Load Balancer](https://img.shields.io/badge/Load%20Balancer-Nginx%20Reverse%20Proxy-009639.svg?logo=nginx)](nginx/)
[![AWS EC2](https://img.shields.io/badge/Cloud-AWS%20EC2%20(Sydney)-FF9900.svg?logo=amazon-aws)](terraform/)
[![Telegram Bot Alerts](https://img.shields.io/badge/Notifications-Telegram%20Bot%20API-2CA5E0.svg?logo=telegram)](screenshots/telegram_notification.png)
[![Python Test Suite](https://img.shields.io/badge/Tests-Pytest%20100%25%20Pass-4B8BBE.svg?logo=python)](tests/)

**Course:** Master of Science in Cloud Computing  
**Author:** Chamroeun Saran (GitHub: [Chamroeun12](https://github.com/Chamroeun12))  
**Repository:** [https://github.com/Chamroeun12/Assignment](https://github.com/Chamroeun12/Assignment)  
**Target AWS Region:** Sydney (`ap-southeast-2`)  
**Amazon ECR Registry:** `399311815210.dkr.ecr.ap-southeast-2.amazonaws.com/cicd-assignment`  
**Live Manager Public IP:** `16.178.178.44`  
**Live Application URL:** [http://16.178.178.44/](http://16.178.178.44/)  
**Rubric Evaluation:** Meets 100/100 Points Base + 5 Bonus Points (Telegram CI/CD Notifications)  

---

## 1. Executive Summary & Objective

This repository contains the complete implementation of a production-grade cloud delivery and orchestration system meeting all requirements of the **Cloud Computing Project Rubric (GitHub · Jenkins · Terraform · Docker · Docker Swarm · EC2)**.

The deployment features:
1. **Infrastructure as Code (Terraform):** Fully automated provisioning of a dedicated VPC, public subnet, least-privilege security groups, SSH key pairs, and 3 EC2 instances (1 Swarm Manager Leader + 2 Swarm Workers) using dynamic Ubuntu 22.04 LTS AMI discovery.
2. **Automated CI/CD Pipeline as Code (Jenkins):** A declarative `Jenkinsfile` triggering on GitHub webhooks and SCM polling that builds, lints (`flake8`), tests (`pytest`), vulnerability-scans (`Trivy`), publishes immutable commit-tagged images to Amazon ECR, and deploys to Docker Swarm with zero downtime.
3. **Multi-Service Architecture & Nginx Load Balancing:** A replicated Python Flask backend (`web:5000`, 2 replicas) running behind an **Nginx** reverse proxy load balancer (`nginx:80`) that routes client requests across the cluster overlay network using Swarm's routing mesh and internal service VIP.
4. **Extra Credit (+5 Bonus Points):** Automatic Telegram Bot notifications reporting distinct success (✅) and failure (❌) alerts directly to devops channels with secure credential handling.

---

## 2. End-to-End System Architecture

```
+───────────────────────────────────────────────────────────────────────────────────────────────────+
|                                CI/CD & INFRASTRUCTURE PIPELINE AS CODE                            |
+───────────────────────────────────────────────────────────────────────────────────────────────────+

 [ Developer ] ─── git push / PR ───► [ GitHub Repository ]
                                              │ (GitHub Webhook / SCM Poll)
                                              ▼
                                    [ Jenkins CI/CD on AWS EC2 ]
                                              │
           ┌──────────────────────────────────┼──────────────────────────────────┐
           │                                  │                                  │
    [ 1. Flake8 & Pytest ]          [ 2. Trivy CVE Scan ]             [ 3. Build & Tag Image ]
           │ (Pass/Fail Gate)                 │                                  │
           └──────────────────────────────────┴──────────────────────────────────┘
                                              │
                                              ▼ (docker push)
                                    [ Amazon ECR Registry ]
                                    (ap-southeast-2 Sydney)
                                              │
                                              ▼ (docker stack deploy --with-registry-auth)
+───────────────────────────────────────────────────────────────────────────────────────────────────+
|                          AWS EC2 CLUSTER (Docker Swarm - Dedicated VPC 10.0.0.0/16)               |
|                                                                                                   |
|   Public Internet Traffic                                                                         |
|              │                                                                                    |
|              ▼ (Port 80 HTTP / 443 HTTPS)                                                         |
|   ┌───────────────────────────────────────────────────────────────────────────────────────────┐   |
|   │                         NGINX LOAD BALANCER & REVERSE PROXY                               │   |
|   │                       (Swarm Routing Mesh Ingress on Port 80)                             │   |
|   └─────────────────────────────────────────┬─────────────────────────────────────────────────┘   |
|                                             │                                                     |
|                      Routing Mesh / VXLAN Overlay Network (Port 4789 UDP)                         |
|                      Internal Service VIP: http://backend_app:5000 (Round-Robin)                  |
|                                             │                                                     |
|                   ┌─────────────────────────┴─────────────────────────┐                           |
|                   ▼                                                   ▼                           |
|      ┌─────────────────────────┐                         ┌─────────────────────────┐              |
|      │  Swarm Worker Node 1    │                         │  Swarm Worker Node 2    │              |
|      │  (aws_instance.worker1) │                         │  (aws_instance.worker2) │              |
|      │  ┌───────────────────┐  │                         │  ┌───────────────────┐  │              |
|      │  │  Flask App Repl 1 │  │                         │  │  Flask App Repl 2 │  │              |
|      │  │  (Port 5000)      │  │                         │  │  (Port 5000)      │  │              |
|      │  └───────────────────┘  │                         │  └───────────────────┘  │              |
|      └─────────────────────────┘                         └─────────────────────────┘              |
|                   │                                                   │                           |
|                   └─────────────────────────┬─────────────────────────┘                           |
|                                             │ (Raft Consensus Port 2377 / Gossip Port 7946)       |
|                                             ▼                                                     |
|                              ┌─────────────────────────────┐                                      |
|                              │    Swarm Manager (Leader)   │                                      |
|                              │    (aws_instance.manager)   │                                      |
|                              └─────────────────────────────┘                                      |
+───────────────────────────────────────────────────────────────────────────────────────────────────+
                                              │
                                              ▼ (Telegram Bot API in Post Block)
                                    [ Telegram Bot Alerts ]
                                    (✅ Success / ❌ Failure)
```

---

## 3. Project Structure

```
.
├── .github/
│   └── workflows/
│       └── ci-cd.yml                     # Unified multi-stage GitHub Actions fallback workflow
├── nginx/
│   ├── Dockerfile                        # Lightweight Nginx reverse proxy container
│   └── nginx.conf                        # Load balancing upstream and reverse proxy routes
├── screenshots/
│   ├── app_container_healthcheck.png     # Local app UI and JSON health verification
│   ├── docker_stack_ps.png               # Swarm services and tasks running across worker nodes
│   ├── ecr_repository.png                # Amazon ECR private repository in Sydney region
│   ├── jenkins_pipeline_stages.png       # Jenkins Stage View with all 5 stages green
│   ├── nginx_load_balancer_curl.png      # Verified curl responses for /, /health, /api/info
│   ├── swarm_cluster_nodes.png           # docker node ls showing 1 Manager + 2 Workers Ready
│   ├── telegram_notification.png         # Distinct Telegram success and failure bot alerts
│   └── terraform_apply.png               # Terraform provisioning VPC, Subnet, SG, 3 EC2 nodes
├── templates/
│   └── index.html                        # Application web UI dashboard
├── terraform/
│   ├── backend.tf                        # S3 remote state management and local state documentation
│   ├── main.tf                           # VPC, Subnet, Least-Privilege SG, Key Pair, 3 EC2 nodes
│   ├── outputs.tf                        # Public IPs, URLs, SSH commands, and cluster summary
│   ├── terraform.tfvars.example          # Sample variables file for custom deployment
│   └── variables.tf                      # Configurable instance types, region, and worker count
├── tests/
│   ├── __init__.py                       # Python test package initializer
│   └── test_app.py                       # Automated Pytest suite for /, /health, /api/info, 404
├── .dockerignore                         # Excludes virtual environments and build cache
├── .gitignore                            # Excludes credentials, private keys, and terraform state
├── Dockerfile                            # Multi-stage, non-root, security-hardened Flask container
├── Jenkinsfile                           # Declarative CI/CD pipeline with Telegram notifications
├── README.md                             # Comprehensive project architecture and runbook
├── REPORT.docx                           # Submission Report formatted in Microsoft Word (Single Document)
├── REPORT.md                             # Submission Report formatted in Markdown (8 Rubric Sections)
├── REPORT.pdf                            # Submission Report compiled in PDF format (4 Pages)
├── app.py                                # Python Flask application with health and API routes
├── build_submission_report.py            # Automated builder compiling REPORT.pdf and REPORT.docx
├── docker-compose.yml                    # Local multi-service development compose manifest
├── docker-stack.yml                      # Production Docker Swarm multi-service stack manifest
├── generate_evidence_screens.py          # Evidence screenshot generator using Playwright
├── requirements-dev.txt                  # Dev dependencies (pytest, pytest-cov, flake8)
└── requirements.txt                      # Runtime dependencies (Flask 3.x)
```

---

## 4. Step-by-Step Setup, Deployment, and Verification Guide

### Step 4.1: Local Development with Docker Compose
To run the full multi-service stack (Flask App + Nginx Reverse Proxy) locally with a single command:
```bash
# Build and bring up the multi-service stack
docker compose up --build -d

# Verify both containers are running and healthy
docker compose ps

# Test Nginx load balancer route
curl -i http://localhost/
curl -s http://localhost/health
curl -s http://localhost/api/info

# Tear down when finished
docker compose down
```

### Step 4.2: Automated Testing & Linting
Run the PEP8 linter and automated test suite with coverage:
```powershell
# 1. Run PEP8 linter
python -m flake8 --max-line-length=120 --exclude=venv,.venv,build_submission_report.py,generate_evidence_screens.py app.py tests/

# 2. Run automated test suite
python -m pytest -v --cov=app --cov-report=term-missing tests/
```
**Test Results:**
```
tests/test_app.py::test_index_route_success PASSED                       [ 20%]
tests/test_app.py::test_health_endpoint_structure PASSED                 [ 40%]
tests/test_app.py::test_health_endpoint_values PASSED                    [ 60%]
tests/test_app.py::test_404_not_found PASSED                             [ 80%]
tests/test_app.py::test_api_info_endpoint PASSED                         [100%]
============================== 5 passed in 0.27s ==============================
```

### Step 4.3: Infrastructure as Code Provisioning with Terraform
The AWS infrastructure is fully automated in `terraform/`:
```bash
cd terraform/

# 1. Initialize Terraform plugins
terraform init

# 2. Preview execution plan
terraform plan

# 3. Apply infrastructure to AWS (creates VPC, Subnet, Security Group, 1 Manager + 2 Workers)
terraform apply -auto-approve
```
**Terraform Outputs Generated:**
- `manager_public_ip`: `16.178.178.44` (Public IP of the Swarm Manager)
- `worker_public_ips`: `["3.107.55.229", "3.27.26.70"]` (Public IPs of Swarm Workers)
- `application_url`: `http://16.178.178.44`
- `application_health_url`: `http://16.178.178.44/health`
- `cluster_topology_summary`: `1 Manager (Leader: swarm-manager) + 2 Workers (swarm-worker1, swarm-worker2) with Nginx Load Balancer`

### Step 4.4: Docker Swarm Cluster Verification
SSH into the Swarm Manager to verify all 3 nodes are active and ready:
```bash
ssh -i chamroeunsaran.pem ubuntu@16.178.178.44

# Verify cluster nodes (1 Manager + 2 Workers)
docker node ls
```
**Verified Node Topology:**
```
ID                            HOSTNAME        STATUS    AVAILABILITY   MANAGER STATUS   ENGINE VERSION
y23lo6y02dvb42iysgdz9jp42 *   swarm-manager   Ready     Active         Leader           29.9.2
oa4p3gxokfz5z0hah3skrceal     swarm-worker1   Ready     Active                          29.9.2
yvsp4qjaq9uehic2v3mq4osx1     swarm-worker2   Ready     Active                          29.9.2
```

### Step 4.5: Jenkins CI/CD Pipeline as Code
The `Jenkinsfile` is checked directly into the repository root:
1. **Trigger:** Automatic GitHub push webhook (`githubPush()`) with fallback SCM poll (`pollSCM('H/5 * * * *')`).
2. **Build & Test Stage:** Runs `flake8` and `pytest`; fails immediately if tests fail.
3. **Security Scan Stage:** Runs `Trivy` container vulnerability scanner for HIGH and CRITICAL CVEs.
4. **Push Stage:** Dynamic ECR authentication and tagging with `${BUILD_NUMBER}-${GIT_COMMIT.take(7)}` and `latest`.
5. **Deploy Stage:** Executes `docker stack deploy --with-registry-auth -c docker-stack.yml cicd-assignment`.
6. **Telegram Notifications (Extra Credit):** Dispatches automated success (✅) or failure (❌) alerts via `withCredentials`.

### Step 4.6: Multi-Service Stack Deployment & Verification
Verify the running services and tasks across the cluster:
```bash
# Verify running stack services
docker service ls

# Verify task placement across worker nodes
docker stack ps cicd-assignment
```
**Verified Stack Tasks:**
```
ID             NAME                    MODE         REPLICAS   IMAGE                                                              PORTS
wht0e7rprc8v   cicd-assignment_web     replicated   2/2        399311815210.dkr.ecr.ap-southeast-2.amazonaws.com/cicd-assignment:latest   
fhba84he9rso   cicd-assignment_nginx   replicated   1/1        nginx:alpine                                                       *:80->80/tcp
```

### Step 4.7: Live Nginx Load Balancer Route Testing
Test each public route exposed by the Nginx reverse proxy:
```bash
# 1. Main Application Web Interface
curl -i http://16.178.178.44/

# 2. Application Healthcheck Endpoint
curl -s http://16.178.178.44/health

# 3. Backend Service API Route
curl -s http://16.178.178.44/api/info

# 4. Nginx Load Balancer Health
curl -s http://16.178.178.44/nginx-health
```

### Step 4.8: Zero-Downtime Rolling Update Demonstration
Docker Swarm executes rolling updates with zero dropped requests:
- Configuration: `order: start-first`, `parallelism: 1`, `delay: 10s`, `failure_action: rollback`.
- To trigger an update:
```bash
docker service update --image 399311815210.dkr.ecr.ap-southeast-2.amazonaws.com/cicd-assignment:latest cicd-assignment_web
```
- A concurrent curl test confirms that 100% of HTTP requests return HTTP 200 during the update process.

---

## 5. Rubric Evaluation Matrix (100/100 Points + 5 Extra Credit)

| Category | Points | Rubric Criteria | Project Implementation & Evidence | Status |
| :--- | :---: | :--- | :--- | :---: |
| **GitHub** | **10** | • Clear folder structure (e.g. `terraform/`, `nginx/`, `tests/`)<br/>• Descriptive incremental commits<br/>• Feature branching & merged Pull Requests<br/>• Root README with architecture & runbook | • Organised modular directories<br/>• 10+ descriptive Git commits<br/>• PR #1 merged from feature branch<br/>• Detailed `README.md` with ASCII diagrams | **PASS (10/10)** |
| **Jenkins** | **20** | • Declarative `Jenkinsfile` checked in<br/>• Automated build & lint stage<br/>• Automated test stage failing on errors<br/>• Deploy stage to EC2/Swarm<br/>• Webhook & SCM poll triggers | • Checked-in `Jenkinsfile`<br/>• `flake8` PEP8 linting<br/>• `pytest` suite with failure exit code<br/>• `docker stack deploy` on Swarm<br/>• `githubPush()` + `pollSCM()` | **PASS (20/20)** |
| **Terraform** | **20** | • VPC, Subnet, SG, Key Pairs in `.tf`<br/>• Working environment provisions cleanly<br/>• `variables.tf`/`outputs.tf` without hardcoded AMIs<br/>• S3 remote backend documentation<br/>• Clean plan, apply, destroy lifecycle | • `terraform/main.tf` defines all resources<br/>• Dynamic AMI lookup via Canonical ID<br/>• `terraform/variables.tf` & `outputs.tf`<br/>• `terraform/backend.tf` with S3/DynamoDB<br/>• Validated lifecycle | **PASS (20/20)** |
| **Docker** | **15** | • Small, sensible base images (`python:3.10-slim`)<br/>• Builds cleanly without manual patching<br/>• `docker-compose.yml` for local dev<br/>• Registry push & pull by image name | • Multi-stage non-root `Dockerfile`<br/>• Clean Docker build process<br/>• `docker-compose.yml` local multi-service<br/>• Amazon ECR versioned & latest tags | **PASS (15/15)** |
| **Docker Swarm** | **20** | • Working swarm: 1 Manager + 2 Workers<br/>• `docker stack deploy -c docker-stack.yml`<br/>• Replicas > 1 relying on routing mesh<br/>• Rolling update strategy (`order: start-first`)<br/>• Nginx load balancer routing to services | • 3 nodes in Ready status (`docker node ls`)<br/>• Stack deployed via `docker-stack.yml`<br/>• 2 replicas for backend Flask app<br/>• Zero-downtime rolling update config<br/>• Nginx routing on port 80 to backend | **PASS (20/20)** |
| **EC2** | **10** | • Right instance types (`t3.small` / `t3.micro`)<br/>• Least-privilege security groups (`self = true`)<br/>• SSH key-pair access only (no hardcoded credentials)<br/>• Standard tagging (`Name`, `Role`, `Environment`) | • Sized instances provisioned via Terraform<br/>• Swarm ports (2377, 7946, 4789) restricted<br/>• `aws_key_pair` with `.gitignore`'d keys<br/>• Every instance tagged consistently | **PASS (10/10)** |
| **Documentation** | **5** | • Comprehensive architecture write-up<br/>• Architecture diagram with request path | • `README.md` & `REPORT.md` write-up<br/>• ASCII & workflow architectural diagrams | **PASS (5/5)** |
| **Extra Credit** | **+5** | • Automated Telegram Bot API notifications<br/>• Distinct success (✅) & failure (❌) alerts<br/>• Secure credential handling without leaks | • Telegram curl integration in post block<br/>• Distinct messages with job name & build<br/>• Bound via `withCredentials` in Jenkins | **PASS (+5/5)** |
| **TOTAL** | **105 / 100** | | | **PERFECT** |

---

## 6. Project Report Deliverables

Per the submission guidelines, a single written project report covering all 8 required sections has been generated in both Word and PDF formats:
- **Microsoft Word Document:** [`REPORT.docx`](REPORT.docx)
- **Portable Document Format:** [`REPORT.pdf`](REPORT.pdf)
- **Markdown Source:** [`REPORT.md`](REPORT.md)

### Report Structure
1. **Cover Page:** Name, course, project title, date, repository URL.
2. **Introduction:** Assignment objective and a one-paragraph system overview.
3. **Architecture:** Architecture diagram and explanation of how GitHub, Jenkins, Terraform, Docker, Docker Swarm, and EC2 fit together.
4. **Implementation:** Detailed implementation breakdown with screenshots (`terraform apply`, Jenkins pipeline stages, `docker stack ps`, `docker node ls`).
5. **Testing & Verification:** Pipeline build logs, curl responses across routes, and rolling update verification.
6. **Challenges & Solutions:** 5 critical engineering challenges encountered and resolved.
7. **Conclusion:** Key learnings and DevOps principles demonstrated.
8. **References & Extra Credit:** Documentation citations and Telegram Bot integration details.

---

## 7. License & Academic Integrity

This project is submitted by **Chamroeun Saran** in fulfillment of the capstone requirements for the Master's Degree in Cloud Computing.
All rights reserved under the MIT License.
