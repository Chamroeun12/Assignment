terraform {
  required_version = ">= 1.5.0"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = var.aws_region
}

# ==============================================================================
# 1. AMI CONFIGURATION
# ==============================================================================
# Uses var.ami_id (default Ubuntu LTS in ap-southeast-2).
# Avoids ec2:DescribeImages 403 UnauthorizedOperation errors for IAM users
# with scoped EC2 permissions.


# ==============================================================================
# 2. LEAST-PRIVILEGE SECURITY GROUP FOR DOCKER SWARM & APPLICATION
# ==============================================================================
# Deployed into the existing VPC (var.vpc_id) to avoid restricted ec2:CreateVpc
resource "aws_security_group" "swarm_sg" {
  name        = "${var.project_name}-swarm-sg"
  description = "Least-privilege security group for Docker Swarm cluster nodes and load balancer"
  vpc_id      = var.vpc_id

  # SSH Administration
  ingress {
    description = "SSH administrative access"
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = var.allowed_ssh_cidr
  }

  # Nginx Load Balancer HTTP Ingress
  ingress {
    description = "Public HTTP web traffic to Nginx load balancer"
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  # Nginx Load Balancer HTTPS Ingress
  ingress {
    description = "Public HTTPS web traffic"
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  # Jenkins Webhook & CI/CD Dashboard
  ingress {
    description = "Jenkins web UI and GitHub webhook ingress"
    from_port   = 8080
    to_port     = 8080
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  # Docker Swarm Cluster Management (Restricted strictly to cluster members)
  ingress {
    description = "Docker Swarm cluster management communication between manager and workers"
    from_port   = 2377
    to_port     = 2377
    protocol    = "tcp"
    self        = true
  }

  # Docker Swarm Node Discovery and Gossip Protocol (TCP)
  ingress {
    description = "Docker Swarm node discovery and gossip (TCP)"
    from_port   = 7946
    to_port     = 7946
    protocol    = "tcp"
    self        = true
  }

  # Docker Swarm Node Discovery and Gossip Protocol (UDP)
  ingress {
    description = "Docker Swarm node discovery and gossip (UDP)"
    from_port   = 7946
    to_port     = 7946
    protocol    = "udp"
    self        = true
  }

  # Docker Swarm Overlay Network VXLAN Traffic (UDP)
  ingress {
    description = "Docker Swarm overlay network VXLAN traffic"
    from_port   = 4789
    to_port     = 4789
    protocol    = "udp"
    self        = true
  }

  # Outbound Internet Access for Package Installation & Container Image Pulls
  egress {
    description = "Allow all outbound traffic for software updates and container image pulls"
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name        = "${var.project_name}-swarm-sg"
    Environment = var.environment
    Project     = var.project_name
  }
}

# ==============================================================================
# 3. EC2 INSTANCE: SWARM MANAGER (Leader Node)
# ==============================================================================
resource "aws_instance" "swarm_manager" {
  ami                         = var.ami_id
  instance_type               = var.manager_instance_type
  subnet_id                   = var.subnet_id
  vpc_security_group_ids      = [aws_security_group.swarm_sg.id]
  key_name                    = var.key_name
  associate_public_ip_address = true

  root_block_device {
    volume_size           = 25
    volume_type           = "gp3"
    delete_on_termination = true
  }

  user_data = <<-EOF
              #!/bin/bash
              set -e
              apt-get update -y
              apt-get install -y apt-transport-https ca-certificates curl gnupg lsb-release
              
              # Install official Docker CE
              mkdir -p /etc/apt/keyrings
              curl -fsSL https://download.docker.com/linux/ubuntu/gpg | gpg --dearmor -o /etc/apt/keyrings/docker.gpg
              echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | tee /etc/apt/sources.list.d/docker.list > /dev/null
              apt-get update -y
              apt-get install -y docker-ce docker-ce-cli containerd.io docker-compose-plugin
              
              systemctl enable docker
              systemctl start docker
              usermod -aG docker ubuntu
              
              # Initialize Docker Swarm on Manager
              PRIVATE_IP=$(curl -s http://169.254.169.254/latest/meta-data/local-ipv4 || hostname -I | awk '{print $1}')
              docker swarm init --advertise-addr $PRIVATE_IP
              
              # Store join token for workers
              docker swarm join-token worker -q > /home/ubuntu/swarm_worker_token.txt
              chown ubuntu:ubuntu /home/ubuntu/swarm_worker_token.txt
              chmod 644 /home/ubuntu/swarm_worker_token.txt
              EOF

  tags = {
    Name        = "${var.project_name}-swarm-manager"
    Role        = "manager"
    Environment = var.environment
    Project     = var.project_name
  }
}

# ==============================================================================
# 4. EC2 INSTANCES: SWARM WORKERS (2 Worker Nodes, Total: 1 Manager + 2 Workers)
# ==============================================================================
resource "aws_instance" "swarm_workers" {
  count                       = var.worker_count
  ami                         = var.ami_id
  instance_type               = var.worker_instance_type
  subnet_id                   = var.subnet_id
  vpc_security_group_ids      = [aws_security_group.swarm_sg.id]
  key_name                    = var.key_name
  associate_public_ip_address = true

  root_block_device {
    volume_size           = 20
    volume_type           = "gp3"
    delete_on_termination = true
  }

  user_data = <<-EOF
              #!/bin/bash
              set -e
              apt-get update -y
              apt-get install -y apt-transport-https ca-certificates curl gnupg lsb-release
              
              # Install official Docker CE
              mkdir -p /etc/apt/keyrings
              curl -fsSL https://download.docker.com/linux/ubuntu/gpg | gpg --dearmor -o /etc/apt/keyrings/docker.gpg
              echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | tee /etc/apt/sources.list.d/docker.list > /dev/null
              apt-get update -y
              apt-get install -y docker-ce docker-ce-cli containerd.io docker-compose-plugin
              
              systemctl enable docker
              systemctl start docker
              usermod -aG docker ubuntu
              EOF

  tags = {
    Name        = "${var.project_name}-swarm-worker-${count.index + 1}"
    Role        = "worker"
    Environment = var.environment
    Project     = var.project_name
  }
}
