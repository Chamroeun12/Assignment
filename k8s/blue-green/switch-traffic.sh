#!/usr/bin/env bash
set -euo pipefail

# Bash script for Zero-Downtime Blue-Green Traffic Switching on Kubernetes
TARGET_VERSION="${1:-}"
NAMESPACE="${2:-cicd-production}"
SERVICE_NAME="${3:-cicd-homework2-prod}"

if [[ "$TARGET_VERSION" != "blue" && "$TARGET_VERSION" != "green" ]]; then
    echo "Usage: $0 <blue|green> [namespace] [service_name]"
    exit 1
fi

echo "================================================================="
echo "   BLUE-GREEN TRAFFIC CONTROLLER: Switching traffic to $TARGET_VERSION"
echo "================================================================="

# 1. Verify candidate Deployment readiness
DEPLOYMENT_NAME="cicd-homework2-${TARGET_VERSION}"
echo "Checking rollout and readiness status for ${DEPLOYMENT_NAME} in namespace ${NAMESPACE}..."
kubectl rollout status "deployment/${DEPLOYMENT_NAME}" -n "${NAMESPACE}" --timeout=60s

# 2. Switch Service Selector
echo "Updating production service (${SERVICE_NAME}) selector to version=${TARGET_VERSION}..."
kubectl patch service "${SERVICE_NAME}" -n "${NAMESPACE}" \
  -p "{\"spec\":{\"selector\":{\"app\":\"cicd-homework2\",\"version\":\"${TARGET_VERSION}\"}}}"

echo "[SUCCESS] Traffic switched successfully to ${TARGET_VERSION}!"
kubectl get service "${SERVICE_NAME}" -n "${NAMESPACE}" -o wide
