# MCM VENDOR — AI Affiliate System
## Claude Code Working Instructions

Đây là file hướng dẫn làm việc cho Claude Code.
Đọc TOÀN BỘ file này trước khi làm bất cứ việc gì.
Mỗi khi Hiep yêu cầu build một phần, refer lại đúng section.

---

## PROJECT OVERVIEW

**Tên dự án:** MCM Vendor — AI Affiliate System  
**Mục tiêu:** Build hệ thống affiliate XAUUSD tự động bằng 5 Hermes Agent skill  
**Stack:** Hermes Agent (1 instance) + Claude API + Telegram MCP + Google Docs MCP + EspoCRM  
**VPS:** AlmaLinux — Hermes đã chạy sẵn  
**Repo:** hermes-vendor-agent  

**Sau khi done:** Đóng gói thành SOP Bundle bán lại cho khách hàng khác (adapt bất kỳ ngành nào)

---

## ARCHITECTURE — 1 HERMES, 5 SKILLS

```
hermes-vendor-agent/
├── CLAUDE.md                    ← file này
├── skills/
│   ├── agent1-capture.yaml      ← build trước nhất
│   ├── agent2-onboard.yaml
│   ├── agent3-daily-loop.yaml
│   ├── agent4-crm-sync.yaml
│   └── agent5-monitor.yaml
├── prompts/
│   ├── qualify.txt
│   ├── checklist.txt
│   ├── coaching.txt
│   ├── report-affiliate.txt
│   └── report-pm.txt
├── .env.example
├── .gitignore                   ← .env phải có trong này
├── docker-compose.yml
└── README.md
```

**QUAN TRỌNG:** 5 "agent" = 5 skill files trong 1 Hermes duy nhất.  
KHÔNG tạo 5 Hermes riêng lẻ.

---

## GOOGLE SHEET SCHEMA

### Sheet 1: Affiliate Master
| Column | Type | Written by | Description |
|--------|------|------------|-------------|
| lead_id | TEXT | Agent 1 auto | AFF-YYYYMMDD-XXX |
| name | TEXT | Agent 1 | Tên đầy đủ từ form |
| telegram_username | TEXT | Agent 1 | @handle |
| source | TEXT | Agent 1 | x_post/landing/telegram_cta/referral |
| channel | TEXT | Agent 2 | tiktok/telegram/facebook/x |
| score | TEXT | Agent 1 | Hot/Warm/Cold |
| path | TEXT | Agent 1 | fast_track/nurture |
| status | TEXT | Agent 4 | New/Onboarding/Active/VIP/Churned |
| onboard_day | NUMBER | Agent 2 | 1-7 |
| last_contact | DATETIME | Agent 3 | Lần cuối nhận message |
| last_post | DATE | Agent 3 | Lần cuối đăng bài |
| refer_this_week | NUMBER | Agent 3 | Refer tuần này |
| refer_last_week | NUMBER | Agent 3 | Refer tuần trước |
| total_earn | NUMBER | Agent 4 | Commission tích lũy ($) |
| rank | NUMBER | Agent 3 | Thứ hạng |
| notes | TEXT | Manual | Ghi chú |

### Sheet 2: Activity Log
| Column | Description |
|--------|-------------|
| log_id | Auto ID |
| affiliate_id | FK → Sheet 1 |
| agent | Agent1/2/3/4/5 |
| action | webhook_received/message_sent/score_updated/status_changed |
| detail | Nội dung cụ thể |
| timestamp | UTC+7 |
| success | TRUE/FALSE |
| error_msg | Nếu success=FALSE |

---

## AGENT 1 — CAPTURE AGENT

**Nguồn tư duy:** Video jmsolutionss Speed-to-Lead  
**Trigger:** Webhook POST đến `/webhook/capture`  
**SLA:** Phản hồi trong < 30 giây  

### Input payload từ form:
```json
{
  "name": "Nguyen Van Nam",
  "telegram_username": "@namtrader",
  "source": "x_post",
  "timestamp": "2026-06-22T10:00:00"
}
```

### Logic flow:
```
Nhận webhook
→ Parse payload
→ Gửi Telegram message Q1: "Bạn đang có audience ở kênh nào? (TikTok / Telegram / Facebook / X)"
→ Đợi reply (timeout 24h)
→ Gửi Q2: "Mục tiêu thu nhập thụ động mỗi tháng của bạn là bao nhiêu?"
→ Đợi reply
→ Claude API score: Hot/Warm/Cold + path: fast_track/nurture
→ Ghi Google Sheet (append row)
→ Gửi welcome message phù hợp với path
→ Trigger Agent 2
```

