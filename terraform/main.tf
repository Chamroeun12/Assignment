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
# 2. SECURITY GROUP CONFIGURATION
# ==============================================================================
# Uses existing Security Group (var.security_group_id) to avoid
# restricted ec2:CreateSecurityGroup IAM permission.


# ==============================================================================
# 3. EC2 INSTANCE: SWARM MANAGER (Leader Node)
# ==============================================================================
resource "aws_instance" "swarm_manager" {
  ami                         = var.ami_id
  instance_type               = var.manager_instance_type
  subnet_id                   = var.subnet_id
  vpc_security_group_ids      = [var.security_group_id]
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
  vpc_security_group_ids      = [var.security_group_id]
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
