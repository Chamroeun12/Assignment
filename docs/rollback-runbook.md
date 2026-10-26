# Operational Runbook: Rollback Procedures & Failure Recovery

**Course:** Master's in Cloud Computing  
**Author:** Chamroeun Saran (GitHub: [Chamroeun12](https://github.com/Chamroeun12))  
**Target Infrastructure:** Amazon EKS / Argo CD / Kubernetes  

---

## 1. Overview & Rollback Philosophy

In a **GitOps-driven continuous delivery architecture** (where Argo CD continuously reconciles the live Kubernetes cluster against a Git repository), **the Git repository is the single source of truth**.

```
[ Git Repository: Single Source of Truth ]
                  │
                  ▼ (Reconciliation Loop: Self-Heal & Prune)
             [ Argo CD ]
                  │
                  ▼ (Desired State Applied)
      [ Amazon EKS Kubernetes Pods ]
```

### The "Self-Healing Conflict" Gotcha
If an engineer executes a traditional `kubectl rollout undo deployment/cicd-homework2` while Argo CD `selfHeal: true` is enabled, Argo CD will detect that the cluster's live state has diverged from Git, treat the manual rollback as configuration drift, and **immediately overwrite your manual rollback with the bad image from Git**!

Therefore, this runbook defines two distinct procedures:
1. **Standard GitOps Rollback (Recommended & Authoritative):** Reverts the image tag in Git, allowing Argo CD to reconcile gracefully.
2. **Emergency Hot-Fix Rollback (Break-Glass):** Temporarily pauses Argo CD auto-sync, rolls back with `kubectl`, and reconciles Git afterward.

---

## 2. Procedure A: Standard GitOps Rollback (Authoritative)

Use this procedure for normal production incidents when Git and CI/CD pipelines are accessible.

### Step 1: Identify the Last Known Good Commit
Check the Git commit history of the deployment manifest:
```bash
git log -n 5 --oneline k8s/deployment.yaml
```
Example output:
```
a1b2c3d ci(gitops): update production image to bad1234 [skip ci]
e5f6g7h ci(gitops): update production image to good567 [skip ci]
```

### Step 2: Revert the Desired State in Git
Execute a git revert on the problematic commit:
```bash
# Option 1: Git revert
git revert a1b2c3d -m "revert: rollback production to last stable release good567"

# Option 2: Point directly to the stable SHA in deployment manifest
# Edit k8s/deployment.yaml to restore the stable image tag
git add k8s/deployment.yaml
git commit -m "fix(gitops): rollback production image to good567 [skip ci]"
git push origin main
```

### Step 3: Trigger or Await Argo CD Reconciliation
Argo CD detects the commit within seconds (or poll interval) and applies the stable manifest to Amazon EKS.
To force instant synchronization via CLI:
```bash
argocd app sync cicd-homework2 --prune
```

### Step 4: Verify Cluster Health
Verify that the pods transition back to healthy status:
```bash
kubectl rollout status deployment/cicd-homework2 -n cicd-production --timeout=60s
kubectl get pods -n cicd-production -l app=cicd-homework2
```

---

## 3. Procedure B: Emergency "Break-Glass" Rollback (Immediate Cluster Recovery)

Use this procedure when an outage is causing active user disruption and waiting for Git pushes is unacceptable.

### Step 1: Suspend Argo CD Automated Reconciliation
Prevent Argo CD from overwriting the manual intervention:
```bash
kubectl patch application cicd-homework2 -n argocd --type merge -p '{"spec":{"syncPolicy":{"automated":null}}}'
```

### Step 2: Execute Instant Kubernetes Rollout Undo
```bash
# Check current revision history
kubectl rollout history deployment/cicd-homework2 -n cicd-production

# Roll back to the previous deployment revision
kubectl rollout undo deployment/cicd-homework2 -n cicd-production
```

### Step 3: Monitor Rollout Progress
```bash
kubectl rollout status deployment/cicd-homework2 -n cicd-production --timeout=60s
```

### Step 4: Validate Service Health
```bash
curl -I http://<SERVICE_PUBLIC_IP>/health
```

### Step 5: Post-Incident Git Synchronization
Once the incident is resolved, update `k8s/deployment.yaml` in Git to match the running image tag, commit and push to Git, and re-enable Argo CD automated sync:
```bash
kubectl patch application cicd-homework2 -n argocd --type merge -p '{"spec":{"syncPolicy":{"automated":{"prune":true,"selfHeal":true}}}}'
```

---

## 4. Procedure C: Blue-Green Instant Traffic Rollback

If operating under the **Blue-Green deployment pattern**, rollback is virtually instantaneous because both versions run concurrently until validation is complete.

### Step 1: Detect Unhealthy Candidate
If the Green candidate generates HTTP 5xx errors or elevated latency on the preview service:

### Step 2: Switch Traffic Back to Stable Blue
**On Windows (PowerShell):**
```powershell
.\k8s\blue-green\switch-traffic.ps1 -TargetVersion blue
```

**On Linux / Mac (Bash):**
```bash
./k8s/blue-green/switch-traffic.sh blue
```

### Step 3: Instant Validation
The production Service immediately points its selector back to `version: blue`. Old traffic never experienced dropped connections because the Blue pods remained `Running` and warm throughout the test window.
