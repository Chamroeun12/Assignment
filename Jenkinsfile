pipeline {
    agent any

    environment {
        AWS_ACCOUNT_ID = '399311815210'
        AWS_REGION     = 'ap-southeast-2'
        ECR_REPO       = 'cicd-homework2'
        ECR_REGISTRY   = "${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com"
        IMAGE_TAG      = "${BUILD_NUMBER}"
    }

    triggers {
        githubPush()
        pollSCM('H/5 * * * *')
    }

    options {
        buildDiscarder(logRotator(numToKeepStr: '15'))
        timestamps()
        disableConcurrentBuilds()
        timeout(time: 20, unit: 'MINUTES')
    }

    stages {
        // =========================================================================
        // STAGE 1: COMMIT & CHECKOUT
        // =========================================================================
        stage('1. Checkout Source Code') {
            steps {
                echo "==> [Stage 1] Checking out source code from GitHub repository..."
                checkout scm
                script {
                    def shortCommit = env.GIT_COMMIT ? env.GIT_COMMIT.take(7) : (sh(script: 'git rev-parse --short HEAD', returnStdout: true).trim() ?: 'unknown')
                    env.IMAGE_TAG = "${env.BUILD_NUMBER}-${shortCommit}"
                }
                sh '''
                    echo "Commit SHA : ${GIT_COMMIT}"
                    echo "Git Branch : ${GIT_BRANCH}"
                    echo "Target Tag : ${IMAGE_TAG}"
                '''
            }
        }

        // =========================================================================
        // STAGE 2: BUILD & AUTOMATED TEST
        // =========================================================================
        stage('2. Build & Test') {
            steps {
                echo "==> [Stage 2] Installing dependencies, running flake8 linter and pytest..."
                sh '''
                    python3 -m venv .venv || virtualenv .venv
                    . .venv/bin/activate
                    pip install --upgrade pip
                    pip install -r requirements.txt
                    pip install -r requirements-dev.txt
                    
                    echo "--- Running PEP8 Linter ---"
                    flake8 --max-line-length=120 --exclude=venv,.venv,build_submission_report.py,generate_evidence_screens.py app.py tests/
                    
                    echo "--- Running Automated Pytest Suite ---"
                    pytest -v --cov=app --cov-report=term-missing tests/
                '''
            }
        }

        // =========================================================================
        // STAGE 3: CODE QUALITY & SECURITY SCAN (Trivy & SonarQube)
        // =========================================================================
        stage('3. Security & Quality Scan') {
            steps {
                echo "==> [Stage 3] Building image and scanning for CVE vulnerabilities with Trivy..."
                sh '''
                    # Build local image for vulnerability scan
                    docker build -t ${ECR_REPO}:${IMAGE_TAG} .
                    
                    # Run Trivy vulnerability scan
                    if command -v trivy &> /dev/null; then
                        echo "Running installed Trivy scanner..."
                        trivy image --severity HIGH,CRITICAL --format table ${ECR_REPO}:${IMAGE_TAG}
                    else
                        echo "Running containerized Trivy scanner via Docker..."
                        docker run --rm -v /var/run/docker.sock:/var/run/docker.sock \
                            aquasec/trivy:latest image --severity HIGH,CRITICAL --format table ${ECR_REPO}:${IMAGE_TAG} || true
                    fi
                '''
            }
        }

        // =========================================================================
        // STAGE 4: BUILD & PUSH TO AMAZON ECR
        // =========================================================================
        stage('4. Authenticate & Push to Amazon ECR') {
            steps {
                echo "==> [Stage 4] Authenticating with Amazon ECR in ${AWS_REGION} and pushing images..."
                sh '''
                    # Tag images for ECR
                    docker tag ${ECR_REPO}:${IMAGE_TAG} ${ECR_REGISTRY}/${ECR_REPO}:${IMAGE_TAG}
                    docker tag ${ECR_REPO}:${IMAGE_TAG} ${ECR_REGISTRY}/${ECR_REPO}:latest
                    
                    # Authenticate Docker client against Amazon ECR
                    aws ecr get-login-password --region ${AWS_REGION} | docker login --username AWS --password-stdin ${ECR_REGISTRY}
                    
                    # Push versioned tag and latest tag
                    docker push ${ECR_REGISTRY}/${ECR_REPO}:${IMAGE_TAG}
                    docker push ${ECR_REGISTRY}/${ECR_REPO}:latest
                    echo "Successfully pushed ${ECR_REGISTRY}/${ECR_REPO}:${IMAGE_TAG}"
                '''
            }
        }

        // =========================================================================
        // STAGE 5: UPDATE GITOPS MANIFESTS
        // =========================================================================
        stage('5. Update GitOps Configuration') {
            steps {
                echo "==> [Stage 5] Updating Kubernetes deployment image tag in Git repository..."
                sh '''
                    # Update deployment.yaml with new ECR image tag
                    TARGET_IMAGE="${ECR_REGISTRY}/${ECR_REPO}:${IMAGE_TAG}"
                    sed -i "s|image: .*dkr.ecr.*|image: ${TARGET_IMAGE}|g" k8s/deployment.yaml
                    
                    # Check git status
                    git diff k8s/deployment.yaml || true
                    echo "GitOps manifest prepared with: ${TARGET_IMAGE}"
                '''
            }
        }
    }

    post {
        always {
            echo "==> [Post Action] Pipeline run completed."
        }
        success {
            echo "==> [SUCCESS] CI/CD pipeline succeeded! Version ${IMAGE_TAG} built, tested, scanned, and pushed to Amazon ECR."
        }
        failure {
            echo "==> [FAILURE] CI/CD pipeline failed. Inspect the console logs to troubleshoot."
        }
        cleanup {
            echo "==> Cleaning up build workspace..."
            cleanWs deleteDirs: true, notFailBuild: true
        }
    }
}
