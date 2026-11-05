# Getting Started & Runbook: High-Availability Cloud Delivery System

> Complete, step-by-step developer and operator guide for running this project locally with Docker Compose or deploying to production on AWS EC2 with Terraform and Docker Swarm.

---

## 📑 Table of Contents
1. [Project Overview](#1-project-overview)
2. [Prerequisites & System Requirements](#2-prerequisites--system-requirements)
3. [Option A: Quick Start — Local Testing (No AWS Required)](#3-option-a-quick-start--local-testing-no-aws-required)
4. [Option B: Full Cloud Deployment on AWS (Terraform + Docker Swarm)](#4-option-b-full-cloud-deployment-on-aws-terraform--docker-swarm)
   - [Step 4.1: Clone Repository & Configure AWS Credentials](#step-41-clone-repository--configure-aws-credentials)
   - [Step 4.2: Provision Infrastructure with Terraform](#step-42-provision-infrastructure-with-terraform)
   - [Step 4.3: Initialize Docker Swarm & Join Worker Nodes](#step-43-initialize-docker-swarm--join-worker-nodes)
   - [Step 4.4: Deploy Multi-Service Stack](#step-44-deploy-multi-service-stack)
   - [Step 4.5: Verify Live Endpoints & Load Balancing](#step-45-verify-live-endpoints--load-balancing)
5. [Option C: Automated CI/CD Pipeline (Jenkins)](#5-option-c-automated-cicd-pipeline-jenkins)
6. [Automated Test Suite & Code Quality Checks](#6-automated-test-suite--code-quality-checks)
7. [Resource Cleanup & Cost Management](#7-resource-cleanup--cost-management)
8. [Troubleshooting & Frequently Asked Questions (FAQ)](#8-troubleshooting--frequently-asked-questions-faq)

---

## 1. Project Overview

This repository provides an enterprise-grade cloud deployment architecture:
- **Application:** Replicated Python Flask backend with dynamic system metrics and JSON health APIs.
- **Reverse Proxy & Ingress:** Nginx container routing public traffic on Port 80 to backend replicas with round-robin load balancing.
- **Infrastructure as Code (IaC):** HashiCorp Terraform provisioning a dedicated VPC, least-privilege security groups, dynamic Ubuntu 22.04 AMI, and 3 EC2 nodes (1 Manager + 2 Workers).
- **Container Orchestration:** 3-node Docker Swarm cluster with internal routing mesh, health monitoring, and zero-downtime rolling updates.
- **CI/CD Automation:** Declarative Jenkins pipeline automating linting (`flake8`), unit tests (`pytest`), container vulnerability scans (`Trivy`), ECR publishing, and Telegram Bot notifications.

---

## 2. Prerequisites & System Requirements

Before running the project, ensure you have the following installed on your machine:

| Requirement | Local Mode | AWS Cloud Mode | Recommended Version |
| :--- | :---: | :---: | :--- |
| **Git** | ✅ Required | ✅ Required | 2.30+ |
| **Docker Engine / Desktop** | ✅ Required | Optional locally | 24.0+ |
| **Python** | Optional (for tests) | Optional | 3.10+ |
| **Terraform CLI** | ❌ Not needed | ✅ Required | 1.5.0+ |
| **AWS CLI** | ❌ Not needed | ✅ Required | 2.10+ |
| **AWS Account** | ❌ Not needed | ✅ Required | Active with EC2/VPC permissions |

---

## 3. Option A: Quick Start — Local Testing (No AWS Required)

If you only want to test the multi-service application (Flask App + Nginx Reverse Proxy) on your own laptop without deploying to AWS:

### Step 3.1: Clone the Repository
```bash
git clone https://github.com/Chamroeun12/Assignment.git
cd Assignment
```

### Step 3.2: Start Multi-Service Stack with Docker Compose
```bash
docker compose up --build -d
```

### Step 3.3: Verify Running Services
```bash
docker compose ps
```
*Expected output: Both `cicd-assignment-web` and `cicd-assignment-nginx` running and healthy.*

### Step 3.4: Test Local Endpoints
Open your browser to:
👉 **[http://localhost/](http://localhost/)**

Or test using curl in your terminal:
```bash
# Main UI Dashboard
curl -i http://localhost/

# Healthcheck
curl -s http://localhost/health

# Backend Metadata
curl -s http://localhost/api/info

# Nginx Health
curl -s http://localhost/nginx-health
```

### Step 3.5: Stop Local Containers
```bash
docker compose down
```

---

## 4. Option B: Full Cloud Deployment on AWS (Terraform + Docker Swarm)

Follow these steps to provision your own 3-node Docker Swarm cluster on AWS EC2 and deploy the live stack.

### Step 4.1: Clone Repository & Configure AWS Credentials
1. Clone the repository:
   ```bash
   git clone https://github.com/Chamroeun12/Assignment.git
   cd Assignment
   ```

2. Configure your AWS credentials in your terminal:
   ```bash
   aws configure
   # Enter your AWS Access Key ID
   # Enter your AWS Secret Access Key
   # Default region name: ap-southeast-2 (or your preferred region)
   # Default output format: json
   ```

3. Ensure you have an SSH Key Pair created in your AWS Region (e.g. `chamroeunsaran.pem`).

---

### Step 4.2: Provision Infrastructure with Terraform
1. Navigate into the `terraform/` directory:
   ```bash
   cd terraform
   ```

2. Initialize Terraform plugins:
   ```bash
   terraform init
   ```

3. Preview the infrastructure plan:
   ```bash
   terraform plan
   ```

4. Apply and provision the AWS infrastructure:
   ```bash
   terraform apply -auto-approve
   ```

5. **Note the Terraform Outputs:**
   Terraform will display the generated IPs:
   ```text
   Outputs:
   application_health_url = "http://<manager_public_ip>/health"
   application_url = "http://<manager_public_ip>"
   manager_private_ip = "172.31.xx.xx"
   manager_public_ip = "<manager_public_ip>"
   worker_public_ips = [
     "<worker1_public_ip>",
     "<worker2_public_ip>"
   ]
   ```
6. Return to root directory:
   ```bash
   cd ..
   ```

---

### Step 4.3: Initialize Docker Swarm & Join Worker Nodes

#### 1. SSH into the Manager Node:
```bash
ssh -i <your-key.pem> ubuntu@<manager_public_ip>
```

#### 2. Initialize Swarm on Manager:
```bash
sudo docker swarm init --advertise-addr <manager_private_ip>
```
*Docker will output a join command starting with `docker swarm join --token SWMTKN-1-... <manager_private_ip>:2377`.*

#### 3. Set Manager Hostname:
```bash
sudo hostnamectl set-hostname swarm-manager
sudo systemctl restart docker
exit
```

#### 4. Join Worker 1 to the Cluster:
```bash
ssh -i <your-key.pem> ubuntu@<worker1_public_ip>
# Run the join command copied from step 2:
sudo docker swarm join --token <TOKEN> <manager_private_ip>:2377
sudo hostnamectl set-hostname swarm-worker1
sudo systemctl restart docker
exit
```

#### 5. Join Worker 2 to the Cluster:
```bash
ssh -i <your-key.pem> ubuntu@<worker2_public_ip>
# Run the join command copied from step 2:
sudo docker swarm join --token <TOKEN> <manager_private_ip>:2377
sudo hostnamectl set-hostname swarm-worker2
sudo systemctl restart docker
exit
```

#### 6. Verify Cluster Status:
SSH back into the Manager:
```bash
ssh -i <your-key.pem> ubuntu@<manager_public_ip>
sudo docker node ls
```
*Expected output: 1 Manager (Leader) + 2 Workers, all in `Ready` and `Active` status.*

---

### Step 4.4: Deploy Multi-Service Stack

From your local machine, copy the application bundle to the Manager node:
```bash
# 1. Package the application files
tar -czf app_bundle.tar.gz Dockerfile app.py requirements.txt templates docker-stack.yml nginx

# 2. SCP bundle to Manager
scp -i <your-key.pem> app_bundle.tar.gz ubuntu@<manager_public_ip>:/home/ubuntu/

# 3. SCP bundle to Worker 1 and Worker 2 (for fast local image availability)
scp -i <your-key.pem> app_bundle.tar.gz ubuntu@<worker1_public_ip>:/home/ubuntu/
scp -i <your-key.pem> app_bundle.tar.gz ubuntu@<worker2_public_ip>:/home/ubuntu/
```

Now build the image on all 3 nodes and deploy the stack:
```bash
# On Worker 1:
ssh -i <your-key.pem> ubuntu@<worker1_public_ip> "tar -xzf app_bundle.tar.gz && sudo docker build -t 399311815210.dkr.ecr.ap-southeast-2.amazonaws.com/cicd-assignment:latest ."

# On Worker 2:
ssh -i <your-key.pem> ubuntu@<worker2_public_ip> "tar -xzf app_bundle.tar.gz && sudo docker build -t 399311815210.dkr.ecr.ap-southeast-2.amazonaws.com/cicd-assignment:latest ."

# On Manager:
ssh -i <your-key.pem> ubuntu@<manager_public_ip>
tar -xzf app_bundle.tar.gz
sudo docker build -t 399311815210.dkr.ecr.ap-southeast-2.amazonaws.com/cicd-assignment:latest .

# Deploy the Docker Swarm stack
sudo docker stack deploy -c docker-stack.yml cicd-assignment
```

Verify services and tasks:
```bash
sudo docker service ls
sudo docker stack ps cicd-assignment
```
*Expected output: `cicd-assignment_nginx` (1/1) and `cicd-assignment_web` (2/2) running.*

---

### Step 4.5: Verify Live Endpoints & Load Balancing

Open your browser to:
👉 **`http://<manager_public_ip>/`**

Test the public APIs via curl:
```bash
# 1. Healthcheck
curl -s http://<manager_public_ip>/health
# Response: {"hostname":"...","status":"healthy","version":"1.0.0"}

# 2. Backend Service Info (Notice hostname alternates between requests)
curl -s http://<manager_public_ip>/api/info
# Response: {"cluster":"docker-swarm","hostname":"...","runtime":"python-flask","service":"cicd-assignment-backend","version":"1.0.0"}

# 3. Nginx Load Balancer Health
curl -s http://<manager_public_ip>/nginx-health
# Response: {"status":"healthy","service":"nginx-load-balancer"}
```

---

## 5. Option C: Automated CI/CD Pipeline (Jenkins)

The repository includes a production-grade declarative [`Jenkinsfile`](Jenkinsfile).

### Pipeline Stages:
1. **Stage 1 (Checkout):** Clones code from GitHub repository.
2. **Stage 2 (Build & Test):** Creates Python virtual environment, executes PEP8 linting (`flake8`), and runs automated unit tests (`pytest`).
3. **Stage 3 (Security Scan):** Scans container layers for CVE vulnerabilities with `Trivy`.
4. **Stage 4 (Push to ECR):** Authenticates with Amazon ECR and publishes versioned and `latest` tags.
5. **Stage 5 (Deploy to Swarm):** Deploys stack with zero downtime using `docker stack deploy`.
6. **Post Actions:** Sends real-time Telegram Bot notifications (✅ Success / ❌ Failure).

### Restoring Pre-Configured Jenkins Locally:
If you want to run our exact Jenkins configuration with all plugins and build history:
```powershell
# 1. Ensure Docker Desktop is running
# 2. Extract the backup archive into the container:
docker run -d --name jenkins -p 8080:8080 -p 50000:50000 -v jenkins_home:/var/jenkins_home jenkins/jenkins:lts
docker cp jenkins_backup.tar.gz jenkins:/tmp/jenkins_backup.tar.gz
docker exec -u 0 jenkins tar xzf /tmp/jenkins_backup.tar.gz -C /var/jenkins_home
docker exec -u 0 jenkins chown -R jenkins:jenkins /var/jenkins_home
docker restart jenkins

# 3. Access in browser:
http://localhost:8080/job/Assignment-CI-CD/
```

---

## 6. Automated Test Suite & Code Quality Checks

To run the automated tests and PEP8 linting locally on your workstation:

```bash
# 1. Set up virtual environment
python -m venv .venv
source .venv/bin/activate    # On Windows: .venv\Scripts\Activate.ps1

# 2. Install dependencies
pip install -r requirements.txt
pip install -r requirements-dev.txt

# 3. Run PEP8 Linter
flake8 --max-line-length=120 --exclude=venv,.venv,build_submission_report.py,generate_evidence_screens.py app.py tests/

# 4. Run Pytest Suite with Coverage
pytest -v --cov=app --cov-report=term-missing tests/
```
*Result: 5/5 passed with 89% statement coverage.*

---

## 7. Resource Cleanup & Cost Management

To avoid incurring ongoing AWS charges after running or testing:

### Option 1: Temporary Pause (Stop EC2 Instances)
Preserves all configurations, containers, and disks while stopping compute billing:
```bash
aws ec2 stop-instances --instance-ids <manager_instance_id> <worker1_instance_id> <worker2_instance_id> --region ap-southeast-2
```

### Option 2: Complete Teardown (Terraform Destroy)
Permanently deletes all AWS resources (VPC, Subnet, SGs, EC2 nodes):
```bash
cd terraform
terraform destroy -auto-approve
```

---

## 8. Troubleshooting & Frequently Asked Questions (FAQ)

### Q1: Why did the public IP change after restarting an EC2 instance?
**A:** AWS assigns dynamic public IPv4 addresses by default. When an instance is stopped, AWS releases the IP back to the shared pool. When restarted, a new IP is assigned. The internal private IPs (e.g. `172.31.xx.xx`) do not change, so the internal Docker Swarm cluster communication remains intact.

### Q2: Why does `curl http://<manager_public_ip>/` show connection refused on startup?
**A:** It takes 15–20 seconds for the Docker Swarm overlay network and DNS resolver to initialize the backend service VIP. Run `sudo docker service ls` to confirm `1/1` and `2/2` replicas are active.

### Q3: How do I view live logs from the backend Flask app in Swarm?
**A:** SSH into the Manager and run:
```bash
sudo docker service logs -f cicd-assignment_web
```

### Q4: How do I test the zero-downtime rolling update?
**A:** Trigger a service image update:
```bash
sudo docker service update --image <IMAGE>:new --update-order start-first cicd-assignment_web
```
Docker Swarm will start new containers and verify healthchecks before stopping old ones.

---

## 9. Maintainer & Academic Information

- **Author:** Chamroeun Saran
- **Degree:** Master of Science in Cloud Computing
- **Repository:** [https://github.com/Chamroeun12/Assignment](https://github.com/Chamroeun12/Assignment)
- **License:** MIT License
