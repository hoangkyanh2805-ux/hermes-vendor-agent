# VENDOR OPS RUNBOOK — Vận Hành Hàng Ngày / Tuần / Tháng

> **Owner:** Admin/Founder + @hermes7979_bot (auto)
> **Dùng chung với:** VENDOR-GROUP-OPS-RUNBOOK.md (ops hiện có) + 11-group-deployment-pack.md (deploy)
> **Agent ecosystem:** marketing_boss (orchestrator) → vendor_qualifier + vendor_draft_review + community_vendor_guide + signal_funnel
> **Date:** 2026-06-15 | **Status:** Runbook sẵn sàng — dùng ngay khi bot live

---

## 1. AGENT MAP — Ai Làm Gì Trong Vendor OPS

```
marketing_boss (orchestrator — VENDOR_GROWTH mode)
│
├── vendor_qualifier (NEW — adapt từ lead_qualifier V5)
│   ├── Score vendor applicants (5-signal rubric)
│   ├── PASS/SOFT_PASS/FAIL → vào group hoặc hẹn lại
│   └── Gate: X profile public, real, non-spam
│
├── vendor_draft_review (NEW — adapt từ content_creator V5)
│   ├── Review vendor drafts (6-checkpoint rubric)
│   ├── APPROVE/REWRITE (kèm bản sửa)/REJECT (kèm lý do)
│   └── Gate: source attribution, copy risk, CTA, fake claim
│
├── community_vendor_guide (UPGRADED V6)
│   ├── Auto-reply vendor FAQ (13 cards)
│   ├── Auto-nudge Tuan 1 (7 ngày activation)
│   ├── Auto-remind Active vendor chưa post
│   └── Escalate: payout/signal/abuse → admin
│
├── signal_funnel (UPDATED V5 + vendor metrics)
│   ├── Weekly vendor report + RANK BOARD
│   ├── Activation rate tracking
│   ├── Churn detection (>14d no post)
│   └── Rank promotion/demotion computation
│
├── system_archivist (EXISTING V5 — vendor paths added)
│   ├── Vendor knowledge pack versioning
│   ├── Vendor SOUL backup
│   └── Vendor registry archive
│
└── researcher (EXISTING V5 — vendor source research)
    ├── Research new recruitment sources
    └── Analyze competitor affiliate programs
```

---

## 2. DAILY OPS — Admin + Bot

```
┌──────┬──────────┬────────────────────────────────────────────────────────┐
│ Giờ   │ Actor    │ Hành động                                              │
├──────┼──────────┼────────────────────────────────────────────────────────┤
│ 08:00 │ 🤖 Bot   │ vendor_nudge cron chạy:                                │
│      │          │ → Quét vendor-registry.json                             │
│      │          │ → Tìm vendor chưa first post                            │
│      │          │ → Tính day N = today - join_date                        │
│      │          │ → Gửi nudge tương ứng vào Tuan 1 topic                  │
│      │          │ → N>7 chưa post → flag cold → báo admin                 │
├──────┼──────────┼────────────────────────────────────────────────────────┤
│ 09:00 │ 👨‍💼 Admin │ Mở Telegram vendor group:                              │
│      │          │ [ ] Check Goc thac mac — bot trả lời đúng không?        │
│      │          │ [ ] Check Post Log — có bài mới chưa validate?          │
│      │          │ [ ] Check Tuan 1 — nudge đã gửi đúng?                   │
│      │          │ [ ] Check Feedback loi — có issue cần xử lý?            │
│      │          │ [ ] Đăng daily content pack vào Thong bao (nếu có)      │
├──────┼──────────┼────────────────────────────────────────────────────────┤
│ 09:30 │ 👨‍💼 Admin │ Review vendor applicants (nếu có):                      │
│      │          │ [ ] Đọc 3 câu trả lời + X profile                      │
│      │          │ [ ] Gọi vendor_qualifier nếu cần score tự động          │
│      │          │ [ ] PASS → gửi invite link + tag vào group              │
│      │          │ [ ] FAIL → gửi lịch sự + hẹn quay lại                   │
├──────┼──────────┼────────────────────────────────────────────────────────┤
│ 12-18 │ 👨‍💼 Admin │ Review vendor drafts (nếu vendor gửi):                   │
│      │          │ [ ] Check 6 checkpoints (Card 5)                        │
│      │          │ [ ] Gọi vendor_draft_review nếu muốn auto               │
│      │          │ [ ] APPROVE → "OK đăng đi em"                           │
│      │          │ [ ] REWRITE → gửi bản sửa + giải thích                  │
│      │          │ [ ] REJECT → nêu lý do + hướng dẫn làm lại              │
├──────┼──────────┼────────────────────────────────────────────────────────┤
│ 18:00 │ 🤖 Bot   │ vendor_reminder cron chạy:                              │
│      │          │ → Quét Active vendor chưa post hôm nay                  │
│      │          │ → Gửi reminder nhẹ: "Còn 30ph — chưa thấy post-log"     │
├──────┼──────────┼────────────────────────────────────────────────────────┤
│ 20:00 │ 👨‍💼 Admin │ EOD check:                                              │
│      │          │ [ ] Đếm bài đã đăng hôm nay?                            │
│      │          │ [ ] Check funnel-db.py dashboard — joins hôm nay?       │
│      │          │ [ ] Log valid_join nếu có join mới                      │
│      │          │ [ ] Note vấn đề → báo founder nếu cần                   │
│      │          │ [ ] Chạy funnel-db.py snapshot                          │
└──────┴──────────┴────────────────────────────────────────────────────────┘
```

