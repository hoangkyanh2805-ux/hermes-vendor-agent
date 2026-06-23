# 5 AGENTS - CHỨC NĂNG CHI TIẾT

## AGENT 1 - CAPTURE & QUALIFY

**Loại:** HTTP Webhook Server (luôn chạy)  
**Port:** 3000  
**Trigger:** POST /webhook/capture từ landing page  
**Service:** `systemctl status mcm-agent1`

### Chức năng:

1. **Nhận lead từ landing page form submit**
   - Input: name, telegram_username, source (x_post, ads, organic)

2. **Gửi Q1 qua Telegram:** "Bạn đang có audience ở đâu?"
   - Choices: X (Twitter), Telegram, Facebook, YouTube Shorts

3. **Nhận answer Q1, gửi Q2:** "Mục tiêu thu nhập?"
   - Choices: <$500, $500-2K, $2K-5K, >$5K

4. **Gửi Q1+Q2 đến 9Router LLM để scoring**
   - Output: Hot / Warm / Cold

5. **Ghi vào Google Sheet:**
   - Affiliate Master: new row với lead info
   - Activity Log: lead_qualified event

6. **Gửi Telegram welcome message:**
   - Hot → FAST_TRACK (3-4 ngày onboard)
   - Warm/Cold → NURTURE (7 ngày onboard)

7. **Lưu state vào agent1_state.json**
   - State: stage (q1_sent, q2_sent, welcome_sent, done)

### Output:
✅ Lead qualified  
✅ Sheet có row mới  
✅ Activity Log có event  
✅ Affiliate nhận welcome message Telegram

---

## AGENT 2 - ONBOARDING D1-D7

**Loại:** Cron Job (chạy 1 lần/ngày)  
**Schedule:** 8:00 AM daily (0 8 * * *)  
**Script:** scripts/run-agent2.sh → agent2.py  
**Log:** /var/log/mcm-agent2.log

### Chức năng:

1. **Query Google Sheet** tìm affiliates status = "Onboarding"

2. **Check onboard_day (0-6):**
   - Day 0 → Send D1
   - Day 1 → Send D2
   - ...
   - Day 6 → Send D7

3. **Load prompt template** từ prompts/onboard-d{N}.txt

4. **Gửi prompt + affiliate data đến 9Router LLM**
   - Variables: {{name}}, {{channel}}, {{day}}, {{target_leads}}

5. **LLM generate personalized message** cho affiliate

6. **Gửi message qua Telegram Bot API**

7. **Update Sheet:**
   - onboard_day++
   - last_contact = now
   - D3+: status "Onboarding" → "Active"

8. **Ghi Activity Log:** onboard_message_sent

9. **Lưu state** vào agent2_state.json (idempotent, 1 message/day)

### Nội dung D1-D7:

- **D1:** Welcome + workflow intro (Telegram → X threads)
- **D2:** X thread format guide + examples (280 chars, hashtags)
- **D3:** Script mẫu copy-paste để dùng luôn
- **D4:** Hook optimization (8-12 từ đầu, action + urgency)
- **D5:** Scale strategy (2-3 threads/day)
- **D6:** Advanced tactics (A/B test hooks, timing)
- **D7:** Graduation + 30-day roadmap → Active affiliate

### Output:
✅ Affiliate nhận 1 message/ngày trong 7 ngày  
✅ Status "New" → "Onboarding" → "Active"  
✅ Có script + examples để post luôn

---

## AGENT 3 - DAILY LOOP (3 modes)

**Loại:** Cron Job (3 lần/ngày)  
**Schedule:** 7AM checklist, 2PM coaching, 9PM report  
**Script:** scripts/run-agent3.sh [mode]  
**Log:** /var/log/mcm-agent3.log

### MODE 1: CHECKLIST (7:00 AM)

**Chức năng:**
1. Query Sheet tìm Active/VIP affiliates
2. Load prompts/checklist.txt
3. LLM generate daily tasks (tối đa 3 việc):
   - Ví dụ: "1. Rewrite tin hiệu mới nhất từ azaam thành X thread"
   - "2. Post lúc 7-9AM với hashtags #xauusd #gold #forex"
   - "3. Reply 5 comments trong 10 phút đầu"
4. Gửi Telegram checklist cho từng affiliate
5. Ghi Activity Log: checklist_sent

**Output:** ✅ Mỗi affiliate nhận 3 tasks cụ thể hôm nay

### MODE 2: COACHING (2:00 PM)

**Chức năng:**
1. Query Sheet tìm affiliates inactive >3 days hoặc refer_this_week = 0
2. Load prompts/coaching.txt
3. LLM generate coaching message:
   - Chỉ ra vấn đề: "3 ngày chưa post"
   - Đề xuất 1 action: "Thử optimize hook theo pattern này"
   - Động viên: ngắn, thân thiện
4. Gửi Telegram 1-on-1
5. Ghi Activity Log: coaching_sent

**Output:** ✅ Affiliates drop nhận coaching cá nhân

### MODE 3: REPORT (9:00 PM)

**Chức năng:**
1. Query Sheet tất cả Active/VIP affiliates
2. Load prompts/report-affiliate.txt
3. LLM generate daily performance report:
   - Hôm nay earn: $X
   - Tổng refer tuần này: Y leads
   - Rank hiện tại: #N
   - Gap to next tier: Z leads
   - Tomorrow goal: "Post 2 threads, target 10 engagement"
