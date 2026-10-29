variable "aws_region" {
  description = "The target AWS region for the Docker Swarm infrastructure"
  type        = string
  default     = "ap-southeast-2"
}

variable "project_name" {
  description = "Project identifier for resource naming and tagging"
  type        = string
  default     = "Assignment"
}

variable "environment" {
  description = "Deployment environment tag (production, staging, dev)"
  type        = string
  default     = "production"
}

variable "manager_instance_type" {
  description = "EC2 instance type for the Swarm Manager node"
  type        = string
  default     = "t3.small"
}

variable "worker_instance_type" {
  description = "EC2 instance type for the Swarm Worker nodes"
  type        = string
  default     = "t3.micro"
}

variable "worker_count" {
  description = "Number of Docker Swarm worker nodes (Rubric requires at least 2 workers)"
  type        = number
  default     = 2
}

variable "ssh_public_key" {
  description = "Public SSH key for EC2 key-pair authentication"
  type        = string
  default     = "ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIExampleKeyForCloudComputingHW2 student@cloud-computing"
}

variable "allowed_ssh_cidr" {
  description = "Allowed CIDR block for SSH administrative ingress"
  type        = list(string)
  default     = ["0.0.0.0/0"]
}