---

## 3. WEEKLY OPS — Thứ 2 (Payment + Rank)

```
┌──────┬──────────┬────────────────────────────────────────────────────────┐
│ Giờ   │ Actor    │ Hành động                                              │
├──────┼──────────┼────────────────────────────────────────────────────────┤
│ 09:00 │ 🤖 Bot   │ vendor_weekly cron chạy:                               │
│      │          │ → Chạy funnel-db.py report --weekly                     │
│      │          │ → Chạy funnel-db.py payment --week                      │
│      │          │ → Tính toán RANK BOARD (promotion/demotion)             │
│      │          │ → Auto-post Weekly Report vào Thong bao                 │
├──────┼──────────┼────────────────────────────────────────────────────────┤
│ 10:00 │ 👨‍💼 Admin │ Verify weekly report:                                    │
│      │          │ [ ] Check số joins — khớp với Telegram Invite Links?    │
│      │          │ [ ] Check RANK BOARD — promotion/demotion hợp lý?       │
│      │          │ [ ] Check best post — vendor nào dẫn đầu?               │
│      │          │ [ ] Confirm payment estimate                            │
│      │          │ [ ] Nếu có vendor cần thanh toán → chuyển tiền          │
├──────┼──────────┼────────────────────────────────────────────────────────┤
│ 11:00 │ 👨‍💼 Admin │ Vendor health check:                                     │
│      │          │ [ ] List cold vendors (>14d no post) → DM check-in      │
│      │          │ [ ] Activation rate: % new vendor first post trong 7d?  │
│      │          │ [ ] Churn: có vendor nào bỏ tuần này?                   │
│      │          │ [ ] Draft quality: APPROVE/REWRITE/REJECT ratio         │
│      │          │ [ ] Nếu activation <40% → tăng nudge intensity          │
├──────┼──────────┼────────────────────────────────────────────────────────┤
│ 12:00 │ 👨‍💼 Admin │ Outreach — đăng pitch tuyển vendor (theo lịch):           │
│      │          │ [ ] Chọn 2-3 nguồn từ vendor-recruit-100.csv            │
│      │          │ [ ] Đăng pitch theo vendor-outreach-kit.md              │
│      │          │ [ ] Reply comment/DM từ tuần trước                      │
└──────┴──────────┴────────────────────────────────────────────────────────┘
```

---

## 4. MONTHLY OPS — Đầu Tháng

