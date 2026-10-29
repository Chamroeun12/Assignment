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
  description = "Public SSH key for EC2 key-pair authentication (derived from chamroeunsaran.pem)"
  type        = string
  default     = "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQDzTs1xOliicOxPF/8mT5iTJzReLVlURM8/Ymtc5pf3st9LK11GMUoxuRtTmVvEW1kYnjncYewDslDckVm4QhKgR5hJWeV+Q7jwXKTZJlAoqmbAIHsYLPH0CvHcPJYgCSNOj89jUXaXEQuZOhJpX60I3JiFEynCe1G4RFhjU/Ei3OO12ZVkqLZFNUDTAgliK8vHwXh7RTSQntT1B9xFf9JOEsVCKvfFSje25I9cmmCvk1lAYzp46RTRkNnbL+6bbTZP7f9aDDIDDyiA1tg5CaeMRwnrphOrwai+VYJkqqbkxyr7JITUk8sdRZcM7urNsWKyI4Y2QDsXG168g6/TaSd3"
}

variable "allowed_ssh_cidr" {
  description = "Allowed CIDR block for SSH administrative ingress"
  type        = list(string)
  default     = ["0.0.0.0/0"]
}

variable "ami_id" {
  description = "Ubuntu AMI ID for ap-southeast-2 Sydney (defaults to verified Ubuntu LTS AMI ami-0dd60a46ecc6eac16)"
  type        = string
  default     = "ami-0dd60a46ecc6eac16"
}

variable "vpc_id" {
  description = "Existing VPC ID to deploy the cluster into"
  type        = string
  default     = "vpc-03aed2e9175c9d4f0"
}

variable "subnet_id" {
  description = "Existing public subnet ID to deploy the cluster into"
  type        = string
  default     = "subnet-0c47f571639f95653"
}

variable "key_name" {
  description = "Existing EC2 Key Pair name in AWS (defaults to chamroeunsaran)"
  type        = string
  default     = "chamroeunsaran"
}

variable "security_group_id" {
  description = "Existing Security Group ID to attach to instances (defaults to sg-0d6f8fa584d32a992)"
  type        = string
  default     = "sg-0d6f8fa584d32a992"
}

