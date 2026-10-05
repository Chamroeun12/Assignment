# CI/CD Homework 2: Flask Web Application

A lightweight Python Flask web application demonstrating an end-to-end automated CI/CD pipeline using GitHub, Jenkins, Docker, Amazon ECR, and Docker Swarm on AWS EC2.

---

## Architecture Pipeline Flow

```
[Developer Push]
       │
       ▼
 1. GitHub (Source Repository & Webhook Trigger)
       │
       ▼
 2. Jenkins (Automated Pipeline: Build, Tag & Auth)
       │
       ▼
 3. Docker (Containerization)
       │
       ▼
 4. Amazon ECR (Private Container Image Registry)
       │
       ▼
 5. Docker Swarm on AWS EC2 (Manager + Worker Rolling Deployment)
       │
       ▼
 [Live Application]
```

### Stage Overview
1. **GitHub**: Houses the application source, `Dockerfile`, `Jenkinsfile`, and `docker-stack.yml`. Pushes trigger Jenkins automatically via Webhook.
2. **Jenkins**: Automates the checkout, container build, AWS ECR login (`aws ecr get-login-password`), image push, and stack deployment.
3. **Docker**: Packages the application into an immutable container image tagged with the build number/commit SHA.
4. **Amazon ECR**: Serves as the private container registry to store and manage versioned Docker images.
5. **Docker Swarm on EC2**: Orchestrates the multi-node cluster (1 Manager + 1 Worker), executing rolling updates without downtime.

---

## Local Development & Setup

### Prerequisites
* Python 3.10+
* pip

### Installation
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Run the application locally:
   ```bash
   python app.py
   ```

3. Open your browser and navigate to:
   * **Web Interface:** [http://localhost:5000](http://localhost:5000)
   * **Health Check API:** [http://localhost:5000/health](http://localhost:5000/health)

---

## Configuration & Environment Variables

| Variable | Default Value | Description |
| :--- | :---: | :--- |
| `APP_VERSION` | `1.0.0` | Injected version tag displayed on the UI and health check |
| `PORT` | `5000` | HTTP port on which Flask listens |
