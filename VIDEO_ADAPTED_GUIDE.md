# VIDEO SETUP GUIDE — Adapted cho MCM Vendor
## Nguồn: jmsolutionss "Claude Code + Hermes Agent = $10,000 AI Agents"
## Trạng thái: ĐÃ ADAPT — thay thế Twilio/ElevenLabs bằng Telegram MCP

---

> **Cách dùng file này với Claude Code:**
> File này là hướng dẫn từng bước đã được adapt từ video gốc sang stack MCM Vendor.
> Mỗi bước có: [VIDEO LÀM GÌ] → [MCM VENDOR LÀM GÌ] → [LỆNH CỤ THỂ]
> Claude Code đọc file này + CLAUDE.md → build theo đúng spec, không cần đoán.

---

## PHẦN 1 — SETUP NỀN TẢNG
### Video: Cài VS Code + Claude Code extension + Tạo folder

**Video làm gì:**
- Cài VS Code từ visualstudio.com/download
- Vào Extensions → cài "Claude Code"
- Tạo folder mới tên "Hermes Agent" trên máy

**MCM Vendor làm gì:**
- VS Code đã có → bỏ qua cài VS Code
- Cài Claude Code extension nếu chưa có
- Tạo folder `hermes-vendor-agent` là repo chính

**Lệnh thực tế:**
```bash
mkdir hermes-vendor-agent
cd hermes-vendor-agent
mkdir skills prompts docs
git init
git remote add origin https://github.com/[USERNAME]/hermes-vendor-agent
```

**Tạo .gitignore ngay:**
```bash
cat > .gitignore << 'IGNORE'
.env
node_modules/
*.log
.DS_Store
IGNORE
```

---

## PHẦN 2 — SETUP VPS VÀ HERMES
### Video: Dùng Hostinger KVM2, Docker 1-click deploy Hermes

**Video làm gì:**
- Mua Hostinger KVM2 VPS
- Vào Docker Manager → tìm "Hermes Agent" → Deploy
- Hermes chạy, copy password lưu lại
- Truy cập dashboard Hermes qua browser

**MCM Vendor làm gì:**
- VPS AlmaLinux đã có → bỏ qua mua VPS
- Hermes đã cài → kiểm tra còn chạy không
- Nếu chưa cài Hermes: dùng Docker

**Kiểm tra Hermes đang chạy:**
```bash
# SSH vào VPS
ssh user@YOUR_VPS_IP

# Kiểm tra Hermes
curl http://localhost:3000
# Nếu thấy response = Hermes đang chạy OK

# Nếu chưa có, cài bằng Docker:
docker run -d \
  --name hermes-vendor \
  --restart unless-stopped \
  -p 3000:3000 \
  -v $(pwd)/hermes-data:/app/data \
  nousresearch/hermes-agent:latest
```

**Lưu thông tin VPS vào .env.example:**
```bash
cat > .env.example << 'ENV'
# VPS
HERMES_URL=http://YOUR_VPS_IP:3000
HERMES_PORT=3000

# Anthropic
ANTHROPIC_API_KEY=sk-ant-...

# Telegram
TELEGRAM_BOT_TOKEN=...
TELEGRAM_CHAT_ID_HIEP=...

# Google Sheet
GOOGLE_SHEET_ID=...
GOOGLE_SERVICE_ACCOUNT_JSON=...

# EspoCRM (điền sau khi cài)
ESPOCRM_URL=http://localhost:8080
ESPOCRM_API_KEY=...

# GitHub (cho Agent 5)
GITHUB_WEBHOOK_SECRET=...
GITHUB_REPO=hermes-vendor-agent
ENV
```

---

## PHẦN 3 — LẤY API KEYS
### Video: Anthropic → Twilio → ElevenLabs → Cal.com → Typeform → GitHub → Google Sheet

**Video làm gì + MCM Vendor adapt:**

### 3.1 Anthropic API Key
**Video:** platform.anthropic.com → tạo API key → copy
**MCM Vendor:** Giống hệt — không thay đổi
```
URL: platform.anthropic.com
Vào: API Keys → Create Key → đặt tên "hermes-vendor"
Copy vào: .env → ANTHROPIC_API_KEY=
```

### 3.2 Twilio ← BỎ QUA
**Video:** Mua số điện thoại $2.15/tháng để AI gọi điện
**MCM Vendor:** KHÔNG DÙNG — thay bằng Telegram MCP
```
LÝ DO BỎ: Affiliate VN dùng Telegram, không cần gọi điện
THAY THẾ: Telegram MCP đã setup sẵn → dùng luôn
```

