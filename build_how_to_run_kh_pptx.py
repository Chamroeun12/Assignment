import os
import pptx
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE

def create_khmer_presentation():
    prs = pptx.Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]

    # Color Tokens
    NAVY_DARK = RGBColor(15, 23, 42)       # #0F172A
    NAVY_CARD = RGBColor(30, 41, 59)       # #1E293B
    BLUE_ACCENT = RGBColor(2, 132, 199)    # #0284C7
    BLUE_LIGHT = RGBColor(224, 242, 254)   # #E0F2FE
    TEXT_DARK = RGBColor(30, 41, 59)       # #1E293B
    TEXT_MUTED = RGBColor(100, 116, 139)   # #64748B
    TEXT_LIGHT = RGBColor(248, 250, 252)   # #F8FAFC
    CARD_BG = RGBColor(241, 245, 249)      # #F1F5F9
    BORDER_COLOR = RGBColor(203, 213, 225) # #CBD5E1
    GREEN_SUCCESS = RGBColor(22, 163, 74)  # #16A34A
    GREEN_LIGHT = RGBColor(220, 252, 231)  # #DCFCE7
    CODE_BG = RGBColor(15, 23, 42)         # #0F172A
    CODE_TEXT = RGBColor(56, 189, 248)     # #38BDF8

    KHMER_FONT = "Noto Sans Khmer"
    CODE_FONT = "Consolas"

    def add_header(slide, category, title, dark=False):
        # Category tracker tag
        tag_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.4), Inches(11.5), Inches(0.35))
        tf_tag = tag_box.text_frame
        tf_tag.word_wrap = True
        tf_tag.margin_left = tf_tag.margin_top = tf_tag.margin_right = tf_tag.margin_bottom = 0
        p_tag = tf_tag.paragraphs[0]
        p_tag.text = category.upper()
        p_tag.font.name = KHMER_FONT
        p_tag.font.size = Pt(10.5)
        p_tag.font.bold = True
        p_tag.font.color.rgb = BLUE_ACCENT

        # Title
        title_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.75), Inches(11.5), Inches(0.75))
        tf_title = title_box.text_frame
        tf_title.word_wrap = True
        tf_title.margin_left = tf_title.margin_top = tf_title.margin_right = tf_title.margin_bottom = 0
        p_title = tf_title.paragraphs[0]
        p_title.text = title
        p_title.font.name = KHMER_FONT
        p_title.font.size = Pt(21)
        p_title.font.bold = True
        p_title.font.color.rgb = TEXT_LIGHT if dark else NAVY_DARK

        # Underline bar
        line = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(1.5), Inches(2.2), Inches(0.04))
        line.fill.solid()
        line.fill.fore_color.rgb = BLUE_ACCENT
        line.line.color.rgb = BLUE_ACCENT

    def add_card(slide, left, top, width, height, bg_color=CARD_BG, border_color=BORDER_COLOR):
        shape = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
        shape.fill.solid()
        shape.fill.fore_color.rgb = bg_color
        shape.line.color.rgb = border_color
        shape.line.width = Pt(1)
        return shape

    def add_code_card(slide, left, top, width, height, code_text):
        card = add_card(slide, left, top, width, height, bg_color=CODE_BG, border_color=NAVY_CARD)
        tb = slide.shapes.add_textbox(left + Inches(0.15), top + Inches(0.12), width - Inches(0.3), height - Inches(0.24))
        tf = tb.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0
        p = tf.paragraphs[0]
        p.text = code_text.strip()
        p.font.name = CODE_FONT
        p.font.size = Pt(9.5)
        p.font.color.rgb = CODE_TEXT
        return card

    # =========================================================================
    # SLIDE 1: COVER SLIDE
    # =========================================================================
    s1 = prs.slides.add_slide(blank_layout)
    bg1 = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(7.5))
    bg1.fill.solid()
    bg1.fill.fore_color.rgb = NAVY_DARK
    bg1.line.fill.background()

    # Title Card
    c1 = add_card(s1, Inches(0.8), Inches(0.8), Inches(11.733), Inches(5.9), bg_color=NAVY_CARD, border_color=RGBColor(51, 65, 85))
    
    t_box = s1.shapes.add_textbox(Inches(1.2), Inches(1.2), Inches(10.9), Inches(3.2))
    tf1 = t_box.text_frame
    tf1.word_wrap = True
    
    p_tag = tf1.paragraphs[0]
    p_tag.text = "CLOUD COMPUTING CAPSTONE — HOW TO RUN GUIDE"
    p_tag.font.name = "Segoe UI"
    p_tag.font.size = Pt(12)
    p_tag.font.bold = True
    p_tag.font.color.rgb = RGBColor(56, 189, 248)

    p_t = tf1.add_paragraph()
    p_t.text = "សៀវភៅណែនាំអំពីរបៀបដំណើរការគម្រោង Cloud Computing"
    p_t.font.name = KHMER_FONT
    p_t.font.size = Pt(26)
    p_t.font.bold = True
    p_t.font.color.rgb = TEXT_LIGHT

    p_sub = tf1.add_paragraph()
    p_sub.text = "ការដំឡើង និងដំណើរការប្រព័ន្ធ Cloud ស្វ័យប្រវត្តិតាមរយៈ Docker Swarm, Terraform, Nginx និង Jenkins"
    p_sub.font.name = KHMER_FONT
    p_sub.font.size = Pt(14)
    p_sub.font.color.rgb = RGBColor(148, 163, 184)

    # Divider line
    div = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(1.2), Inches(4.3), Inches(10.9), Inches(0.02))
    div.fill.solid()
    div.fill.fore_color.rgb = RGBColor(51, 65, 85)
    div.line.fill.background()

    # Metadata badges
    m_box = s1.shapes.add_textbox(Inches(1.2), Inches(4.5), Inches(10.9), Inches(1.8))
    tf_m = m_box.text_frame
    tf_m.word_wrap = True
    
    p_m1 = tf_m.paragraphs[0]
    p_m1.text = "👤 និស្សិតរៀបចំ៖ ចំរើន សារ៉ាន់ (Chamroeun Saran)  |  🎓 ថ្នាក់សិក្សា៖ Master of Science in Cloud Computing"
    p_m1.font.name = KHMER_FONT
    p_m1.font.size = Pt(11)
    p_m1.font.color.rgb = TEXT_LIGHT

    p_m2 = tf_m.add_paragraph()
    p_m2.text = "🌐 Git Repository: https://github.com/Chamroeun12/Assignment  |  📍 តំបន់ AWS: Sydney (ap-southeast-2)"
    p_m2.font.name = KHMER_FONT
    p_m2.font.size = Pt(11)
    p_m2.font.color.rgb = RGBColor(148, 163, 184)

    p_m3 = tf_m.add_paragraph()
    p_m3.text = "🚀 Live Cluster IP: 16.178.206.23  |  📅 កាលបរិច្ឆេទ៖ ខែវិច្ឆិកា ឆ្នាំ ២០២៦"
    p_m3.font.name = KHMER_FONT
    p_m3.font.size = Pt(11)
    p_m3.font.bold = True
    p_m3.font.color.rgb = RGBColor(56, 189, 248)

    # =========================================================================
    # SLIDE 2: SYSTEM ARCHITECTURE
    # =========================================================================
    s2 = prs.slides.add_slide(blank_layout)
    add_header(s2, "១. ស្ថាបត្យកម្មប្រព័ន្ធ", "ទិដ្ឋភាពទូទៅនៃស្ថាបត្យកម្មគម្រោង (System Architecture)")

    cards_s2 = [
        ("Terraform (IaC)", "បង្កើតប្រព័ន្ធបណ្តាញ VPC (10.0.0.0/16), Security Groups, និង EC2 ចំនួន ៣ (១ Manager + ២ Workers) ដោយស្វ័យប្រវត្តិតាមកូដ HCL។"),
        ("Docker Swarm", "គ្រប់គ្រងកុងតឺន័រលើម៉ាស៊ីនមេចំនួន ៣ ជាមួយការផ្ទេរបន្ទុក និងការផ្លាស់ប្តូរកំណែថ្មីដោយគ្មានការដាច់សេវា (Zero-Downtime Rolling Update)។"),
        ("Nginx Load Balancer", "Reverse Proxy លើ Port 80 ចែករំលែកចរាចរណ៍ (Round-Robin Traffic) ទៅកាន់ Replicated Flask Application ខាងក្រោយ។"),
        ("Jenkins CI/CD", "ស្វ័យប្រវត្តិកម្មនៃការទាញយកកូដ, ត្រួតពិនិត្យ (Flake8), តេស្ត (Pytest), ស្កេនមេរោគ (Trivy), និងផ្ញើសារជូនដំណឹងទៅកាន់ Telegram។")
    ]

    for idx, (title, desc) in enumerate(cards_s2):
        col = idx % 2
        row = idx // 2
        left = Inches(0.8 + col * 5.95)
        top = Inches(1.8 + row * 2.6)
        add_card(s2, left, top, Inches(5.75), Inches(2.35))
        
        tb = s2.shapes.add_textbox(left + Inches(0.3), top + Inches(0.25), Inches(5.15), Inches(1.85))
        tf = tb.text_frame
        tf.word_wrap = True
        
        p = tf.paragraphs[0]
        p.text = f"🔹 {title}"
        p.font.name = KHMER_FONT
        p.font.size = Pt(14)
        p.font.bold = True
        p.font.color.rgb = BLUE_ACCENT
        
        p_d = tf.add_paragraph()
        p_d.text = desc
        p_d.font.name = KHMER_FONT
        p_d.font.size = Pt(11)
        p_d.font.color.rgb = TEXT_DARK

    # =========================================================================
    # SLIDE 3: PREREQUISITES
    # =========================================================================
    s3 = prs.slides.add_slide(blank_layout)
    add_header(s3, "២. តម្រូវការប្រព័ន្ធ", "តម្រូវការចាំបាច់មុនពេលចាប់ផ្តើមដំណើរការ (Prerequisites)")

    # Table
    table_shape = s3.shapes.add_table(6, 4, Inches(0.8), Inches(1.8), Inches(11.733), Inches(4.8))
    table = table_shape.table
    table.columns[0].width = Inches(2.2)
    table.columns[1].width = Inches(2.8)
    table.columns[2].width = Inches(2.8)
    table.columns[3].width = Inches(3.933)

    headers = ["កម្មវិធី / ឧបករណ៍", "សម្រាប់រត់លើ Laptop ផ្ទាល់ខ្លួន", "សម្រាប់រត់លើ AWS Cloud", "ការណែនាំបន្ថែម"]
    for i, h in enumerate(headers):
        cell = table.cell(0, i)
        cell.fill.solid()
        cell.fill.fore_color.rgb = NAVY_DARK
        p = cell.text_frame.paragraphs[0]
        p.text = h
        p.font.name = KHMER_FONT
        p.font.size = Pt(11)
        p.font.bold = True
        p.font.color.rgb = TEXT_LIGHT

    rows_data = [
        ("Git", "ចាំបាច់ត្រូវមាន", "ចាំបាច់ត្រូវមាន", "កំណែ 2.30+ សម្រាប់ទាញយក Source Code"),
        ("Docker Desktop", "ចាំបាច់ត្រូវមាន", "មិនចាំបាច់មានទេ", "កំណែ 24.0+ (រួមមាន Docker Compose)"),
        ("AWS CLI", "មិនបាច់មាន", "ចាំបាច់ត្រូវមាន", "កំណត់សិទ្ធិ Access Key & Secret Key"),
        ("Terraform", "មិនបាច់មាន", "ចាំបាច់ត្រូវមាន", "កំណែ 1.5.0+ សម្រាប់បង្កើត Server លើ AWS"),
        ("SSH Key (.pem)", "មិនបាច់មាន", "ចាំបាច់ត្រូវមាន", "ឯកសារ chamroeunsaran.pem សម្រាប់ Login")
    ]
    for row_idx, rdata in enumerate(rows_data, start=1):
        for col_idx, text in enumerate(rdata):
            cell = table.cell(row_idx, col_idx)
            cell.fill.solid()
            cell.fill.fore_color.rgb = RGBColor(255, 255, 255) if row_idx % 2 == 1 else CARD_BG
            p = cell.text_frame.paragraphs[0]
            p.text = text
            p.font.name = KHMER_FONT
            p.font.size = Pt(10.5)
            if col_idx == 0:
                p.font.bold = True
                p.font.color.rgb = NAVY_DARK
            elif text == "ចាំបាច់ត្រូវមាន":
                p.font.bold = True
                p.font.color.rgb = GREEN_SUCCESS
            else:
                p.font.color.rgb = TEXT_MUTED

    # =========================================================================
    # SLIDE 4: METHOD A - LOCAL TESTING
    # =========================================================================
    s4 = prs.slides.add_slide(blank_layout)
    add_header(s4, "៣. វិធីសាស្ត្រទី ១", "ការរត់តេស្តលើ Laptop ផ្ទាល់ខ្លួន (Docker Compose ត្រឹមតែ ៣០ វិនាទី)")

    add_card(s4, Inches(0.8), Inches(1.8), Inches(5.75), Inches(5.1))
    tb_l = s4.shapes.add_textbox(Inches(1.0), Inches(2.0), Inches(5.35), Inches(4.7))
    tf_l = tb_l.text_frame
    tf_l.word_wrap = True
    
    p = tf_l.paragraphs[0]
    p.text = "📌 គុណសម្បត្តិនៃការរត់លើកុំព្យូទ័រផ្ទាល់ខ្លួន："
    p.font.name = KHMER_FONT
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = BLUE_ACCENT
    
    bullet_l = [
        "មិនចាំបាច់មានគណនី AWS ឬចំណាយលុយឡើយ។",
        "ដំណើរការ Full Multi-Service Stack (Flask Backend + Nginx Reverse Proxy) លើ Bridge Network។",
        "ងាយស្រួលសាកល្បងកែប្រែកូដ និងតេស្តមើល UI ភ្លាមៗ។",
        "បើកមើលលើ Browser ត្រឹមតែ៖ http://localhost/",
        "បិទប្រព័ន្ធវិញយ៉ាងងាយស្រួលដោយប្រើ 'docker compose down'។"
    ]
    for b in bullet_l:
        p_b = tf_l.add_paragraph()
        p_b.text = f"• {b}"
        p_b.font.name = KHMER_FONT
        p_b.font.size = Pt(11)
        p_b.font.color.rgb = TEXT_DARK

    # Right Column: Code block
    code_s4 = (
        "# ១. ទាញយកកូដពី GitHub\n"
        "git clone https://github.com/Chamroeun12/Assignment.git\n"
        "cd Assignment\n\n"
        "# ២. បញ្ជាឱ្យ Build និងដំណើរការ Container ទាំងអស់\n"
        "docker compose up --build -d\n\n"
        "# ៣. ពិនិត្យមើលស្ថានភាពកុងតឺន័រ\n"
        "docker compose ps\n\n"
        "# ៤. តេស្ត Endpoints តាមរយៈ curl:\n"
        "curl -i http://localhost/\n"
        "curl -s http://localhost/health\n"
        "curl -s http://localhost/api/info\n"
        "curl -s http://localhost/nginx-health\n\n"
        "# ៥. បិទកុងតឺន័រទាំងអស់ពេលឈប់ប្រើ\n"
        "docker compose down"
    )
    add_code_card(s4, Inches(6.8), Inches(1.8), Inches(5.733), Inches(5.1), code_s4)

    # =========================================================================
    # SLIDE 5: METHOD B - TERRAFORM IAC
    # =========================================================================
    s5 = prs.slides.add_slide(blank_layout)
    add_header(s5, "៤. វិធីសាស្ត្រទី ២", "ការបង្កើតហេដ្ឋារចនាសម្ព័ន្ធលើ AWS ដោយស្វ័យប្រវត្តិ (Terraform)")

    add_card(s5, Inches(0.8), Inches(1.8), Inches(5.75), Inches(5.1))
    tb_t = s5.shapes.add_textbox(Inches(1.0), Inches(2.0), Inches(5.35), Inches(4.7))
    tf_t = tb_t.text_frame
    tf_t.word_wrap = True
    
    p = tf_t.paragraphs[0]
    p.text = "⚙️ ជំហាននៃការបង្កើតម៉ាស៊ីនមេជាមួយ Terraform："
    p.font.name = KHMER_FONT
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = BLUE_ACCENT
    
    tf_steps = [
        "១. កំណត់សិទ្ធិ AWS CLI ជាមួយ Access Key & Secret Key។",
        "២. ដំណើរការ 'terraform init' ដើម្បីដំឡើង AWS Provider Plugins។",
        "៣. ដំណើរការ 'terraform plan' ដើម្បីត្រួតពិនិត្យធនធានដែលត្រូវបង្កើត។",
        "៤. ដំណើរការ 'terraform apply -auto-approve' ដើម្បីបង្កើត VPC, Subnet, Security Groups, និង EC2 ចំនួន ៣ (១ Manager + ២ Workers)។",
        "៥. ទទួលបាន Public IP និង Private IP របស់ម៉ាស៊ីនមេទាំង ៣ ដោយស្វ័យប្រវត្តិ។"
    ]
    for st in tf_steps:
        p_st = tf_t.add_paragraph()
        p_st.text = st
        p_st.font.name = KHMER_FONT
        p_st.font.size = Pt(11)
        p_st.font.color.rgb = TEXT_DARK

    code_s5 = (
        "# ១. កំណត់សិទ្ធិ AWS CLI\n"
        "aws configure\n\n"
        "# ២. ចូលទៅកាន់ថត terraform និងដំណើរការ\n"
        "cd terraform\n"
        "terraform init\n"
        "terraform plan\n"
        "terraform apply -auto-approve\n\n"
        "# លទ្ធផលទទួលបានពី Terraform Outputs:\n"
        "manager_public_ip  = \"16.178.206.23\"\n"
        "manager_private_ip = \"172.31.34.160\"\n"
        "worker_public_ips  = [\"3.107.96.140\", \"13.211.213.228\"]\n"
        "worker_private_ips = [\"172.31.36.22\", \"172.31.47.183\"]\n"
        "application_url    = \"http://16.178.206.23\"\n\n"
        "cd .."
    )
    add_code_card(s5, Inches(6.8), Inches(1.8), Inches(5.733), Inches(5.1), code_s5)

    # =========================================================================
    # SLIDE 6: DOCKER SWARM CLUSTERING
    # =========================================================================
    s6 = prs.slides.add_slide(blank_layout)
    add_header(s6, "៤. វិធីសាស្ត្រទី ២ (បន្ត)", "ការចាប់ផ្តើម និងតភ្ជាប់ Docker Swarm Nodes (Clustering)")

    code_s6_l = (
        "# ១. SSH ចូលទៅកាន់ Manager Node\n"
        "ssh -i chamroeunsaran.pem ubuntu@16.178.206.23\n\n"
        "# ២. ចាប់ផ្តើម Docker Swarm លើ Manager\n"
        "sudo docker swarm init --advertise-addr 172.31.34.160\n"
        "sudo hostnamectl set-hostname swarm-manager\n"
        "sudo systemctl restart docker\n\n"
        "# ចម្លងយក Join Token ដែលបង្ហាញលើអេក្រង់:\n"
        "# docker swarm join --token SWMTKN-1-... 172.31.34.160:2377"
    )
    add_code_card(s6, Inches(0.8), Inches(1.8), Inches(5.75), Inches(5.1), code_s6_l)

    code_s6_r = (
        "# ៣. ភ្ជាប់ Worker 1 ចូលទៅក្នុង Swarm\n"
        "ssh -i chamroeunsaran.pem ubuntu@3.107.96.140\n"
        "sudo docker swarm join --token <TOKEN> 172.31.34.160:2377\n"
        "sudo hostnamectl set-hostname swarm-worker1\n"
        "sudo systemctl restart docker\n"
        "exit\n\n"
        "# ៤. ភ្ជាប់ Worker 2 ចូលទៅក្នុង Swarm\n"
        "ssh -i chamroeunsaran.pem ubuntu@13.211.213.228\n"
        "sudo docker swarm join --token <TOKEN> 172.31.34.160:2377\n"
        "sudo hostnamectl set-hostname swarm-worker2\n"
        "sudo systemctl restart docker\n"
        "exit\n\n"
        "# ៥. ផ្ទៀងផ្ទាត់បញ្ជី Nodes លើ Manager:\n"
        "ssh -i chamroeunsaran.pem ubuntu@16.178.206.23 \"sudo docker node ls\""
    )
    add_code_card(s6, Inches(6.8), Inches(1.8), Inches(5.733), Inches(5.1), code_s6_r)

    # =========================================================================
    # SLIDE 7: DOCKER STACK DEPLOY
    # =========================================================================
    s7 = prs.slides.add_slide(blank_layout)
    add_header(s7, "៤. វិធីសាស្ត្រទី ២ (បន្ត)", "ការបញ្ជូន និងដាក់ឱ្យដំណើរការ Application Stack (Docker Stack Deploy)")

    code_s7_l = (
        "# ១. ខ្ចប់កូដគម្រោងពីលើ Laptop របស់អ្នក\n"
        "tar -czf app_bundle.tar.gz Dockerfile app.py \\\n"
        "  requirements.txt templates docker-stack.yml nginx\n\n"
        "# ២. បញ្ជូនកូដទៅម៉ាស៊ីនទាំង ៣ តាមរយៈ SCP\n"
        "scp -i chamroeunsaran.pem app_bundle.tar.gz \\\n"
        "  ubuntu@16.178.206.23:/home/ubuntu/\n"
        "scp -i chamroeunsaran.pem app_bundle.tar.gz \\\n"
        "  ubuntu@3.107.96.140:/home/ubuntu/\n"
        "scp -i chamroeunsaran.pem app_bundle.tar.gz \\\n"
        "  ubuntu@13.211.213.228:/home/ubuntu/"
    )
    add_code_card(s7, Inches(0.8), Inches(1.8), Inches(5.75), Inches(5.1), code_s7_l)

    code_s7_r = (
        "# ៣. Build រូបភាពកុងតឺន័រលើ Worker 1 & 2\n"
        "ssh -i chamroeunsaran.pem ubuntu@3.107.96.140 \\\n"
        "  \"tar -xzf app_bundle.tar.gz && sudo docker build \\\n"
        "  -t 399311815210.dkr.ecr.ap-southeast-2.amazonaws.com/cicd-assignment:latest .\"\n\n"
        "ssh -i chamroeunsaran.pem ubuntu@13.211.213.228 \\\n"
        "  \"tar -xzf app_bundle.tar.gz && sudo docker build \\\n"
        "  -t 399311815210.dkr.ecr.ap-southeast-2.amazonaws.com/cicd-assignment:latest .\"\n\n"
        "# ៤. Deploy Stack នៅលើ Manager Node\n"
        "ssh -i chamroeunsaran.pem ubuntu@16.178.206.23\n"
        "tar -xzf app_bundle.tar.gz\n"
        "sudo docker build -t .../cicd-assignment:latest .\n"
        "sudo docker stack deploy -c docker-stack.yml cicd-assignment"
    )
    add_code_card(s7, Inches(6.8), Inches(1.8), Inches(5.733), Inches(5.1), code_s7_r)

    # =========================================================================
    # SLIDE 8: ENDPOINT VERIFICATION & LOAD BALANCING
    # =========================================================================
    s8 = prs.slides.add_slide(blank_layout)
    add_header(s8, "៤. វិធីសាស្ត្រទី ២ (បន្ត)", "ការតេស្តសាកល្បង Endpoints & Load Balancing ជាក់ស្តែង")

    add_card(s8, Inches(0.8), Inches(1.8), Inches(5.75), Inches(5.1))
    tb_v = s8.shapes.add_textbox(Inches(1.0), Inches(2.0), Inches(5.35), Inches(4.7))
    tf_v = tb_v.text_frame
    tf_v.word_wrap = True
    
    p = tf_v.paragraphs[0]
    p.text = "🎯 ការផ្ទៀងផ្ទាត់សេវាកម្ម និង Load Balancing："
    p.font.name = KHMER_FONT
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = BLUE_ACCENT
    
    verif_items = [
        "ពិនិត្យសេវាកម្ម 'sudo docker service ls' ឃើញ៖\n  • cicd-assignment_nginx (1/1 replicas)\n  • cicd-assignment_web (2/2 replicas)",
        "ពិនិត្យ Task Distribution 'sudo docker stack ps cicd-assignment' ឃើញការបែងចែក Replicas លើ Nodes ផ្សេងគ្នា។",
        "បើកមើលលើ Web Browser៖ http://16.178.206.23/ បង្ហាញ UI DevOps Swarm Operations Console។",
        "ចុចប៊ូតុង 'Send Request via Nginx Reverse Proxy' នឹងឃើញ Hostname ឆ្លាស់គ្នាបញ្ជាក់ពី Round-Robin Load Balancing។"
    ]
    for vi in verif_items:
        p_vi = tf_v.add_paragraph()
        p_vi.text = f"• {vi}"
        p_vi.font.name = KHMER_FONT
        p_vi.font.size = Pt(10.5)
        p_vi.font.color.rgb = TEXT_DARK

    code_s8 = (
        "# ១. ពិនិត្យសេវាកម្មលើ Manager\n"
        "sudo docker service ls\n"
        "sudo docker stack ps cicd-assignment\n\n"
        "# ២. តេស្ត Application Health:\n"
        "curl -s http://16.178.206.23/health\n"
        "# Output: {\"hostname\":\"...\",\"status\":\"healthy\"}\n\n"
        "# ៣. តេស្ត Round-Robin Backend Replicas:\n"
        "curl -s http://16.178.206.23/api/info\n"
        "# ដំណើរការច្រើនដង Hostname នឹងឆ្លាស់គ្នា\n\n"
        "# ៤. តេស្ត Nginx Load Balancer Health:\n"
        "curl -s http://16.178.206.23/nginx-health\n"
        "# Output: {\"status\":\"healthy\",\"service\":\"nginx\"}"
    )
    add_code_card(s8, Inches(6.8), Inches(1.8), Inches(5.733), Inches(5.1), code_s8)

    # =========================================================================
    # SLIDE 9: METHOD C - JENKINS CI/CD
    # =========================================================================
    s9 = prs.slides.add_slide(blank_layout)
    add_header(s9, "៥. វិធីសាស្ត្រទី ៣", "ការដំណើរការ Jenkins CI/CD ស្វ័យប្រវត្តិកម្ម (Restore Backup)")

    add_card(s9, Inches(0.8), Inches(1.8), Inches(5.75), Inches(5.1))
    tb_j = s9.shapes.add_textbox(Inches(1.0), Inches(2.0), Inches(5.35), Inches(4.7))
    tf_j = tb_j.text_frame
    tf_j.word_wrap = True
    
    p = tf_j.paragraphs[0]
    p.text = "⚡ ការផ្ទេរ និងបើក Jenkins លើម៉ាស៊ីនថ្មី："
    p.font.name = KHMER_FONT
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = BLUE_ACCENT
    
    j_items = [
        "មិនបាច់ដំឡើង និង Configure Job សារជាថ្មីឡើយ។",
        "ប្រើប្រាស់ឯកសារ 'jenkins_backup.tar.gz' ដើម្បី Restore នូវ Plugins, Credentials, និង Build History (Build #7 ដល់ #21)។",
        "ដោះសោរ Security ដើម្បីកុំឱ្យទាមទារ Password ពេលធ្វើបទបង្ហាញ។",
        "ដំណាក់កាលទាំង ៥ នៃ Pipeline៖\n  1. Checkout SCM\n  2. Build & Test (Flake8, Pytest)\n  3. Security Scan (Trivy CVE)\n  4. Push to Amazon ECR\n  5. Deploy Stack to Swarm (+ Telegram Alerts)"
    ]
    for ji in j_items:
        p_ji = tf_j.add_paragraph()
        p_ji.text = f"• {ji}"
        p_ji.font.name = KHMER_FONT
        p_ji.font.size = Pt(10.5)
        p_ji.font.color.rgb = TEXT_DARK

    code_s9 = (
        "# ១. បង្កើត Container Jenkins ថ្មី\n"
        "docker run -d --name jenkins -p 8080:8080 -p 50000:50000 \\\n"
        "  -v jenkins_home:/var/jenkins_home jenkins/jenkins:lts\n\n"
        "# ២. ផ្ទេរទិន្នន័យ Backup ចូលក្នុង Container\n"
        "docker cp jenkins_backup.tar.gz jenkins:/tmp/jenkins_backup.tar.gz\n"
        "docker exec -u 0 jenkins tar xzf /tmp/jenkins_backup.tar.gz -C /var/jenkins_home\n"
        "docker exec -u 0 jenkins chown -R jenkins:jenkins /var/jenkins_home\n\n"
        "# ៣. បិទការទាមទារ Password ពេល Demo\n"
        "docker exec -u 0 jenkins sed -i 's/<useSecurity>true<\\/useSecurity>/<useSecurity>false<\\/useSecurity>/' \\\n"
        "  /var/jenkins_home/config.xml\n"
        "docker restart jenkins\n\n"
        "# ៤. បើក Browser មើល Jenkins Job ភ្លាមៗ:\n"
        "http://localhost:8080/job/Assignment-CI-CD/"
    )
    add_code_card(s9, Inches(6.8), Inches(1.8), Inches(5.733), Inches(5.1), code_s9)

    # =========================================================================
    # SLIDE 10: TESTING & LINTING
    # =========================================================================
    s10 = prs.slides.add_slide(blank_layout)
    add_header(s10, "៦. គុណភាពកូដ", "ការរត់តេស្តស្វ័យប្រវត្តិកម្ម និងត្រួតពិនិត្យស្តង់ដារកូដ (Testing & Linting)")

    add_card(s10, Inches(0.8), Inches(1.8), Inches(5.75), Inches(5.1))
    tb_te = s10.shapes.add_textbox(Inches(1.0), Inches(2.0), Inches(5.35), Inches(4.7))
    tf_te = tb_te.text_frame
    tf_te.word_wrap = True
    
    p = tf_te.paragraphs[0]
    p.text = "🧪 ស្តង់ដារគុណភាពកូដ និងការតេស្ត："
    p.font.name = KHMER_FONT
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = BLUE_ACCENT
    
    te_items = [
        "PEP 8 Code Linting (Flake8)៖\n  ត្រួតពិនិត្យទម្រង់កូដមិនឱ្យមាន Error ឬកូដខុសស្តង់ដារ (ទទួលបាន 0 errors)។",
        "Automated Pytest Suite (tests/test_app.py)៖\n  • test_index_route_success (HTTP 200 & HTML)\n  • test_health_endpoint_structure (JSON Schema)\n  • test_health_endpoint_values (App Version)\n  • test_404_not_found (Error Handling)\n  • test_api_info_endpoint (Swarm Metadata)",
        "Code Coverage (pytest-cov)៖\n  កម្រិតគ្របដណ្តប់នៃកូដ 89% Statement Coverage។"
    ]
    for tei in te_items:
        p_tei = tf_te.add_paragraph()
        p_tei.text = f"• {tei}"
        p_tei.font.name = KHMER_FONT
        p_tei.font.size = Pt(10.5)
        p_tei.font.color.rgb = TEXT_DARK

    code_s10 = (
        "# ១. បង្កើត Virtual Environment សម្រាប់ Python\n"
        "python -m venv .venv\n"
        "source .venv/bin/activate  # Windows: .venv\\Scripts\\Activate.ps1\n\n"
        "# ២. ដំឡើងបណ្ណាល័យជំនួយ\n"
        "pip install -r requirements.txt\n"
        "pip install -r requirements-dev.txt\n\n"
        "# ៣. រត់ត្រួតពិនិត្យទម្រង់កូដតាមស្តង់ដារ PEP 8\n"
        "flake8 --max-line-length=120 \\\n"
        "  --exclude=venv,.venv,build_submission_report.py app.py tests/\n\n"
        "# ៤. រត់តេស្តស្វ័យប្រវត្តិកម្ម Pytest ជាមួយ Coverage\n"
        "pytest -v --cov=app --cov-report=term-missing tests/\n\n"
        "# លទ្ធផល: 5 passed in 0.71s (89% coverage)"
    )
    add_code_card(s10, Inches(6.8), Inches(1.8), Inches(5.733), Inches(5.1), code_s10)

    # =========================================================================
    # SLIDE 11: COST MANAGEMENT
    # =========================================================================
    s11 = prs.slides.add_slide(blank_layout)
    add_header(s11, "៧. ការគ្រប់គ្រងការចំណាយ", "ការផ្អាក ឬលុបម៉ាស៊ីនមេ AWS ចោលដើម្បីកុំឱ្យអស់លុយ (Cost Management)")

    # Option 1 Card
    add_card(s11, Inches(0.8), Inches(1.8), Inches(5.75), Inches(5.1), bg_color=CARD_BG, border_color=BLUE_ACCENT)
    tb_c1 = s11.shapes.add_textbox(Inches(1.0), Inches(2.0), Inches(5.35), Inches(4.7))
    tf_c1 = tb_c1.text_frame
    tf_c1.word_wrap = True
    
    p = tf_c1.paragraphs[0]
    p.text = "⏸️ ជម្រើសទី ១៖ ផ្អាកដំណើរការបណ្តោះអាសន្ន (Stop)"
    p.font.name = KHMER_FONT
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = BLUE_ACCENT
    
    p_desc1 = tf_c1.add_paragraph()
    p_desc1.text = "ស័ក្តិសមបំផុតប្រសិនបើអ្នកគ្រាន់តែសម្រាក ហើយចង់បើកដំណើរការឡើងវិញនៅពេលក្រោយ៖\n• បញ្ឈប់ការគិតថ្លៃសេវា Compute ម៉ោងរបស់ EC2\n• ទិន្នន័យ, កុងតឺន័រ, និង Docker Swarm Setup នៅដដែលមិនបាត់បង់ឡើយ\n• ពេលចង់ប្រើឡើងវិញគ្រាន់តែ Start Instances វិញជាការស្រេច"
    p_desc1.font.name = KHMER_FONT
    p_desc1.font.size = Pt(10.5)
    p_desc1.font.color.rgb = TEXT_DARK
    
    code_c1 = (
        "# បិទម៉ាស៊ីនមេទាំង ៣ បណ្តោះអាសន្ន:\n"
        "aws ec2 stop-instances \\\n"
        "  --instance-ids i-0932b2a74fdd78211 \\\n"
        "  i-07fab0b80a64ac7df i-04d5f124712e975e6 \\\n"
        "  --region ap-southeast-2\n\n"
        "# បើកដំណើរការឡើងវិញពេលចង់ប្រើ:\n"
        "aws ec2 start-instances \\\n"
        "  --instance-ids i-0932b2a74fdd78211 \\\n"
        "  i-07fab0b80a64ac7df i-04d5f124712e975e6 \\\n"
        "  --region ap-southeast-2"
    )
    add_code_card(s11, Inches(1.0), Inches(4.3), Inches(5.35), Inches(2.4), code_c1)

    # Option 2 Card
    add_card(s11, Inches(6.8), Inches(1.8), Inches(5.733), Inches(5.1), bg_color=CARD_BG, border_color=RGBColor(239, 68, 68))
    tb_c2 = s11.shapes.add_textbox(Inches(7.0), Inches(2.0), Inches(5.333), Inches(4.7))
    tf_c2 = tb_c2.text_frame
    tf_c2.word_wrap = True
    
    p = tf_c2.paragraphs[0]
    p.text = "🗑️ ជម្រើសទី ២៖ លុបធនធានចោលជាស្ថាពរ (Destroy)"
    p.font.name = KHMER_FONT
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = RGBColor(220, 38, 38)
    
    p_desc2 = tf_c2.add_paragraph()
    p_desc2.text = "អនុវត្តតែនៅពេលដែលអ្នកបានបញ្ចប់ការធ្វើបទបង្ហាញ និងទទួលបានពិន្ទុរួចរាល់ ១០០%៖\n• លុបចោលទាំងស្រុងនូវ EC2, VPC, Subnets, និង Security Groups\n• គ្មានការគិតថ្លៃសេវាណាមួយបន្តទៀតឡើយ ($0/month)\n• ពេលចង់បង្កើតថ្មីគ្រាន់តែរត់ 'terraform apply' ឡើងវិញ"
    p_desc2.font.name = KHMER_FONT
    p_desc2.font.size = Pt(10.5)
    p_desc2.font.color.rgb = TEXT_DARK
    
    code_c2 = (
        "# លុបធនធានទាំងអស់នៅលើ AWS ចោលជាស្ថាពរ:\n"
        "cd terraform\n"
        "terraform destroy -auto-approve\n\n"
        "# (ជម្រើសបន្ថែម) លុប ECR Image Repository:\n"
        "aws ecr delete-repository \\\n"
        "  --repository-name cicd-assignment \\\n"
        "  --force --region ap-southeast-2"
    )
    add_code_card(s11, Inches(7.0), Inches(4.3), Inches(5.333), Inches(2.4), code_c2)

    # =========================================================================
    # SLIDE 12: CONCLUSION & FAQ
    # =========================================================================
    s12 = prs.slides.add_slide(blank_layout)
    add_header(s12, "៨. សេចក្តីសន្និដ្ឋាន & FAQ", "សំណួរ និងចម្លើយបច្ចេកទេសដែលសួរញឹកញាប់ (Technical FAQ)")

    faqs = [
        ("❓ សួរ៖ ហេតុអ្វីបានជា Public IP ផ្លាស់ប្តូរពេល Restart ម៉ាស៊ីន EC2?",
         "💡 ឆ្លើយ៖ តាមលំនាំដើម AWS ប្រើប្រាស់ Dynamic IP ពី Public Pool។ នៅពេល Stop ម៉ាស៊ីន AWS ដក IP យកទៅឱ្យអ្នកផ្សេងប្រើវិញ។ នៅពេល Start ឡើងវិញ ទើបផ្តល់ IP ថ្មី។ ប៉ុន្តែ Private IP នៅក្នុងបណ្តាញខាងក្នុងមិនផ្លាស់ប្តូរឡើយ ដូច្នេះ Docker Swarm ដំណើរការធម្មតា។ ក្នុង Production គេប្រើ AWS Elastic IP (EIP) ដើម្បីកុំឱ្យផ្លាស់ប្តូរ IP។"),
        ("❓ សួរ៖ តើត្រូវធ្វើដូចម្តេចដើម្បីតេស្តមើល Zero-Downtime Rolling Update?",
         "💡 ឆ្លើយ៖ ដំណើរការបញ្ជា៖ 'sudo docker service update --image <IMAGE>:v2 --update-order start-first cicd-assignment_web'។ Swarm នឹងបង្កើតកុងតឺន័រថ្មីឱ្យដើរស្រួលបួល និងឆ្លងកាត់ Healthcheck សិន ទើបបិទកុងតឺន័រចាស់។"),
        ("❓ សួរ៖ តើត្រូវមើល Logs របស់ Flask App លើ Swarm យ៉ាងដូចម្តេច?",
         "💡 ឆ្លើយ៖ វាយពាក្យបញ្ជា៖ 'sudo docker service logs -f cicd-assignment_web'។")
    ]

    for idx, (q, a) in enumerate(faqs):
        top = Inches(1.8 + idx * 1.7)
        add_card(s12, Inches(0.8), top, Inches(11.733), Inches(1.55))
        
        tb = s12.shapes.add_textbox(Inches(1.0), top + Inches(0.15), Inches(11.333), Inches(1.25))
        tf = tb.text_frame
        tf.word_wrap = True
        
        p = tf.paragraphs[0]
        p.text = q
        p.font.name = KHMER_FONT
        p.font.size = Pt(11.5)
        p.font.bold = True
        p.font.color.rgb = BLUE_ACCENT
        
        p_a = tf.add_paragraph()
        p_a.text = a
        p_a.font.name = KHMER_FONT
        p_a.font.size = Pt(10.5)
        p_a.font.color.rgb = TEXT_DARK

    prs.save("HOW_TO_RUN_KH.pptx")
    print("Successfully built HOW_TO_RUN_KH.pptx (12 slides)!")

if __name__ == "__main__":
    create_khmer_presentation()
