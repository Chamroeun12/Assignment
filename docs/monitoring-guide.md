# Full-Stack Observability, Monitoring & Logging Guide

**Course:** Master's in Cloud Computing  
**Author:** Chamroeun Saran (GitHub: [Chamroeun12](https://github.com/Chamroeun12))  
**Observability Components:** Prometheus, Grafana, AWS CloudWatch, Container Insights  

---

## 1. Observability Architecture Overview

The monitoring subsystem provides three complementary pillars of observability:
1. **Metrics:** Prometheus Operator scrapes runtime telemetry from Kubernetes pods and nodes every 15 seconds.
2. **Visual Dashboards:** Grafana visualizes real-time pod health, CPU/memory consumption, replica status, and container restart counters.
3. **Log Aggregation:** AWS CloudWatch Container Insights collects standard output and standard error logs directly from all container runtimes without requiring application-level log shipping agents.

```
       [ Kubernetes Worker Nodes (EKS) ]
              │                   │
    (cAdvisor & Kube-State)   (Stdout/Stderr Logs)
              │                   │
              ▼                   ▼
      [ Prometheus ]     [ CloudWatch Fluent Bit ]
              │                   │
              ▼                   ▼
      [ Grafana UI ]     [ CloudWatch Log Groups ]
```

---

## 2. Metrics Collection & Prometheus Operator

### 2.1 ServiceMonitor Configuration
The ServiceMonitor resource (`monitoring/prometheus/servicemonitor.yaml`) directs Prometheus to auto-discover and scrape the application endpoints:
```yaml
apiVersion: monitoring.coreos.com/v1
kind: ServiceMonitor
metadata:
  name: cicd-homework2-monitor
  namespace: cicd-production
spec:
  selector:
    matchLabels:
      app: cicd-homework2
  endpoints:
    - port: http
      path: /health
      interval: 15s
```

### 2.2 Alert Rules (`monitoring/prometheus/alert-rules.yaml`)
Configured alerts notify the DevOps team before user impact occurs:
- **`PodNotReady`:** Triggers when available replicas < 1 for > 1 minute (Severity: Critical).
- **`PodCrashLooping`:** Triggers when container restarts > 2 times in 5 minutes (Severity: Warning).
- **`HighCPUUsage`:** Triggers when container exceeds 80% CPU request threshold for > 3 minutes (Severity: Warning).

---

## 3. Grafana Dashboards

The pre-configured dashboard JSON is located at `monitoring/grafana/dashboard-cicd.json`.

### Key Metrics Monitored:
1. **Healthy Pod Replicas:** `kube_deployment_status_replicas_available{deployment="cicd-homework2"}`
2. **Total Restarts:** `sum(kube_pod_container_status_restarts_total{container="web-app"})`
3. **Pod CPU Utilization (mCPU):** `sum(rate(container_cpu_usage_seconds_total{container="web-app"}[2m])) by (pod) * 1000`
4. **Pod Memory Working Set (MiB):** `sum(container_memory_working_set_bytes{container="web-app"}) by (pod) / 1024 / 1024`

### Importing the Dashboard:
1. Log into Grafana (`kubectl port-forward svc/prometheus-grafana 3000:80`).
2. Navigate to **Dashboards > Import**.
3. Upload `monitoring/grafana/dashboard-cicd.json` or paste the JSON content.
4. Select the Prometheus data source and click **Import**.

---

## 4. Amazon CloudWatch Container Insights

For production environments on AWS, CloudWatch Container Insights provides centralized, high-durability log aggregation.

### Installing Container Insights via DaemonSet:
```bash
# 1. Apply CloudWatch namespace and cluster configuration
kubectl apply -f monitoring/cloudwatch/container-insights.yaml

# 2. Deploy AWS Fluent Bit daemonset
kubectl apply -f https://raw.githubusercontent.com/aws-samples/amazon-cloudwatch-container-insights/latest/k8s-deployment-manifest-templates/deployment-mode/daemonset/container-insights-monitoring/fluent-bit/fluent-bit.yaml
```

Logs will stream to AWS CloudWatch Log Groups under:
`/aws/containerinsights/cicd-eks-cluster/application`

### Viewing Logs in AWS CLI:
```bash
aws logs tail /aws/containerinsights/cicd-eks-cluster/application --follow --region ap-southeast-2
```

---

## 5. Cost Analysis & Financial Safety

| Observability Component | AWS Cost Model | Optimization Strategy |
| :--- | :--- | :--- |
| **Prometheus & Grafana (In-Cluster)** | Free Open-Source (uses existing node CPU/RAM) | Retain metrics for 7–14 days in EBS volume. |
| **CloudWatch Log Ingestion** | ~$0.50 per GB ingested | Set log retention period to 7 days in CloudWatch log group. |
| **CloudWatch Custom Metrics** | ~$0.30 per metric/month | Disable Container Insights detailed metric collection if only log streaming is needed. |
