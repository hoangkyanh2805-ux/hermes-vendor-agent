# Payment Invoice Template — Hermes X Farm

> Cho: Team Tuấn + Founder | Dùng: Thứ 2 hàng tuần
> Tự động: `python3 /root/hermes-bin/vendor-layer/funnel-db.py payment --week`
> Rate: 10,000 VND / valid Telegram join

---

## Invoice — Tuần ___ (___/___ - ___/___)

```
═══════════════════════════════════════════
  HERMES X FARM — PAYMENT INVOICE
═══════════════════════════════════════════

Date: ___/___/2026
Period: ___/___ - ___/___
Prepared by: _______________
Approved by: _______________

───────────────────────────────────────────
  CLUSTER BREAKDOWN
───────────────────────────────────────────
  Cluster         Joins    Rate       Amount
───────────────────────────────────────────
  Gulf             ___    10,000đ    _______ VND
  Europe           ___    10,000đ    _______ VND
  Africa           ___    10,000đ    _______ VND
  South Asia       ___    10,000đ    _______ VND
  Americas         ___    10,000đ    _______ VND
  Legacy           ___    10,000đ    _______ VND
───────────────────────────────────────────
  TOTAL            ___               _______ VND
═══════════════════════════════════════════

Payment method: _______________
Payment due: ___/___/2026
Status: ☐ Paid  ☐ Pending

───────────────────────────────────────────
  NOTES
───────────────────────────────────────────
  • Rate cố định: 10,000 VND/join
  • Minimum payout: 50,000 VND (5 joins)
  • Thanh toán: Thứ 2 hàng tuần
  • Link tracking: Telegram Invite Links
  • Data source: /root/hermes-data/tracking/funnel.jsonl
───────────────────────────────────────────

Signed: _______________  Date: _______________
```

---

## Cách Dùng

### Tự động (VPS)

```bash
# Xem payment report tuần này
python3 /root/hermes-bin/vendor-layer/funnel-db.py payment --week

# Xem payment report tháng này
python3 /root/hermes-bin/vendor-layer/funnel-db.py payment --month

# Xuất toàn bộ cluster summary
python3 /root/hermes-bin/vendor-layer/funnel-db.py clusters
```

### Thủ công (nếu VPS chưa có data)

1. Mở Telegram → @azzamgoldpro → Settings → Invite Links
2. Đếm joins mỗi link
3. Điền vào bảng trên
4. Tính: joins × 10,000đ = payment
5. Gửi invoice cho Founder duyệt

---

## Verification Checklist

Trước khi thanh toán, xác nhận:

- [ ] Số joins khớp với Telegram Invite Links (không bịa)
- [ ] Mỗi cluster có ít nhất 1 link tracking
- [ ] Legacy accounts vẫn đang tracking
- [ ] Không có join spam/bot (check tần suất bất thường)
- [ ] Founder đã approve

---

## Monthly Rollup

| Tháng | Gulf | Europe | Africa | S.Asia | Americas | Legacy | TỔNG | Payment |
|-------|------|--------|--------|--------|----------|--------|------|---------|
| 6/2026 | | | | | | | | |
| 7/2026 | | | | | | | | |
| 8/2026 | | | | | | | | |
