# Daily Operations SOP — Hermes X Farm

> Cho: Team Tuấn | Cập nhật: 2026-06-08
> Dùng: In ra / mở mỗi sáng — tick khi xong

---

## Tổng quan ngày

```
SÁNG (08:00-09:00):  Ingest content → Queue
TRƯA (12:00-13:00):  Đăng bài phiên London
CHIỀU (16:00-17:00): Đăng bài phiên NY + Reply
TỐI (20:00-20:30):   Check + EOD report
```

---

## Checklist hằng ngày

### SLOT SÁNG — 08:00-09:00

| # | Việc | Làm gì | Xong |
|---|------|--------|------|
| 1 | **Check nguồn** | Đọc @azzamgoldpro — có tín hiệu mới không? | ☐ |
| 2 | **Check account** | Mở GenLogin — 4 account có bị khóa/checkpoint không? | ☐ |
| 3 | **Lên queue** | Chọn 2-4 bài cho hôm nay từ content có sẵn | ☐ |
| 4 | **Route** | Gán bài vào account: Founder 1-2, Risk 1, SMC 1, Macro 1 | ☐ |
| 5 | **Log health** | Ghi số bài dự kiến hôm nay vào tracker | ☐ |

### SLOT TRƯA — 12:00-13:00 (London session)

| # | Việc | Làm gì | Xong |
|---|------|--------|------|
| 1 | **Đăng Founder** | @azzam_gold: 1 bài signal_tease hoặc education | ☐ |
| 2 | **Đăng Risk** | @goldrisk_vip: 1 bài risk_post hoặc discipline | ☐ |
| 3 | **Đăng SMC** | @smc_xauusd: 1 bài structure_read | ☐ |
| 4 | **Ghi nhận** | Ghi số bài đã đăng vào tracker | ☐ |

### SLOT CHIỀU — 16:00-17:00 (NY session)

| # | Việc | Làm gì | Xong |
|---|------|--------|------|
| 1 | **Đăng Macro** | @goldmacro_: 1 bài macro_context hoặc data | ☐ |
| 2 | **Reply** | Check reply trên 4 account — trả lời comment thật | ☐ |
| 3 | **Engage** | Like 3 bài, reply 3 bài, retweet 3 bài trong niche | ☐ |
| 4 | **Ghi nhận** | Ghi số reply + engage vào tracker | ☐ |

### SLOT TỐI — 20:00-20:30 (EOD)

| # | Việc | Làm gì | Xong |
|---|------|--------|------|
| 1 | **Đếm** | Tổng bài đã đăng hôm nay? | ☐ |
| 2 | **Check funnel** | Có ai click link Telegram không? | ☐ |
| 3 | **Check account** | Account nào có dấu hiệu lạ? | ☐ |
| 4 | **EOD 5 dòng** | Điền EOD report | ☐ |

---

## EOD 5 Dòng (điền mỗi tối)

```
Ngày: ____/____/________

Shipped (đã đăng):     ___ bài (Founder:__ Risk:__ SMC:__ Macro:__)
Open (đang dang dở):   ___
Leads (click/join):    ___ clicks, ___ joins
Blocker (vấn đề):      ___
Tomorrow (1 việc):     ___
```

---

## Quy tắc vàng

1. **Không spam** — mỗi account tối đa 3-5 bài/ngày, cách 2 tiếng
2. **Không duplicate** — không đăng cùng nội dung 2 account cùng ngày
3. **Check account trước** — nếu account bị checkpoint/locked → dừng, báo Founder
4. **Reply thật** — không bot, không spam, không copy-paste
5. **Ghi nhận đủ** — mỗi ngày phải có EOD, không bỏ

---

## Số khẩn cấp

| Vấn đề | Liên hệ |
|--------|---------|
| Account bị khóa | Báo Founder ngay — dừng đăng |
| Content bị report | Gỡ bài — báo Founder |
| Bot/API lỗi | Check VPS 103.97.126.117:2018 |
| Không có content | Dùng content queue có sẵn — không bịa |
