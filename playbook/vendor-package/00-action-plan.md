# Vendor Operation Layer — Action Plan

> Audit bởi: marketing_boss + researcher + signal_funnel + system_archivist + lead_qualifier
> Date: 2026-06-08 | Status: ACTIONABLE

---

## ĐỢT 1 — Fix Critical (hôm nay)

### 1.1 Thêm cronjob daily snapshot

```bash
# Trên VPS — chạy mỗi 23:55
crontab -e
# Thêm:
55 23 * * * python3 /root/hermes-bin/vendor-layer/funnel-db.py snapshot
```

**Agent:** signal_funnel | **Effort:** 2 phút | **Impact:** Có dữ liệu week-over-week

### 1.2 Thêm quality gate vào payment

Script mới: `funnel-db.py verify` — check spam joins trước khi thanh toán.

```python
# Logic: nếu 1 source có >50 joins trong <1 giờ → flag spam
python3 /root/hermes-bin/vendor-layer/funnel-db.py verify --cluster gulf
```

**Agent:** lead_qualifier | **Effort:** 30 phút | **Impact:** Không trả tiền cho spam

### 1.3 Tạo 1-page weekly summary

Script mới: `weekly-summary.py` — gộp 5 data source thành 1 báo cáo.

```
═══ HERMES WEEKLY — Week 24 ═══
Joins: 47 (+12% vs last week) | Target: 75 | Remaining: 28
Top cluster: Gulf (18 joins, 38%)
Top source: azzamgoldpro (60% of published)
Account health: 95/100 active | 5 suspended
Payment: 470,000 VND
═══ 1 câu bottom line: Gulf đang dẫn đầu, Europe cần thêm content ═══
```

**Agent:** researcher | **Effort:** 45 phút | **Impact:** 1 file thay vì 5

### 1.4 Realistic OKR baseline

Tính target dựa trên thực tế:

```
100 accounts × 3 posts/day × 100 impressions/post = 30,000 impressions/day
× 0.1% CTR = 30 clicks/day
× 30% join rate = 9 joins/day
× 30 ngày = 270 joins/tháng (baseline thực tế)

→ M1 target: 270 (không phải 300)
→ M2 target: 540 (tăng gấp đôi sau khi tối ưu)
→ M3 target: 1,080
```

**Agent:** marketing_boss | **Effort:** 10 phút | **Impact:** Target realistic

---

## ĐỢT 2 — Nâng Cao (tuần này)

### 2.1 Tiered payment structure

```python
# Cập nhật funnel-db.py payment
VND_PER_JOIN = {
    "T1": 15_000,  # Chất lượng cao nhất
    "T2": 10_000,  # Tiêu chuẩn
    "T3":  7_000,  # Số lượng
}
```

**Agent:** lead_qualifier | **Effort:** 30 phút

### 2.2 A/B test tracking

Thêm `content-analytics.py ab-test` — so sánh 2 hook/format trong cùng cluster.

```bash
python3 /root/hermes-bin/vendor-layer/content-analytics.py ab-test \
  --hook_a question_hook --hook_b number_pattern --cluster gulf --days 14
```

**Agent:** researcher | **Effort:** 1 giờ

### 2.3 Alert system

Script `alert.py` — cronjob mỗi sáng, check:
- Account suspended? → Telegram alert
- Joins = 0 trong 3 ngày liên tiếp? → Alert
- CTR < 0.1%? → Alert

**Agent:** signal_funnel | **Effort:** 1 giờ

---

## ĐỢT 3 — Tối Ưu (tuần sau)

### 3.1 VIP conversion tracking

Thêm pipeline: Joins → DM → Lead score → VIP sale → Revenue

```python
# funnel-db.py add --source x_gulf_t1_01 --event vip_sale --value 97
```

**Agent:** marketing_boss | **Effort:** 1.5 giờ

### 3.2 Document index + quick reference

File `vendor-package/INDEX.md` — bảng "Vấn đề → Đọc file nào"

**Agent:** system_archivist | **Effort:** 30 phút

### 3.3 Performance bonus calculator

```python
python3 /root/hermes-bin/vendor-layer/funnel-db.py bonus --month
# Output: Gulf vượt target 20% → bonus 200,000 VND
```

**Agent:** lead_qualifier | **Effort:** 45 phút

---

## Tổng Kết

| Đợt | Việc | Effort | Agent chủ trì |
|------|------|--------|---------------|
| 1.1 | Cronjob snapshot | 2ph | signal_funnel |
| 1.2 | Quality gate verify | 30ph | lead_qualifier |
| 1.3 | Weekly summary | 45ph | researcher |
| 1.4 | Realistic OKR baseline | 10ph | marketing_boss |
| 2.1 | Tiered payment | 30ph | lead_qualifier |
| 2.2 | A/B test tracking | 1h | researcher |
| 2.3 | Alert system | 1h | signal_funnel |
| 3.1 | VIP conversion tracking | 1.5h | marketing_boss |
| 3.2 | Document index | 30ph | system_archivist |
| 3.3 | Bonus calculator | 45ph | lead_qualifier |

**Tổng effort: ~7 giờ | Ưu tiên: Đợt 1 (1.5h) → dùng được ngay mai**