### 3.3 ElevenLabs ← BỎ QUA
**Video:** Tạo voice AI để đọc script trong cuộc gọi
**MCM Vendor:** KHÔNG DÙNG — không có cuộc gọi
```
LÝ DO BỎ: Phụ thuộc Twilio → bỏ Twilio thì bỏ ElevenLabs
THAY THẾ: Claude API viết text message → Telegram gửi
```

### 3.4 Telegram Bot Token ← THÊM MỚI (không có trong video)
**MCM Vendor dùng thay Twilio:**
```
URL: t.me/BotFather
Lệnh: /newbot
Đặt tên: MCM Vendor Bot
Copy: BOT_TOKEN vào .env → TELEGRAM_BOT_TOKEN=
```

### 3.5 Google Sheet + Service Account
**Video:** console.cloud.google.com → tạo project → enable Sheets API → tạo Service Account → download JSON key
**MCM Vendor:** Giống hệt — Google Docs MCP đã setup nhưng cần Sheet ID mới

```
Bước 1: console.cloud.google.com
Bước 2: Chọn project hoặc tạo mới "mcm-vendor"
Bước 3: APIs & Services → Enable → tìm "Google Sheets API" → Enable
Bước 4: Credentials → Create Credentials → Service Account
Bước 5: Đặt tên "hermes-mcm" → Create → Done
Bước 6: Click vào service account → Keys → Add Key → JSON → Download
Bước 7: Copy toàn bộ nội dung JSON file vào .env:
         GOOGLE_SERVICE_ACCOUNT_JSON='{"type":"service_account",...}'

Bước 8: sheets.new → tạo sheet mới → đặt tên "MCM Vendor DB"
Bước 9: Copy Sheet ID từ URL (phần sau /d/ đến /edit)
         GOOGLE_SHEET_ID=1BxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs74OgVE2upms

Bước 10: Share sheet với email của Service Account
          (email dạng: hermes-mcm@project-id.iam.gserviceaccount.com)
          → Share → Editor
```

### 3.6 Cal.com ← ADAPT THÀNH ONBOARD SEQUENCE
**Video:** Cal.com để đặt lịch kiểm tra mái nhà
**MCM Vendor:** KHÔNG DÙNG Cal.com
```
LÝ DO: MCM không cần đặt lịch — cần onboard sequence
THAY THẾ: Agent 2 gửi D1-D7 qua Telegram theo cron
```

### 3.7 Typeform ← ADAPT THÀNH LANDING PAGE FORM
**Video:** Typeform tạo form → webhook trigger khi submit
**MCM Vendor:** Dùng form trên landing page → webhook tương tự

```
LOGIC GIỐNG HỆT:
Video:       Typeform submit → webhook POST → Hermes
MCM Vendor:  Landing form submit → webhook POST → Hermes

WEBHOOK URL format (giống video):
Video:       https://[hermes-url]/webhook/typeform
MCM Vendor:  https://[VPS_IP]:3000/webhook/capture

FIELDS form MCM Vendor (thay vì mái nhà):
- name (họ tên)
- telegram_username (@handle)
- source (từ đâu biết đến: x_post/telegram/referral)
- timestamp (tự động)
```

### 3.8 GitHub Repo
**Video:** Tạo repo → copy URL → dùng để Claude Code push code lên
**MCM Vendor:** Giống hệt
```
URL: github.com/new
Tên: hermes-vendor-agent
Private: YES (chứa business logic)
Copy URL: https://github.com/[USERNAME]/hermes-vendor-agent
```

---

## PHẦN 4 — CLAUDE CODE VIẾT CODE
### Video: Paste prompt vào Claude Code → nó tự tạo toàn bộ file structure

**Video làm gì:**
- Paste prompt mô tả hệ thống vào Claude Code
- Claude Code tự tạo: folders, files, docker-compose.yml, .env
- Paste các API keys vào .env file
- Push code lên GitHub

**MCM Vendor làm gì — PROMPT CHÍNH xác cho Claude Code:**

```
Prompt 1 — Tạo cấu trúc project:

Tôi đang build MCM Vendor AI Affiliate System.
Đọc file CLAUDE.md để hiểu toàn bộ project.

Tạo cấu trúc folder đầy đủ:
- skills/agent1-capture.yaml (placeholder)
- skills/agent2-onboard.yaml (placeholder)
- skills/agent3-daily-loop.yaml (placeholder)
- skills/agent4-crm-sync.yaml (placeholder)
- skills/agent5-monitor.yaml (placeholder)
- prompts/qualify.txt (placeholder)
- prompts/checklist.txt (placeholder)
- prompts/coaching.txt (placeholder)
- prompts/report-affiliate.txt (placeholder)
- prompts/report-hiep.txt (placeholder)
- .env.example (theo spec trong CLAUDE.md)
- docker-compose.yml (cho Hermes Agent)
- README.md (mô tả project)
```