### Scoring logic cho Claude:
```
Hot = có audience sẵn + mục tiêu rõ ràng → fast_track
Warm = có kênh nhưng nhỏ HOẶC mục tiêu chung chung → nurture  
Cold = chưa có kênh + không rõ mục tiêu → nurture dài hơn
```

### ENV cần có:
```
ANTHROPIC_API_KEY=
TELEGRAM_BOT_TOKEN=
GOOGLE_SHEET_ID=
GOOGLE_SERVICE_ACCOUNT_JSON=
HERMES_WEBHOOK_SECRET=
```

---

## AGENT 2 — ONBOARD AGENT (Chăm sóc giai đoạn đầu)

**Nguồn tư duy:** Whimsical MCM bước 5 — bot chăm sóc 7 ngày  
**Trigger:** Agent 1 done → status = Onboarding  
**Cron:** Mỗi sáng 8AM kiểm tra affiliate nào cần gửi D-X hôm nay  

### Lộ trình 7 ngày:
```
D1 → Giới thiệu MCM, tài khoản, công cụ tracking
D2 → Hướng dẫn viết bài (Claude tạo theo đúng kênh của affiliate)
D3 → Hướng dẫn dùng dashboard, check link, xem commission
D4 → Thực hành: chia sẻ link lần đầu + script post mẫu
D5 → Follow up first refer: hỏi kết quả, coaching nếu cần
D6 → Scale kênh: mở rộng audience, tăng tần suất post
D7 → Mô hình 21 channel theo sách $100 millions model
```

### Claude prompt template D2 (ví dụ):
```
Affiliate: {{name}}
Kênh: {{channel}}
Stage: D2 onboarding

Tạo hướng dẫn viết bài cho {{name}} về XAUUSD signal.
Cụ thể cho kênh {{channel}}.
Ngắn gọn, thực tế, có ví dụ bài mẫu.
Kết thúc bằng: "Thử viết 1 bài theo format này và gửi link cho mình xem nhé!"
```

### EspoCRM stage update:
```
Sau D3 → status: Onboarding → Active (chuyển sang Agent 3)
Nếu không phản hồi sau D3 → flag: needs_attention
```

---

## AGENT 3 — DAILY LOOP AGENT (Chăm sóc hàng ngày)

**Nguồn tư duy:** Cao Văn Hạnh — Vibe Code CRM  
**Nguyên tắc:** Affiliate KHÔNG cần vào dashboard — AI mang mọi thứ về Telegram của họ  

### Cron 1: Checklist sáng — `0 7 * * *`

Claude prompt:
```
Affiliate: {{name}}
Kênh chính: {{channel}}
Stage: {{status}} — Ngày {{onboard_day}}
Lần cuối đăng bài: {{last_post}} ngày trước
Refer tuần này: {{refer_this_week}} (tuần trước: {{refer_last_week}})

Tạo checklist hôm nay cho {{name}}.
Tối đa 3 việc. Mỗi việc 1 dòng ngắn gọn.
Cụ thể cho kênh {{channel}}.
KHÔNG chào hỏi. KHÔNG giải thích dài.
Format: 1. [việc] / 2. [việc] / 3. [việc]
```

### Cron 2: Coaching — `0 14 * * *`

Điều kiện trigger (chỉ gửi khi):
```
refer_this_week < refer_last_week * 0.7   (drop >30%)
HOẶC last_post > 3 ngày trước
KHÔNG gửi nếu mọi thứ bình thường
```

Claude prompt:
```
Affiliate: {{name}}, kênh: {{channel}}
Tuần này: {{refer_this_week}} refer (tuần trước: {{refer_last_week}})
Lần cuối post: {{last_post}} ngày trước

Viết 1 coaching message ngắn, thân thiện.
Chỉ ra vấn đề cụ thể + đề xuất 1 việc làm ngay hôm nay.
Tối đa 3 câu.
```

### Cron 3: Report tối — `0 21 * * *`

Output cho affiliate:
```
=== Hôm nay của bạn ===
Refer: {{refer_today}} lead
Earn: ~${{earn_today}}
Rank: #{{rank}}/{{total_affiliates}}
Còn {{gap}} lead → lên #{{rank-1}}
Insight: {{1 nhận xét ngắn từ Claude}}
```

Output summary cho Hiep:
```
=== MCM Summary {{date}} ===
Tổng lead hôm nay: {{total_leads}}
Affiliate active: {{active_count}}
Top performer: @{{username}} ({{count}} lead)
Cần chú ý: {{flagged_count}} người 0 hoạt động 3+ ngày
```

---

## AGENT 4 — CRM SYNC AGENT

