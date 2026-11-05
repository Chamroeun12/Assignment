import os
from playwright.sync_api import sync_playwright

EDGE_PATH = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"

def get_english_html():
    return """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>How to Run Project - Comprehensive Guide</title>
    <style>
        @page {
            size: A4 portrait;
            margin: 12mm 14mm 12mm 14mm;
            @bottom-right {
                content: "Page " counter(page) " of " counter(pages);
                font-size: 8pt;
                color: #64748b;
            }
        }
        * {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
        }
        body {
            font-size: 9pt;
            line-height: 1.5;
            color: #1e293b;
            background: #ffffff;
            padding-bottom: 20px;
        }
        .header {
            background: #0f172a;
            color: #ffffff;
            padding: 16px 20px;
            border-radius: 8px;
            margin-bottom: 16px;
        }
        .header h1 {
            font-size: 16pt;
            color: #38bdf8;
            margin-bottom: 4px;
        }
        .header .subtitle {
            font-size: 9.5pt;
            color: #94a3b8;
        }
        .meta-bar {
            display: flex;
            flex-wrap: wrap;
            gap: 12px;
            background: #f1f5f9;
            padding: 8px 12px;
            border-radius: 6px;
            font-size: 8pt;
            color: #475569;
            margin-bottom: 16px;
            border-left: 4px solid #0284c7;
        }
        .meta-bar span strong {
            color: #0f172a;
        }
        h2 {
            font-size: 12pt;
            color: #0f172a;
            border-bottom: 1.5px solid #cbd5e1;
            padding-bottom: 4px;
            margin-top: 18px;
            margin-bottom: 10px;
            display: flex;
            align-items: center;
        }
        h3 {
            font-size: 10pt;
            color: #0369a1;
            margin-top: 12px;
            margin-bottom: 6px;
        }
        p {
            margin-bottom: 8px;
        }
        ul, ol {
            margin-left: 20px;
            margin-bottom: 10px;
        }
        li {
            margin-bottom: 4px;
        }
        pre {
            background: #0f172a;
            color: #38bdf8;
            padding: 8px 12px;
            border-radius: 6px;
            font-family: Consolas, "Courier New", monospace;
            font-size: 8pt;
            line-height: 1.4;
            margin: 6px 0 10px 0;
            overflow-x: auto;
            border-left: 3px solid #38bdf8;
        }
        code {
            background: #f1f5f9;
            color: #0369a1;
            padding: 1px 4px;
            border-radius: 3px;
            font-family: Consolas, monospace;
            font-size: 8.5pt;
        }
        pre code {
            background: transparent;
            color: inherit;
            padding: 0;
        }
        table {
            width: 100%;
            border-collapse: collapse;
            font-size: 8pt;
            margin: 8px 0 12px 0;
        }
        th, td {
            border: 1px solid #cbd5e1;
            padding: 6px 10px;
            text-align: left;
        }
        th {
            background: #f8fafc;
            color: #0f172a;
            font-weight: 600;
        }
        .alert {
            background: #eff6ff;
            border: 1px solid #bfdbfe;
            border-left: 4px solid #3b82f6;
            padding: 8px 12px;
            border-radius: 4px;
            margin: 10px 0;
            font-size: 8pt;
        }
        .alert.warning {
            background: #fffbeb;
            border-color: #fde68a;
            border-left-color: #f59e0b;
        }
        .badge {
            display: inline-block;
            padding: 2px 6px;
            border-radius: 4px;
            font-size: 7.5pt;
            font-weight: 600;
        }
        .badge-green { background: #dcfce7; color: #15803d; }
        .badge-blue { background: #e0f2fe; color: #0369a1; }
        .page-break { page-break-before: always; }
    </style>
</head>
<body>

    <div class="header">
        <h1>Cloud Computing Capstone: End-to-End Execution Guide</h1>
        <div class="subtitle">Complete Step-by-Step Runbook for Local Development &amp; AWS EC2 Docker Swarm Production</div>
    </div>

    <div class="meta-bar">
        <span><strong>Author:</strong> Chamroeun Saran</span>
        <span><strong>Course:</strong> Master of Science in Cloud Computing</span>
        <span><strong>Repository:</strong> github.com/Chamroeun12/Assignment</span>
        <span><strong>Target AWS:</strong> ap-southeast-2 (Sydney)</span>
    </div>

    <h2>1. Project Architecture Overview</h2>
    <p>This repository provides a production-grade container orchestration and cloud delivery system on Amazon Web Services (AWS):</p>
    <ul>
        <li><strong>Infrastructure as Code (Terraform):</strong> Provisions dedicated VPC (10.0.0.0/16), public subnets, least-privilege security groups, and 3 EC2 nodes (1 Manager + 2 Workers) with dynamic Canonical Ubuntu 22.04 LTS AMI discovery.</li>
        <li><strong>Container Orchestration (Docker Swarm):</strong> 3-node cluster operating behind an overlay network with internal service VIP routing and zero-downtime rolling updates (<code>order: start-first</code>).</li>
        <li><strong>Ingress &amp; Load Balancing (Nginx):</strong> Reverse proxy on Port 80 terminating public traffic and balancing requests across replicated Python Flask containers.</li>
        <li><strong>CI/CD Automation (Jenkins):</strong> Declarative pipeline running Flake8 linting, Pytest test suites, Trivy CVE vulnerability scans, and Telegram Bot push notifications.</li>
    </ul>

    <h2>2. System Prerequisites</h2>
    <table>
        <tr>
            <th>Tool / Requirement</th>
            <th>Local Testing Mode</th>
            <th>AWS Cloud Mode</th>
            <th>Recommended Version</th>
        </tr>
        <tr>
            <td><strong>Git</strong></td>
            <td><span class="badge badge-green">Required</span></td>
            <td><span class="badge badge-green">Required</span></td>
            <td>2.30+</td>
        </tr>
        <tr>
            <td><strong>Docker Desktop</strong></td>
            <td><span class="badge badge-green">Required</span></td>
            <td><span class="badge badge-blue">Optional</span></td>
            <td>24.0+ (Docker Compose v2)</td>
        </tr>
        <tr>
            <td><strong>AWS CLI</strong></td>
            <td><span class="badge badge-blue">Not Needed</span></td>
            <td><span class="badge badge-green">Required</span></td>
            <td>2.10+ (configured with access keys)</td>
        </tr>
        <tr>
            <td><strong>Terraform CLI</strong></td>
            <td><span class="badge badge-blue">Not Needed</span></td>
            <td><span class="badge badge-green">Required</span></td>
            <td>1.5.0+</td>
        </tr>
        <tr>
            <td><strong>SSH Key Pair</strong></td>
            <td><span class="badge badge-blue">Not Needed</span></td>
            <td><span class="badge badge-green">Required</span></td>
            <td><code>chamroeunsaran.pem</code> (400 permissions)</td>
        </tr>
    </table>

    <h2>3. Method A: Quick Local Testing with Docker Compose (No AWS Required)</h2>
    <p>If you do not have an AWS account and want to test the full multi-service application (Flask App + Nginx Load Balancer) locally on your laptop in 30 seconds:</p>

    <h3>Step 3.1: Clone Repository</h3>
    <pre><code>git clone https://github.com/Chamroeun12/Assignment.git
cd Assignment</code></pre>

    <h3>Step 3.2: Build and Launch Multi-Service Stack</h3>
    <pre><code>docker compose up --build -d</code></pre>

    <h3>Step 3.3: Verify Running Services</h3>
    <pre><code>docker compose ps</code></pre>
    <p>Both <code>cicd-assignment-web</code> (Flask Backend on port 5000) and <code>cicd-assignment-nginx</code> (Reverse Proxy on port 80) will be running and healthy.</p>

    <h3>Step 3.4: Test Endpoints in Browser or Terminal</h3>
    <p>Open your browser at: <strong><code>http://localhost/</code></strong></p>
    <pre><code>curl -i http://localhost/            # Main Web UI Dashboard
curl -s http://localhost/health       # JSON Healthcheck
curl -s http://localhost/api/info     # Backend Service & Hostname
curl -s http://localhost/nginx-health # Nginx Proxy Health</code></pre>

    <h3>Step 3.5: Clean Up Local Containers</h3>
    <pre><code>docker compose down</code></pre>

    <div class="page-break"></div>

    <h2>4. Method B: Full Production Deployment on AWS EC2 (Terraform &amp; Docker Swarm)</h2>
    <p>Follow these steps to provision your own 3-node cluster on AWS EC2 and deploy the production Docker Swarm stack:</p>

    <h3>Step 4.1: Configure AWS CLI</h3>
    <pre><code>aws configure
# AWS Access Key ID: [Your Access Key]
# AWS Secret Access Key: [Your Secret Key]
# Default region: ap-southeast-2
# Default output format: json</code></pre>

    <h3>Step 4.2: Provision Infrastructure with Terraform</h3>
    <pre><code>cd terraform
terraform init
terraform plan
terraform apply -auto-approve</code></pre>
    <p>Terraform outputs the generated public and private IPs:</p>
    <pre><code>Outputs:
manager_public_ip = "16.178.206.23"
manager_private_ip = "172.31.34.160"
worker_public_ips = ["3.107.96.140", "13.211.213.228"]
worker_private_ips = ["172.31.36.22", "172.31.47.183"]
application_url = "http://16.178.206.23"</code></pre>

    <h3>Step 4.3: Initialize Docker Swarm &amp; Connect Nodes</h3>
    <p><strong>1. SSH into the Manager Node:</strong></p>
    <pre><code>ssh -i chamroeunsaran.pem ubuntu@&lt;manager_public_ip&gt;</code></pre>
    <p><strong>2. Initialize Docker Swarm on Manager:</strong></p>
    <pre><code>sudo docker swarm init --advertise-addr &lt;manager_private_ip&gt;
sudo hostnamectl set-hostname swarm-manager
sudo systemctl restart docker</code></pre>
    <p><em>Copy the worker join token command printed on screen (<code>docker swarm join --token SWMTKN-1-...</code>).</em></p>

    <p><strong>3. Join Worker 1 to Swarm:</strong></p>
    <pre><code>ssh -i chamroeunsaran.pem ubuntu@&lt;worker1_public_ip&gt;
sudo docker swarm join --token &lt;TOKEN&gt; &lt;manager_private_ip&gt;:2377
sudo hostnamectl set-hostname swarm-worker1
sudo systemctl restart docker
exit</code></pre>

    <p><strong>4. Join Worker 2 to Swarm:</strong></p>
    <pre><code>ssh -i chamroeunsaran.pem ubuntu@&lt;worker2_public_ip&gt;
sudo docker swarm join --token &lt;TOKEN&gt; &lt;manager_private_ip&gt;:2377
sudo hostnamectl set-hostname swarm-worker2
sudo systemctl restart docker
exit</code></pre>

    <p><strong>5. Verify Swarm Topology on Manager:</strong></p>
    <pre><code>sudo docker node ls
# ID            HOSTNAME        STATUS    AVAILABILITY   MANAGER STATUS
# xxxxxxxx *    swarm-manager   Ready     Active         Leader
# yyyyyyyy      swarm-worker1   Ready     Active
# zzzzzzzz      swarm-worker2   Ready     Active</code></pre>

    <h3>Step 4.4: Deploy Application Stack</h3>
    <p>Copy code bundle to the cluster nodes and deploy:</p>
    <pre><code># Package from local workstation:
tar -czf app_bundle.tar.gz Dockerfile app.py requirements.txt templates docker-stack.yml nginx

# SCP to all 3 nodes:
scp -i chamroeunsaran.pem app_bundle.tar.gz ubuntu@&lt;manager_public_ip&gt;:/home/ubuntu/
scp -i chamroeunsaran.pem app_bundle.tar.gz ubuntu@&lt;worker1_public_ip&gt;:/home/ubuntu/
scp -i chamroeunsaran.pem app_bundle.tar.gz ubuntu@&lt;worker2_public_ip&gt;:/home/ubuntu/

# Build image on nodes:
ssh -i chamroeunsaran.pem ubuntu@&lt;worker1_public_ip&gt; "tar -xzf app_bundle.tar.gz &amp;&amp; sudo docker build -t 399311815210.dkr.ecr.ap-southeast-2.amazonaws.com/cicd-assignment:latest ."
ssh -i chamroeunsaran.pem ubuntu@&lt;worker2_public_ip&gt; "tar -xzf app_bundle.tar.gz &amp;&amp; sudo docker build -t 399311815210.dkr.ecr.ap-southeast-2.amazonaws.com/cicd-assignment:latest ."

# Deploy on Manager:
ssh -i chamroeunsaran.pem ubuntu@&lt;manager_public_ip&gt;
tar -xzf app_bundle.tar.gz
sudo docker build -t 399311815210.dkr.ecr.ap-southeast-2.amazonaws.com/cicd-assignment:latest .
sudo docker stack deploy -c docker-stack.yml cicd-assignment</code></pre>

    <h3>Step 4.5: Verify Services &amp; Live Endpoints</h3>
    <pre><code>sudo docker service ls
sudo docker stack ps cicd-assignment</code></pre>
    <p>Test the live endpoints via curl:</p>
    <pre><code>curl -s http://&lt;manager_public_ip&gt;/health
curl -s http://&lt;manager_public_ip&gt;/api/info
curl -s http://&lt;manager_public_ip&gt;/nginx-health</code></pre>

    <div class="page-break"></div>

    <h2>5. Method C: Automated Jenkins CI/CD Setup</h2>
    <p>To run our pre-configured Jenkins environment locally with all plugins, credentials, and build history:</p>
    <pre><code># 1. Start Jenkins container
docker run -d --name jenkins -p 8080:8080 -p 50000:50000 -v jenkins_home:/var/jenkins_home jenkins/jenkins:lts

# 2. Inject backup archive
docker cp jenkins_backup.tar.gz jenkins:/tmp/jenkins_backup.tar.gz
docker exec -u 0 jenkins tar xzf /tmp/jenkins_backup.tar.gz -C /var/jenkins_home
docker exec -u 0 jenkins chown -R jenkins:jenkins /var/jenkins_home

# 3. Disable authentication for instant presentation access
docker exec -u 0 jenkins sed -i 's/&lt;useSecurity&gt;true&lt;\\/useSecurity&gt;/&lt;useSecurity&gt;false&lt;\\/useSecurity&gt;/' /var/jenkins_home/config.xml
docker restart jenkins

# 4. Open in browser:
http://localhost:8080/job/Assignment-CI-CD/</code></pre>

    <h2>6. Automated Testing &amp; Linting</h2>
    <p>Run the test suite and PEP8 linter on your workstation:</p>
    <pre><code># Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\\Scripts\\Activate.ps1

# Install requirements
pip install -r requirements.txt
pip install -r requirements-dev.txt

# Run Flake8 linter
flake8 --max-line-length=120 --exclude=venv,.venv,build_submission_report.py,generate_evidence_screens.py app.py tests/

# Run Pytest suite with coverage
pytest -v --cov=app --cov-report=term-missing tests/</code></pre>
    <p><em>Result: 5/5 tests passed with 89% statement coverage.</em></p>

    <h2>7. Cost Management &amp; Teardown</h2>
    <div class="alert warning">
        <strong>Important:</strong> AWS charges hourly for running EC2 instances and attached EBS volumes. Remember to stop or destroy instances when finished!
    </div>

    <h3>To Pause Instances (Stops Compute Billing, Keeps Data Intact):</h3>
    <pre><code>aws ec2 stop-instances --instance-ids &lt;mgr_id&gt; &lt;w1_id&gt; &lt;w2_id&gt; --region ap-southeast-2</code></pre>

    <h3>To Permanently Destroy All AWS Resources:</h3>
    <pre><code>cd terraform
terraform destroy -auto-approve</code></pre>

    <h2>8. Frequently Asked Questions (FAQ)</h2>
    <ul>
        <li><strong>Q: Why did my public IP change after stopping EC2?</strong><br/>
        AWS dynamic public IPs are released back into the Amazon pool upon instance stop. Internal private IPs remain fixed, keeping the internal Swarm cluster intact.</li>
        <li><strong>Q: How do I test the zero-downtime rolling update?</strong><br/>
        Execute: <code>sudo docker service update --image &lt;IMAGE&gt;:v2 --update-order start-first cicd-assignment_web</code>. Swarm provisions healthy new containers before stopping old ones.</li>
        <li><strong>Q: How do I view live application logs?</strong><br/>
        Run: <code>sudo docker service logs -f cicd-assignment_web</code>.</li>
    </ul>

</body>
</html>
"""

