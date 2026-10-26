variable "aws_region" {
  description = "The AWS region to deploy the EKS cluster in"
  type        = string
  default     = "ap-southeast-2"
}

variable "cluster_name" {
  description = "The name of the Amazon EKS cluster"
  type        = string
  default     = "cicd-eks-cluster"
}

variable "kubernetes_version" {
  description = "The Kubernetes version for the EKS control plane"
  type        = string
  default     = "1.30"
}

variable "node_instance_types" {
  description = "EC2 instance types for the EKS managed node group"
  type        = list(string)
  default     = ["t3.medium"]
}

variable "desired_nodes" {
  description = "Desired number of worker nodes"
  type        = number
  default     = 2
}

variable "min_nodes" {
  description = "Minimum number of worker nodes"
  type        = number
  default     = 1
}

variable "max_nodes" {
  description = "Maximum number of worker nodes"
  type        = number
  default     = 3
}
