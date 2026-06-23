# Account Health Monitor — Hermes X Farm

> Cho: Team Tuấn | Cập nhật: hàng ngày
> Mục tiêu: Phát hiện sớm rủi ro — trước khi account bị khóa

---

## Health Dashboard — Điền Hàng Ngày

| Account | Tuổi (ngày) | Bài hôm nay | Bài 7 ngày | Cảnh báo? | Risk |
|---------|------------|-------------|-----------|-----------|------|
| @azzam_gold | | | | | 🟢🟡🔴 |
| @goldrisk_vip | | | | | 🟢🟡🔴 |
| @smc_xauusd | | | | | 🟢🟡🔴 |
| @goldmacro_ | | | | | 🟢🟡🔴 |

---

## Risk Scoring (chấm điểm mỗi ngày)

### Cách tính — cho điểm 0-100

| Yếu tố | Trừ điểm |
|--------|----------|
| Account < 7 ngày tuổi | -20 (warmup phase) |
| Không đăng bài 7 ngày | -40 (DORMANT — nguy cơ cao) |
| Đăng < 3 ngày trong 7 ngày | -20 (low activity) |
| Đăng > 5 bài/ngày trung bình | -10 (spam risk) |
| Có dấu hiệu checkpoint/flag | -30 (CRITICAL) |
| Đăng đều 5+/7 ngày | +5 (healthy) |
| Tần suất 2-4 bài/ngày | +5 (optimal) |

### Mức risk

| Điểm | Mức | Hành động |
|------|-----|-----------|
| 80-100 | 🟢 GREEN | Khỏe — tiếp tục |
| 50-79 | 🟡 YELLOW | Cảnh báo — theo dõi sát |
| 0-49 | 🔴 RED | Nguy cơ — giảm tần suất, báo Founder |

---

## Quy Tắc An Toàn Account

### KHÔNG LÀM (sẽ bị ban)

- Đăng >10 bài/ngày trên 1 account mới
- Follow >50 người/ngày
- Like >100 bài/ngày
- DM hàng loạt
- Dùng cùng IP cho nhiều account
- Post link trong body bài (để link ở bio)
- Spam comment giống nhau
- Dùng ảnh/video có bản quyền

### NÊN LÀM (giữ account khỏe)

- Tăng dần tần suất: tuần 1 (1-2 bài/ngày) → tuần 2 (2-3) → tuần 3+ (3-5)
- Tương tác tự nhiên: like, reply thật, retweet có chọn lọc
- Đổi nội dung thường xuyên — không lặp
- Mỗi account 1 proxy riêng (GenLogin quản lý)
- Check account mỗi sáng trước khi đăng

---

## Warmup Schedule (Account Mới)

| Tuần | Bài/ngày | Follow/ngày | Like/ngày | Loại content |
|------|----------|------------|-----------|-------------|
| 1 | 1-2 | 5-10 | 10-20 | Education, market note |
| 2 | 2-3 | 10-15 | 20-30 | Thêm discipline, macro |
| 3 | 3-4 | 15-20 | 30-40 | Thêm signal tease, proof |
| 4+ | 3-5 | Bình thường | Bình thường | Tất cả format |

---

## Cảnh Báo Khẩn Cấp

Nếu thấy bất kỳ dấu hiệu nào sau → **DỪNG ĐĂNG NGAY → BÁO FOUNDER:**

- [ ] Account bị khóa / suspended
- [ ] Yêu cầu xác minh số điện thoại
- [ ] Checkpoint / captcha bất thường
- [ ] Giảm reach đột ngột (>50%)
- [ ] Bị report / gắn cờ
- [ ] Email/phone bị đổi

---

## Weekly Health Report (Thứ 7)

```
HERMES ACCOUNT HEALTH — Tuần ___

@azzam_gold:    🟢 ____ bài | Risk score: ___
@goldrisk_vip:  🟢 ____ bài | Risk score: ___
@smc_xauusd:    🟢 ____ bài | Risk score: ___
@goldmacro_:    🟢 ____ bài | Risk score: ___

Vấn đề: ___
Hành động: ___
```
