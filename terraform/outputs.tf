output "manager_public_ip" {
  description = "Public IPv4 address of the Docker Swarm Manager"
  value       = aws_instance.swarm_manager.public_ip
}

output "manager_private_ip" {
  description = "Private IPv4 address of the Docker Swarm Manager (used for Swarm advertise address)"
  value       = aws_instance.swarm_manager.private_ip
}

output "worker_public_ips" {
  description = "Public IPv4 addresses of the Docker Swarm Workers"
  value       = aws_instance.swarm_workers[*].public_ip
}

output "worker_private_ips" {
  description = "Private IPv4 addresses of the Docker Swarm Workers"
  value       = aws_instance.swarm_workers[*].private_ip
}

output "application_url" {
  description = "Public URL to access the deployed application through the Nginx load balancer"
  value       = "http://${aws_instance.swarm_manager.public_ip}"
}

output "application_health_url" {
  description = "Public URL for application health status check"
  value       = "http://${aws_instance.swarm_manager.public_ip}/health"
}

output "ssh_connect_manager" {
  description = "SSH connection command for Docker Swarm Manager"
  value       = "ssh -i <your-private-key.pem> ubuntu@${aws_instance.swarm_manager.public_ip}"
}

output "cluster_topology_summary" {
  description = "High-availability Docker Swarm cluster topology summary"
  value = {
    manager_nodes = 1
    worker_nodes  = length(aws_instance.swarm_workers)
    total_nodes   = 1 + length(aws_instance.swarm_workers)
    region        = var.aws_region
    architecture  = "1 Manager (Leader) + 2 Workers with Nginx Load Balancer"
  }
}
