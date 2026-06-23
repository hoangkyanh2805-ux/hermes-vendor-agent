# Content Routing System — Hermes X Farm

> Cho: Team Tuấn | Cập nhật: 2026-06-08
> Mục tiêu: Quản lý luồng content từ nguồn → 4 account → lịch đăng

---

## Content Flow

```
Nguồn (@azzamgoldpro / content_creator)
        │
        ▼
  [Queue] ── Chọn bài ── Gán format ── Check duplicate
        │
        ▼
  [Route] ── Gán account ── Chọn giờ ── Check lịch
        │
        ▼
  [Publish] ── GenLogin ── Đăng ── Log
        │
        ▼
  [Track] ── Ghi nhận ── Đo engagement ── Báo cáo
```

---

## Content Queue — Template

Điền mỗi sáng:

| ID | Nội dung (tóm tắt) | Format | Hook | Account | Giờ | Status |
|----|-------------------|--------|------|---------|-----|--------|
| 1 | "Gold setup forming..." | signal_tease | scarcity | Founder | 12:00 | ☐ |
| 2 | "BE rule saves accounts" | risk_post | loss_aversion | Risk | 12:30 | ☐ |
| 3 | "BOS confirmed on H1" | structure_read | authority | SMC | 13:00 | ☐ |
| 4 | "DXY softening, yields..." | macro_context | specificity | Macro | 16:00 | ☐ |
| 5 | "Failed 3 challenges..." | story_post | pratfall | Founder | 17:00 | ☐ |

---

## Lịch Đăng Chuẩn — Mỗi Ngày

| Giờ (GMT+7) | UTC | Account | Loại content ưu tiên |
|-------------|-----|---------|---------------------|
| 08:00 | 01:00 | Macro | Data snapshot, calendar |
| 12:00 | 05:00 | Founder | Signal tease, education |
| 12:30 | 05:30 | Risk | Risk post, discipline |
| 13:00 | 06:00 | SMC | Structure read, concept |
| 16:00 | 09:00 | Macro | Market context, news |
| 16:30 | 09:30 | Founder | Proof post, journal |
| 17:00 | 10:00 | Risk | BE rule, position sizing |
| 20:00 | 13:00 | SMC | Education thread |

---

## Quy Tắc Phân Phối

### Format Rotation (không lặp 2 ngày liên tiếp)

| Account | Format pool |
|---------|------------|
| Founder | signal_tease → education_post → proof_post → market_note → story_post |
| Risk | risk_post → discipline_quote → position_sizing → journal_stat → risk_post |
| SMC | structure_read → session_setup → concept_edu → market_note → structure_read |
| Macro | data_snapshot → macro_context → calendar_preview → market_note → data_snapshot |

### Hook Rotation (không lặp 24h)

```
Hôm nay dùng: scarcity → Ngày mai: loss_aversion → Ngày kia: authority...
Mỗi ngày chọn 1 hook KHÁC cho mỗi account.
```

---

## Anti-Duplicate Check

Trước khi vào queue, kiểm tra:

- [ ] Nội dung này đã đăng trong 7 ngày qua chưa?
- [ ] Account này đã dùng format này hôm qua chưa?
- [ ] Account này đã dùng hook này trong 24h chưa?
- [ ] Có trùng >80% text với bài khác không?

Nếu CÓ bất kỳ → **chọn bài khác.**

---

## Content Categories

Mỗi account có thế mạnh riêng. Phân bổ theo tỉ lệ:

| Category | Founder | Risk | SMC | Macro |
|----------|---------|------|-----|-------|
| Education | 20% | 20% | 40% | 20% |
| Market context | 20% | 10% | 20% | 40% |
| Proof/Journal | 30% | 20% | 10% | 10% |
| Discipline | 20% | 40% | 20% | 10% |
| Engagement | 10% | 10% | 10% | 20% |
