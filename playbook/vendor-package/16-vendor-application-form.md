# VENDOR APPLICATION — Form + Bot Flow

> **Dùng cho:** Admin tạo form đăng ký vendor + bot xử lý apply tự động
> **Flow:** Người lạ thấy pitch → click link form → điền 5 câu → admin review → PASS/FAIL
> **Date:** 2026-06-15

---

## 1. GOOGLE FORM TEMPLATE — Copy-Paste Để Tạo

Mở [forms.google.com](https://forms.google.com) → tạo form mới → copy từng section bên dưới.

### Tiêu đề & Mô tả

```
Tiêu đề: Hermes Vendor — Đăng Ký Trở Thành Affiliate XAUUSD

Mô tả:
Đăng lại content có sẵn lên X (Twitter) — kiếm 10,000-18,000 VND/người join Telegram.
Không cần vốn. Không cần kinh nghiệm. 30 phút/ngày. Làm tại nhà.

Điền form này (2 phút). Admin review trong 24h. Nếu pass → mời vào group Telegram.
```

### Câu 1 — X Profile

```
Câu hỏi: Link X (Twitter) profile của bạn?
Loại: Short answer
Required: Yes
Validation: URL
Helper text: Ví dụ: https://x.com/yourhandle — Phải để PUBLIC, không khóa.
```

### Câu 2 — Kinh Nghiệm

```
Câu hỏi: Bạn biết gì về XAUUSD / Gold / Prop Firm Trading?
Loại: Multiple choice
Required: Yes
Options:
  - Chưa biết gì — nhưng muốn học
  - Biết một chút (đã xem/tìm hiểu)
  - Có kiến thức cơ bản (đã trade demo)
  - Đã trade thật / đang thi FTMO
  - Chuyên nghiệp (trade full-time)
```

### Câu 3 — Thời Gian

```
Câu hỏi: Mỗi ngày bạn có thể dành 30 phút để đăng bài không?
Loại: Multiple choice
Required: Yes
Options:
  - Có — 30 phút/ngày, đều đặn
  - Có — nhưng không đều (3-5 ngày/tuần)
  - Không chắc — tùy lịch
  - Không — dưới 30 phút/ngày
```

### Câu 4 — Kinh Nghiệm Affiliate / Content

```
Câu hỏi: Bạn đã từng làm affiliate / đăng content lên mạng xã hội chưa?
Loại: Multiple choice
Required: No
Options:
  - Chưa từng — đây là lần đầu
  - Đã từng làm affiliate sàn TMĐT (Shopee, TikTok Shop)
  - Đã từng đăng content lên X / Facebook / TikTok
  - Đã từng làm affiliate tài chính (Accesstrade, ngân hàng)
  - Đã làm nhiều loại affiliate
```

### Câu 5 — Mục Tiêu

```
Câu hỏi: Mục tiêu thu nhập của bạn với việc này?
Loại: Multiple choice
Required: No
Options:
  - Kiếm thêm 1-3 triệu/tháng (part-time)
  - Kiếm 5-10 triệu/tháng (nghiêm túc)
  - Kiếm 15+ triệu/tháng (full-time)
  - Chưa có mục tiêu cụ thể — muốn thử trước
```

### Câu 6 — Liên Hệ

```
Câu hỏi: Telegram @username của bạn (để admin liên hệ nếu pass)?
Loại: Short answer
Required: Yes
Helper text: Ví dụ: @yourtelegram — Đây là cách admin mời bạn vào group nếu pass.
```

### Cài Đặt Form

```
Settings:
  ☑ Thu thập email (để admin liên hệ backup)
  ☑ Giới hạn 1 response/người
  ☐ Không yêu cầu đăng nhập (để dễ apply)
  
  Response destination: Google Sheets (tự động tạo)
  → Tạo sheet tên "Hermes Vendor Applications"
```

---

## 2. SCORING RUBRIC — Admin Chấm

Dùng vendor_qualifier SOUL (`scripts/souls/vendor_qualifier_SOUL.md`) — 5 signals:

| Signal | Score | Cách chấm |
|--------|-------|----------|
| **X profile** | 0-30 | Public + followers ≥100 + bio có XAUUSD/trading = 30. Public nhưng ít followers = 15. Khóa = 0. |
| **Kinh nghiệm trading** | 0-20 | Chuyên nghiệp = 20. Đã trade = 15. Biết chút = 10. Chưa biết = 5 (vẫn nhận — dạy được). |
| **Cam kết thời gian** | 0-25 | 30ph/ngày đều = 25. 3-5 ngày/tuần = 15. Không chắc = 5. Không = 0. |
| **Kinh nghiệm affiliate** | 0-15 | Đã làm affiliate tài chính = 15. Affiliate TMĐT = 12. Content creator = 10. Chưa từng = 5. |
| **Mục tiêu** | 0-10 | 5-10M/tháng = 10 (nghiêm túc). 1-3M = 8 (thực tế). 15M+ = 5 (có thể ảo tưởng). Chưa có = 5. |

**Tổng:**

| Score | Kết quả |
|-------|---------|
| **60-100** | ✅ PASS → Mời vào group, cấp source tag |
| **40-59** | ⚠️ SOFT_PASS → Nhắn "profile cần thêm X, quay lại sau" |
| **0-39** | ❌ FAIL → Lịch sự từ chối: "Chưa phù hợp, hẹn bạn dịp khác" |

---

## 3. RESPONSE TEMPLATE — Admin Gửi Sau Khi Chấm

### PASS (Score ≥60)

```
Chào {name},

Profile của bạn đã được duyệt! Chào mừng đến với Hermes Vendor Program.

Link vào group: {invite_link}

Sau khi vào group:
1. Vào topic "Nguoi moi" — đọc pinned message.
2. Đọc 3 quy tắc vàng.
3. Nhắn "done" để nhận source tag + tracking link.

Mục tiêu 7 ngày: ĐĂNG BÀI ĐẦU TIÊN.

Hẹn gặp trong group!
@hiephoang47
```

### SOFT_PASS (Score 40-59)

```
Chào {name},

Cảm ơn bạn đã ứng tuyển. Profile của bạn gần đạt — chỉ cần thêm:

{follower: cần thêm follower / bio: cần thêm XAUUSD / profile: cần để public}

Bạn có thể:
- Chỉnh sửa profile X theo gợi ý trên
- Apply lại sau 1-2 tuần

Mình sẽ giữ thông tin của bạn. Nhắn lại khi bạn sẵn sàng nhé.

@hiephoang47
```

### FAIL (Score <40)

```
Chào {name},

Cảm ơn bạn đã ứng tuyển vào Hermes Vendor Program.

Sau khi review, mình thấy hiện tại profile của bạn chưa phù hợp với chương trình.

Chương trình yêu cầu:
- X profile public, có nội dung liên quan tài chính/XAUUSD
- Cam kết 30 phút/ngày

Bạn có thể quay lại apply khi đã sẵn sàng. Chúc bạn may mắn!

@hiephoang47
```

---

## 4. BOT FLOW — Tự Động Hóa (P2, Sau Khi Pilot)

Sau khi có 5-10 vendor đầu (manual review ổn), có thể tự động hóa:

```
Người lạ DM "vendor" hoặc "/apply" → Bot tự động:
  1. Gửi link Google Form
  2. Hoặc hỏi 3 câu trực tiếp trong chat:
     Q1: Link X profile?
     Q2: Biết XAUUSD không? (có/không/một chút)
     Q3: 30ph/ngày được không?
  3. Lưu vào vendor-registry.json với status = "applicant"
  4. Báo admin: "Có applicant mới — review tại [Google Sheet link]"
```

**Chưa code — để trong plan P2.** Manual review 10-20 vendor đầu để hiểu pattern trước khi auto.

---

## 5. LINK FORM — Đặt Ở Đâu

```
1. X bio @azzam_gold: "Vendor apply → [link form]"
2. Post X ghim: cuối bài có "Apply: [link form]"
3. Template outreach: cuối mỗi pitch có link form
4. Telegram group description: link form cho người muốn apply
5. Google Sheet response: tự động collect → admin check mỗi sáng
```

---

*Dùng kèm: vendor-icp-bundles.md (pitch) + vendor-outreach-kit.md (template) + vendor-recruit-100.csv (nguồn đăng)*
*Scoring: vendor_qualifier SOUL.md (5-signal rubric)*
*Sau khi pass: flow onboarding hiện có trong 00-new-vendor-onboarding.md*
*Cập nhật: 2026-06-15*