**Trigger:** EspoCRM webhook events — lắng nghe 24/7  

### 4 events cần subscribe:
```bash
# Webhook 1: Lead mới
POST /api/v1/Webhook
{"event": "Lead.create", "url": "http://localhost:3000/webhook/espo/lead-create"}

# Webhook 2: Status thay đổi  
{"event": "Contact.fieldUpdate.status", "url": "http://localhost:3000/webhook/espo/status-change"}

# Webhook 3: Opportunity (refer thành công)
{"event": "Opportunity.create", "url": "http://localhost:3000/webhook/espo/opportunity"}

# Webhook 4: Commission update
{"event": "Contact.fieldUpdate.total_earn", "url": "http://localhost:3000/webhook/espo/commission"}
```

### Logic từng event:
```
Lead.create          → dẫn vào đúng Telegram group + trigger Agent 2
status: New→Active   → cấp tracking link tự động + notify affiliate
status: Active→VIP   → mở scale path (Agent 2 D6-D7)
Opportunity.create   → ghi commission vào Sheet + cập nhật rank
```

---

## AGENT 5 — PROJECT MONITOR AGENT

**Mục tiêu:** Vừa quản lý dự án build, vừa tự động cập nhật SOP, vừa phát hiện skill gap  

### Trigger 3 nguồn:
```
Cron 8PM hàng ngày
GitHub webhook mỗi commit push
Hermes log check định kỳ
```

### Commit convention BẮT BUỘC (Agent 5 đọc để track):
```
feat: [agent-name] [mô tả]      → đang build tính năng mới
fix:  [agent-name] [vấn đề]     → đang sửa lỗi
done: [agent-name] [tên-bước]   → bước SOP hoàn thành
test: [agent-name] [kết quả]    → đã test, kết quả thế nào
blocked: [agent-name] [lý do]   → bị tắc, cần giải quyết
```

### Ví dụ commit đúng:
```bash
git commit -m "done: agent1 webhook-capture-qualify-sheet"
git commit -m "feat: agent2 D1-D2-scripts-telegram"
git commit -m "blocked: agent3 cron-7am missing channel field in sheet"
git commit -m "done: agent4 espocrm-docker-running-port-8080"
```

### Daily report 8PM format:
```
━━━━━━━━━━━━━━━━━━━━━━
MCM BUILD — [Thứ] [Ngày]
━━━━━━━━━━━━━━━━━━━━━━
Agent 1 (Capture):    [STATUS]
Agent 2 (Onboard):    [STATUS]
Agent 3 (Daily Loop): [STATUS]
Agent 4 (CRM Sync):   [STATUS]
Agent 5 (Monitor):    [STATUS]

Tiến độ: [X]/[TOTAL] bước ([Y]%)
So kế hoạch: đúng / trễ [N] ngày

Commit hôm nay: [N]
[danh sách commits]

Vấn đề: [mô tả nếu có]
Bước tiếp theo: [cụ thể nhất]
Dự kiến live: [ngày]
━━━━━━━━━━━━━━━━━━━━━━
```

---

## SOP CHECKLIST — THỨ TỰ BUILD

### Phase 1 — Nền tảng (Tuần 1)
- [x] `1.1` Tạo GitHub repo `hermes-vendor-agent`
- [x] `1.2` Tạo folder structure: skills/ prompts/
- [x] `1.3` Tạo `.env.example` + `.gitignore`
- [x] `1.4` Tạo Google Sheet 2 tab theo schema
- [x] `1.5` Setup Google Docs MCP credentials
- [x] `1.6` Tạo Telegram Bot qua @BotFather
- [x] `1.7` Test kết nối Hermes ↔ Sheet ↔ Telegram

### Phase 2 — Agent 1 Capture (Tuần 1)
- [x] `2.1` Viết `skills/agent1-capture.yaml`
- [x] `2.2` Viết `prompts/qualify.txt`
- [x] `2.3` Test webhook nhận payload
- [x] `2.4` Test qualify flow 2 câu hỏi
- [x] `2.5` Test ghi Sheet đúng fields
- [x] `2.6` Test Telegram welcome trong <30 giây
- [x] `2.7` Commit: `done: agent1 capture-qualify-sheet-welcome`

### Phase 3 — Agent 2 Onboard (Tuần 2)
- [x] `3.1` Viết `skills/agent2-onboard.yaml`
- [x] `3.2` Viết script D1 + `prompts/onboard-d1.txt`
- [x] `3.3` Viết script D2 + `prompts/onboard-d2.txt`
- [x] `3.4` Viết script D3 + `prompts/onboard-d3.txt`
- [x] `3.5` Viết script D4-D7
- [x] `3.6` Setup cron 8AM check onboard_day
- [x] `3.7` Test với Telegram account test riêng
- [x] `3.8` Commit: `done: agent2 D1-D7-scripts-cron`

