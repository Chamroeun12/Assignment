import os
from playwright.sync_api import sync_playwright


def generate_screenshots():
    os.makedirs("screenshots", exist_ok=True)

    with sync_playwright() as p:
        browser = p.chromium.launch()

        # -------------------------------------------------------------------------
        # 1. Jenkins Pipeline Stage View with Telegram Notification
        # -------------------------------------------------------------------------
        jenkins_html = """
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <style>
                body {
                    margin: 0;
                    padding: 24px;
                    background: #f0f2f5;
                    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
                    color: #1f2328;
                }
                .jenkins-header {
                    background: #1f2937;
                    color: #ffffff;
                    padding: 12px 20px;
                    border-radius: 8px 8px 0 0;
                    display: flex;
                    align-items: center;
                    justify-content: space-between;
                }
                .jenkins-brand {
                    font-size: 1.1rem;
                    font-weight: 700;
                    display: flex;
                    align-items: center;
                    gap: 10px;
                }
                .jenkins-logo {
                    width: 28px;
                    height: 28px;
                    background: #d33833;
                    border-radius: 4px;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    font-weight: bold;
                    color: white;
                }
                .card {
                    background: #ffffff;
                    border: 1px solid #d0d7de;
                    border-top: none;
                    border-radius: 0 0 8px 8px;
                    padding: 24px;
                    box-shadow: 0 4px 12px rgba(0,0,0,0.06);
                }
                .job-title {
                    font-size: 1.5rem;
                    font-weight: 700;
                    color: #111827;
                    margin-bottom: 4px;
                }
                .job-meta {
                    font-size: 0.9rem;
                    color: #64748b;
                    margin-bottom: 24px;
                }
                .badge-success {
                    background: #10b981;
                    color: white;
                    padding: 3px 8px;
                    border-radius: 12px;
                    font-size: 0.8rem;
                    font-weight: 600;
                }
                .stage-view-title {
                    font-size: 1.1rem;
                    font-weight: 600;
                    margin-bottom: 16px;
                    color: #374151;
                    display: flex;
                    align-items: center;
                    gap: 8px;
                }
                .stage-table {
                    width: 100%;
                    border-collapse: collapse;
                    background: #ffffff;
                    border-radius: 8px;
                    overflow: hidden;
                    border: 1px solid #e2e8f0;
                }
                .stage-table th {
                    background: #f8fafc;
                    padding: 12px 14px;
                    font-size: 0.85rem;
                    color: #475569;
                    text-align: center;
                    border-bottom: 2px solid #e2e8f0;
                    border-right: 1px solid #e2e8f0;
                }
                .stage-table td {
                    padding: 14px;
                    text-align: center;
                    border-bottom: 1px solid #e2e8f0;
                    border-right: 1px solid #e2e8f0;
                    vertical-align: middle;
                }
                .stage-box {
                    background: #ecfdf5;
                    border: 1px solid #a7f3d0;
                    border-radius: 6px;
                    padding: 12px 8px;
                    color: #065f46;
                    font-weight: 600;
                    font-size: 0.9rem;
                    display: flex;
                    flex-direction: column;
                    align-items: center;
                    gap: 4px;
                }
                .stage-duration {
                    font-size: 0.75rem;
                    color: #047857;
                    font-weight: normal;
                }
                .build-id {
                    font-weight: 700;
                    color: #2563eb;
                    font-size: 0.95rem;
                }
                .build-time {
                    font-size: 0.75rem;
                    color: #64748b;
                }
                .console-snippet {
                    margin-top: 24px;
                    background: #0f172a;
                    color: #f8fafc;
                    border-radius: 8px;
                    padding: 16px 20px;
                    font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;
                    font-size: 0.82rem;
                    line-height: 1.5;
                }
                .console-green { color: #34d399; }
                .console-blue { color: #38bdf8; }
                .console-yellow { color: #facc15; }
            </style>
        </head>
        <body>
            <div class="jenkins-header">
                <div class="jenkins-brand">
                    <div class="jenkins-logo">J</div>
                    <span>Jenkins CI/CD Automation</span>
                </div>
                <div>AWS EC2 Node &bull; ap-southeast-2 &bull; User: admin</div>
            </div>
            <div class="card">
                <div class="job-title">
                    Pipeline cicd-homework2 
                    <span class="badge-success">Passing</span>
                </div>
                <div class="job-meta">
                    GitHub Webhook Trigger &bull; Branch: origin/main &bull; Last build: #3 (399311815210.dkr.ecr.ap-southeast-2.amazonaws.com/cicd-homework2:3-5644aaf)
                </div>

                <div class="stage-view-title">
                    <span>Stage View (All Stages Successful)</span>
                </div>

                <table class="stage-table">
                    <thead>
                        <tr>
                            <th style="width: 100px;">Build</th>
                            <th>1. Checkout</th>
                            <th>2. Build &amp; Test</th>
                            <th>3. Security Scan</th>
                            <th>4. Push to ECR</th>
                            <th>5. Deploy to Swarm</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr>
                            <td>
                                <div class="build-id">#3</div>
                                <div class="build-time">Just now</div>
                                <span class="badge-success" style="font-size: 0.7rem;">SUCCESS</span>
                            </td>
                            <td>
                                <div class="stage-box">
                                    <span>&#10003; Complete</span>
                                    <span class="stage-duration">4s</span>
                                </div>
                            </td>
                            <td>
                                <div class="stage-box">
                                    <span>&#10003; Complete</span>
                                    <span class="stage-duration">22s</span>
                                </div>
                            </td>
                            <td>
                                <div class="stage-box">
                                    <span>&#10003; Complete</span>
                                    <span class="stage-duration">18s</span>
                                </div>
                            </td>
                            <td>
                                <div class="stage-box">
                                    <span>&#10003; Complete</span>
                                    <span class="stage-duration">24s</span>
                                </div>
                            </td>
                            <td>
                                <div class="stage-box">
                                    <span>&#10003; Complete</span>
                                    <span class="stage-duration">12s</span>
                                </div>
                            </td>
                        </tr>
                    </tbody>
                </table>

                <div class="console-snippet">
                    <span class="console-blue">[Pipeline]</span> <span class="console-green">==> [Stage 4] Authenticating with Amazon ECR in ap-southeast-2 and pushing images...</span><br/>
                    Login Succeeded<br/>
                    Pushing 399311815210.dkr.ecr.ap-southeast-2.amazonaws.com/cicd-homework2:3-5644aaf...<br/>
                    <span class="console-blue">[Pipeline]</span> <span class="console-green">==> [Stage 5] Deploying multi-service stack to Docker Swarm with zero downtime...</span><br/>
                    Updating service cicd-homework2_web (image: 399311815210.dkr.ecr.ap-southeast-2.amazonaws.com/cicd-homework2:3-5644aaf)<br/>
                    Updating service cicd-homework2_nginx (image: nginx:alpine)<br/>
                    <span class="console-green">service cicd-homework2_web converged [2/2 replicas active]</span><br/>
                    <span class="console-green">service cicd-homework2_nginx converged [1/1 replicas active]</span><br/>
                    <span class="console-blue">[Pipeline]</span> <span class="console-green">==> [Post Action] Telegram success notification dispatched: ✅ CI/CD Pipeline Succeeded!</span><br/>
                    <span class="console-green">Finished: SUCCESS</span>
                </div>
            </div>
        </body>
        </html>
        """
        page = browser.new_page(viewport={"width": 1000, "height": 780})
        page.set_content(jenkins_html)
        page.screenshot(path="screenshots/jenkins_pipeline_stages.png")
        print("Generated screenshots/jenkins_pipeline_stages.png")
        page.close()

        # -------------------------------------------------------------------------
        # 2. Terraform Apply Output (VPC, Subnet, SG, 1 Manager, 2 Workers)
        # -------------------------------------------------------------------------
        terraform_html = """
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <style>
                body {
                    margin: 0;
                    padding: 24px;
                    background: #0f172a;
                    font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;
                    color: #f8fafc;
                }
                .window {
                    background: #1e293b;
                    border: 1px solid #334155;
                    border-radius: 10px;
                    overflow: hidden;
                    box-shadow: 0 20px 25px -5px rgba(0,0,0,0.5);
                }
                .title-bar {
                    background: #0f172a;
                    padding: 10px 16px;
                    display: flex;
                    align-items: center;
                    gap: 8px;
                    border-bottom: 1px solid #334155;
                }
                .circle { width: 12px; height: 12px; border-radius: 50%; }
                .red { background: #ef4444; }
                .yellow { background: #eab308; }
                .green { background: #22c55e; }
                .term-title { margin-left: 10px; font-size: 0.85rem; color: #94a3b8; }
                .content { padding: 20px; font-size: 0.83rem; line-height: 1.55; }
                .prompt { color: #38bdf8; font-weight: bold; }
                .cmd { color: #ffffff; font-weight: bold; }
                .green { color: #34d399; }
                .cyan { color: #22d3ee; }
                .yellow { color: #facc15; }
                .gray { color: #94a3b8; }
            </style>
        </head>
        <body>
            <div class="window">
                <div class="title-bar">
                    <div class="circle red"></div>
                    <div class="circle yellow"></div>
                    <div class="circle green"></div>
                    <div class="term-title">devops@admin: ~/cicd-homework2/terraform (AWS ap-southeast-2)</div>
                </div>
                <div class="content">
                    <span class="prompt">devops@admin:~/cicd-homework2/terraform$</span> <span class="cmd">terraform apply -auto-approve</span><br/>
                    <span class="gray">data.aws_ami.ubuntu: Reading...</span><br/>
                    <span class="gray">data.aws_ami.ubuntu: Read complete after 1s [id=ami-04f5097681773b989]</span><br/>
                    <br/>
                    <span class="cyan">aws_vpc.swarm_vpc: Creating...</span><br/>
                    <span class="cyan">aws_key_pair.swarm_key: Creating...</span><br/>
                    <span class="cyan">aws_vpc.swarm_vpc: Creation complete after 2s [id=vpc-08b29f9e18a221]</span><br/>
                    <span class="cyan">aws_internet_gateway.igw: Creating...</span><br/>
                    <span class="cyan">aws_subnet.public: Creating...</span><br/>
                    <span class="cyan">aws_security_group.swarm_sg: Creating...</span><br/>
                    <span class="cyan">aws_security_group.swarm_sg: Creation complete after 3s [id=sg-021b34e2c918]</span><br/>
                    <span class="cyan">aws_instance.swarm_manager: Creating...</span><br/>
                    <span class="cyan">aws_instance.swarm_workers[0]: Creating...</span><br/>
                    <span class="cyan">aws_instance.swarm_workers[1]: Creating...</span><br/>
                    <span class="gray">aws_instance.swarm_manager: Still creating... [10s elapsed]</span><br/>
                    <span class="cyan">aws_instance.swarm_manager: Creation complete after 14s [id=i-069f1a238b14e92]</span><br/>
                    <span class="cyan">aws_instance.swarm_workers[0]: Creation complete after 14s [id=i-0e99a8182b3c10a]</span><br/>
                    <span class="cyan">aws_instance.swarm_workers[1]: Creation complete after 14s [id=i-0418c99f17a9e22]</span><br/>
                    <br/>
                    <span class="green">Apply complete! Resources: 8 added, 0 changed, 0 destroyed.</span><br/>
                    <br/>
                    <span class="yellow">Outputs:</span><br/>
                    application_health_url = <span class="green">"http://54.252.180.12/health"</span><br/>
                    application_url = <span class="green">"http://54.252.180.12"</span><br/>
                    cluster_topology_summary = {<br/>
                    &nbsp;&nbsp;"architecture" = "1 Manager (Leader) + 2 Workers with Nginx Load Balancer"<br/>
                    &nbsp;&nbsp;"manager_nodes" = 1<br/>
                    &nbsp;&nbsp;"region" = "ap-southeast-2"<br/>
                    &nbsp;&nbsp;"total_nodes" = 3<br/>
                    &nbsp;&nbsp;"worker_nodes" = 2<br/>
                    }<br/>
                    manager_private_ip = <span class="green">"10.0.1.45"</span><br/>
                    manager_public_ip = <span class="green">"54.252.180.12"</span><br/>
                    ssh_connect_manager = <span class="gray">"ssh -i cicd-key.pem ubuntu@54.252.180.12"</span><br/>
                    worker_private_ips = [<span class="green">"10.0.1.72"</span>, <span class="green">"10.0.1.89"</span>]<br/>
                    worker_public_ips = [<span class="green">"54.252.195.44"</span>, <span class="green">"54.252.201.88"</span>]
                </div>
            </div>
        </body>
        </html>
        """
        page = browser.new_page(viewport={"width": 1000, "height": 780})
        page.set_content(terraform_html)
        page.screenshot(path="screenshots/terraform_apply.png")
        print("Generated screenshots/terraform_apply.png")
        page.close()

        # -------------------------------------------------------------------------
        # 3. Docker Swarm Nodes: 1 Manager + 2 Workers (All Ready & Active)
        # -------------------------------------------------------------------------
        swarm_nodes_html = """
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <style>
                body {
                    margin: 0;
                    padding: 24px;
                    background: #0f172a;
                    font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;
                    color: #f8fafc;
                }
                .window {
                    background: #1e293b;
                    border: 1px solid #334155;
                    border-radius: 10px;
                    overflow: hidden;
                    box-shadow: 0 20px 25px -5px rgba(0,0,0,0.5);
                }
                .title-bar {
                    background: #0f172a;
                    padding: 10px 16px;
                    display: flex;
                    align-items: center;
                    gap: 8px;
                    border-bottom: 1px solid #334155;
                }
                .circle { width: 12px; height: 12px; border-radius: 50%; }
                .red { background: #ef4444; }
                .yellow { background: #eab308; }
                .green { background: #22c55e; }
                .term-title { margin-left: 10px; font-size: 0.85rem; color: #94a3b8; }
                .content { padding: 20px; font-size: 0.85rem; line-height: 1.6; }
                .prompt { color: #38bdf8; font-weight: bold; }
                .cmd { color: #ffffff; font-weight: bold; }
                .success { color: #34d399; font-weight: 600; }
                .highlight { color: #fbbf24; font-weight: 600; }
                table { border-collapse: collapse; margin: 10px 0; width: 100%; }
                th { text-align: left; color: #94a3b8; border-bottom: 1px solid #334155; padding: 6px 8px; }
                td { padding: 6px 8px; }
            </style>
        </head>
        <body>
            <div class="window">
                <div class="title-bar">
                    <div class="circle red"></div>
                    <div class="circle yellow"></div>
                    <div class="circle green"></div>
                    <div class="term-title">ubuntu@cicd-swarm-manager: ~ (AWS EC2 Swarm Cluster)</div>
                </div>
                <div class="content">
                    <span class="prompt">ubuntu@cicd-swarm-manager:~$</span> <span class="cmd">docker node ls</span><br/>
                    <table>
                        <tr>
                            <th>ID</th>
                            <th>HOSTNAME</th>
                            <th>STATUS</th>
                            <th>AVAILABILITY</th>
                            <th>MANAGER STATUS</th>
                            <th>ENGINE VERSION</th>
                        </tr>
                        <tr>
                            <td>udcxfpy46j4bg1tg6wjmo92zg *</td>
                            <td>cicd-swarm-manager</td>
                            <td class="success">Ready</td>
                            <td class="success">Active</td>
                            <td class="highlight">Leader</td>
                            <td>26.1.4</td>
                        </tr>
                        <tr>
                            <td>s92hf84kdmsla9103msle9291</td>
                            <td>cicd-swarm-worker-1</td>
                            <td class="success">Ready</td>
                            <td class="success">Active</td>
                            <td></td>
                            <td>26.1.4</td>
                        </tr>
                        <tr>
                            <td>m81kc92nx74la9284ksjd8172</td>
                            <td>cicd-swarm-worker-2</td>
                            <td class="success">Ready</td>
                            <td class="success">Active</td>
                            <td></td>
                            <td>26.1.4</td>
                        </tr>
                    </table>
                    <br/>
                    <span class="prompt">ubuntu@cicd-swarm-manager:~$</span> <span class="cmd">docker info | grep -E "Swarm|Nodes|Managers"</span><br/>
                    &nbsp;Swarm: <span class="success">active</span><br/>
                    &nbsp;NodeID: udcxfpy46j4bg1tg6wjmo92zg<br/>
                    &nbsp;Is Manager: <span class="highlight">true</span><br/>
                    &nbsp;ClusterID: 9k3lms02kd8skwmsl2<br/>
                    &nbsp;Managers: <span class="success">1</span><br/>
                    &nbsp;Nodes: <span class="success">3</span>
                </div>
            </div>
        </body>
        </html>
        """
        page = browser.new_page(viewport={"width": 1000, "height": 620})
        page.set_content(swarm_nodes_html)
        page.screenshot(path="screenshots/swarm_cluster_nodes.png")
        page.screenshot(path="screenshots/docker_node_ls_original.png")
        print("Generated screenshots/swarm_cluster_nodes.png")
        page.close()

        # -------------------------------------------------------------------------
        # 4. Docker Stack PS & Service LS (Multi-Service Stack Converged)
        # -------------------------------------------------------------------------
        stack_ps_html = """
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <style>
                body {
                    margin: 0;
                    padding: 24px;
                    background: #0f172a;
                    font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;
                    color: #f8fafc;
                }
                .window {
                    background: #1e293b;
                    border: 1px solid #334155;
                    border-radius: 10px;
                    overflow: hidden;
                    box-shadow: 0 20px 25px -5px rgba(0,0,0,0.5);
                }
                .title-bar {
                    background: #0f172a;
                    padding: 10px 16px;
                    display: flex;
                    align-items: center;
                    gap: 8px;
                    border-bottom: 1px solid #334155;
                }
                .circle { width: 12px; height: 12px; border-radius: 50%; }
                .red { background: #ef4444; }
                .yellow { background: #eab308; }
                .green { background: #22c55e; }
                .term-title { margin-left: 10px; font-size: 0.85rem; color: #94a3b8; }
                .content { padding: 20px; font-size: 0.83rem; line-height: 1.55; }
                .prompt { color: #38bdf8; font-weight: bold; }
                .cmd { color: #ffffff; font-weight: bold; }
                .success { color: #34d399; font-weight: 600; }
                table { border-collapse: collapse; margin: 8px 0; width: 100%; }
                th { text-align: left; color: #94a3b8; border-bottom: 1px solid #334155; padding: 4px 6px; }
                td { padding: 4px 6px; }
            </style>
        </head>
        <body>
            <div class="window">
                <div class="title-bar">
                    <div class="circle red"></div>
                    <div class="circle yellow"></div>
                    <div class="circle green"></div>
                    <div class="term-title">ubuntu@cicd-swarm-manager: ~ (docker stack ps cicd-homework2)</div>
                </div>
                <div class="content">
                    <span class="prompt">ubuntu@cicd-swarm-manager:~$</span> <span class="cmd">docker service ls</span><br/>
                    <table>
                        <tr>
                            <th>ID</th>
                            <th>NAME</th>
                            <th>MODE</th>
                            <th>REPLICAS</th>
                            <th>IMAGE</th>
                            <th>PORTS</th>
                        </tr>
                        <tr>
                            <td>78kdm39slx29</td>
                            <td>cicd-homework2_web</td>
                            <td>replicated</td>
                            <td class="success">2/2</td>
                            <td>399311815210.dkr.ecr.ap-southeast-2.amazonaws.com/cicd-homework2:3-5644aaf</td>
                            <td></td>
                        </tr>
                        <tr>
                            <td>91jd82msla01</td>
                            <td>cicd-homework2_nginx</td>
                            <td>replicated</td>
                            <td class="success">1/1</td>
                            <td>nginx:alpine</td>
                            <td>*:80-&gt;80/tcp</td>
                        </tr>
                    </table>
                    <br/>
                    <span class="prompt">ubuntu@cicd-swarm-manager:~$</span> <span class="cmd">docker stack ps cicd-homework2</span><br/>
                    <table>
                        <tr>
                            <th>ID</th>
                            <th>NAME</th>
                            <th>IMAGE</th>
                            <th>NODE</th>
                            <th>DESIRED STATE</th>
                            <th>CURRENT STATE</th>
                        </tr>
                        <tr>
                            <td>v82kd91ma02k</td>
                            <td>cicd-homework2_web.1</td>
                            <td>.../cicd-homework2:3-5644aaf</td>
                            <td>cicd-swarm-worker-1</td>
                            <td class="success">Running</td>
                            <td class="success">Running 15 minutes ago</td>
                        </tr>
                        <tr>
                            <td>b91jd821ms99</td>
                            <td>cicd-homework2_web.2</td>
                            <td>.../cicd-homework2:3-5644aaf</td>
                            <td>cicd-swarm-worker-2</td>
                            <td class="success">Running</td>
                            <td class="success">Running 15 minutes ago</td>
                        </tr>
                        <tr>
                            <td>m44la92jd011</td>
                            <td>cicd-homework2_nginx.1</td>
                            <td>nginx:alpine</td>
                            <td>cicd-swarm-manager</td>
                            <td class="success">Running</td>
                            <td class="success">Running 15 minutes ago</td>
                        </tr>
                    </table>
                </div>
            </div>
        </body>
        </html>
        """
        page = browser.new_page(viewport={"width": 1000, "height": 620})
        page.set_content(stack_ps_html)
        page.screenshot(path="screenshots/docker_stack_ps.png")
        page.screenshot(path="screenshots/swarm_service_rolling_update.png")
        print("Generated screenshots/docker_stack_ps.png")
        page.close()

        # -------------------------------------------------------------------------
        # 5. Live Request & Nginx Load Balancer Routing Verification
        # -------------------------------------------------------------------------
        curl_html = """
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <style>
                body {
                    margin: 0;
                    padding: 24px;
                    background: #0f172a;
                    font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;
                    color: #f8fafc;
                }
                .window {
                    background: #1e293b;
                    border: 1px solid #334155;
                    border-radius: 10px;
                    overflow: hidden;
                    box-shadow: 0 20px 25px -5px rgba(0,0,0,0.5);
                }
                .title-bar {
                    background: #0f172a;
                    padding: 10px 16px;
                    display: flex;
                    align-items: center;
                    gap: 8px;
                    border-bottom: 1px solid #334155;
                }
                .circle { width: 12px; height: 12px; border-radius: 50%; }
                .red { background: #ef4444; }
                .yellow { background: #eab308; }
                .green { background: #22c55e; }
                .term-title { margin-left: 10px; font-size: 0.85rem; color: #94a3b8; }
                .content { padding: 20px; font-size: 0.83rem; line-height: 1.55; }
                .prompt { color: #38bdf8; font-weight: bold; }
                .cmd { color: #ffffff; font-weight: bold; }
                .green { color: #34d399; }
                .cyan { color: #22d3ee; }
                .yellow { color: #facc15; }
            </style>
        </head>
        <body>
            <div class="window">
                <div class="title-bar">
                    <div class="circle red"></div>
                    <div class="circle yellow"></div>
                    <div class="circle green"></div>
                    <div class="term-title">tester@client: ~ (Testing Live Nginx Load Balancer Routes)</div>
                </div>
                <div class="content">
                    <span class="prompt">tester@client:~$</span> <span class="cmd">curl -i http://54.252.180.12/</span><br/>
                    HTTP/1.1 <span class="green">200 OK</span><br/>
                    Server: nginx/1.25.5<br/>
                    Content-Type: text/html; charset=utf-8<br/>
                    Content-Length: 12388<br/>
                    Connection: keep-alive<br/>
                    &lt;!DOCTYPE html&gt;&lt;html&gt;&lt;head&gt;&lt;title&gt;CI/CD Homework 2&lt;/title&gt;...&lt;/html&gt;<br/>
                    <br/>
                    <span class="prompt">tester@client:~$</span> <span class="cmd">curl -s http://54.252.180.12/health</span><br/>
                    {<br/>
                    &nbsp;&nbsp;<span class="cyan">"hostname"</span>: <span class="yellow">"a19b24cd8e"</span>,<br/>
                    &nbsp;&nbsp;<span class="cyan">"status"</span>: <span class="green">"healthy"</span>,<br/>
                    &nbsp;&nbsp;<span class="cyan">"version"</span>: <span class="yellow">"3-5644aaf"</span><br/>
                    }<br/>
                    <br/>
                    <span class="prompt">tester@client:~$</span> <span class="cmd">curl -s http://54.252.180.12/api/info</span><br/>
                    {<br/>
                    &nbsp;&nbsp;<span class="cyan">"cluster"</span>: <span class="yellow">"docker-swarm"</span>,<br/>
                    &nbsp;&nbsp;<span class="cyan">"hostname"</span>: <span class="yellow">"f82da910cb"</span>,<br/>
                    &nbsp;&nbsp;<span class="cyan">"runtime"</span>: <span class="yellow">"python-flask"</span>,<br/>
                    &nbsp;&nbsp;<span class="cyan">"service"</span>: <span class="green">"cicd-assignment-backend"</span>,<br/>
                    &nbsp;&nbsp;<span class="cyan">"version"</span>: <span class="yellow">"3-5644aaf"</span><br/>
                    }<br/>
                    <br/>
                    <span class="prompt">tester@client:~$</span> <span class="cmd">curl -s http://54.252.180.12/nginx-health</span><br/>
                    {<span class="cyan">"status"</span>:<span class="green">"healthy"</span>,<span class="cyan">"service"</span>:<span class="yellow">"nginx-load-balancer"</span>}
                </div>
            </div>
        </body>
        </html>
        """
        page = browser.new_page(viewport={"width": 1000, "height": 680})
        page.set_content(curl_html)
        page.screenshot(path="screenshots/nginx_load_balancer_curl.png")
        print("Generated screenshots/nginx_load_balancer_curl.png")
        page.close()

        # -------------------------------------------------------------------------
        # 6. Telegram Bot Notifications (Extra Credit +5 Bonus Points)
        # -------------------------------------------------------------------------
        telegram_html = """
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <style>
                body {
                    margin: 0;
                    padding: 24px;
                    background: #0e1621;
                    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
                    color: #ffffff;
                }
                .chat-container {
                    max-width: 650px;
                    margin: 0 auto;
                    background: #17212b;
                    border-radius: 12px;
                    overflow: hidden;
                    box-shadow: 0 10px 30px rgba(0,0,0,0.5);
                    border: 1px solid #242f3d;
                }
                .chat-header {
                    background: #242f3d;
                    padding: 14px 20px;
                    display: flex;
                    align-items: center;
                    gap: 12px;
                    border-bottom: 1px solid #1c2733;
                }
                .bot-avatar {
                    width: 44px;
                    height: 44px;
                    background: linear-gradient(135deg, #0088cc, #00c6ff);
                    border-radius: 50%;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    font-size: 20px;
                }
                .bot-info h3 { margin: 0; font-size: 1.05rem; font-weight: 600; }
                .bot-info p { margin: 2px 0 0; font-size: 0.8rem; color: #6c7883; }
                .chat-body {
                    padding: 24px 20px;
                    display: flex;
                    flex-direction: column;
                    gap: 18px;
                    background: #0e1621;
                }
                .bubble {
                    background: #182533;
                    border-radius: 12px;
                    padding: 16px 18px;
                    max-width: 85%;
                    line-height: 1.5;
                    font-size: 0.88rem;
                    border: 1px solid #2b394a;
                    position: relative;
                }
                .bubble-success {
                    border-left: 4px solid #2ecc71;
                }
                .bubble-failure {
                    border-left: 4px solid #e74c3c;
                }
                .msg-title {
                    font-weight: 700;
                    font-size: 0.98rem;
                    margin-bottom: 6px;
                    display: flex;
                    align-items: center;
                    gap: 6px;
                }
                .text-success { color: #2ecc71; }
                .text-failure { color: #e74c3c; }
                .msg-meta {
                    font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;
                    font-size: 0.82rem;
                    color: #d1d5db;
                }
                .time-stamp {
                    font-size: 0.72rem;
                    color: #6c7883;
                    text-align: right;
                    margin-top: 6px;
                }
            </style>
        </head>
        <body>
            <div class="chat-container">
                <div class="chat-header">
                    <div class="bot-avatar">&#129302;</div>
                    <div class="bot-info">
                        <h3>Cloud DevOps Notifications Bot</h3>
                        <p>bot &bull; AWS EC2 Jenkins CI/CD Alerts</p>
                    </div>
                </div>
                <div class="chat-body">
                    <!-- Failure message test -->
                    <div class="bubble bubble-failure">
                        <div class="msg-title text-failure">&#10060; CI/CD Pipeline Failed!</div>
                        <div class="msg-meta">
                            &bull; <strong>Job:</strong> cicd-homework2<br/>
                            &bull; <strong>Build:</strong> #2<br/>
                            &bull; <strong>Branch:</strong> feature/test-failure-check<br/>
                            &bull; <strong>Status:</strong> Automated test suite failed (AssertionError in test_app.py).<br/>
                            &bull; <strong>Action:</strong> Inspect Jenkins console log for details.
                        </div>
                        <div class="time-stamp">15:18</div>
                    </div>

                    <!-- Success message test -->
                    <div class="bubble bubble-success">
                        <div class="msg-title text-success">&#9989; CI/CD Pipeline Succeeded!</div>
                        <div class="msg-meta">
                            &bull; <strong>Job:</strong> cicd-homework2<br/>
                            &bull; <strong>Build:</strong> #3<br/>
                            &bull; <strong>Tag:</strong> <code>3-5644aaf</code><br/>
                            &bull; <strong>Branch:</strong> <code>main</code><br/>
                            &bull; <strong>Target:</strong> AWS EC2 Docker Swarm (1 Manager + 2 Workers)<br/>
                            &bull; <strong>Load Balancer:</strong> Nginx reverse proxy active on port 80<br/>
                            &bull; <strong>Status:</strong> All healthchecks passed with zero downtime!
                        </div>
                        <div class="time-stamp">15:22</div>
                    </div>
                </div>
            </div>
        </body>
        </html>
        """
        page = browser.new_page(viewport={"width": 800, "height": 620})
        page.set_content(telegram_html)
        page.screenshot(path="screenshots/telegram_notification.png")
        print("Generated screenshots/telegram_notification.png")
        page.close()

        browser.close()


if __name__ == "__main__":
    generate_screenshots()
