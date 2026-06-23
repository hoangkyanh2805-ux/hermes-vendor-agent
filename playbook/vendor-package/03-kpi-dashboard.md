# KPI Dashboard — Hermes X Farm

> Cho: Team Tuấn + Founder | Cập nhật: hàng ngày
> Dùng: Copy bảng này → điền số → gửi Founder mỗi tối

---

## KPI Chính — Theo Dõi Hàng Ngày

### Bảng A: Content Output

| Ngày | Founder @azzam_gold | Risk @goldrisk_vip | SMC @smc_xauusd | Macro @goldmacro_ | TỔNG |
|------|--------------------|--------------------|--------------------|--------------------|------|
| T2 | | | | | |
| T3 | | | | | |
| T4 | | | | | |
| T5 | | | | | |
| T6 | | | | | |
| T7 | | | | | |
| CN | | | | | |
| **Tuần** | | | | | |

### Bảng B: Engagement

| Ngày | Likes | Replies | Retweets | Impressions | Engagement Rate |
|------|-------|---------|----------|-------------|-----------------|
| T2 | | | | | |
| T3 | | | | | |
| ... | | | | | |
| **Tuần** | | | | | |

### Bảng C: Funnel (X → Telegram)

| Ngày | Clicks | Joins | CTR | Cost (VNĐ) | Cost/Sub (VNĐ) |
|------|--------|-------|-----|------------|-----------------|
| T2 | | | | | |
| T3 | | | | | |
| ... | | | | | |
| **Tuần** | | | | | |

---

## KPI Mục Tiêu — 3 Tháng (Realistic Baseline — Đã Audit 2026-06-08)

### Cách Tính (marketing_boss Hormozi audit)

```
Daily Joins = Active Accounts × Posts/Day × Impressions/Post × CTR × Join Rate
Monthly    = Daily Joins × 30

M1 Baseline: 80 active × 3 posts × 100 imp × 0.1% CTR × 30% join = 7.2/day → 220/month
M2 Optimized: 90 active × 4 posts × 150 imp × 0.2% CTR × 35% join = 37.8/day → 1,100/month
M3 Scale: 100 active × 4 posts × 200 imp × 0.25% CTR × 40% join = 80/day → 2,400/month
```

| Tháng | Target Joins | Payment Budget | Scenario |
|-------|-------------|---------------|----------|
| **M1 (Jun)** | **220** | 2,200,000 VND | Realistic Baseline |
| **M2 (Jul)** | **1,100** | 11,000,000 VND | Optimized |
| **M3 (Aug)** | **2,400** | 24,000,000 VND | Scale |

### Weekly Target — M1 (Jun)

| Week | Target | Status |
|------|--------|--------|
| W1 (Jun 8-14) | 25 | ☐ |
| W2 (Jun 15-21) | 40 | ☐ |
| W3 (Jun 22-28) | 55 | ☐ |
| W4 (Jun 29-Jul 5) | 70 | ☐ |

> **So với target cũ:** M1: 300→220 (thực tế hơn 27%), M2: 800→1,100 (có cơ sở), M3: 2000→2,400 (scale đúng)

---

## Dashboard Nhanh (in ra treo tường)

```
┌─────────────────────────────────────────┐
│  HERMES X FARM — WEEK __                │
├─────────────────────────────────────────┤
│  Posts:  ___ / 40 target                │
│  Clicks: ___ → Joins: ___ (___% CTR)    │
│  Best account: _______________          │
│  Account health: 🟢🟢🟢🟢               │
│  Cost/sub: ______ VNĐ                   │
└─────────────────────────────────────────┘
```

---

## Cách Đo

| Metric | Công cụ | Tần suất |
|--------|---------|----------|
| Bài đăng | Đếm tay + content-router.py | Hàng ngày |
| Impressions | X Analytics (mỗi account) | Hàng tuần |
| Likes/Replies/RT | X Analytics | Hàng ngày |
| Clicks | Telegram Invite Links | Hàng tuần |
| Joins | Telegram Settings → Invite Links | Hàng tuần |
| CTR | Joins ÷ Clicks × 100 | Hàng tuần |
| Cost | Tổng chi phí team ÷ số subscriber mới | Hàng tháng |

---

## Cách Tính Cost/Subscriber

```
Cost/Sub = (Chi phí team tháng + Chi phí tool tháng) ÷ Số subscriber mới

Ví dụ:
  Team: 5,000,000đ/tháng
  Tool: 500,000đ/tháng (proxy, GenLogin)
  Sub mới: 500/tháng
  → Cost/Sub = 11,000đ

Mục tiêu: <10,000đ/subscriber
```