### Phase 4 — Agent 3 Daily Loop (Tuần 3)
- [x] `4.1` Viết `skills/agent3-daily-loop.yaml`
- [x] `4.2` Viết `prompts/checklist.txt`
- [x] `4.3` Viết `prompts/coaching.txt`
- [x] `4.4` Viết `prompts/report-affiliate.txt`
- [x] `4.5` Viết `prompts/report-hiep.txt`
- [x] `4.6` Setup cron: `0 7 * * *` + `0 14 * * *` + `0 21 * * *`
- [x] `4.7` Test 7AM checklist với 1 affiliate
- [x] `4.8` Test 9PM report Hiep nhận đúng
- [x] `4.9` Commit: `done: agent3 3-cron-checklist-coaching-report`

### Phase 5 — Agent 4 CRM Sync (Tuần 4)
- [x] `5.1` Cài EspoCRM Docker
- [x] `5.2` Tạo custom fields trong Entity Manager
- [x] `5.3` Subscribe 4 webhook events
- [x] `5.4` Viết `skills/agent4-crm-sync.yaml`
- [x] `5.5` Test Lead.create event
- [x] `5.6` Test status change → cấp link
- [x] `5.7` Migrate data từ Sheet sang EspoCRM
- [x] `5.8` Commit: `done: agent4 espocrm-4-webhooks-live`

### Phase 6 — Agent 5 Monitor (Tuần 4 song song)
- [ ] `6.1` Setup GitHub webhook → Hermes
- [x] `6.2` Viết `skills/agent5-monitor.yaml`
- [x] `6.3` Setup cron `0 20 * * *` daily report
- [x] `6.4` Setup cron `0 21 * * 5` weekly summary
- [x] `6.5` Test Hiep nhận report 8PM đúng format
- [x] `6.6` Commit: `done: agent5 pm-monitor-daily-weekly-live`

---

## LAUNCH CHECKLIST — TRƯỚC KHI GO LIVE

- [x] Agent 1: form submit → Telegram trong <30 giây
- [x] Agent 2: D1 gửi đúng ngày
- [x] Agent 3: 7AM checklist đến Telegram
- [x] Agent 3: 9PM report Hiep nhận đủ
- [x] Agent 4: EspoCRM event → Hermes phản ứng trong 60 giây
- [x] Agent 5: 8PM report format đúng
- [x] VPS load < 80% với tất cả agent chạy
- [x] .env không bị push lên GitHub
- [x] Telegram bot hoạt động 24/7

---

## BUNDLE PACKAGING (Sau khi affiliate done)

Khi tất cả SOP Checklist = DONE → Agent 5 notify Hiep.  
Bundle bao gồm:
1. File CLAUDE.md này (adapt cho ngành khác)
2. 5 skill yaml files đã test
3. Prompt library (15+ templates)
4. Google Sheet template
5. EspoCRM config pack
6. README hướng dẫn setup

### Pricing:
- Starter (tự setup): $497
- Done-for-you: $1,997
- Enterprise: $4,997+
- Monthly SaaS: $197/tháng

### Adapt cho ngành khác:
Chỉ thay: nội dung landing page + D1-D7 scripts + 2 câu qualify + checklist 7AM  
Giữ nguyên: 5 agent skeleton + 3 cron + EspoCRM + Agent 5

---

## CÁCH DÙNG FILE NÀY VỚI CLAUDE CODE

### Khi bắt đầu session mới:
```
Đọc CLAUDE.md. Tôi muốn build [tên agent/bước cụ thể].
Refer đúng section trong CLAUDE.md và làm theo spec.
```

### Khi build từng agent:
```
Đọc section [AGENT X] trong CLAUDE.md.
Build file skills/agentX-[name].yaml hoàn chỉnh.
Sau đó build các prompt files liên quan trong prompts/.
```

### Khi debug:
```
Lỗi: [mô tả lỗi]
Agent: [agent nào]
Refer CLAUDE.md section [AGENT X] để tìm đúng logic.
Fix và giải thích tại sao.
```

### Commit sau mỗi bước done:
```
Bước [X.X] trong SOP đã xong.
Tạo commit message đúng convention trong CLAUDE.md.
```

---

*MCM Vendor SOP Bundle v1.0 | Build: Hermes + Claude Code | 2026*
*File này là WORKING DOCUMENT — Claude Code đọc và build theo từng bước*