```
[ ] Tổng kết vendor KPI tháng (gọi marketing_boss VENDOR_GROWTH mode)
[ ] Review rank ladder — ai cần thăng/giáng thủ công?
[ ] Audit vendor knowledge pack — cần update card nào không?
[ ] Backup vendor-registry.json + funnel.jsonl
[ ] Research thêm nguồn tuyển mới → cập nhật vendor-recruit-100.csv
[ ] Đánh giá bot performance: reply accuracy, nudge timing, error rate
[ ] Gửi Monthly Vendor Report cho founder
[ ] Đề xuất thay đổi policy (nếu có) → founder duyệt
```

---

## 5. ESCALATION RUNBOOK — Bot → Admin

```
┌──────────────────────────┬────────────────────────────────────────────────┐
│ Tình huống                │ Admin xử lý                                    │
├──────────────────────────┼────────────────────────────────────────────────┤
│ Bot detect "payout",     │ → DM riêng vendor                               │
│ "tiền", "thanh toán",    │ → Không confirm trong group                     │
│ "khiếu nại"              │ → "Phần này admin sẽ trao đổi riêng nhé"       │
│                          │ → Check tracker → xác nhận hoặc giải thích     │
├──────────────────────────┼────────────────────────────────────────────────┤
│ Bot detect "Entry",      │ → DM riêng vendor                               │
│ "SL", "TP" trong draft   │ → "Em vui lòng không chia sẻ Entry/SL/TP       │
│                          │   cụ thể. Chỉ dùng context chung từ source."   │
├──────────────────────────┼────────────────────────────────────────────────┤
│ Vendor report link       │ → Xác nhận link có tồn tại không               │
│ không hoạt động          │ → Nếu link chết → báo vendor sửa               │
│                          │ → Nếu bài bị xóa → không tính join              │
├──────────────────────────┼────────────────────────────────────────────────┤
│ Vendor bị report spam    │ → Check vendor history                         │
│ / vi phạm rule           │ → Revoke link nếu vi phạm nghiêm trọng (V1-V6)│
│                          │ → Hold payout pending review                   │
│                          │ → Không tranh luận trong group                 │
├──────────────────────────┼────────────────────────────────────────────────┤
│ Bot không trả lời        │ → Check VPS: bot còn chạy không?               │
│ (down)                   │ → Nếu bot down → admin trả lời thủ công        │
│                          │   dùng community_vendor_guide manual           │
│                          │ → Restart bot + check log lỗi                  │
├──────────────────────────┼────────────────────────────────────────────────┤
│ Bot trả lời sai          │ → Admin sửa ngay trong group                   │
│                          │ → "Bot trả lời chưa chính xác. Đây là câu      │
│                          │   trả lời đúng: [correct answer]"              │
│                          │ → Log lỗi → cập nhật knowledge pack nếu cần   │
├──────────────────────────┼────────────────────────────────────────────────┤
│ Vendor mới join nhưng    │ → Admin gửi welcome message thủ công            │
│ bot không detect         │ → Check vendor-registry.json — vendor đã       │
│                          │   được ghi chưa? Nếu chưa → thêm thủ công      │
├──────────────────────────┼────────────────────────────────────────────────┤
│ Có vendor muốn rời       │ → Hỏi lý do (không bắt buộc)                    │
│                          │ → Cảm ơn + chúc may mắn                        │
│                          │ → Update registry: status=inactive              │
│                          │ → Revoke tracking link                          │
│                          │ → Không thuyết phục ở lại — tôn trọng quyết định│
└──────────────────────────┴────────────────────────────────────────────────┘
```

---

## 6. BOT MAINTENANCE — Xử Lý Sự Cố

### Bot Down — Triệu Chứng & Cách Fix

