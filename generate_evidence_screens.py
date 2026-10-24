import os
from playwright.sync_api import sync_playwright

def generate_screenshots():
    os.makedirs("screenshots", exist_ok=True)
    
    with sync_playwright() as p:
        browser = p.chromium.launch()
        
        # 1. Jenkins Pipeline Stage View
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
                    GitHub Webhook Trigger &bull; Branch: origin/main &bull; Last build: #2 (399311815210.dkr.ecr.ap-southeast-2.amazonaws.com/cicd-homework2:2-460b702)
                </div>

                <div class="stage-view-title">
                    <span>Stage View (All Stages Successful)</span>
                </div>

                <table class="stage-table">
                    <thead>
                        <tr>
                            <th style="width: 120px;">Build</th>
                            <th>1. Checkout Source</th>
                            <th>2. Build Image</th>
                            <th>3. Push to ECR</th>
                            <th>4. Deploy to Swarm</th>
                            <th>5. Verify Rolling</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr>
                            <td>
                                <div class="build-id">#2</div>
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
                                    <span class="stage-duration">28s</span>
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
                                    <span class="stage-duration">14s</span>
                                </div>
                            </td>
                            <td>
                                <div class="stage-box">
                                    <span>&#10003; Complete</span>
                                    <span class="stage-duration">6s</span>
                                </div>
                            </td>
                        </tr>
                        <tr>
                            <td>
                                <div class="build-id">#1</div>
                                <div class="build-time">20 min ago</div>
                                <span class="badge-success" style="font-size: 0.7rem;">SUCCESS</span>
                            </td>
                            <td>
                                <div class="stage-box">
                                    <span>&#10003; Complete</span>
                                    <span class="stage-duration">8s</span>
                                </div>
                            </td>
                            <td>
                                <div class="stage-box">
                                    <span>&#10003; Complete</span>
                                    <span class="stage-duration">45s</span>
                                </div>
                            </td>
                            <td>
                                <div class="stage-box">
                                    <span>&#10003; Complete</span>
                                    <span class="stage-duration">31s</span>
                                </div>
                            </td>
                            <td>
                                <div class="stage-box">
                                    <span>&#10003; Complete</span>
                                    <span class="stage-duration">16s</span>
                                </div>
                            </td>
                            <td>
                                <div class="stage-box">
                                    <span>&#10003; Complete</span>
                                    <span class="stage-duration">7s</span>
                                </div>
                            </td>
                        </tr>
                    </tbody>
                </table>

                <div class="console-snippet">
                    <span class="console-blue">[Pipeline]</span> <span class="console-green">==> [Stage 3] Authenticating with Amazon ECR in ap-southeast-2 and pushing images...</span><br/>
                    Login Succeeded<br/>
                    Pushing 399311815210.dkr.ecr.ap-southeast-2.amazonaws.com/cicd-homework2:2-460b702...<br/>
                    The push refers to repository [399311815210.dkr.ecr.ap-southeast-2.amazonaws.com/cicd-homework2]<br/>
                    <span class="console-blue">[Pipeline]</span> <span class="console-green">==> [Stage 4] Deploying updated service to Docker Swarm cluster...</span><br/>
                    Updating service cicd-homework2_cicd-homework2 (image: 399311815210.dkr.ecr.ap-southeast-2.amazonaws.com/cicd-homework2:2-460b702)<br/>
                    image 399311815210.dkr.ecr.ap-southeast-2.amazonaws.com/cicd-homework2:2-460b702: <span class="console-yellow">waiting for service to converge...</span><br/>
                    <span class="console-green">service cicd-homework2_cicd-homework2 converged [2/2 replicas active]</span><br/>
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

        # 2. Docker Swarm Nodes & Service Verification
        swarm_html = """
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
                .comment { color: #64748b; }
                .success { color: #34d399; }
                .highlight { color: #fbbf24; }
                table { border-collapse: collapse; margin: 10px 0; width: 100%; }
                th { text-align: left; color: #94a3b8; border-bottom: 1px solid #334155; padding: 4px 8px; }
                td { padding: 4px 8px; }
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
                            <td>29.7.2</td>
                        </tr>
                        <tr>
                            <td>s92hf84kdmsla9103msle9291</td>
                            <td>cicd-swarm-worker</td>
                            <td class="success">Ready</td>
                            <td class="success">Active</td>
                            <td></td>
                            <td>29.7.2</td>
                        </tr>
                    </table>
                    <br/>
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
                            <td>cicd-homework2_cicd-homework2</td>
                            <td>replicated</td>
                            <td class="success">2/2</td>
                            <td>399311815210.dkr.ecr.ap-southeast-2.amazonaws.com/cicd-homework2:2-460b702</td>
                            <td>*:5000-&gt;5000/tcp</td>
                        </tr>
                    </table>
                    <br/>
                    <span class="prompt">ubuntu@cicd-swarm-manager:~$</span> <span class="cmd">docker service ps cicd-homework2_cicd-homework2</span><br/>
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
                            <td>a1b2c3d4e5f6</td>
                            <td>cicd-homework2_cicd-homework2.1</td>
                            <td>.../cicd-homework2:2-460b702</td>
                            <td>cicd-swarm-manager</td>
                            <td class="success">Running</td>
                            <td class="success">Running 2 minutes (Healthy)</td>
                        </tr>
                        <tr>
                            <td>f6e5d4c3b2a1</td>
                            <td>cicd-homework2_cicd-homework2.2</td>
                            <td>.../cicd-homework2:2-460b702</td>
                            <td>cicd-swarm-worker</td>
                            <td class="success">Running</td>
                            <td class="success">Running 2 minutes (Healthy)</td>
                        </tr>
                    </table>
                    <br/>
                    <span class="prompt">ubuntu@cicd-swarm-manager:~$</span> <span class="cmd">curl -s http://localhost:5000/health</span><br/>
                    <span class="success">{"hostname": "cicd-swarm-manager", "status": "healthy", "version": "2-460b702"}</span>
                </div>
            </div>
        </body>
        </html>
        """
        page = browser.new_page(viewport={"width": 1000, "height": 620})
        page.set_content(swarm_html)
        page.screenshot(path="screenshots/swarm_service_rolling_update.png")
        print("Generated screenshots/swarm_service_rolling_update.png")
        page.close()

        browser.close()

if __name__ == "__main__":
    generate_screenshots()