4. Gửi Telegram cho từng affiliate
5. Ghi Activity Log: report_sent

**Output:** ✅ Mỗi affiliate biết performance + goal ngày mai

---

## AGENT 4 - CRM SYNC (Webhook Listener)

**Loại:** HTTP Webhook Server (luôn chạy)  
**Port:** 3001  
**Trigger:** POST /webhook từ EspoCRM  
**Service:** `systemctl status mcm-agent4`

### Chức năng:

1. **Lắng nghe EspoCRM webhook events:**
   - Lead.create
   - Contact.status_change
   - Opportunity.create
   - Contact.total_earn_update

2. **EVENT: Lead.create**
   - Tạo/update row trong Sheet
   - Notify Hiep qua Telegram

3. **EVENT: Contact.status_change (Qualified → Customer)**
   - Generate tracking link
   - Send link to affiliate qua Telegram
   - Update Sheet: tracking_link column

4. **EVENT: Opportunity.create (refer thành công)**
   - Increment refer_this_week
   - Update commission_total
   - Recalculate rank (#1-#100)
   - Check tier upgrade (Active → VIP)
   - Update Sheet

5. **EVENT: Contact.total_earn_update**
   - Sync earnings to Sheet
   - Recalc VIP tier (>10 refers/week)
   - Alert Agent 2 nếu promotable

6. **Ghi Activity Log** cho mọi event

### Output:
✅ Sheet luôn sync real-time với CRM  
✅ Commission + rank auto-update  
✅ Tier promotion tự động

---

## AGENT 5 - MONITOR & AUDIT (3 modes)

**Loại:** Cron Job (daily/weekly/hourly)  
**Schedule:** 8PM daily, 9PM Friday, hourly sync  
**Script:** scripts/run-agent5.sh [mode]  
**Log:** /var/log/mcm-agent5.log

### MODE 1: DAILY REPORT (8:00 PM)

**Chức năng:**
1. Query Sheet tất cả affiliates
2. Calculate metrics:
   - Total active: X affiliates
   - New today: Y
   - Total refers today: Z
   - Top performer: @username (N refers)
   - Drop risk: affiliates inactive >7 days
3. Check services health:
   - Agent 1, 4 status
   - 9Router uptime
   - Sheet API latency
4. Load prompts/report-pm.txt
5. LLM generate executive summary
6. Gửi Telegram cho Hiep (admin_chat_id)
7. Ghi Activity Log: pm_report_sent

**Output:** ✅ Hiep nhận daily summary mỗi tối

### MODE 2: WEEKLY SUMMARY (9:00 PM Friday)

**Chức năng:**
1. Query Sheet toàn bộ data tuần này
2. Calculate:
   - Total refers this week vs last week
   - New affiliates: X
   - Promoted to VIP: Y
   - Churned: Z (inactive >14 days)
   - Top 5 performers
   - Revenue trend
3. LLM generate weekly insights
4. Gửi Telegram cho Hiep
5. Trigger GitHub action (nếu có)
6. Ghi Activity Log: weekly_report_sent

**Output:** ✅ Hiep nhận weekly summary mỗi tối thứ 6

### MODE 3: SHEET→CRM SYNC (Every hour)

**Chức năng:**
1. Query Sheet: all rows
2. Query EspoCRM: all Contacts
3. Compare data:
   - Sheet có, CRM không có → create Contact
   - Sheet update, CRM stale → update Contact
   - CRM có, Sheet không có → alert Hiep (anomaly)
4. Bulk sync:
   - Batch 10 records/request
   - Rate limit: 1 req/second
5. Update Sheet: last_sync_time
6. Ghi Activity Log: sync_completed
7. Nếu có errors → notify Hiep

**Output:** ✅ Sheet ↔ CRM luôn sync (backup hourly)  
✅ Data consistency guaranteed

---

## FLOW TỔNG THỂ: LEAD → VIP

```
1. Lead submit form
   ↓ Agent 1
2. Q1 + Q2 → Score → Sheet → Welcome
   ↓ Agent 2
3. D1 (8AM ngày 1) → D2 (8AM ngày 2) → ... → D7 (8AM ngày 7)
   ↓ Status: Onboarding → Active
4. Daily loop starts (Agent 3):
   - 7AM: Checklist (rewrite Telegram signals to X threads)
   - 2PM: Coaching (nếu inactive)
   - 9PM: Report (rank, earn, goal)
   ↓ Affiliate posts threads, refers leads
5. Refer thành công
   ↓ Agent 4
6. CRM webhook → Sheet update: refer++, commission+, rank recalc
   ↓ Agent 3
7. Next day 9PM report: "Hôm nay +$50, rank #25, gap to #20: 3 leads"
   ↓ Repeat daily
8. Refer >10/week
   ↓ Agent 4
9. Tier: Active → VIP
   ↓ Agent 5
10. Weekly report: "@username promoted to VIP, total $500 this week"
```

**Hiep nhận:**
- 8PM daily: system health + top performers
- 9PM Friday: weekly summary + insights
- Real-time: CRM event alerts

**TẤT CẢ TỰ ĐỘNG, KHÔNG CẦN CAN THIỆP!** 🚀