def get_khmer_html():
    return """<!DOCTYPE html>
<html lang="km">
<head>
    <meta charset="UTF-8">
    <title>សៀវភៅណែនាំការដំឡើង និងដំណើរការគម្រោង (How to Run Project)</title>
    <style>
        @page {
            size: A4 portrait;
            margin: 12mm 14mm 12mm 14mm;
            @bottom-right {
                content: "ទំព័រ " counter(page) " នៃ " counter(pages);
                font-size: 8pt;
                color: #64748b;
            }
        }
        * {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
            font-family: "Noto Sans Khmer", "Khmer OS Battambang", "Khmer OS", "Leelawadee UI", sans-serif;
        }
        body {
            font-size: 9pt;
            line-height: 1.65;
            color: #1e293b;
            background: #ffffff;
            padding-bottom: 20px;
        }
        .header {
            background: #0f172a;
            color: #ffffff;
            padding: 16px 20px;
            border-radius: 8px;
            margin-bottom: 16px;
        }
        .header h1 {
            font-size: 15pt;
            color: #38bdf8;
            margin-bottom: 6px;
            line-height: 1.35;
        }
        .header .subtitle {
            font-size: 9.5pt;
            color: #94a3b8;
        }
        .meta-bar {
            display: flex;
            flex-wrap: wrap;
            gap: 12px;
            background: #f1f5f9;
            padding: 8px 12px;
            border-radius: 6px;
            font-size: 8pt;
            color: #475569;
            margin-bottom: 16px;
            border-left: 4px solid #0284c7;
        }
        .meta-bar span strong {
            color: #0f172a;
        }
        h2 {
            font-size: 11.5pt;
            color: #0f172a;
            border-bottom: 1.5px solid #cbd5e1;
            padding-bottom: 4px;
            margin-top: 18px;
            margin-bottom: 10px;
        }
        h3 {
            font-size: 9.5pt;
            color: #0369a1;
            margin-top: 12px;
            margin-bottom: 6px;
        }
        p {
            margin-bottom: 8px;
        }
        ul, ol {
            margin-left: 20px;
            margin-bottom: 10px;
        }
        li {
            margin-bottom: 4px;
        }
        pre {
            background: #0f172a;
            color: #38bdf8;
            padding: 8px 12px;
            border-radius: 6px;
            font-family: Consolas, "Courier New", monospace;
            font-size: 8pt;
            line-height: 1.4;
            margin: 6px 0 10px 0;
            overflow-x: auto;
            border-left: 3px solid #38bdf8;
        }
        code {
            background: #f1f5f9;
            color: #0369a1;
            padding: 1px 4px;
            border-radius: 3px;
            font-family: Consolas, monospace;
            font-size: 8.5pt;
        }
        pre code {
            background: transparent;
            color: inherit;
            padding: 0;
        }
        table {
            width: 100%;
            border-collapse: collapse;
            font-size: 8pt;
            margin: 8px 0 12px 0;
        }
        th, td {
            border: 1px solid #cbd5e1;
            padding: 6px 10px;
            text-align: left;
        }
        th {
            background: #f8fafc;
            color: #0f172a;
            font-weight: 600;
        }
        .alert {
            background: #eff6ff;
            border: 1px solid #bfdbfe;
            border-left: 4px solid #3b82f6;
            padding: 8px 12px;
            border-radius: 4px;
            margin: 10px 0;
            font-size: 8pt;
        }
        .alert.warning {
            background: #fffbeb;
            border-color: #fde68a;
            border-left-color: #f59e0b;
        }
        .badge {
            display: inline-block;
            padding: 2px 6px;
            border-radius: 4px;
            font-size: 7.5pt;
            font-weight: 600;
        }
        .badge-green { background: #dcfce7; color: #15803d; }
        .badge-blue { background: #e0f2fe; color: #0369a1; }
        .step-num {
            display: inline-block;
            background: #0284c7;
            color: white;
            border-radius: 50%;
            width: 18px;
            height: 18px;
            text-align: center;
            font-size: 8pt;
            line-height: 18px;
            margin-right: 6px;
        }
        .page-break { page-break-before: always; }
    </style>
</head>
<body>

    <div class="header">
        <h1>សៀវភៅណែនាំលម្អិតអំពីរបៀបដំណើរការគម្រោង Cloud Computing</h1>
        <div class="subtitle">ការដំឡើង និងដំណើរការប្រព័ន្ធ Cloud ស្វ័យប្រវត្តិតាមរយៈ Docker Swarm, Terraform, Nginx និង Jenkins</div>
    </div>

    <div class="meta-bar">
        <span><strong>អ្នករៀបចំគម្រោង៖</strong> ចំរើន សារ៉ាន់ (Chamroeun Saran)</span>
        <span><strong>ថ្នាក់សិក្សា៖</strong> Master of Science in Cloud Computing</span>
        <span><strong>តំណភ្ជាប់ Git៖</strong> github.com/Chamroeun12/Assignment</span>
        <span><strong>តំបន់ AWS៖</strong> Sydney (ap-southeast-2)</span>
    </div>

    <h2>១. សេចក្តីផ្តើមអំពីស្ថាបត្យកម្មគម្រោង (System Architecture)</h2>
    <p>គម្រោងនេះត្រូវបានបង្កើតឡើងសម្រាប់កិច្ចការបញ្ចប់ថ្នាក់អនុបណ្ឌិត Cloud Computing ដោយរួមបញ្ចូលនូវបច្ចេកវិទ្យាសំខាន់ៗចំនួន ៥៖</p>
    <ul>
        <li><strong>Infrastructure as Code (Terraform)៖</strong> បង្កើតប្រព័ន្ធបណ្តាញសុវត្ថិភាព VPC (10.0.0.0/16), Security Groups, និងម៉ាស៊ីនមេ AWS EC2 ចំនួន ៣ (១ Manager + ២ Workers) ដោយស្វ័យប្រវត្តិ។</li>
        <li><strong>Container Orchestration (Docker Swarm)៖</strong> គ្រប់គ្រងកុងតឺន័រនៅលើម៉ាស៊ីនមេចំនួន ៣ ជាមួយការផ្លាស់ប្តូរកំណែថ្មីដោយគ្មានការដាច់សេវា (Zero-Downtime Rolling Update)។</li>
        <li><strong>Nginx Reverse Proxy &amp; Load Balancing៖</strong> ចែករំលែកបន្ទុកចរាចរណ៍ (Round-Robin Traffic) លើ Port 80 ទៅកាន់ Application Replicas។</li>
        <li><strong>CI/CD Pipeline (Jenkins)៖</strong> ស្វ័យប្រវត្តិកម្មនៃការត្រួតពិនិត្យកូដ (Flake8), តេស្ត (Pytest), ស្កេនមេរោគ (Trivy), និងផ្ញើសារដំណឹងទៅ Telegram Bot។</li>
    </ul>

    <h2>២. តម្រូវការប្រព័ន្ធមុនពេលចាប់ផ្តើម (Prerequisites)</h2>
    <table>
        <tr>
            <th>កម្មវិធី / ឧបករណ៍</th>
            <th>សម្រាប់រត់លើ Laptop ផ្ទាល់ខ្លួន</th>
            <th>សម្រាប់រត់លើ AWS EC2 Cloud</th>
            <th>ការណែនាំ</th>
        </tr>
        <tr>
            <td><strong>Git</strong></td>
            <td><span class="badge badge-green">ចាំបាច់ត្រូវមាន</span></td>
            <td><span class="badge badge-green">ចាំបាច់ត្រូវមាន</span></td>
            <td>កំណែ 2.30+ សម្រាប់ទាញយកកូដ</td>
        </tr>
        <tr>
            <td><strong>Docker Desktop</strong></td>
            <td><span class="badge badge-green">ចាំបាច់ត្រូវមាន</span></td>
            <td><span class="badge badge-blue">មិនចាំបាច់មានទេ</span></td>
            <td>កំណែ 24.0+ (រួមមាន Docker Compose)</td>
        </tr>
        <tr>
            <td><strong>AWS CLI</strong></td>
            <td><span class="badge badge-blue">មិនបាច់មាន</span></td>
            <td><span class="badge badge-green">ចាំបាច់ត្រូវមាន</span></td>
            <td>កំណត់សិទ្ធិ Access Key &amp; Secret Key</td>
        </tr>
        <tr>
            <td><strong>Terraform</strong></td>
            <td><span class="badge badge-blue">មិនបាច់មាន</span></td>
            <td><span class="badge badge-green">ចាំបាច់ត្រូវមាន</span></td>
            <td>កំណែ 1.5.0+ សម្រាប់បង្កើត Server</td>
        </tr>
        <tr>
            <td><strong>SSH Key (.pem)</strong></td>
            <td><span class="badge badge-blue">មិនបាច់មាន</span></td>
            <td><span class="badge badge-green">ចាំបាច់ត្រូវមាន</span></td>
            <td>ឯកសារ <code>chamroeunsaran.pem</code> សម្រាប់ Login</td>
        </tr>
    </table>

    <h2>៣. វិធីសាស្ត្រទី ១៖ ការរត់តេស្តលើ Laptop ផ្ទាល់ខ្លួន (Docker Compose)</h2>
    <p>ប្រសិនបើអ្នកមិនចង់ចំណាយលុយលើ AWS ឬគ្មានគណនី AWS អ្នកអាចរត់សាកល្បង Full Stack (Flask + Nginx) លើកុំព្យូទ័ររបស់អ្នកក្នុងរយៈពេលត្រឹមតែ ៣០ វិនាទី៖</p>

    <h3>ជំហាន ៣.១៖ ទាញយកកូដពី GitHub (Clone Repo)</h3>
    <pre><code>git clone https://github.com/Chamroeun12/Assignment.git
cd Assignment</code></pre>

    <h3>ជំហាន ៣.២៖ បញ្ជាឱ្យដំណើរការកុងតឺន័រទាំងអស់</h3>
    <pre><code>docker compose up --build -d</code></pre>

    <h3>ជំហាន ៣.៣៖ ពិនិត្យមើលស្ថានភាពកុងតឺន័រ</h3>
    <pre><code>docker compose ps</code></pre>
    <p>អ្នកនឹងឃើញកុងតឺន័រទាំងពីរដំណើរការធម្មតា៖ <code>cicd-assignment-web</code> (Flask Backend) និង <code>cicd-assignment-nginx</code> (Nginx Reverse Proxy)។</p>

    <h3>ជំហាន ៣.៤៖ តេស្តមើលលទ្ធផលនៅលើ Browser</h3>
    <p>បើកកម្មវិធី Browser (Chrome/Edge) ហើយវាយអាសយដ្ឋាន៖ <strong><code>http://localhost/</code></strong></p>
    <pre><code>curl -i http://localhost/            # បង្ហាញ Dashboard លើ Web
curl -s http://localhost/health       # បង្ហាញស្ថានភាពសុខភាពប្រព័ន្ធ
curl -s http://localhost/api/info     # បង្ហាញព័ត៌មានលម្អិត និង Hostname
curl -s http://localhost/nginx-health # បញ្ជាក់ថា Nginx ដំណើរការល្អ</code></pre>

    <h3>ជំហាន ៣.៥៖ បិទប្រព័ន្ធពេលឈប់ប្រើ</h3>
    <pre><code>docker compose down</code></pre>

    <div class="page-break"></div>

    <h2>៤. វិធីសាស្ត្រទី ២៖ ការដំឡើង និងដំណើរការលើ AWS EC2 Cloud (Terraform &amp; Docker Swarm)</h2>
    <p>នេះជាការដំឡើងជាក់ស្តែងលើម៉ាស៊ីនមេ AWS EC2 ចំនួន ៣ ដូចនៅក្នុងការធ្វើបទបង្ហាញថ្នាក់រៀន៖</p>

    <h3>ជំហាន ៤.១៖ កំណត់សិទ្ធិគណនី AWS CLI</h3>
    <pre><code>aws configure
# វាយបញ្ចូល AWS Access Key ID របស់អ្នក
# វាយបញ្ចូល AWS Secret Access Key របស់អ្នក
# Default region: ap-southeast-2 (Sydney)
# Default output format: json</code></pre>

    <h3>ជំហាន ៤.២៖ បង្កើតហេដ្ឋារចនាសម្ព័ន្ធដោយស្វ័យប្រវត្តិតាមរយៈ Terraform</h3>
    <pre><code>cd terraform
terraform init
terraform plan
terraform apply -auto-approve</code></pre>
    <p>នៅពេលដំណើរការចប់ Terraform នឹងបង្ហាញ IP ម៉ាស៊ីនមេទាំង ៣ ដោយស្វ័យប្រវត្តិ៖</p>
    <pre><code>Outputs:
manager_public_ip = "16.178.206.23"
manager_private_ip = "172.31.34.160"
worker_public_ips = ["3.107.96.140", "13.211.213.228"]
worker_private_ips = ["172.31.36.22", "172.31.47.183"]
application_url = "http://16.178.206.23"</code></pre>
    <pre><code>cd ..</code></pre>

    <h3>ជំហាន ៤.៣៖ ចាប់ផ្តើម Docker Swarm និងភ្ជាប់ Worker Nodes</h3>
    <p><strong>១. ចូលទៅកាន់ Manager Node តាមរយៈ SSH៖</strong></p>
    <pre><code>ssh -i chamroeunsaran.pem ubuntu@16.178.206.23</code></pre>

    <p><strong>២. ចាប់ផ្តើម Docker Swarm នៅលើ Manager៖</strong></p>
    <pre><code>sudo docker swarm init --advertise-addr 172.31.34.160
sudo hostnamectl set-hostname swarm-manager
sudo systemctl restart docker</code></pre>
    <p><em>(ប្រព័ន្ធនឹងផ្តល់ Token មួយខ្សែសម្រាប់ឱ្យ Worker យកទៅ Join ដូចជា៖ <code>docker swarm join --token SWMTKN-1-... 172.31.34.160:2377</code>)</em></p>

    <p><strong>៣. ភ្ជាប់ Worker 1 ចូលទៅក្នុង Swarm៖</strong></p>
    <pre><code>ssh -i chamroeunsaran.pem ubuntu@3.107.96.140
sudo docker swarm join --token &lt;TOKEN&gt; 172.31.34.160:2377
sudo hostnamectl set-hostname swarm-worker1
sudo systemctl restart docker
exit</code></pre>

    <p><strong>៤. ភ្ជាប់ Worker 2 ចូលទៅក្នុង Swarm៖</strong></p>
    <pre><code>ssh -i chamroeunsaran.pem ubuntu@13.211.213.228
sudo docker swarm join --token &lt;TOKEN&gt; 172.31.34.160:2377
sudo hostnamectl set-hostname swarm-worker2
sudo systemctl restart docker
exit</code></pre>

    <p><strong>៥. ផ្ទៀងផ្ទាត់បញ្ជី Nodes នៅលើ Manager៖</strong></p>
    <pre><code>ssh -i chamroeunsaran.pem ubuntu@16.178.206.23
sudo docker node ls
# អ្នកនឹងឃើញ 1 Manager (Leader) + 2 Workers ស្ថិតក្នុងស្ថានភាព Ready និង Active</code></pre>

    <h3>ជំហាន ៤.៤៖ បញ្ជូន និងដាក់ឱ្យដំណើរការ Application Stack</h3>
    <p>ពីលើកុំព្យូទ័ររបស់អ្នក ត្រូវខ្ចប់កូដ ហើយផ្ញើទៅកាន់ម៉ាស៊ីនមេទាំង ៣៖</p>
    <pre><code># ១. ខ្ចប់កូដគម្រោង
tar -czf app_bundle.tar.gz Dockerfile app.py requirements.txt templates docker-stack.yml nginx

# ២. បញ្ជូនកូដទៅកាន់ម៉ាស៊ីនទាំង ៣ តាម SCP
scp -i chamroeunsaran.pem app_bundle.tar.gz ubuntu@16.178.206.23:/home/ubuntu/
scp -i chamroeunsaran.pem app_bundle.tar.gz ubuntu@3.107.96.140:/home/ubuntu/
scp -i chamroeunsaran.pem app_bundle.tar.gz ubuntu@13.211.213.228:/home/ubuntu/

# ៣. Build រូបភាពកុងតឺន័រលើ Worker 1 និង Worker 2
ssh -i chamroeunsaran.pem ubuntu@3.107.96.140 "tar -xzf app_bundle.tar.gz &amp;&amp; sudo docker build -t 399311815210.dkr.ecr.ap-southeast-2.amazonaws.com/cicd-assignment:latest ."
ssh -i chamroeunsaran.pem ubuntu@13.211.213.228 "tar -xzf app_bundle.tar.gz &amp;&amp; sudo docker build -t 399311815210.dkr.ecr.ap-southeast-2.amazonaws.com/cicd-assignment:latest ."

# ៤. Deploy Stack នៅលើ Manager Node
ssh -i chamroeunsaran.pem ubuntu@16.178.206.23
tar -xzf app_bundle.tar.gz
sudo docker build -t 399311815210.dkr.ecr.ap-southeast-2.amazonaws.com/cicd-assignment:latest .
sudo docker stack deploy -c docker-stack.yml cicd-assignment</code></pre>

    <h3>ជំហាន ៤.៥៖ ពិនិត្យមើលលទ្ធផលនៅលើ Browser និង Terminal</h3>
    <pre><code>sudo docker service ls
sudo docker stack ps cicd-assignment</code></pre>
    <p>បើកមើលលើ Browser៖ <strong><code>http://16.178.206.23/</code></strong></p>
    <pre><code>curl -s http://16.178.206.23/health
curl -s http://16.178.206.23/api/info        # Hostname នឹងឆ្លាស់គ្នាបញ្ជាក់ពី Load Balancing
curl -s http://16.178.206.23/nginx-health</code></pre>

    <div class="page-break"></div>

    <h2>៥. វិធីសាស្ត្រទី ៣៖ ការប្រើប្រាស់ Jenkins CI/CD ស្វ័យប្រវត្តិកម្ម</h2>
    <p>ប្រសិនបើអ្នកចង់បើកមើល Jenkins ដែលមាន Build History ទាំងអស់ (Build #7 ដល់ #21) នៅលើម៉ាស៊ីនថ្មី៖</p>
    <pre><code># ១. បង្កើត Container Jenkins ថ្មី
docker run -d --name jenkins -p 8080:8080 -p 50000:50000 -v jenkins_home:/var/jenkins_home jenkins/jenkins:lts

# ២. ផ្ទេរទិន្នន័យ Backup ចូលទៅក្នុង Container
docker cp jenkins_backup.tar.gz jenkins:/tmp/jenkins_backup.tar.gz
docker exec -u 0 jenkins tar xzf /tmp/jenkins_backup.tar.gz -C /var/jenkins_home
docker exec -u 0 jenkins chown -R jenkins:jenkins /var/jenkins_home

# ៣. ដោះសោរ Security ដើម្បីកុំឱ្យទាមទារ Password ពេល Demo
docker exec -u 0 jenkins sed -i 's/&lt;useSecurity&gt;true&lt;\\/useSecurity&gt;/&lt;useSecurity&gt;false&lt;\\/useSecurity&gt;/' /var/jenkins_home/config.xml
docker restart jenkins

# ៤. បើក Browser មើល Jenkins Job ភ្លាមៗ៖
http://localhost:8080/job/Assignment-CI-CD/</code></pre>

    <h2>៦. ការរត់តេស្តគុណភាពកូដ (Testing &amp; Linting)</h2>
    <pre><code># បង្កើត Virtual Environment សម្រាប់ Python
python -m venv .venv
source .venv/bin/activate  # លើ Windows ប្រើ៖ .venv\\Scripts\\Activate.ps1

# ដំឡើងបណ្ណាល័យជំនួយ
pip install -r requirements.txt
pip install -r requirements-dev.txt

# រត់ត្រួតពិនិត្យទម្រង់កូដតាមស្តង់ដារ PEP 8
flake8 --max-line-length=120 --exclude=venv,.venv,build_submission_report.py,generate_evidence_screens.py app.py tests/

# រត់តេស្តស្វ័យប្រវត្តិកម្ម Pytest ជាមួយ Coverage
pytest -v --cov=app --cov-report=term-missing tests/</code></pre>
    <p><em>លទ្ធផលទទួលបាន៖ ជាប់ 100% (5 passed) ជាមួយកម្រិត Code Coverage 89%។</em></p>

    <h2>៧. ការគ្រប់គ្រងការចំណាយ និងការបិទម៉ាស៊ីនមេ (Cost Management)</h2>
    <div class="alert warning">
        <strong>ការប្រុងប្រយ័ត្ន៖</strong> AWS គិតលុយតាមម៉ោងដំណើរការរបស់ EC2 និងទំហំផ្ទុក Hard Disk (EBS)។ សូមបិទ ឬលុបម៉ាស៊ីនមេពេលដែលធ្វើបទបង្ហាញចប់!
    </div>

    <h3>ជម្រើសទី ១៖ ផ្អាកដំណើរការបណ្តោះអាសន្ន (Stop Instances - មិនបាត់បង់ទិន្នន័យ)</h3>
    <pre><code>aws ec2 stop-instances --instance-ids &lt;manager_id&gt; &lt;worker1_id&gt; &lt;worker2_id&gt; --region ap-southeast-2</code></pre>

    <h3>ជម្រើសទី ២៖ លុបធនធានទាំងអស់ចោលជាស្ថាពរ (Terraform Destroy)</h3>
    <pre><code>cd terraform
terraform destroy -auto-approve</code></pre>

    <h2>៨. សំណួរ និងចម្លើយបច្ចេកទេស (FAQ)</h2>
    <ul>
        <li><strong>សួរ៖ ហេតុអ្វីបានជា Public IP ផ្លាស់ប្តូរពេល Restart ម៉ាស៊ីន EC2?</strong><br/>
        <strong>ឆ្លើយ៖</strong> តាមលំនាំដើម AWS ប្រើប្រាស់ Dynamic IP ពី Public Pool។ នៅពេល Stop ម៉ាស៊ីន AWS ដក IP យកទៅឱ្យអ្នកផ្សេងប្រើវិញ។ នៅពេល Start ឡើងវិញ ទើបផ្តល់ IP ថ្មី។ ប៉ុន្តែ Private IP នៅក្នុងបណ្តាញខាងក្នុងមិនផ្លាស់ប្តូរឡើយ ដូច្នេះ Docker Swarm ដំណើរការធម្មតា។</li>
        <li><strong>សួរ៖ តើត្រូវធ្វើដូចម្តេចដើម្បីតេស្តមើល Zero-Downtime Rolling Update?</strong><br/>
        <strong>ឆ្លើយ៖</strong> ដំណើរការបញ្ជា៖ <code>sudo docker service update --image &lt;IMAGE&gt;:v2 --update-order start-first cicd-assignment_web</code>។ Swarm នឹងបង្កើតកុងតឺន័រថ្មីឱ្យដើរស្រួលបួលសិន ទើបបិទកុងតឺន័រចាស់។</li>
        <li><strong>សួរ៖ តើត្រូវមើល Logs របស់ Flask App លើ Swarm យ៉ាងដូចម្តេច?</strong><br/>
        <strong>ឆ្លើយ៖</strong> វាយពាក្យបញ្ជា៖ <code>sudo docker service logs -f cicd-assignment_web</code>។</li>
    </ul>

</body>
</html>
"""

