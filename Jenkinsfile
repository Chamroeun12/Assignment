pipeline {
    agent any

    environment {
        AWS_ACCOUNT_ID = '399311815210'
        AWS_REGION     = 'ap-southeast-2'
        ECR_REPO       = 'cicd-homework2'
        ECR_REGISTRY   = "${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com"
        IMAGE_TAG      = "${BUILD_NUMBER}-${GIT_COMMIT.take(7)}"
        STACK_NAME     = 'cicd-homework2'
    }

    triggers {
        githubPush()
        pollSCM('H/5 * * * *')
    }

    options {
        buildDiscarder(logRotator(numToKeepStr: '15'))
        timestamps()
        disableConcurrentBuilds()
        timeout(time: 15, unit: 'MINUTES')
    }

    stages {
        stage('Checkout Source Code') {
            steps {
                echo "==> [Stage 1] Checking out source code from GitHub repository..."
                checkout scm
                sh '''
                    echo "Commit: ${GIT_COMMIT}"
                    echo "Branch: ${GIT_BRANCH}"
                    echo "Build Tag: ${IMAGE_TAG}"
                '''
            }
        }

        stage('Build Docker Image') {
            steps {
                echo "==> [Stage 2] Building Docker image for ${ECR_REPO}:${IMAGE_TAG}..."
                sh '''
                    docker build \
                        -t ${ECR_REGISTRY}/${ECR_REPO}:${IMAGE_TAG} \
                        -t ${ECR_REGISTRY}/${ECR_REPO}:latest .
                '''
            }
        }

        stage('Authenticate & Push to Amazon ECR') {
            steps {
                echo "==> [Stage 3] Authenticating with Amazon ECR in ${AWS_REGION} and pushing images..."
                sh '''
                    # Authenticate Docker client against Amazon ECR registry
                    aws ecr get-login-password --region ${AWS_REGION} | docker login --username AWS --password-stdin ${ECR_REGISTRY}
                    
                    # Push uniquely tagged version (build number + commit SHA)
                    echo "Pushing ${ECR_REGISTRY}/${ECR_REPO}:${IMAGE_TAG}..."
                    docker push ${ECR_REGISTRY}/${ECR_REPO}:${IMAGE_TAG}

                    # Push latest tag for reference
                    echo "Pushing ${ECR_REGISTRY}/${ECR_REPO}:latest..."
                    docker push ${ECR_REGISTRY}/${ECR_REPO}:latest
                '''
            }
        }

        stage('Deploy to Docker Swarm') {
            steps {
                echo "==> [Stage 4] Deploying updated service to Docker Swarm cluster..."
                script {
                    if (env.SWARM_MANAGER_IP) {
                        echo "Deploying remotely to Swarm Manager at ${SWARM_MANAGER_IP} via SSH..."
                        sshagent(credentials: ['swarm-manager-ssh-key']) {
                            sh '''
                                scp -o StrictHostKeyChecking=no docker-stack.yml ubuntu@${SWARM_MANAGER_IP}:~/docker-stack.yml
                                ssh -o StrictHostKeyChecking=no ubuntu@${SWARM_MANAGER_IP} "
                                    aws ecr get-login-password --region ${AWS_REGION} | docker login --username AWS --password-stdin ${ECR_REGISTRY}
                                    export IMAGE_TAG=${IMAGE_TAG}
                                    docker stack deploy --with-registry-auth -c ~/docker-stack.yml ${STACK_NAME}
                                "
                            '''
                        }
                    } else {
                        echo "Deploying directly to local Docker Swarm node..."
                        sh '''
                            export IMAGE_TAG=${IMAGE_TAG}
                            docker stack deploy --with-registry-auth -c docker-stack.yml ${STACK_NAME}
                        '''
                    }
                }
            }
        }

        stage('Verify Rolling Deployment') {
            steps {
                echo "==> [Stage 5] Verifying Swarm service convergence and task distribution..."
                script {
                    if (env.SWARM_MANAGER_IP) {
                        sshagent(credentials: ['swarm-manager-ssh-key']) {
                            sh '''
                                ssh -o StrictHostKeyChecking=no ubuntu@${SWARM_MANAGER_IP} "
                                    echo '--- Docker Swarm Nodes ---'
                                    docker node ls
                                    echo '--- Docker Swarm Services ---'
                                    docker service ls
                                    echo '--- Tasks for Service ${STACK_NAME}_cicd-homework2 ---'
                                    docker service ps ${STACK_NAME}_cicd-homework2
                                "
                            '''
                        }
                    } else {
                        sh '''
                            echo "--- Docker Swarm Nodes ---"
                            docker node ls || true
                            echo "--- Docker Swarm Services ---"
                            docker service ls || true
                            echo "--- Tasks for Service ${STACK_NAME}_cicd-homework2 ---"
                            docker service ps ${STACK_NAME}_cicd-homework2 || true
                        '''
                    }
                }
            }
        }
    }

    post {
        always {
            echo "==> [Post Action] Pipeline run completed."
        }
        success {
            echo "==> [SUCCESS] CI/CD pipeline succeeded! Version ${IMAGE_TAG} is live on Docker Swarm."
        }
        failure {
            echo "==> [FAILURE] CI/CD pipeline failed. Check console output for troubleshooting."
        }
        cleanup {
            echo "==> Cleaning up build workspace..."
            cleanWs deleteDirs: true, notFailBuild: true
        }
    }
}