```
TRIỆU CHỨNG:
  - Vendor gõ /help → không trả lời
  - Nudge 08:00 không gửi
  - Post-log không được validate

CHECKLIST:
  [ ] SSH vào VPS: ssh root@103.97.126.117
  [ ] Check process: ps aux | grep vendor_listener
  [ ] Check process: ps aux | grep vendor_nudge
  [ ] Check log: tail -100 /root/hermes-data/logs/vendor-bot.log
  [ ] Check .env: cat /root/hermes-bin/vendor-bot/.env (token còn valid?)
  [ ] Check disk: df -h (hết disk không?)
  [ ] Check RAM: free -m (hết RAM không?)

FIX:
  [ ] Restart: cd /root/hermes-bin/vendor-bot && ./restart.sh
  [ ] Check lại: gõ /help trong group → bot trả lời?
  [ ] Nếu vẫn fail → check Telegram Bot API status
  [ ] Nếu token hết hạn → tạo token mới → cập nhật .env
  [ ] Báo founder nếu >30ph chưa fix được
```

### Bot Trả Lời Sai — Cách Sửa

```
[ ] Ghi lại chính xác câu hỏi + câu trả lời sai của bot
[ ] Xác định lỗi: sai card? sai routing? sai guardrail?
[ ] Cập nhật knowledge pack nếu card thiếu / sai
[ ] Cập nhật SOUL nếu intent routing sai
[ ] Test lại: gửi câu hỏi tương tự → bot trả lời đúng chưa?
[ ] Báo founder nếu lỗi nghiêm trọng (lộ internal info, confirm payout sai)
```

---

## 7. QUICK REFERENCE — Lệnh & File

### Lệnh VPS thường dùng

```bash
# Xem vendor funnel
python3 /root/hermes-bin/vendor-layer/funnel-db.py dashboard

# Xem weekly report
python3 /root/hermes-bin/vendor-layer/funnel-db.py report --weekly

# Xem payment
python3 /root/hermes-bin/vendor-layer/funnel-db.py payment --week

# Log event
python3 /root/hermes-bin/vendor-layer/funnel-db.py log --source x_gulf_v_tuan --join
python3 /root/hermes-bin/vendor-layer/funnel-db.py log --source x_gulf_v_tuan --valid-join --vendor tuan
python3 /root/hermes-bin/vendor-layer/funnel-db.py activate --vendor tuan

# Snapshot EOD
python3 /root/hermes-bin/vendor-layer/funnel-db.py snapshot

# Bot control
cd /root/hermes-bin/vendor-bot && ./restart.sh
cd /root/hermes-bin/vendor-bot && ./status.sh

# Xem vendor registry
cat /root/hermes-data/vendor-registry.json | python3 -m json.tool

# Xem bot log
tail -50 /root/hermes-data/logs/vendor-bot.log
```

### File quan trọng

| File | Dùng khi |
|------|---------|
| `VENDOR_KNOWLEDGE_PACK.md` | Bot trả lời vendor — 13 cards |
| `community_vendor_guide-SOUL.md` | Cấu hình bot agent |
| `vendor_qualifier_SOUL.md` | Score applicant tự động |
| `vendor_draft_review_SOUL.md` | Review draft tự động |
| `vendor-registry.json` | Kiểm tra trạng thái vendor |
| `funnel.jsonl` | Data gốc — không sửa tay |
| `vendor-recruit-100.csv` | Chọn nguồn đăng pitch |
| `vendor-outreach-kit.md` | Template pitch từng kênh |
| `vendor-icp-bundles.md` | Pitch cho 5 ICP khác nhau |

---

## 8. GUARDRAIL — OPS

```
✅ Mỗi sáng check group 5 phút — bot + admin = 2 lớp bảo vệ
✅ Mỗi thứ 2 chạy payment + rank — không trễ
✅ Mỗi tuần đăng pitch 2-3 nơi — giữ pipeline tuyển
✅ Mỗi tháng review KPI + update knowledge pack nếu cần
✅ Bot down → admin cover thủ công ngay — không để vendor chờ

❌ KHÔNG confirm payout trong group — luôn DM riêng
❌ KHÔNG để bot chạy 1 mình >48h không check
❌ KHÔNG sửa funnel.jsonl tay — dùng funnel-db.py
❌ KHÔNG tự đổi payment rate — escalate founder
❌ KHÔNG tuyển vendor ồ ạt khi activation rate <40% — fix activation trước
```
