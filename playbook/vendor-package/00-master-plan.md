# Vendor Operation Layer — Master Plan

> Phase: BUILD (80%) → OPS (20%) | Updated: 2026-06-08
> Team: Tuấn (X farm) + Founder (strategy) + Claude (build)

---

## 1. Hiện Trạng

### Đã Build Xong

| Layer | Component | Status |
|-------|-----------|--------|
| **Infra** | 100-account GenLogin farm | ✅ Tuấn done |
| **Content** | Posting + reply + interact | ✅ Tuấn done |
| **Tracking** | Telegram invite links (15 links) | ⬜ Cần tạo thủ công |
| **Scripts** | 5 Python scripts v2 (1,196 dòng) | ✅ Deployed VPS |
| **Docs** | 8 tài liệu vendor-package | ✅ Done |
| **Config** | accounts-v2.json (100 accounts) | ✅ Done |

### Scripts v2 — Trên VPS

| Script | Dòng | Chức năng |
|--------|------|-----------|
| `funnel-db.py` | 307 | Cluster joins + payment 10K/join |
| `account-health.py` | 359 | 100-account tier risk scoring |
| `kpi-dashboard.py` | 228 | 2-sided view (company + team) |
| `content-router.py` | 210 | 3 nguồn + geo cluster routing |
| `content-analytics.py` | 230 | Cluster/source/hook/niche analysis |

---

## 2. Agents Được Kích Hoạt

```
marketing_boss (Hormozi+Seth)
    ├── Thiết kế KPI/OKR target (300/800/2000 joins)
    ├── Payment structure (10K/join, weekly billing)
    └── Brand consistency across 5 clusters

researcher (Ali+Hormozi)
    ├── Phân tích funnel data → insight
    ├── Bottom-line clarity trong báo cáo
    └── Data freshness gate

signal_funnel (Ali+Hormozi)
    ├── Journal-style tracking cho joins
    ├── Weekly/Monthly report template
    └── Growth metrics (week-over-week)

system_archivist (Seth+Ali)
    ├── SOP version control
    ├── Vendor package structure
    └── Document findability

lead_qualifier (Trump)
    ├── Payment rate negotiation (10K VND)
    ├── Invoice template
    └── "Decide. No hesitation." — approve/reject
```

---

## 3. Còn Thiếu

| # | Việc | Priority | Ai | Thời gian |
|---|------|----------|-----|-----------|
| 1 | **Tạo 15 Telegram invite links** | 🔴 P0 | Founder/Tuấn | 15 phút |
| 2 | **accounts.jsonl starter** | 🔴 P0 | `account-health.py init` | 1 lệnh |
| 3 | **Test funnel flow** | 🟡 P1 | Team Tuấn | 1 tuần |
| 4 | **Sync scripts v2 lên VPS** | 🟡 P1 | Claude | 5 phút |
| 5 | **Payment automation** | 🟢 P2 | Claude | 30 phút |
| 6 | **Alert system** | 🟢 P2 | Claude | 1 giờ |

---

## 4. KPI Target — 3 Tháng

| Tháng | Target Joins | OKR | Payment Budget |
|-------|-------------|-----|---------------|
| M1 (Jun) | 300 | 300 joins | 3,000,000 VND |
| M2 (Jul) | 800 | 800 joins | 8,000,000 VND |
| M3 (Aug) | 2,000 | 2000 joins | 20,000,000 VND |

**Breakeven:** Khi 1 VIP subscriber (97 USD/tháng) bù được cost của 4-5 joins (40-50K VND).

---

## 5. Lệnh Hằng Ngày

```bash
# Team Tuấn — mỗi tối
python3 /root/hermes-bin/vendor-layer/kpi-dashboard.py --summary

# Founder — mỗi sáng
python3 /root/hermes-bin/vendor-layer/kpi-dashboard.py --company

# Thứ 2 — payment
python3 /root/hermes-bin/vendor-layer/funnel-db.py payment --week
```

---

## 6. Agents Gọi Hỗ Trợ

Trên @hermes7979_bot:

```text
dashboard           → KPI dashboard (company + team view)
funnel stats        → Cluster summary + payment
account health      → 100-account risk overview  
content queue       → Content routing status
content analytics   → Best cluster/source/hook
```