```
Prompt 2 — Build Agent 1:

Đọc section AGENT 1 trong CLAUDE.md.
Build skills/agent1-capture.yaml hoàn chỉnh.
Build prompts/qualify.txt với 2 câu hỏi qualify.

Yêu cầu:
- Nhận webhook POST /webhook/capture
- Parse: name, telegram_username, source
- Gửi 2 câu qualify qua Telegram
- Score: Hot/Warm/Cold
- Ghi Google Sheet theo schema trong CLAUDE.md
- Gửi welcome message phù hợp với score
- Toàn bộ trong < 30 giây
```

```
Prompt 3 — Build Agent 2:

Đọc section AGENT 2 trong CLAUDE.md.
Build skills/agent2-onboard.yaml.
Build prompts/onboard-d1.txt đến onboard-d7.txt.

Yêu cầu:
- Cron 8AM check affiliate nào cần D-X hôm nay
- D1: giới thiệu MCM
- D2: hướng dẫn viết bài (dùng {{channel}} variable)
- D3: hướng dẫn dùng tool
- D4-D7: thực hành → scale → 21 channel model
- Cập nhật EspoCRM stage sau D3
```

```
Prompt 4 — Build Agent 3:

Đọc section AGENT 3 trong CLAUDE.md.
Build skills/agent3-daily-loop.yaml.
Build 3 prompt files: checklist.txt, coaching.txt, report-affiliate.txt, report-hiep.txt

Yêu cầu:
- 7AM: checklist cá nhân theo {{channel}}
- 2PM: coaching chỉ khi refer drop >30% hoặc không post 3+ ngày
- 9PM: report từng affiliate + summary Hiep
- Tất cả dùng biến {{name}} {{channel}} {{refer_this_week}} etc.
```

---

## PHẦN 5 — DEPLOY LÊN VPS
### Video: Paste code vào terminal VPS → docker-compose up -d → 12 containers chạy

**Video làm gì:**
```bash
mkdir -p docker-lead-up
nano docker-compose.yml
# paste nội dung
Ctrl+O → Enter → Ctrl+X
docker-compose up -d
# "12/12 containers started" = OK
# "Hermes agent listening on 0.0.0.0:3000" = DONE
```

**MCM Vendor làm gì — workflow local → VPS:**

```bash
# LOCAL: sau khi Claude Code viết xong
git add .
git commit -m "done: project-structure + agent1-capture"
git push origin main

# VPS: pull về và restart Hermes
ssh user@YOUR_VPS_IP
cd hermes-vendor-agent
git pull origin main

# Hermes tự nhận skill mới (không cần restart)
# Kiểm tra:
curl http://localhost:3000/health
# → {"status":"ok","skills":["agent1-capture",...]}
```

**Nếu cần restart Hermes:**
```bash
docker restart hermes-vendor
# hoặc
pm2 restart hermes
```

---

## PHẦN 6 — SETUP WEBHOOK
### Video: Typeform → Connect → Webhooks → Add webhook → paste URL → Enable → Test

**Video làm gì:**
- Vào Typeform form → Connect → Webhooks
- Thêm URL: `https://[hermes-url]/webhook/typeform`
- Bật ON
- Test: submit form → xem log real-time

**MCM Vendor làm gì:**
- Landing page form thay Typeform
- Webhook URL: `https://[VPS_IP]:3000/webhook/capture`

**Test webhook giống video — dùng curl:**
```bash
# Test thủ công (thay vì submit form)
curl -X POST https://[VPS_IP]:3000/webhook/capture \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Nguyen Van Nam Test",
    "telegram_username": "@namtest",
    "source": "x_post",
    "timestamp": "2026-06-22T10:00:00"
  }'

# Kết quả mong đợi:
# → Telegram bot gửi message cho @namtest trong < 30 giây
# → Google Sheet có row mới
# → Log: "Agent 1 processed lead: @namtest → Warm"
```

**Xem log real-time (như video xem terminal):**
```bash
# Trên VPS
docker logs -f hermes-vendor
# hoặc
tail -f /var/log/hermes/agent.log
```

---

## PHẦN 7 — LIVE TEST
### Video: Submit Typeform thật → AI gọi điện 10 giây → đặt lịch → Google Calendar + Sheet update

