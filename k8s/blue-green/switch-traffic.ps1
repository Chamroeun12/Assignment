# PowerShell Script for Zero-Downtime Blue-Green Traffic Switching on Kubernetes
param (
    [Parameter(Mandatory=$true)]
    [ValidateSet('blue', 'green')]
    [string]$TargetVersion,
    
    [string]$Namespace = "cicd-production",
    [string]$ServiceName = "cicd-assignment-prod"
)

Write-Host "=================================================================" -ForegroundColor Cyan
Write-Host "   BLUE-GREEN TRAFFIC CONTROLLER: Switching traffic to $TargetVersion" -ForegroundColor Cyan
Write-Host "=================================================================" -ForegroundColor Cyan

# 1. Verify candidate Deployment readiness
$deploymentName = "cicd-assignment-$TargetVersion"
Write-Host "Checking rollout and readiness status for $deploymentName in namespace $Namespace..."
kubectl rollout status deployment/$deploymentName -n $Namespace --timeout=60s

if ($LASTEXITCODE -ne 0) {
    Write-Host "[ERROR] Target deployment $deploymentName is not fully ready! Aborting traffic switch." -ForegroundColor Red
    exit 1
}

Write-Host "[OK] Candidate pods are Ready and healthy." -ForegroundColor Green

# 2. Switch Service Selector
Write-Host "Updating production service ($ServiceName) selector to version=$TargetVersion..."
$patchJson = '{"spec":{"selector":{"app":"cicd-assignment","version":"' + $TargetVersion + '"}}}'
kubectl patch service $ServiceName -n $Namespace -p $patchJson

if ($LASTEXITCODE -eq 0) {
    Write-Host "[SUCCESS] Traffic switched successfully to $TargetVersion!" -ForegroundColor Green
    Write-Host "Active service details:"
    kubectl get service $ServiceName -n $Namespace -o wide
} else {
    Write-Host "[ERROR] Failed to patch service selector." -ForegroundColor Red
    exit 1
}
