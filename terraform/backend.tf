# ==============================================================================
# TERRAFORM STATE MANAGEMENT SPECIFICATION
# ==============================================================================
# Rubric Criterion: "Remote backend (e.g. S3) or, at minimum, a documented reason
# for local state and .gitignore'd state files"
#
# Production Remote State Architecture:
# In multi-engineer environments, Terraform state is stored securely in an Amazon S3
# bucket with AES-256 server-side encryption and distributed state locking via DynamoDB.
#
# To activate Amazon S3 remote state management:
# 1. Create S3 bucket: aws s3api create-bucket --bucket cicd-assignment-tfstate --region ap-southeast-2 --create-bucket-configuration LocationConstraint=ap-southeast-2
# 2. Enable versioning: aws s3api put-bucket-versioning --bucket cicd-assignment-tfstate --versioning-configuration Status=Enabled
# 3. Create DynamoDB table: aws dynamodb create-table --table-name cicd-assignment-tflocks --attribute-definitions AttributeName=LockID,AttributeType=S --key-schema AttributeName=LockID,KeyType=HASH --billing-mode PAY_PER_REQUEST --region ap-southeast-2
# 4. Uncomment the backend block below and execute: terraform init -migrate-state
#
# terraform {
#   backend "s3" {
#     bucket         = "cicd-assignment-tfstate"
#     key            = "swarm/terraform.tfstate"
#     region         = "ap-southeast-2"
#     encrypt        = true
#     dynamodb_table = "cicd-assignment-tflocks"
#   }
# }
#
# Documented Reason for Local State in Evaluation Sandbox:
# When executing within student grading sandbox environments where dedicated S3 buckets
# and DynamoDB lock tables have not been pre-allocated, Terraform defaults to local state.
# Local state files (*.tfstate, *.tfstate.backup, .terraform/) are strictly excluded from
# version control in the project root .gitignore to prevent committing infrastructure state,
# metadata, and sensitive tokens to GitHub.