**Video demo:**
- James Michael điền form: tên, SĐT, email, mái nhà bị dột
- 10 giây sau: AI gọi điện
- AI hỏi: "Cho tôi biết thêm về vấn đề mái nhà?"
- Đặt lịch: "Thứ Ba 9/6 lúc 3:30 chiều"
- Google Calendar: lịch hẹn xuất hiện
- Google Sheet: row mới với đầy đủ thông tin

**MCM Vendor live test tương đương:**
```
Bước 1: Mở landing page MCM Vendor
Bước 2: Điền form với account Telegram test:
  - Tên: Nguyen Van Test
  - Telegram: @[account test của Hiep]
  - Nguồn: landing

Bước 3: Kiểm tra trong < 30 giây:
  ✓ Telegram @[account test] nhận message Q1
  ✓ Trả lời Q1 → nhận Q2
  ✓ Trả lời Q2 → nhận welcome message với score

Bước 4: Kiểm tra Google Sheet:
  ✓ Row mới xuất hiện với đủ fields
  ✓ score = Hot/Warm/Cold đúng với câu trả lời

Bước 5: Ngày hôm sau 7AM:
  ✓ Nhận checklist buổi sáng (nếu Agent 3 đã build)

TEST PASS = hệ thống live được
```

---

## PHẦN 8 — PRICING & PACKAGING
### Video: Setup $3,000-$10,000 + retainer $1,000-$2,000/tháng

**Video pricing logic:**
- Tính phí theo giá trị mỗi lead với doanh nghiệp
- Lead mái nhà = $3,000-$5,000 giá trị → charge $10,000 setup
- Per appointment booked = model khác

**MCM Vendor pricing adapt:**
```
DÙNG CHÍNH XÁC LOGIC NÀY cho bundle sale:

Với affiliate program:
- Mỗi affiliate active = $X commission/tháng cho chủ DN
- Hệ thống 5 agent tự động nuôi dưỡng affiliate 24/7
- Charge: setup $1,997 + $197/tháng maintain

Pitch template (adapt từ video):
"Hệ thống tự động chăm sóc affiliate của bạn 24/7:
- Gửi checklist cá nhân mỗi sáng
- Coaching khi performance drop
- Report commission mỗi tối
Không cần thêm nhân sự. Done-for-you hoàn toàn."
```

---

## TÓM TẮT — VIDEO vs MCM VENDOR

| Bước | Video (Roofing) | MCM Vendor | Giữ/Thay/Bỏ |
|------|-----------------|------------|--------------|
| VS Code + Claude Code | Cài từ đầu | Đã có | Giữ nguyên |
| Hostinger VPS | Mua mới KVM2 | AlmaLinux VPS đã có | Thay VPS |
| Hermes Agent | Deploy Docker | Đã chạy | Kiểm tra còn chạy |
| Anthropic API | platform.anthropic.com | Giống hệt | Giữ nguyên |
| Twilio số điện thoại | Mua $2.15/tháng | **BỎ** | Telegram MCP thay |
| ElevenLabs voice | $6/tháng | **BỎ** | Claude text thay |
| Cal.com đặt lịch | Tạo event | **BỎ** | Onboard sequence thay |
| Typeform form | Tạo form + webhook | Landing page + webhook | Cùng logic khác tool |
| Google Sheet | Tạo sheet + Service Account | Tạo sheet mới | Giống hệt |
| GitHub repo | Tạo repo | Tạo repo mới | Giống hệt |
| docker-compose up -d | 12 containers | Hermes skill files | Cùng lệnh |
| Webhook test | Submit Typeform | curl POST test | Cùng logic |
| Live demo | Gọi điện 10 giây | Telegram message 30 giây | Cùng speed-to-lead |

---

## PROMPT MASTER CHO CLAUDE CODE

Paste cái này vào Claude Code lần đầu tiên mở project:

```
Đọc 2 files sau trong project:
1. CLAUDE.md — toàn bộ spec dự án MCM Vendor
2. VIDEO_ADAPTED_GUIDE.md — hướng dẫn từng bước đã adapt từ video

Tôi muốn bắt đầu từ Phần 1 của VIDEO_ADAPTED_GUIDE.md.
Làm theo đúng thứ tự, từng bước một.
Sau mỗi bước xong báo tôi để confirm trước khi sang bước tiếp.
Mỗi bước done → tạo commit message đúng convention trong CLAUDE.md.
```

---

*Nguồn gốc: Transcript video NoteGPT_Claude_Code___Hermes_Agent____10_000_AI_Agents.txt*
*Đã adapt cho MCM Vendor — Hermes Agent + Telegram MCP + Google Sheet*
*File này = hướng dẫn làm việc cho Claude Code, không phải tài liệu đọc*