def generate_pdfs():
    print("Starting PDF generation with Microsoft Edge headless...")
    os.makedirs("output", exist_ok=True)
    
    with sync_playwright() as p:
        browser = p.chromium.launch(
            executable_path=EDGE_PATH,
            headless=True
        )

        # 1. Generate English PDF
        print("Rendering HOW_TO_RUN_EN.pdf...")
        page_en = browser.new_page()
        page_en.set_content(get_english_html())
        page_en.pdf(
            path="HOW_TO_RUN_EN.pdf",
            format="A4",
            print_background=True,
            margin={"top": "12mm", "bottom": "12mm", "left": "14mm", "right": "14mm"}
        )
        page_en.close()
        print(f"Successfully generated HOW_TO_RUN_EN.pdf ({os.path.getsize('HOW_TO_RUN_EN.pdf')} bytes)")

        # 2. Generate Khmer PDF
        print("Rendering HOW_TO_RUN_KH.pdf...")
        page_kh = browser.new_page()
        page_kh.set_content(get_khmer_html())
        page_kh.pdf(
            path="HOW_TO_RUN_KH.pdf",
            format="A4",
            print_background=True,
            margin={"top": "12mm", "bottom": "12mm", "left": "14mm", "right": "14mm"}
        )
        page_kh.close()
        print(f"Successfully generated HOW_TO_RUN_KH.pdf ({os.path.getsize('HOW_TO_RUN_KH.pdf')} bytes)")

        browser.close()

if __name__ == "__main__":
    generate_pdfs()
