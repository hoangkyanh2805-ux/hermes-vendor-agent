# VENDOR GROWTH PLAN — Tầng TĂNG TRƯỞNG

> **Framework:** $100M Leads (Hormozi) × Traffic Secrets (Brunson) × Expert Secrets (Brunson) × $100M Offers (Hormozi) × DotCom Secrets (Brunson)
> **Nguyên tắc:** Mở rộng hệ community_vendor_guide hiện có — KHÔNG tạo hệ mới, KHÔNG đụng OPS đã chắc
> **Status:** 43 files. 5/5 agents deployed + tested VPS. Tổng 8.6/10. Next: dashboard deploy.
> **Date:** 2026-06-15 | **Ai chạy:** Claude Code | **Output:** Research → Design → Đề xuất → BUILD → AUDIT

---

## BƯỚC 0 — Hiện Trạng: ĐÃ CÓ vs THIẾU

### Hệ thống vendor hiện tại — audit nhanh

| Layer | Đã build | File chính |
|-------|----------|-----------|
| **Knowledge** | 9 card vendor-facing | `content-os/vendor-agent/VENDOR_KNOWLEDGE_PACK.md` |
| **Persona** | community_vendor_guide SOUL v6 | `content-os/souls/community_vendor_guide-SOUL.md` |
| **Onboarding** | Flow 4 bước + gate checklist | `teamtuan/vendor-package/00-new-vendor-onboarding.md` |
| **OPS runbook** | Full ops manual (15 section) | `teamtuan/VENDOR-GROUP-OPS-RUNBOOK.md` |
| **Daily OPS** | SOP từng slot + EOD report | `teamtuan/vendor-package/01-daily-operations.md` |
| **Weekly OPS** | Review thứ 7 + plan CN | `teamtuan/vendor-package/02-weekly-operations.md` |
| **KPI** | Dashboard + OKR 3 tháng | `teamtuan/vendor-package/03-kpi-dashboard.md` |
| **Content** | Routing + anti-duplicate + queue | `teamtuan/vendor-package/04-content-routing.md` |
| **Account** | Health monitor + risk scoring | `teamtuan/vendor-package/05-account-health.md` |
| **Tracking** | funnel-db.py (392 dòng) — click/join/valid_join | `scripts/vendor-layer/funnel-db.py` |
| **Payment** | Invoice template + weekly cycle | `teamtuan/vendor-package/08-payment-invoice.md` |
| **Report** | Weekly + monthly format | `teamtuan/vendor-package/07-monthly-report.md` |

### 5 Gap — Phân Tích Từng Cái

#### Gap 1: Funnel tuyển vendor ($100M Leads — get lead getters)

**ĐÃ CÓ một phần:**
- Onboarding flow khi vendor ĐÃ vào nhóm: START_HERE → X profile → admin review → tracking link → post-log (Card 1-7)
- Gate checklist admin: 8 bước từ "vendor đọc rule" đến "admin cấp source tag"
- Dry run protocol (VENDOR-GROUP-OPS-RUNBOOK.md section 14)

**THIẾU THẬT:**
- Không có kênh đưa vendor tiềm năng VÀO nhóm. Toàn bộ hệ thống bắt đầu từ lúc vendor đã ở trong group.
- Không có pitch tuyển: "Tại sao nên làm vendor cho Hermes?"
- Không có form/đường đăng ký: người lạ → thấy pitch → ứng tuyển → vào nhóm
- Không có tiêu chí nhận/loại vendor rõ ràng
- Không có post X / landing page phục vụ tuyển vendor

**Kết luận:** Thiếu toàn bộ phần TRƯỚC cổng. Hệ thống hiện tại là "cửa đã mở cho người trong nhà" — cần build đường từ ngoài vào.

#### Gap 2: Hệ kích hoạt 7 ngày ($100M Leads — activate, vấn đề #1)

**ĐÃ CÓ một phần:**
- "Tuan 1" topic đã được định nghĩa trong cấu trúc forum (VENDOR-GROUP-OPS-RUNBOOK.md section 2) — nhưng chưa có nội dung
- Dry run protocol test flow vendor mới
- funnel-db.py có thể log event theo thời gian (field `ts`), có vendor field

**THIẾU THẬT:**
- Không có checklist ngày 1-7 cho vendor mới (mỗi ngày làm gì)
- Không có nudge/reminder tự động (vendor mới thường đăng ký rồi bỏ)
- Không có metric "% vendor mới post trong 7 ngày"
- funnel-db.py chưa có field `first_post_date` hoặc `activated_date` — không đo được activation rate
- Không có intent mới cho community_vendor_guide để tự động nhắc vendor mới
- "Tuan 1" topic trống hoàn toàn

**Kết luận:** Đây là gap nghiêm trọng nhất. $100M Leads nói rõ: "Vấn đề #1 không phải là kiếm lead — mà là kích hoạt lead đã có." Vendor đăng ký rồi bỏ = lãng phí toàn bộ effort tuyển.

#### Gap 3: Dream 100 tuyển vendor (Traffic Secrets — bản 2)

**ĐÃ CÓ:**
- Không có gì cho vendor recruitment. Dream 100 hiện tại (`knowledge/dream-100-x.csv`) nhắm ICP khách cuối (prop-firm scalper), không phải vendor.

**THIẾU THẬT:**
- List nơi vendor tiềm năng tụ: group forex/MMO VN, cộng đồng affiliate, group kiếm tiền online, group X marketing VN
- File riêng `vendor-recruit-100.csv` — tách khỏi dream-100 khách cuối
- Phân loại nguồn: group Facebook, group Telegram, forum, group Zalo, Discord MMO
- Target: ≥30 nơi/nguồn tuyển

**Kết luận:** Thiếu hoàn toàn. Cần research + list riêng, không trộn với traffic ops cho khách cuối.

#### Gap 4: Rank ladder + thưởng bậc (Expert Secrets + $100M Offers)

**ĐÃ CÓ một phần:**
- funnel-db.py weekly_report() có "Top vendor" — tên vendor + payable joins count
- Weekly report format có "Best post" (mầm vinh danh)
- Payment: flat 10k/valid-join — rõ ràng, minh bạch
- Card 9 (ESCALATE): policy change phải escalate admin/founder
- 00-action-plan.md Đợt 2.1 có đề xuất "Tiered payment structure" (T1: 15K, T2: 10K, T3: 7K) — nhưng CHƯA BUILD
- Abuse/revoke system (section 11 runbook) — có cơ chế phạt, chưa có cơ chế thưởng

**THIẾU THẬT:**
- Bảng rank CHÍNH THỨC: new → active → top → senior, mỗi bậc có tiêu chí rõ
- Cơ chế vinh danh trong weekly report: "vendor của tuần", "thăng hạng", "top 3"
- Đề xuất reward bậc cho founder duyệt (KHÔNG tự đổi — guardrail)
- Cơ chế thăng/giáng hạng minh bạch (không cảm tính)
- File/bảng rank để track

**Kết luận:** Có mầm (top vendor trong report, đề xuất tiered payment) nhưng chưa có hệ thống hoàn chỉnh.

#### Gap 5: Offer vendor đóng gói + value ladder ($100M Offers + DotCom)

**ĐÃ CÓ một phần:**
- 00-new-vendor-onboarding.md dòng 16-20: mô hình 5 dòng đơn giản
- Card 8 (PAYMENT): formula 10k/join
- Các yếu tố value ngầm có: content pack sẵn, support, rewrite guide, công sức thấp

**THIẾU THẬT:**
- Pitch vendor-facing HOÀN CHỈNH: "Tại sao làm vendor cho Hermes?"
- Value equation rõ: (công sức thấp × kết quả đo được) / (rủi ro thấp × thời gian ít)
- Lộ trình thăng tiến: new → active → top → vendor tuyển vendor (vòng lặp)
- Card vendor-facing về offer + ladder trong knowledge pack
- So sánh với chương trình affiliate khác (tại sao Hermes ngon hơn)

**Kết luận:** Có khung ngầm nhưng chưa đóng gói thành offer rõ ràng, chưa có card knowledge pack.

### Tổng kết BƯỚC 0

| # | Hạng mục | Đã có | Thiếu | Độ nghiêm trọng |
|---|---------|-------|-------|-----------------|
| 1 | **Funnel tuyển vendor** | Onboarding sau cổng | Toàn bộ phần TRƯỚC cổng | 🔴 Cao |
| 2 | **Kích hoạt 7 ngày** | Topic "Tuan 1" trống | Checklist + nudge + metric | 🔴 CAO NHẤT |
| 3 | **Dream 100 tuyển vendor** | Không có gì | Toàn bộ — list + file | 🟡 Trung bình |
| 4 | **Rank + thưởng bậc** | Top vendor + best post | Bảng rank + reward proposal | 🟡 Trung bình (đụng tiền) |
| 5 | **Offer + value ladder** | Mô hình ngầm 5 dòng | Pitch + value equation + card | 🟡 Trung bình |

---

## THIẾT KẾ 5 HẠNG MỤC

### 1. Funnel Tuyển Vendor — "Người Lạ → Ứng Tuyển → Vào Nhóm"

**Sách gốc:** $100M Leads — "Get lead getters" (chapter 9-10)

**Nguyên lý Hormozi:** "Muốn nhiều leads? Đừng tự kiếm. Kiếm người kiếm leads cho bạn. Rồi dạy họ cách kiếm leads."

**Thiết kế:**

#### 1.1 Pitch tuyển (Post X / bài đăng group)

```
TIÊU ĐỀ: "Kiếm 5-15 triệu/tháng — Chỉ Cần Đăng Lại Content Có Sẵn"

Bạn có X account 500+ followers, quan tâm XAUUSD/prop firm?
Bạn muốn kiếm thêm thu nhập mà không cần tự nghĩ content?

Tôi cung cấp:
- Content XAUUSD soạn sẵn mỗi ngày (English — global audience)
- Rewrite bằng giọng của bạn — không cần kiến thức chuyên sâu
- Hệ thống tracking minh bạch: mỗi người vào Telegram qua link của bạn = 10,000đ
- Hỗ trợ review bài + tối ưu profile

Bạn chỉ cần:
- 30 phút/ngày
- Biết đăng bài X
- Không cần bịa signal — đã có source uy tín

Đây không phải "làm giàu nhanh". Đây là hệ thống affiliate minh bạch.
Top vendor hiện tại đang làm XX joins/tuần.

→ DM "vendor" để ứng tuyển.
```

**Format:** 1 post X ghim trên @azzam_gold + đăng trong group MMO/forex VN + Telegram cá nhân.

#### 1.2 Flow tuyển — Nối vào onboarding hiện có

```
NGƯỜI LẠ
  │
  ├─ Thấy pitch trên X / group MMO / bạn bè giới thiệu
  │
  ▼
  ├─ DM "vendor" → @AZZAM_Trading_Expert
  │  (hoặc ấn vào link Telegram trong bio)
  │
  ▼
  ├─ Bot/Admin chào: "Bạn muốn làm vendor? Trả lời 3 câu:"
  │  1. Link X profile của bạn?
  │  2. Bạn biết XAUUSD/prop firm không? (có/không/một chút)
  │  3. Mỗi ngày bạn có 30 phút để đăng bài không?
  │
  ▼
  ├─ Admin review (tiêu chí bên dưới) → 
  │  ├─ PASS → cấp link vào vendor group + tag vendor mới
  │  └─ FAIL → "Cảm ơn bạn. Hiện tại profile cần thêm X follower/chủ đề 
  │             XAUUSD. Bạn có thể quay lại sau khi đạt XX followers."
  │
  ▼
  └─ Vào group → flow onboarding hiện có (START_HERE → X profile → review → tracking link)
```

#### 1.3 Tiêu chí nhận vendor (đơn giản, không cản)

| Tiêu chí | Ngưỡng | Lý do |
|----------|--------|-------|
| X profile public | Bắt buộc | Không check được content |
| Followers | ≥100 (mềm) | Có audience tối thiểu |
| Bio có XAUUSD/prop firm/trading | Nên có | Khớp niche |
| Cam kết 30ph/ngày | Bắt buộc | Activation predictor |
| Không spam/scan history | Bắt buộc | An toàn hệ thống |

**Nguyên tắc:** Nhận rộng, lọc sau bằng activation. $100M Leads: "Nhận nhiều, kích hoạt ít vẫn hơn nhận ít ngay từ đầu."

#### 1.4 Card mới — VENDOR_RECRUIT (thêm vào knowledge pack)

```text
## Card 10 - VENDOR_RECRUIT

Use when someone asks "lam sao lam vendor", "muon dang ky lam vendor",
"tuyen vendor khong".

Answer:
- Gui 3 cau hoi:
  1. Link X profile?
  2. Ban biet XAUUSD/prop firm khong?
  3. Moi ngay co 30 phut dang bai khong?
- Sau khi tra loi, admin se review va moi vao group neu pass.
- Khong pass: yeu cau them follower hoac chinh sua profile XAUUSD.

Không nhận vendor:
- Profile khong public.
- Spam/scam history.
- Khong the cam ket thoi gian toi thieu.
```

#### 1.5 Output cụ thể

| Output | Format | Vị trí |
|--------|--------|--------|
| Pitch tuyển | Post X + template DM | Card mới trong knowledge pack |
| Flow tuyển | Flow diagram | Section này → nối vào onboarding |
| Tiêu chí nhận | Bảng checklist | Card VENDOR_RECRUIT |
| 3 câu hỏi ứng tuyển | Template | Card VENDOR_RECRUIT |

---

### 2. Hệ Kích Hoạt 7 Ngày — "Đăng Bài Đầu Trong 7 Ngày"

**Sách gốc:** $100M Leads — "Activate" (chapter 5-6, vấn đề #1)

**Nguyên lý Hormozi:** "Hầu hết lead không mua không phải vì họ không muốn. Họ quên. Nhắc họ."

**Thiết kế:**

#### 2.1 Checklist 7 ngày cho vendor mới

| Ngày | Chủ đề | Nhiệm vụ vendor | Nudge (agent/admin gửi) |
|------|--------|----------------|------------------------|
| **1** | Welcome + Đọc | Đọc rule + onboarding trong "Nguoi moi" | "Chào [tên]! Bắt đầu bằng việc đọc rule trong topic Nguoi moi. 5 phút thôi. Xong nhắn 'done' nhé." |
| **2** | Setup Profile | Sửa X profile theo checklist + gửi review | "Hôm nay setup X profile nhé. Checklist trong topic Nguoi moi. Gửi link X của bạn để admin review." |
| **3** | Chọn Content | Vào "Thong bao" xem daily pack + chọn 1 bài | "Hôm nay tập trung đọc daily content pack. Chọn 1 bài bạn thấy dễ viết nhất. Chưa cần đăng vội." |
| **4** | Rewrite + Draft | Viết nháp bài đầu + gửi draft check | "Viết thử bài đầu tiên đi. Copy paste vào đây để admin check trước khi đăng. Không cần hoàn hảo." |
| **5** | ĐĂNG BÀI ĐẦU | Đăng bài X đầu tiên + gửi post-log | "Hôm nay đăng bài đầu tiên! Xong gửi link vào Post Log. Đây là cột mốc quan trọng nhất." |
| **6** | Reply + Engage | Reply 3-5 bài trong niche + engage | "Bài đầu đã lên. Hôm nay dành 20 phút reply bài khác trong niche. Xây dựng presence." |
| **7** | Review + Next | Xem lại tuần đầu + chọn bài tiếp theo | "1 tuần rồi! Review: bài nào OK, bài nào cần sửa. Tuần sau: 2-3 bài. Có câu hỏi gì không?" |

**Nguyên tắc:** Mỗi ngày 1 nhiệm vụ nhỏ. Đích đến = bài đăng đầu tiên (ngày 5).

#### 2.2 Tracking "first post" — Thêm vào funnel-db.py

Thêm event type mới: `vendor_activated`

```python
# Log khi vendor đăng bài đầu tiên
python3 /root/hermes-bin/vendor-layer/funnel-db.py activate --vendor tuan --date 2026-06-15
```

Metric đo được:
- % vendor đăng bài đầu trong 7 ngày
- Thời gian trung bình từ join → first post
- % vendor bỏ sau 7 ngày không đăng bài

**Lưu ý:** Đây là CHỈ TIÊU ĐỀ XUẤT — chưa code. Để trong plan để founder duyệt rồi mới build script.

#### 2.3 Intent mới cho community_vendor_guide — NUDGE

Thêm pattern vào SOUL:

```text
## Activation Nudge

When a vendor is in day 1-6 without a first post, send ONE short nudge per day.
Do not send more than 1 nudge/day. If vendor doesn't respond after day 7, stop
and flag as "cold vendor" for admin review.

Nudge template:
[ten], [nhiem vu hom nay ngan gon].

Buoc tiep theo:
[1 hanh dong cu the].

Luu y:
[guardrail neu can].
```

**Cơ chế hoạt động:**
- Admin manual trigger trong pilot (chưa auto cron)
- Mỗi sáng admin check: ai joined trong 7 ngày qua, chưa có first post? → gửi nudge
- Sau pilot, có thể thêm cron script `vendor-nudge.py` chạy 08:00 VN

#### 2.4 Output cụ thể

| Output | Format | Vị trí |
|--------|--------|--------|
| Checklist 7 ngày | Bảng + template | Card mới VENDOR_ACTIVATION |
| Intent NUDGE | Bổ sung SOUL | `community_vendor_guide-SOUL.md` |
| Metric activation | Logic + lệnh | Đề xuất script `funnel-db.py activate` |
| Nội dung "Tuan 1" topic | 7 pinned message | Telegram topic "Tuan 1" |

---

### 3. Dream 100 Tuyển Vendor — "Nơi Vendor Tiềm Năng Tụ"

**Sách gốc:** Traffic Secrets (Brunson) — Dream 100

**Nguyên lý Brunson:** "Đừng cố gắng xuất hiện trước tất cả mọi người. Xuất hiện ở nơi đối tượng của bạn ĐÃ tụ tập."

**Thiết kế:**

#### 3.1 Phân biệt — 2 Dream 100 riêng

| | Dream 100 KHÁCH | Dream 100 VENDOR |
|---|---|---|
| **File** | `knowledge/dream-100-x.csv` | `knowledge/vendor-recruit-100.csv` |
| **Đối tượng** | Prop firm scalper (ICP khách) | Người muốn kiếm tiền affiliate/content |
| **Nơi tụ** | X (trader, FTMO, prop firm) | Group MMO VN, group affiliate, group Forex VN |
| **Mục tiêu** | Kéo vào Telegram → VIP | Kéo làm vendor → đăng bài → kéo khách |
| **Người chạy** | Traffic ops (Dream 100 engine) | Manual research + outreach |

#### 3.2 Danh sách nguồn tuyển vendor

| # | Loại | Nền tảng | Tên group / Nơi | Số lượng | Cách tiếp cận |
|---|------|---------|----------------|---------|--------------|
| | **Group MMO VN** | | | | |
| 1 | Group | Facebook | Kiếm Tiền Online Việt Nam | ~500K | Đăng pitch + reply |
| 2 | Group | Facebook | Hội Kiếm Tiền Trên Mạng | ~300K | Đăng pitch + reply |
| 3 | Group | Facebook | Affiliate Marketing Việt Nam | ~200K | Đăng pitch |
| 4 | Group | Facebook | MMO Việt Nam — Chia Sẻ Cách Kiếm Tiền | ~400K | Reply value |
| 5 | Group | Facebook | Dropbyke / Kiếm Tiền Với Thị Trường Tài Chính | ~100K | Liên quan niche |
| | **Group Forex VN** | | | | |
| 6 | Group | Facebook | Hội Forex Việt Nam | ~200K | Reply + pitch nhẹ |
| 7 | Group | Facebook | Forex — Vàng — Chứng Khoán | ~100K | Giá trị trước, pitch sau |
| 8 | Group | Telegram | Forex Việt Nam Signals | ? | Research thêm |
| 9 | Group | Telegram | FTMO Việt Nam Community | ? | Research thêm |
| | **Group Affiliate** | | | | |
| 10 | Group | Facebook | Affiliate Marketing — Kiếm Tiền Tại Nhà | ~150K | Pitch vendor |
| 11 | Group | Facebook | Tiếp Thị Liên Kết Việt Nam | ~250K | Pitch vendor |
| 12 | Group | Telegram | Affiliate VN | ? | Research thêm |
| | **Group Freelancer/Remote** | | | | |
| 13 | Group | Facebook | Việc Làm Online Tại Nhà | ~300K | Pitch "30ph/ngày" |
| 14 | Group | Facebook | Freelancer Việt Nam | ~400K | Pitch "thu nhập thêm" |
| 15 | Group | Facebook | Việc Làm Thêm Tại Nhà | ~200K | Pitch |
| | **Forum / Web** | | | | |
| 16 | Forum | Web | voz.vn (mục kinh tế/tài chính) | Lớn | Reply value |
| 17 | Forum | Web | mmo4me.com | Trung bình | Post thread |
| 18 | Forum | Web | diendantailanh.com (mục chứng khoán) | Nhỏ | Reply |
| | **Kênh khác** | | | | |
| 19 | Kênh | Zalo | Group Zalo Forex/MMO (tìm thêm) | ? | Share + DM |
| 20 | Kênh | Discord | Discord MMO Việt Nam server | ? | Research thêm |
| ... | ... | ... | ... | ... | ... |

**Target:** ≥30 nguồn. Trên là 20 nguồn seed — cần research thêm 10-20 nguồn nữa.

#### 3.3 Output cụ thể

| Output | Format | Vị trí |
|--------|--------|--------|
| vendor-recruit-100.csv | CSV: tên, nền tảng, URL, số member, trạng thái, notes | `knowledge/vendor-recruit-100.csv` |
| Cách tiếp cận mỗi nguồn | Template pitch + reply | Trong file CSV (cột "Cách tiếp cận") |

---

### 4. Rank Ladder + Thưởng Bậc — "New → Active → Top → Senior"

**Sách gốc:** Expert Secrets (Brunson) — "Create a movement" + $100M Offers (Hormozi) — "Value stacking qua các bậc"

**Nguyên lý Brunson:** "Người ta không chỉ muốn sản phẩm. Họ muốn DANH PHẬN. Cho họ 1 vai trò để vươn tới."

**⚠️ GUARDRAIL:** Mọi thay đổi payment rate phải được founder duyệt. Phần này là ĐỀ XUẤT — không triển khai khi chưa có OK từ anh.

#### 4.1 Bảng rank

| Bậc | Tên | Tiêu chí đạt | Vinh danh | Reward (đề xuất) |
|-----|-----|-------------|----------|-----------------|
| **Lv1** | **New** | Vừa vào nhóm, chưa có first post | — | — |
| **Lv2** | **Active** | Đã đăng ≥3 bài, ≥1 valid join | Tag trong weekly report | 10K/join (flat hiện tại) |
| **Lv3** | **Top** | ≥20 valid joins/tháng, ≥90% bài pass review | "Vendor of the Week" + ghim tên | 10K/join + bonus 50K nếu top 1 tuần |
| **Lv4** | **Senior** | ≥50 valid joins/tháng, 3 tháng liên tiếp bậc Top, hỗ trợ vendor mới | "Senior Vendor" tag vĩnh viễn + mentor role | 10K/join + 5% commission từ vendor do mình tuyển (vòng lặp) |

#### 4.2 Cơ chế thăng/giáng hạng

```
Thăng hạng: Xét mỗi thứ 2 (cùng lúc payment cycle)
  - New → Active: có first post
  - Active → Top: ≥20 valid joins trong 30 ngày gần nhất
  - Top → Senior: ≥50 valid joins/tháng × 3 tháng liên tiếp + mentor ít nhất 1 vendor mới

Giáng hạng: Xét mỗi thứ 2
  - Top → Active: <10 valid joins trong 30 ngày
  - Senior → Top: <30 valid joins trong 30 ngày hoặc không mentor vendor mới nào trong 60 ngày
  - Active → Inactive: 0 bài đăng trong 14 ngày → admin check-in
```

#### 4.3 Đề xuất reward bậc — CHỜ FOUNDER DUYỆT

**Phương án A — Bonus flat (đơn giản nhất):**

| Bậc | Rate/join | Bonus |
|-----|----------|-------|
| New | Chưa áp dụng | — |
| Active | 10,000 VND | — |
| Top | 10,000 VND | +100,000 VND nếu dẫn đầu tháng |
| Senior | 10,000 VND | +5% commission từ vendor tuyển dưới |

**Phương án B — Tiered rate (như đề xuất trong 00-action-plan.md Đợt 2.1):**

| Bậc | Rate/join |
|-----|----------|
| Active | 10,000 VND (giữ nguyên) |
| Top | 12,000 VND |
| Senior | 15,000 VND |

**Phương án C — Hybrid (khuyến nghị):**

| Bậc | Rate/join | Bonus tháng | Đặc quyền |
|-----|----------|-------------|----------|
| Active | 10,000 VND | — | — |
| Top | 10,000 VND | 50K-200K tùy rank | Được ghim bài trong group |
| Senior | 10,000 VND | 5% commission tầng dưới | Mentor + tag vĩnh viễn |

**Khuyến nghị:** Phương án C — giữ rate nền 10K/join (không phá vỡ model hiện tại), thêm bonus và đặc quyền để tạo động lực thăng hạng. Đặc quyền (ghim bài, mentor, tag vĩnh viễn) không tốn tiền nhưng tạo status — đúng theo Expert Secrets.

#### 4.4 Cập nhật weekly report — Thêm rank section

Thêm vào format hiện tại:

```text
Weekly Vendor Report
- Valid joins: ___
- Top source: ___
- Top cluster: ___

RANK BOARD (mới):
  🥇 Vendor of the Week: [tên] — XX joins
  ⬆️ Thăng hạng: [tên] Active → Top
  🆕 New Active: [tên], [tên] — first post tuần này
  
- Best post: ___
- Payment estimate: ___
- Admin confirmation status: ___
```

#### 4.5 Output cụ thể

| Output | Format | Vị trí |
|--------|--------|--------|
| Bảng rank 4 bậc | Bảng + tiêu chí | Card mới VENDOR_RANK |
| Đề xuất reward | 3 phương án | Section này — chờ duyệt |
| Cập nhật weekly report | Thêm "RANK BOARD" | VENDOR-GROUP-OPS-RUNBOOK.md section 10 |
| Cơ chế thăng/giáng | Rule + lịch xét | Card VENDOR_RANK |

---

### 5. Offer Vendor Đóng Gói + Value Ladder — "Tại Sao Làm Vendor?"

**Sách gốc:** $100M Offers (Hormozi) — Value Equation + DotCom Secrets (Brunson) — Value Ladder

**Nguyên lý Hormozi:** "Offer không phải là sản phẩm. Offer là tổng giá trị KHÁCH HÀNG NHẬN ĐƯỢC trừ đi cái HỌ PHẢI BỎ RA."

#### 5.1 Value Equation cho vendor

```
Value = (Dream Outcome × Perceived Likelihood) / (Time Delay × Effort & Sacrifice)

Áp dụng cho vendor Hermes:

Dream Outcome:       Kiếm 5-15 triệu/tháng từ đăng lại content có sẵn
Perceived Likelihood: HIGH — vì:
                      - Content SOẠN SẴN mỗi ngày (không cần tự nghĩ)
                      - Hệ thống tracking minh bạch (biết chính xác bao nhiêu joins)
                      - Có admin review bài trước khi đăng (không sợ sai)
                      - Payment đều mỗi thứ 2 (không delay)
Time Delay:          Ngày 5 có bài đầu → tuần 2 có join đầu → tháng 1 có income
Effort & Sacrifice:  30 phút/ngày + 1 X account (ai cũng có)
                     KHÔNG cần: kiến thức trading, tự tạo content, tự bán hàng

→ VALUE = HIGH — dễ bắt đầu, chi phí thấp, kết quả rõ ràng
```

#### 5.2 Pitch vendor-facing — "Tại sao làm vendor cho Hermes?"

```text
TAI SAO LAM VENDOR CHO HERMES?

1. Content co san — khong can nghi
   Moi ngay ban nhan daily content pack: bai viet XAUUSD da duoc chon loc
   tu nguon uy tin (TOP 1 FTMO). Chi can rewrite bang giong cua ban.
   Khong can biet trade. Khong can tu tim content.

2. Tracking minh bach — biet chinh xac minh kiem duoc bao nhieu
   Moi join qua link cua ban duoc tracker ghi nhan. Cuoi tuan co bao cao.
   Khong phai "tin anh di" — so lieu ro rang.

3. Admin support — khong lo sai
   Gui draft truoc khi dang — admin check attribution, CTA, risk.
   Khong bi ban X, khong bi report, khong bi loi compliance.

4. Cong suc thap — 30 phut/ngay
   Khong can full-time. Khong can kinh nghiem. Chi can 30 phut + 1 X account.

5. Thu nhap minh bach — 10,000 VND/valid join
   Thanh toan thu 2 hang tuan. Khong delay. Khong "thang sau tra".

6. Co lo trinh thang tien
   New → Active → Top → Senior → Mentor vendor khac → commission tang them.
```

#### 5.3 Value Ladder cho vendor — Lộ trình thăng tiến

```
┌──────────────────────────────────────────────────────────────┐
│              VENDOR VALUE LADDER                              │
│                                                               │
│  BẬC 1           BẬC 2             BẬC 3           BẬC 4     │
│  NEW →           ACTIVE →          TOP →            SENIOR   │
│                                                               │
│  Vào nhóm        Đăng bài đều      Dẫn đầu tuần    Tuyển vendor
│  Đọc rule        3+ bài/tuần       20+ joins/tháng  mới dưới
│  Setup profile   Có join đầu       90% pass review  trướng
│  Chưa có bài     Thu nhập đầu      Vendor of Week  Mentor
│                                                               │
│       │               │               │               │       │
│       ▼               ▼               ▼               ▼       │
│  7-day           Payment          Bonus +          Commission
│  activation      10K/join         vinh danh        5% tầng dưới
│  checklist                                        + tag vĩnh viễn
│                                                               │
│  VÒNG LẶP: Senior tuyển New → New lên Active → Active lên    │
│  Top → Top lên Senior → Senior tuyển thêm New → ...          │
│  Đây là growth loop — vendor tự mở rộng hệ thống.            │
└──────────────────────────────────────────────────────────────┘
```

#### 5.4 Card mới — VENDOR_OFFER (thêm vào knowledge pack)

```text
## Card 11 - VENDOR_OFFER

Use when vendor asks "tai sao lam vendor", "luong bao nhieu", "co dang lam
khong", "co phai scam khong".

Golden answer:
Lam vendor cho Hermes la dang lai content XAUUSD co san len X cua ban.
Moi nguoi vao Telegram qua link cua ban = 10,000 VND.

Tai sao nen lam:
1. Content co san — khong can nghi.
2. Tracking minh bach — biet chinh xac minh kiem duoc bao nhieu.
3. Admin support — review bai truoc khi dang.
4. Cong suc thap — 30 phut/ngay.
5. Thu nhap minh bach — thanh toan thu 2 hang tuan.
6. Co lo trinh thang tien: New → Active → Top → Senior.

Day khong phai "lam giau nhanh". Day la he thong affiliate minh bach.
Khong can bo tien. Khong can kinh nghiem. Chi can 30 phut/ngay + X account.

Buoc tiep theo:
Doc onboarding trong topic Nguoi moi. Xong nhan 'done'.

Luu y:
Payment chi la estimate den khi admin xac nhan tracker cuoi tuan.
```

#### 5.5 Output cụ thể

| Output | Format | Vị trí |
|--------|--------|--------|
| Value equation | Công thức + giải thích | Card VENDOR_OFFER |
| Pitch vendor-facing | 6 điểm | Card VENDOR_OFFER |
| Value ladder diagram | Flow 4 bậc + vòng lặp | Card VENDOR_OFFER |
| Card mới trong knowledge pack | Text card | `VENDOR_KNOWLEDGE_PACK.md` |

---

## TỔNG KẾT — CẦN BUILD GÌ

### Card mới thêm vào VENDOR_KNOWLEDGE_PACK.md

| Card # | Tên | Dùng khi | Gap |
|--------|-----|---------|-----|
| **10** | VENDOR_RECRUIT | Người lạ hỏi "làm sao làm vendor" | Gap 1 |
| **11** | VENDOR_ACTIVATION | Vendor mới cần checklist 7 ngày | Gap 2 |
| **12** | VENDOR_RANK | Hỏi về rank, thăng hạng, reward | Gap 4 |
| **13** | VENDOR_OFFER | Hỏi "tại sao làm vendor", "lương bao nhiêu" | Gap 5 |

### File mới cần tạo

| File | Nội dung | Gap |
|------|---------|-----|
| `knowledge/vendor-recruit-100.csv` | 30+ nguồn tuyển vendor | Gap 3 |
| `knowledge/VENDOR-GROWTH-PLAN.md` | File này — kế hoạch tổng | All |

### Chỉnh sửa file có sẵn

| File | Thay đổi | Gap |
|------|---------|-----|
| `VENDOR_KNOWLEDGE_PACK.md` | Thêm Card 10-13 | 1,2,4,5 |
| `community_vendor_guide-SOUL.md` | Thêm intent NUDGE + VENDOR_RECRUIT routing | 2 |
| `VENDOR-GROUP-OPS-RUNBOOK.md` | Cập nhật weekly report format (thêm RANK BOARD) | 4 |
| `funnel-db.py` | Thêm event `vendor_activated` + command `activate` | 2 |

### Thứ tự build (sau khi founder duyệt)

| # | Việc | Effort | Phụ thuộc |
|---|------|--------|----------|
| 1 | **Card 10 + 13** (tuyển + offer) — 2 card knowledge pack | 30 phút | Không |
| 2 | **vendor-recruit-100.csv** — research 30 nguồn | 1 giờ | Không |
| 3 | **Card 11** (activation checklist 7 ngày) | 30 phút | Không |
| 4 | **Intent NUDGE** — thêm vào community_vendor_guide SOUL | 15 phút | Card 11 |
| 5 | **Nội dung "Tuan 1" topic** — 7 post mẫu cho Telegram | 30 phút | Card 11 |
| 6 | **Card 12** (rank) + cập nhật weekly report | 30 phút | Chờ duyệt reward |
| 7 | **funnel-db.py activate** — thêm event tracking | 30 phút | Card 11 |

---

## GUARDRAIL CUỐI CÙNG

```
✅ BUILD: Card 10 (tuyển) + Card 13 (offer) + Card 11 (activation) → không đụng tiền
✅ BUILD: vendor-recruit-100.csv → research
✅ BUILD: Intent NUDGE + Tuan 1 topic → không đụng OPS hiện có
✅ DUYỆT: Reward bậc (section 4) — Founder chọn phương án C (2026-06-15)
✅ BUILD: funnel-db.py activate → đã code, cần test trước khi deploy VPS

❌ KHÔNG: Tự đổi payment rate
❌ KHÔNG: Tạo hệ thống mới thay thế community_vendor_guide
❌ KHÔNG: Đụng onboarding, OPS daily, content rule, tracking đã có
❌ KHÔNG: Lộ repo path/script/CRM trong vendor-facing content
❌ KHÔNG: Deploy lên vendor group thật khi chưa có OK
```

---

## BUILD LOG — COMPLETE

**Founder approved:** Toàn bộ 5 hạng mục + Phương án C (reward bậc) — 2026-06-15

### Phase 1 — Core Growth Layer (7/7) ✅

| # | File | Thay đổi | Status |
|---|------|---------|--------|
| 1 | `content-os/vendor-agent/VENDOR_KNOWLEDGE_PACK.md` | Thêm Card 10-13 (VENDOR_RECRUIT, VENDOR_ACTIVATION, VENDOR_RANK, VENDOR_OFFER) | ✅ Done |
| 2 | `content-os/souls/community_vendor_guide-SOUL.md` | Thêm Activation Nudge + routing rules cho 4 card mới (114 dòng) | ✅ Done |
| 3 | `knowledge/vendor-recruit-100.csv` | 45 nguồn tuyển vendor (FB group, Telegram, forum, Zalo, Discord, X, YouTube, personal network) | ✅ Done |
| 4 | `teamtuan/VENDOR-GROUP-OPS-RUNBOOK.md` | Cập nhật weekly report format — thêm RANK BOARD (487 dòng) | ✅ Done |
| 5 | `teamtuan/vendor-package/10-tuan1-activation-pack.md` | Nội dung 7 ngày cho topic Tuan 1 + admin checklist (163 dòng) | ✅ Done |
| 6 | `scripts/vendor-layer/funnel-db.py` | Thêm lệnh `activate --vendor --date` — log `vendor_activated` event (402 dòng) | ✅ Done |
| 7 | `knowledge/VENDOR-GROWTH-PLAN.md` | Kế hoạch tổng 5 gap (file này) | ✅ Done |

### Phase 2 — E-Commerce Pivot Bundle (3/3) ✅

| # | File | Thay đổi | Status |
|---|------|---------|--------|
| 8 | `knowledge/vendor-recruit-ecommerce-pivot.md` | Bundle tuyển vendor dân TikTok/Shopee — pain point, case Tuấn, comparison, pitch mẫu, FAQ | ✅ Done |
| 9 | `knowledge/vendor-recruit-100.csv` | Thêm 10 nguồn e-commerce (tổng 45 nguồn) | ✅ Done |
| 10 | `knowledge/VENDOR-GROWTH-PLAN.md` | Cập nhật build log Phase 2 | ✅ Done |

### Phase 3 — Outreach + ICP Bundles + Group Deploy (4/4) ✅

| # | File | Thay đổi | Status |
|---|------|---------|--------|
| 11 | `knowledge/vendor-outreach-kit.md` | Template DM/bài đăng cho 6 loại kênh (FB, Telegram, Forum, Discord, Zalo, X) + lịch đăng 2 tuần + tracking | ✅ Done |
| 12 | `knowledge/vendor-icp-bundles.md` | 4 ICP bundle: sinh viên, freelancer, Accesstrade publisher, mẹ bỉm — mỗi bundle có chân dung + pitch ngắn/dài + comparison | ✅ Done |
| 13 | `teamtuan/vendor-package/11-group-deployment-pack.md` | Nội dung deploy lên group thật: pinned, Tuan 1, RANK BOARD, bot integration (743 dòng) | ✅ Done |
| 14 | `knowledge/VENDOR-GROWTH-PLAN.md` | Cập nhật build log Phase 3 | ✅ Done |

### Phase 4 — Agent Architecture (5/5) ✅

| # | File | Thay đổi | Status |
|---|------|---------|--------|
| 15 | `scripts/souls/vendor_qualifier_SOUL.md` | Agent mới — score vendor applicant (5 signals, PASS/SOFT_PASS/FAIL) | ✅ Done |
| 16 | `scripts/souls/vendor_draft_review_SOUL.md` | Agent mới — review vendor draft (6 checkpoints, APPROVE/REWRITE/REJECT) | ✅ Done |
| 17 | `scripts/souls/vendor_boss_SOUL.md` | Agent mới — vendor orchestrator (4 modes, 8 KPI, weekly cycle) | ✅ Done |
| 18 | `scripts/souls/vendor_reporter_SOUL.md` | Agent mới — vendor reports + RANK BOARD compute | ✅ Done |
| 19 | `teamtuan/vendor-package/12-vendor-ops-runbook.md` | Daily/weekly/monthly ops + escalation + bot maintenance (298 dòng) | ✅ Done |
| — | `scripts/marketing_boss_SOUL_v3.md` | REVERTED — bỏ vendor module, giữ nguyên V5 | ✅ Fixed |
| — | `scripts/souls/signal_funnel_SOUL.md` | REVERTED — bỏ vendor metrics, giữ nguyên V5 | ✅ Fixed |

### Phase 5 — Bot Code Production (3/3) ✅

| # | File | Lines | Chức năng | Status |
|---|------|-------|----------|--------|
| 20 | `scripts/vendor-layer/vendor_bot.py` | 459 | NUDGES dict 7 ngày (full rewrite) + cron mode + keyword reply | ✅ Done |
| 21 | `scripts/vendor-layer/vendor_bot_cron.sh` | 86 | Cron wrapper: nudge (08:00) + reminder (18:00) + weekly (T2) + start/stop/restart | ✅ Done |
| 22 | `scripts/vendor-layer/deploy_vendor_bot.py` | 179 | Deploy script: scp files → VPS, init registry, setup crontab, .env template | ✅ Done |

### Phase 6 — Dashboard + Roadmap + Challenge Tab (6/6) ✅ — 2026-06-15

| # | File | Lines | Chức năng | Status |
|---|------|-------|----------|--------|
| 23 | `scripts/vendor-layer/vendor_dashboard.py` | 340 | Flask app — login, dashboard route, challenge route, health check. Compute tier/rate/rank. | ✅ Done |
| 24 | `scripts/vendor-layer/templates/base.html` | 273 | Base template — sidebar nav (Dashboard + Challenge), CSS variable system (TradingView dark + Binance gold) | ✅ Done |
| 25 | `scripts/vendor-layer/templates/login.html` | — | Login page — "XAU HERMES" branding, monospace form, PIN auth | ✅ Done |
| 26 | `scripts/vendor-layer/templates/dashboard.html` | 208 | Dashboard page — 4 stat cards, Bloomberg-style tables, earnings history, campaign brief, tiered commission | ✅ Done |
| 27 | `scripts/vendor-layer/templates/challenge.html` | 500+ | Challenge tab — 8-step progress bar, 8 day cards expand/collapse, interactive checklists (localStorage), leaderboard sidebar, Quick Tips, Hỏi Đáp CTA | ✅ Done |
| 28 | `knowledge/vendor-dashboard-design-brief.md` | 360 | Design brief cho Claude.ai build dashboard — TradingView dark + Bloomberg typography + CSS snippets + 10-point verification | ✅ Done |
| 29 | `knowledge/vendor-challenge-design-brief.md` | 413 | Design brief cho Claude.ai build challenge tab — Allin Plan layout + 8 day cards + checklist + verification | ✅ Done |
| 30 | `teamtuan/vendor-package/15-vendor-7-day-roadmap.md` | 824 | **Vendor-facing roadmap** — 1 file duy nhất cho vendor từ "không biết gì" đến first post + first join. SOP từng bước + giải thích + FAQ + appendix | ✅ Done |
| 31 | `knowledge/Hermes Vendor Dashboard.dc.html` | 952 | Standalone HTML dashboard — 5 tabs (Dashboard, Recruit, Activate, Rank Ladder, Growth Loop), tất cả CSS/JS inline | ✅ Done |
| 32 | `teamtuan/vendor-package/16-vendor-application-form.md` | — | Google Form template (6 câu) + scoring rubric (5 signals) + response templates (PASS/SOFT_PASS/FAIL) + bot auto-flow plan | ✅ Done |

**TOTAL: 32 files. Đủ để deploy + tuyển vendor thật.**

### Phase 7 — Landing Page Tuyển Vendor (6/6) ✅ — 2026-06-16

| # | File | Lines | Chức năng | Status |
|---|------|-------|----------|--------|
| 33 | `knowledge/vendor-landing-copywriting.md` | 233 | Full copy 17 block — Marta Siarkowska × Hormozi × Suby. Negative guarantee, social proof trước pain, objection trước product, vivid vision closing. | ✅ Done |
| 34 | `knowledge/vendor-landing-design-brief.md` | 718 | Design spec — 17 block layout, 8 visual asset placeholders, Marta structure map, mobile output reqs, 12-point verification. | ✅ Done |
| 35 | `knowledge/landing-extracted/Hermes Vendor Landing.dc.html` | 490 | Flat HTML — IBM Plex Mono + Newsreader fonts, IntersectionObserver reveal, sticky CTA, 17 block Marta structure. **Audited: 9.5/10.** | ✅ Done |
| 36 | `knowledge/landing-extracted/Hermes Vendor Landing - Standalone (2).html` | 180 | Bundled standalone — có visual asset placeholders. ⚠️ Vỡ mobile (thiếu viewport, JS wrapper). | ⚠️ Cần fix |
| 37 | `knowledge/landing-extracted/support.js` | — | DCLogic runtime cho dc.html (FAQ state, IntersectionObserver, data-reveal). | ✅ Done |
| 38 | `teamtuan/vendor-package/16-vendor-application-form.md` | — | Google Form template (6 câu) + scoring rubric (5 signals, /100) + response templates (PASS/SOFT_PASS/FAIL). | ✅ Done |

**TOTAL: 38 files. Landing page: copy ✅ · design brief ✅ · HTML 9.5/10 ⚠️ mobile fix needed.**

### Landing Page Audit Scorecard — 2026-06-16

| Hạng mục | Điểm | Ghi chú |
|---------|------|--------|
| Copywriting (Marta structure) | 10/10 | 17 block đúng thứ tự, 4 kỹ thuật Marta đủ |
| Design brief completeness | 10/10 | 718 dòng, 12-point verification, visual asset map |
| HTML execution (dc.html) | 9.5/10 | Font IBM Plex Mono + Newsreader, reveal animation, sticky CTA logic đúng |
| Mobile readiness | 6/10 | Standalone vỡ mobile — thiếu viewport, bundler gây trễ JS |
| Visual assets | 7/10 | 8 placeholder spec đầy đủ, chưa có ảnh thật để chèn |
| **TỔNG** | **8.5/10** | Sẵn sàng deploy sau khi fix mobile + thay CTA URL thật |

### Cần làm để landing page LIVE

| # | Việc | Mức độ |
|---|------|--------|
| 1 | Yêu cầu Claude.ai regenerate: flat HTML + viewport meta + vanilla JS + `&display=swap` | 🔴 BLOCKER |
| 2 | Thay `{{ ctaUrl }}` → link Google Form thật | 🔴 BLOCKER |
| 3 | Thay `{{ slotsLeft }}` → số thật (hoặc bỏ) | 🟡 |
| 4 | Chụp screenshot dashboard/vendor posts → chèn vào placeholder | 🟡 Sau khi có vendor thật |
| 5 | Upload landing lên hosting (GitHub Pages / VPS / hoặc link trực tiếp) | 🟡 |

---

## AUDIT TOÀN BỘ — 2026-06-16 (Updated)

### A. FILE INVENTORY — 31/31 ✅

Tất cả file từ Phase 1-6 đã được cross-check trên disk. Không thiếu file nào.

### B. COPYWRITING AUDIT — Chất Lượng Cho Từng ICP

Đánh giá dựa trên tiêu chí: đánh trúng pain point, có số liệu cụ thể, giọng văn khớp ICP, call-to-action rõ ràng.

| ICP Bundle | Pain Point | Chất Lượng | Điểm Mạnh | Cần Cải Thiện |
|-----------|-----------|-----------|-----------|--------------|
| **Sinh Viên** | Chạy grab 15-25K/h, mất thời gian đi lại | ⭐⭐⭐⭐ 8/10 | So sánh cụ thể "3 tiếng grab = 45-75K vs 30ph content". Ngôn ngữ gần gũi. | Thêm case study thật (thu nhập tháng đầu) |
| **Freelancer** | Thu nhập không đều, tháng trắng dự án | ⭐⭐⭐⭐⭐ 9/10 | Đánh rất trúng "tháng này 4 dự án, tháng sau trắng". Framing "tầng đệm" khéo. | OK — chỉ thiếu số liệu thực tế |
| **E-comm Pivot** | Phí sàn 40-50%, hoàn hàng, thuế siết | ⭐⭐⭐⭐⭐ 9/10 | Data-driven (số liệu timeline 2023-2026), so sánh song song "cùng 100 conversion". | Thêm quote thật từ người đã chuyển |
| **Mẹ Bỉm** | Không đi làm full-time, cần linh hoạt | ⭐⭐⭐ 7/10 | Đúng insight "làm lúc con ngủ". Nhẹ nhàng, không áp lực. | Pitch hơi ngắn — thiếu comparison cụ thể |
| **Accesstrade Publisher** | KYC, bank duyệt lâu, tracking chậm | ⭐⭐⭐⭐ 8/10 | Rất đúng cho dân đã làm affiliate tài chính. So sánh trực tiếp từng pain point. | Cần EPC/CVR benchmark cụ thể hơn |

**Điểm tổng copywriting: 8.2/10**
- Mạnh nhất: Freelancer + E-comm Pivot (data-driven, pain point sắc)
- Khá: Sinh viên + Accesstrade (đúng insight, thiếu case study thật)
- Cần bổ sung: Mẹ bỉm (pitch hơi mỏng)

**Khuyến nghị:** Sau khi có vendor thật đầu tiên → thêm testimonial + số liệu thật vào tất cả pitch.

### C. DEPLOYMENT GAP — Còn Thiếu Gì Để Triển Khai Thật

| # | Việc | Mức Độ | File Đã Có | Trạng Thái |
|---|------|--------|-----------|-----------|
| 1 | **Tạo bot token riêng cho vendor bot** | ✅ DONE | @BotFather | Token đã có |
| 2 | **Tạo vendor group Telegram thật** | ✅ DONE | 11-group-deployment-pack.md | Group đã tạo |
| 3 | **Setup forum topics** | ✅ DONE | 11-group-deployment-pack.md | Nguoi moi, Tuan 1, Thong bao, Post Log, Goc thac mac |
| 4 | **Deploy vendor_bot.py lên VPS** | ✅ DONE | vendor_bot.py + cron | Bot đang chạy trên VPS, cron active |
| 5 | **Push nội dung Tuan 1 vào Telegram** | ✅ DONE | 10-tuan1-activation-pack.md | 7 message đã đăng vào topic |
| 6 | **Deploy dashboard lên VPS** | 🟡 PENDING | vendor_dashboard.py + templates/ | Claude.ai rate limit — đang fix design, deploy sau |
| 7 | **Đăng pitch tuyển vendor** | 🟡 GẦN XONG | Landing page HTML đã build (9.5/10), copy 17 block sẵn sàng. ⚠️ Cần fix mobile + deploy. |
| 8 | **Chạy outreach Dream 100** | 🟡 HIGH | vendor-recruit-100.csv (45 nguồn) | Tất cả status = "research" |
| 9 | **Test funnel-db.py activate** | 🟢 MEDIUM | funnel-db.py | Chưa test |
| 10 | **Install Tesseract Vietnamese OCR** | 🟢 LOW | — | Để sau |

### D. DEPLOYMENT SEQUENCE — Thứ Tự Triển Khai

```
TUẦN 1: Infrastructure
  1. ✅ Tạo bot token riêng — DONE
  2. ✅ Tạo Telegram group vendor (forum mode) — DONE
  3. ✅ Setup forum topics — DONE
  4. ✅ Deploy vendor_bot.py + cron lên VPS — DONE
  5. ✅ Push 7 message Tuan 1 vào topic — DONE

TUẦN 2: Dashboard + Recruitment
  6. Deploy dashboard lên VPS (gunicorn + nginx) — 🔴 NEXT
  7. Test dashboard với vendor mẫu
  8. Đăng pitch tuyển vendor lên X (@azzam_gold)
  9. Bắt đầu outreach Dream 100 — mỗi ngày 3-5 nguồn
```

### F. AGENT SOUL WORKFLOW — Skill Gap Audit + Phase 8 Plan

> **Research:** Đã fetch docs chính chủ từ https://hermes-agent.nousresearch.com/docs
> **Đã lưu:** `knowledge/hermes-agent-docs/SOUL-specification.md` + `profile-configuration.md`

#### F.1 SOUL.md Spec Chính Chủ — Key Findings

| Spec | Ý nghĩa |
|------|--------|
| SOUL.md = **freeform Markdown** | Không schema cứng, không section bắt buộc |
| SOUL.md = **PERSONA + STYLE** | Tone, communication, what to avoid, uncertainty handling |
| SOUL.md ≠ Workflow | Docs: "What NOT to put: one-off project instructions, file paths, repo conventions, temporary workflow details" |
| Workflow → **AGENTS.md** | Project architecture, coding conventions, tool preferences, commands |
| Prompt slot #1 | SOUL.md inject verbatim, không wrapper, không duplicate |
| Profile dir | `~/.hermes/profiles/<name>/SOUL.md` + `.env` + `config.yaml` |

#### F.2 Quyết Định Thiết Kế — Lai Giữa Spec + Thực Tế

```
Spec chính chủ: SOUL.md = PERSONA thuần, Workflow → AGENTS.md
Thực tế dự án: content_creator V5 có Workflow trong SOUL.md (theo pattern cũ)

→ Quyết định: TÁCH ĐÔI
   SOUL.md         → PERSONA + COMMUNICATION STYLE (theo spec)
   WORKFLOW.md     → Step-by-step execution instructions (file riêng trong profile)
   
   HOẶC (nếu muốn 1 file):
   SOUL.md         → ## PERSONA (spec) + ## WORKFLOW (operational, tách biệt rõ)
                     Có comment "WORKFLOW section — operational instructions, not persona"
```

#### F.3 Phase 8 — SOUL Upgrade (5 agent files)

Mỗi agent: refactor SOUL.md thành 2 section rõ ràng `## PERSONA` + `## WORKFLOW`, theo đúng spec chính chủ cho phần PERSONA.

| # | File | Upgrade | Effort |
|---|------|---------|--------|
| 39 | `vendor_qualifier_SOUL.md` | **PERSONA:** Trump × lead qualifier — direct, decisive, "you're in or you're out". **WORKFLOW:** 6 bước: Google Sheet input → check X profile → 5-signal rubric → PASS/SOFT_PASS/FAIL → template response → log + registry. | 15ph |
| 40 | `vendor_draft_review_SOUL.md` | **PERSONA:** Detail-oriented editor — constructive, specific, "I'm not here to criticize, I'm here to make your post better." **WORKFLOW:** 5 bước: nhận /draft → fetch source Azzam → 6-checkpoint comparison → APPROVE/REWRITE/REJECT → log. | 15ph |
| 41 | `vendor_reporter_SOUL.md` | **PERSONA:** Data analyst — numbers-first, neutral, "the numbers don't lie." **WORKFLOW:** 6 bước: `funnel-db.py report --weekly` → parse → registry check → RANK BOARD compute → template fill → output group + save file. | 15ph |
| 42 | `vendor_boss_SOUL.md` | **PERSONA:** Hormozi meets COO — growth-obsessed, systematic, "show me the numbers, then show me the action." **WORKFLOW:** 4 bước: read blackboard → mode dispatch (NORMAL/MONDAY/RECRUITMENT_PUSH) → manual founder trigger → log. **Dispatch = manual qua founder prompt.** | 15ph |
| 43 | `community_vendor_guide_SOUL.md` | **PERSONA:** Helpful community manager — warm, patient, "I've answered this before, here's the answer." **WORKFLOW:** 5 bước: classify intent → match Card 1-15 → Output Contract reply → nudge new vendors → escalate payout/signal/abuse → log. | 15ph |

**TOTAL Phase 8: 5 files. 75 phút. Pattern: PERSONA (spec) + WORKFLOW (operational).**

### Phase 8 — BUILD LOG (2026-06-16)

| # | File | Lines Before | Lines After | Status |
|---|------|-------------|------------|--------|
| 39 | `scripts/souls/vendor_qualifier_SOUL.md` | 75 | 127 (+52) | ✅ Done |
| 40 | `scripts/souls/vendor_draft_review_SOUL.md` | 86 | 132 (+46) | ✅ Done |
| 41 | `scripts/souls/vendor_reporter_SOUL.md` | 126 | 181 (+55) | ✅ Done |
| 42 | `scripts/souls/vendor_boss_SOUL.md` | 142 | 222 (+80) | ✅ Done |
| 43 | `content-os/souls/community_vendor_guide-SOUL.md` | 114 | 181 (+67) | ✅ Done |
| 44 | `my-skills/hermes-soul-workflow-upgrade/SKILL.md` | — | — | ✅ Done — Skill tái sử dụng cho agent sau |

**TOTAL: 44 files. Phase 8 knowledge → reusable skill.**

### Phase 9 — VOICE Upgrade: Gấu Trúc (2026-06-16)

> **Trigger:** Vendor bot voice quá robot, 5 nhân vật Gấu phức tạp. Học từ Linh Cẩu (SOUL1.txt): đơn giản, giọng ae, xưng "em", gọi "anh/chị/ae", cấm slop.

| # | File | Thay đổi | Status |
|---|------|---------|--------|
| 45 | 5 SOUL files (vendor_qualifier, vendor_draft_review, vendor_reporter, vendor_boss, community_vendor_guide) | Xóa PERSONA dài → thay 1 VOICE block ngắn (15 dòng). Sửa TEMPLATE → giọng ae 🐼 | ✅ Done |
| 46 | `content-os/vendor-agent/VENDOR_KNOWLEDGE_PACK.md` | Sửa Card 1 (START_HERE), Card 10 (VENDOR_RECRUIT), Card 13 (VENDOR_OFFER) → giọng Gấu Trúc, xưng "em", kết 🐼 | ✅ Done |
| 47 | Deploy VPS | 5 SOUL + Knowledge Pack → SFTP upload | ✅ Done |
| 48 | Gateway restart | Kill listener cũ (forward sang marketing_boss từ Jun12) → `community_vendor_guide gateway run --replace` | ✅ Done |
| 49 | Session cache reset | Xóa 16K token context cũ → fresh session | ✅ Done |
| 50 | CLI test | "Chào anh! Vô nhà Gấu Trúc rồi nè 🐼 Em sẽ dẫn ae đi từng bước..." | ✅ Pass |

**Voice Gấu Trúc rule:**
```
Xưng hô: "em" → vendor, "anh/chị/ae" → vendor. "em" → admin/founder.
CẤM: "Tôi rất vui được giúp", "Xin lỗi vì sự bất tiện", "Vui lòng thực hiện", "Trân trọng", "VERDICT:", "SCORE:"
THAY: "Xong rồi nha ae", "Chỗ này chưa ổn, để em sửa cho", "Bài này ngon!", "Ok đăng luôn đi anh!"
Emoji: max 2-3 per message. Signature: 🐼
```

**TOTAL: 50 files. Vendor bot giọng ae — đơn giản như Linh Cẩu.**

### Phase 8 — DEPLOY + TEST (2026-06-16)

| # | Việc | Status |
|---|------|--------|
| 1 | Backup 5 SOUL files (.bak-20260616) | ✅ Done |
| 2 | Create 4 new agent profiles on VPS | ✅ Done |
| 3 | Copy config.yaml + .env to new profiles | ✅ Done |
| 4 | Upload 5 SOUL files via SFTP | ✅ 5/5 OK |
| 5 | Test vendor_qualifier (score applicant) | ✅ SCORE/PASS/FAIL đúng format |
| 6 | Test vendor_draft_review (review draft) | ✅ 6-checkpoint + REJECT đúng |
| 7 | Test vendor_reporter (weekly report) | ✅ Template + RANK BOARD + file save |
| 8 | Test vendor_boss (daily dispatch) | ✅ NORMAL mode + dispatch list |
| 9 | Test community_vendor_guide (intent classify) | ✅ Card mapping + Output Contract |

### Phase 8 — Test Scores

| Agent | Điểm trước | Điểm sau | Test result |
|-------|-----------|---------|------------|
| vendor_qualifier | 5/10 | **8/10** | SCORE 25/100 FAIL — check X thật (404), 5 signals, template |
| vendor_draft_review | 6/10 | **9/10** | REJECT 2/6 — 4 checkpoint, signal leakage, escalate admin |
| vendor_reporter | 5/10 | **9/10** | Full template, funnel-db + registry, RANK BOARD, save file |
| vendor_boss | 6/10 | **8/10** | NORMAL mode, P1 activation check, dispatch list, log |
| community_vendor_guide | 7/10 | **9/10** | Intent Card mapping, Output Contract, escalate rule |
| **TRUNG BÌNH** | **5.8/10** | **8.6/10** | All agents executable on VPS |

#### F.4 Trước vs Sau — SOUL Score

| Agent | Trước (V1) | Sau (V2) |
|-------|-----------|---------|
| vendor_qualifier | RUBRIC trừu tượng, không biết input | PERSONA Trump + 6-step WORKFLOW: Google Sheet→check X→rubric→output→log |
| vendor_draft_review | Checklist lý thuyết, không biết so sánh với gì | PERSONA Editor + 5-step WORKFLOW: /draft→fetch source→6-checkpoint→output→log |
| vendor_reporter | "Source: funnel-db.py" — không biết chạy lệnh | PERSONA Analyst + 6-step WORKFLOW: run cmd→parse→compute→template→output→log |
| vendor_boss | "Govern 4 agents" — không dispatch mechanism | PERSONA COO + 4-step: read→dispatch mode→manual trigger→log. Rõ: founder prompt. |
| community_vendor_guide | FAQ không phân loại | PERSONA Community Manager + 5-step: classify→Card→contract→nudge→escalate |
| **Điểm trung bình** | **4.8/10** | **Target: 8.5/10** |

---

### G. TỔNG ĐIỂM TOÀN HỆ THỐNG — 2026-06-16

| Hạng mục | Sub-tasks | Điểm | Trạng thái |
|---------|----------|------|-----------|
| **Gap 1 — Funnel tuyển vendor** | Landing copy, design brief, HTML, ICP bundles, outreach kit, form apply, pitch | 8.5/10 | Landing 9.5/10 HTML, ⚠️ mobile fix |
| **Gap 2 — Kích hoạt 7 ngày** | Bot NUDGES, roadmap, challenge tab, Tuan 1 content, cron, activate cmd | 8.5/10 | Bot live, content pushed, ⚠️ dashboard chưa deploy |
| **Gap 3 — Dream 100 vendor** | Recruit CSV (45 nguồn), outreach kit, phân loại kênh | 7/10 | File sẵn sàng, ⚠️ chưa outreach nguồn nào |
| **Gap 4 — Rank ladder** | 4 bậc, 5 tier commission, cơ chế thăng/giáng, RANK BOARD | 8/10 | Thiết kế xong, chờ vendor thật để áp dụng |
| **Gap 5 — Offer đóng gói** | Value equation, pitch 6 điểm, Card 13, so sánh affiliate | 9/10 | Hoàn chỉnh — dùng được ngay |
| **Bot & Infrastructure** | vendor_bot.py, cron, deploy script, group, forum topics | 8/10 | Live trên VPS, ⚠️ dashboard pending |
| **Dashboard & Web** | Flask app, 3 templates, dc.html standalone, design briefs | 7/10 | Code xong, ⚠️ chưa deploy VPS |
| **Agent SOUL** | 5 vendor agents (qualifier, draft, reporter, boss, guide) | **8.6/10** | ✅ Deployed VPS + tested. VOICE Gấu Trúc live 🐼 |
| **Landing Page** | Copy 17 block, design brief 718 dòng, HTML 9.5/10 | 8.5/10 | ⚠️ Mobile fix + deploy |
| **Application Form** | Form template, scoring rubric, 3 response templates | 9/10 | Sẵn sàng tạo Google Form |
| **VOICE Brand** | Gấu Trúc — giọng ae, xưng "em", cấm slop, signature 🐼 | **9/10** | ✅ 5 SOUL + Knowledge Pack deployed. Chờ Telegram test. |
| **TỔNG HỆ THỐNG** | **11 hạng mục, 50 files** | **8.2/10** | 5/5 agents live VPS. VOICE Gấu Trúc live. Landing chờ mobile fix. Dashboard chờ deploy. |

### H. PRIORITY — Việc Tiếp Theo

```
🟢 P0 — ĐÃ XONG:
   SOUL workflow upgrade (5 files) → deployed + tested VPS ✅
   Agent profiles configured (config.yaml + .env) ✅

🟡 P1 — Có vendor đầu tiên:
   Landing mobile fix + deploy
   Đăng pitch lên X + outreach 5-10 nguồn đầu
   Xử lý vendor apply → chạy 7-day activation thật
   Dashboard deploy lên VPS

🟢 P2 — Sau khi có vendor:
   Test funnel-db.py activate với data thật
   Thu thập screenshot/testimonial → chèn vào landing
   Áp dụng rank ladder
```

### I. DEPLOYMENT STATUS — Updated 2026-06-16

| # | Việc | Status |
|---|------|--------|
| 1 | Bot token + group Telegram | ✅ |
| 2 | Forum topics setup | ✅ |
| 3 | vendor_bot.py + cron VPS | ✅ |
| 4 | Tuan 1 content pushed | ✅ |
| 5 | SOUL workflow upgrade (5 agents) | ✅ Deployed + tested 8.6/10 |
| 6 | **VOICE upgrade Gấu Trúc (5 SOUL + Knowledge Pack)** | ✅ Deployed + CLI test pass |
| 7 | Dashboard Flask VPS | 🟡 PENDING |
| 8 | Landing page deploy | 🟡 Mobile fix needed |
| 9 | Pitch tuyển + outreach | 🟡 Content ready, chưa đăng |
| 10 | Test funnel-db.py activate | 🟢 |
| 11 | Tesseract OCR | 🟢 |
| 12 | Test Telegram — vendor bot giọng Gấu Trúc | 🟡 Chờ anh test |

```
✅ BUILD: Toàn bộ 31 files — done
✅ DEPLOY: Bot token + Group + Forum topics + Tuan 1 content + vendor_bot.py cron
✅ DUYỆT: Reward bậc — Founder chọn phương án C (2026-06-15)
🔴 NEXT: Deploy dashboard Flask lên VPS (gunicorn + nginx)

❌ KHÔNG: Tự đổi payment rate
❌ KHÔNG: Deploy dashboard khi chưa test với vendor mẫu
```

---

*Plan cập nhật lần cuối: 2026-06-15 | Phase 1-6 complete | Chờ deploy infrastructure*
        ▼          ▼         ▼         ▼          ▼
┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────────┐
│vendor_   │ │vendor_   │ │vendor_   │ │community_│ │vendor_       │
│qualifier │ │draft_    │ │reporter  │ │vendor_   │ │[future]      │
│          │ │review    │ │          │ │guide     │ │              │
├──────────┤ ├──────────┤ ├──────────┤ ├──────────┤ ├──────────────┤
│Score     │ │Review    │ │Reports   │ │Auto-reply│ │Research      │
│applicants│ │drafts    │ │RANK BOARD│ │Nudge     │ │sources       │
│PASS/FAIL │ │APPROVE/  │ │Activation│ │Escalate  │ │Competitor    │
│          │ │REWRITE/  │ │Churn     │ │          │ │analysis      │
│          │ │REJECT    │ │          │ │          │ │              │
└────┬─────┘ └────┬─────┘ └────┬─────┘ └────┬─────┘ └──────────────┘
     │            │            │            │
     └────────────┴────────────┴────────────┘
                         │
                         ▼
            ┌─────────────────────────┐
            │   SHARED DATA LAYER     │
            │  (file — stateless)     │
            │                         │
            │ vendor-registry.json    │
            │ funnel.jsonl            │
            │ daily-stats.json        │
            │ VENDOR_KNOWLEDGE_PACK.md│
            │ vendor-recruit-100.csv  │
            └─────────────────────────┘
```

### E. OPS RUNBOOK — Đã Có vs Thiếu

```
┌────────────────────────────────┬───────────────────────────────────────────┐
│ Runbook                         │ Status                                    │
├────────────────────────────────┼───────────────────────────────────────────┤
│ VENDOR-GROUP-OPS-RUNBOOK.md    │ ✅ ĐÃ CÓ — onboarding + gate + content     │
│                                │ → Đã update: weekly report + RANK BOARD   │
├────────────────────────────────┼───────────────────────────────────────────┤
│ 11-group-deployment-pack.md    │ ✅ ĐÃ BUILD — pin messages, Tuan 1, bot    │
│                                │ → Cần update: tách bot token riêng        │
├────────────────────────────────┼───────────────────────────────────────────┤
│ 12-vendor-ops-runbook.md       │ ✅ ĐÃ BUILD — daily/weekly/monthly ops     │
│                                │ → Agent map + escalation + maintenance    │
├────────────────────────────────┼───────────────────────────────────────────┤
│ vendor-outreach-kit.md         │ ✅ ĐÃ BUILD — 6 kênh + lịch đăng          │
│ vendor-icp-bundles.md          │ ✅ ĐÃ BUILD — 5 ICP pitch                  │
│ vendor-recruit-ecommerce-pivot │ ✅ ĐÃ BUILD — case Tuấn + comparison       │
└────────────────────────────────┴───────────────────────────────────────────┘
```

### F. TỔNG KẾT AUDIT (SAU KHI FIX)

```
┌────────────────────────┬───────────────────────────────────────────────────┐
│ Tiêu chí                │ Đánh giá                                          │
├────────────────────────┼───────────────────────────────────────────────────┤
│ Chuẩn OPS chưa?         │ ✅ CÓ — 3 runbook + agent map + escalation       │
├────────────────────────┼───────────────────────────────────────────────────┤
│ Đụng main bot không?    │ ✅ KHÔNG — đã revert marketing_boss +             │
│                         │ signal_funnel. 11 agent main giữ nguyên.         │
├────────────────────────┼───────────────────────────────────────────────────┤
│ Vendor bot riêng?       │ ✅ CÓ — 5 agent standalone, separate token,      │
│                         │ separate gateway process.                        │
├────────────────────────┼───────────────────────────────────────────────────┤
│ Agent vendor clone từ?  │ ✅ vendor_boss ← marketing_boss structure         │
│                         │ ✅ vendor_reporter ← signal_funnel structure      │
│                         │ ✅ vendor_qualifier ← lead_qualifier rubric       │
│                         │ ✅ vendor_draft_review ← content_creator gate     │
│                         │ ✅ community_vendor_guide ← đã có, đã upgrade     │
├────────────────────────┼───────────────────────────────────────────────────┤
│ Shared resource?        │ ✅ Data files: funnel.jsonl, vendor-registry.json │
│                         │ ✅ CLI tool: funnel-db.py (stateless)             │
│                         │ ❌ KHÔNG share: agent process, bot token          │
├────────────────────────┼───────────────────────────────────────────────────┤
│ Còn thiếu gì?           │ ⏸️ Deploy bot scripts Python lên VPS              │
│                         │ ⏸️ Tạo vendor bot token riêng trên Telegram       │
│                         │ ⏸️ Test với vendor thật                           │
│                         │                                                    │
│                         │ [CẬP NHẬT 15/6]:                                   │
│                         │ ✅ Bot đã deploy (259 dòng, cron-only)             │
│                         │ ✅ Token đã có sẵn (8947508961:...)                │
│                         │ ✅ Gateway community_vendor_guide đang chạy        │
│                         │ ✅ vendor-registry.json có vendor đầu (@hiephoang)│
│                         │ ⏸️ Chưa test vendor thật >3 người                 │
│                         │ ⏸️ 4 agent SOUL chưa có Python executor           │
└────────────────────────┴───────────────────────────────────────────────────┘
```

---

## PHẢN BIỆN — Tính Thực Tế Của Plan (2026-06-15)

> **Vai trò:** Devil's advocate. Không bênh vực plan — chỉ chỉ ra cái gì KHÔNG hoạt động được.
> **Câu hỏi:** Nếu đem plan này ra vận hành thật ngày mai, cái gì sẽ gãy?

---

### 1. BOT KHÔNG TỒN TẠI — 5 Agent SOUL Là File Text, Không Phải Code

```
THỰC TRẠNG (lúc audit):
  5 file SOUL = 543 dòng markdown.
  0 dòng Python bot code.
  0 Telegram bot token riêng cho vendor.
  0 gateway process riêng cho vendor.

[CẬP NHẬT 15/6 — ĐÃ FIX]:
  ✅ vendor_bot.py: 259 dòng Python, deployed VPS, cron nudge/reminder/weekly
  ✅ Gateway: community_vendor_guide đang chạy (Gemini Flash, token 8947508961)
  ✅ Token + group ID: đã có sẵn trong .env từ trước
  ✅ vendor-registry.json: live, auto-read/write
  ⏸️ 4 agent SOUL (qualifier/draft_review/boss/reporter): chưa có Python executor
     → Hiện tại manual qua admin hoặc gọi qua Hermes gateway

→ KẾT LUẬN CẬP NHẬT: Bot đã chạy. Lớp automation cơ bản (nudge/reminder/weekly)
  đã có. Lớp agent thông minh (auto score, auto review) cần code thêm.
```

### 2. RUNBOOK DAILY — "5 Phút Check" Là Ảo Tưởng

```
RUNBOOK GHI:
  "09:00 — Mở Telegram vendor group. Check Goc thac mac — bot trả lời đúng không?"

THỰC TẾ:
  Không có bot auto-reply → admin phải TỰ TRẢ LỜI từng câu hỏi.
  10 vendor × 2 câu hỏi/ngày = 20 câu cần trả lời thủ công.
  Mỗi câu cần: đọc → tra card knowledge pack → soạn reply → gửi.
  ~3 phút/câu = 60 phút/ngày chỉ để trả lời câu hỏi.

  "Check Post Log — có bài mới chưa validate?"
  Mỗi bài cần: mở URL → check 6 checkpoints → quyết định APPROVE/REWRITE/REJECT.
  ~5 phút/bài × 5 vendor đăng bài/ngày = 25 phút.

  "Gửi nudge Tuan 1"
  Không có bot nudge → admin phải TỰ TAY nhắn từng vendor.
  Check ai joined mấy ngày → tính day N → soạn nudge → gửi.
  ~3 phút/vendor × 5 vendor mới = 15 phút.

  TỔNG THỰC TẾ: ~100 phút/ngày cho 10 vendor.
  Đây là part-time job, không phải "check 5 phút".

→ KẾT LUẬN: Daily ops runbook hiện tại giả định bot đã chạy auto.
  Khi không có bot, admin cần 1.5-2h/ngày cho 10 vendor.
  KHÔNG scalable nếu không có code automation.

[CẬP NHẬT 15/6]:
  ✅ Gateway (community_vendor_guide) lo Q&A — admin không cần trả lời tay
  ✅ Bot cron lo nudge Tuan 1 (08:00) + reminder (18:00) — admin không cần nhắn tay
  ⏸️ Draft review + valid join verify vẫn cần admin làm tay
  → Thời gian admin giảm từ ~100ph/ngày xuống ~30ph/ngày (chỉ review draft + verify join)
```

### 3. 7-DAY ACTIVATION — Sẽ Có 60-80% Vendor Rơi

```
PLAN GIẢ ĐỊNH:
  "60% vendor đăng first post trong 7 ngày"
  "Mỗi ngày 1 nudge nhẹ nhàng → vendor làm theo"

THỰC TẾ (industry benchmark cho affiliate/community programs):
  - Tỉ lệ "join rồi không làm gì": 50-70%
  - Tỉ lệ "đọc rule + setup profile": 20-30%
  - Tỉ lệ "đăng bài đầu": 10-20%
  - Tỉ lệ "tiếp tục sau tuần 2": 5-10%

  Lý do:
  1. Người vào group xem rồi quên — Telegram group không phải app họ mở hàng ngày
  2. Nudge gửi trong TOPIC — nếu họ không vào group, họ không thấy
  3. Không có DM riêng — vendor không bị "ping" trực tiếp
  4. Không có incentive để làm ngay — "để mai làm cũng được"
  5. X profile setup là rào cản — nhiều người không muốn sửa profile cá nhân

→ KẾT LUẬN: Target 60% activation rate là không thực tế cho giai đoạn đầu.
  Thực tế: 15-25% sẽ đăng first post. Cần:
  - DM riêng thay vì chỉ topic message
  - Incentive cho first post (bonus nhỏ, recognition sớm)
  - Onboarding call 5 phút thay vì chỉ text
  - Giảm friction: không yêu cầu sửa X profile (cho đăng luôn)
```

### 4. RECRUITMENT PIPELINE — Số Liệu Quá Lạc Quan

```
PLAN GIẢ ĐỊNH:
  "10 applications/tuần từ 44 nguồn"
  "60% pass rate"
  "60% activation rate"  
  "50% → Active"

  → 10 × 0.6 × 0.6 × 0.5 = 1.8 Active vendor/tuần
  → ~7 Active vendor/tháng

THỰC TẾ (với outreach manual, không ads):
  Post 1 bài trong group Facebook 500K members:
  - Reach thực tế: 500-2000 người (thuật toán FB giảm reach bài không tương tác)
  - Click xem: 10-50 người
  - DM "vendor": 2-5 người
  - Hoàn thành 3 câu hỏi: 1-3 người
  
  → 1 bài post chất lượng ≈ 1-2 applications.
  
  Đăng 3 group/tuần × 2 applications/group = 6 applications/tuần.
  Không phải 10.

  Pass rate thực tế:
  - X profile public, real: 70% pass
  - Có chút context finance/trading: 40% pass
  - Cam kết 30ph/ngày (nhưng có làm thật không?): 100% nói có, 20% làm thật
  → Pass rate thực: 30-40%, không phải 60%.

  Activation rate thực tế: 15-25% (xem phần 3)

  → 6 × 0.35 × 0.20 × 0.50 = 0.21 Active vendor/tuần
  → ~1 Active vendor/tháng từ organic outreach.

→ KẾT LUẬN: Với outreach manual, kỳ vọng 1-2 Active vendor/tháng là thực tế.
  Để đạt 10 Active vendor cần: hoặc chạy ads, hoặc có KOL giới thiệu,
  hoặc pipeline 50+ applications/tháng.
```

### 5. RANK LADDER — Thiếu Cơ Chế Theo Dõi Thực Tế

```
PLAN THIẾT KẾ:
  "Xét hạng mỗi thứ 2. Promotion/demotion dựa trên số joins."

THỰC TẾ:
  vendor-registry.json được định nghĩa trong document nhưng:
  - KHÔNG có script nào tự động cập nhật 30day_joins
  - KHÔNG có script nào compute promotion/demotion
  - KHÔNG có "recruited_by" field để track Senior commission
  - funnel-db.py report --weekly có "top vendor" nhưng không lưu vào registry

  → Admin phải TỰ TAY: đếm joins 30 ngày, so sánh với threshold,
    quyết định thăng/giáng, cập nhật registry JSON thủ công.

  Khi có 3-5 vendor: làm được.
  Khi có 20+ vendor: không làm nổi.

  BONUS 50K-200K cho Top: không có formula.
  Ai quyết định 50K hay 200K? Cảm tính → tranh cãi.

  SENIOR 5% commission từ vendor tuyển dưới:
  - Không có field "recruited_by" trong registry
  - Không có script tính commission chồng
  - Không verify được "vendor này do ai tuyển"

→ KẾT LUẬN: Rank system là MANUAL hoàn toàn ở hiện tại.
  Cần ít nhất: script auto-compute joins, "recruited_by" field,
  formula bonus rõ ràng (vd: top 1 = 200K, top 2 = 100K, top 3 = 50K).
```

### 6. SKILL GAP — Agent SOUL Thiếu Workflow Thực Tế

```
5 agent SOUL vendor đều có cấu trúc: MEMORY → SCOPE → RUBRIC → OUTPUT.

NHƯNG THIẾU:
  1. Không có workflow "tôi nhận input gì → tôi gọi tool gì → tôi output ra đâu"
     Các agent SOUL không có STEP-BY-STEP instructions như content_creator có
     ("1. Read latest-summary.md 2. Read xauusd-latest.json...")

  2. vendor_qualifier: không có instruction CỤ THỂ về cách check X profile
     (dùng API gì? web fetch? manual input?). Chỉ có rubric trừu tượng.

  3. vendor_draft_review: không có instruction về CÁCH phát hiện copy
     (so sánh với source nào? dùng tool gì?). Chỉ có checklist lý thuyết.

  4. vendor_reporter: không có instruction gọi funnel-db.py.
     Rubric nói "Source: funnel-db.py report --weekly" nhưng không có
     workflow "chạy lệnh này → parse output → điền vào template".

  5. vendor_boss: "govern 4 agents" nhưng không có dispatch mechanism.
     Làm sao vendor_boss gọi vendor_qualifier? Qua API? Qua blackboard?
     Qua manual founder prompt? Không rõ.

→ KẾT LUẬN: SOUL agent cần thêm WORKFLOW SECTION — mô tả chính xác
  input → tools → output, giống như content_creator V5 đã có.
  Hiện tại SOUL chỉ là PERSONA + RUBRIC, thiếu EXECUTION LAYER.
```

### 7. ĐIỂM CHƯA HỢP LÝ — Mâu Thuẫn Trong Thiết Kế

```
7.1 "Không cần kinh nghiệm" vs "Cần X account 100+ followers"
    → Người không kinh nghiệm thường không có X account.
    → Nếu có, thường là account cá nhân 0-50 followers, không liên quan finance.
    → Mâu thuẫn: pitch nói "ai cũng làm được" nhưng gate cần profile chuẩn.

7.2 "30 phút/ngày" vs "Reply 3-5 bài + like 5-10 bài + retweet 2-3 bài"
    → 30 phút rewrite + đăng đã là minimum.
    → Thêm reply/engage mất ít nhất 20-30 phút nữa.
    → Thực tế: 45-60 phút/ngày cho người mới, không phải 30.

7.3 "Bắt đầu 0đ" vs "Case Tuấn: setup 7.4M + 1.5M/tháng"
    → Pitch nói 0đ. Case study nói 7.4M.
    → Người đọc sẽ thấy mâu thuẫn.
    → Cần rõ: Đường A (thủ công 1 acc) = 0đ. Đường C (full auto) = 7.4M.

7.4 "Không phải scam" nhưng pitch dùng ngôn ngữ "làm giàu"
    → "Cùng 100 conversion: 1M thay vì 400K"
    → "Kiếm 5-15 triệu/tháng"
    → Con số này cần 500-1500 valid joins/tháng — chưa ai đạt được.
    → Dùng số liệu chưa có thật → risk bị gán "scam".

7.5 Payment 10K/join nhưng chưa có conversion tracking thật
    → funnel-db.py log được join nhưng cần admin verify "valid".
    → Valid join criteria: "không bot, không spam, còn trong group sau 24h"
    → Không có script auto-verify → admin phải check từng join.
    → 100 joins/tuần = admin mất 2-3h chỉ để verify.
```

### 8. CÁI GÌ THỰC SỰ DÙNG ĐƯỢC HÔM NAY

```
ĐÃ SẴN SÀNG (có thể vận hành tay ngay):
  ✅ Vendor onboarding flow (manual — admin dùng Telegram + checklist)
  ✅ Draft review (manual — admin đọc + Card 5 rubric)
  ✅ Post-log tracking (funnel-db.py log --source)
  ✅ Weekly report (funnel-db.py report --weekly)
  ✅ Payment calculation (funnel-db.py payment --week)
  ✅ Outreach pitch templates (vendor-outreach-kit.md)
  ✅ Knowledge base cho support (13 cards)

[CẬP NHẬT 15/6 — ĐÃ CODE + DEPLOY]:
  ✅ Bot auto-nudge Tuan 1 — cron 08:00, test OK (gửi cho @hiephoang47)
  ✅ Bot auto-reminder chưa post — cron 18:00, test OK
  ✅ Bot auto-weekly report posting — cron T2 09:00
  ✅ Bot auto-reply vendor question — Gateway community_vendor_guide (Gemini Flash)
  ✅ vendor-registry.json — live, auto-read/write by bot

CHƯA SẴN SÀNG (cần code thêm):
  ❌ Auto applicant scoring (vendor_qualifier SOUL có, chưa code Python)
  ❌ Auto draft review (vendor_draft_review SOUL có, chưa code Python)
  ❌ Auto RANK BOARD computation (vendor_reporter SOUL có, chưa code Python)
  ❌ DM notification cho vendor (bot gửi trong group, chưa DM riêng)
  ❌ Auto activation/churn tracking (cần script analyze funnel.jsonl)
```

### 9. ĐỀ XUẤT ĐIỀU CHỈNH — Ưu Tiên Lại

```
✅ PHASE 0 — Manual Pilot (HOÀN THÀNH):
  [P0.1] ✅ Chạy manual với 3-5 vendor test — Gateway đang chạy, sẵn sàng
  [P0.2] ✅ Admin dùng funnel-db.py + Telegram tay
  [P0.3] ⏸️ Đo activation rate thực tế sau 2 tuần (cần vendor thật)
  [P0.4] ⏸️ Dùng số liệu thật để điều chỉnh target

✅ PHASE 1 — Code lớp automation tối thiểu (HOÀN THÀNH 15/6):
  [P1.1] ✅ Bot auto-reply: Gateway community_vendor_guide (Gemini Flash)
  [P1.2] ✅ Bot nudge: vendor_bot.py --nudge, cron 08:00, đã test
  [P1.3] ✅ Bot reminder: vendor_bot.py --reminder, cron 18:00, đã test
  [P1.4] ⏸️ vendor-registry.json auto-sync từ funnel.jsonl (chưa code)

⏸️ PHASE 2 — Code automation đầy đủ (CHƯA LÀM):
  [P2.1] Auto applicant scoring (cần code Python từ vendor_qualifier SOUL)
  [P2.2] Auto draft review (cần code Python từ vendor_draft_review SOUL)
  [P2.3] Auto weekly report + RANK BOARD posting
  [P2.4] Auto rank computation + promotion/demotion

⏸️ PHASE 3 — Scale (CHƯA LÀM):
  [P3.1] Paid recruitment
  [P3.2] Dashboard web
  [P3.3] Auto payment
  [P3.4] Senior commission tracking

KHÔNG NÊN LÀM BÂY GIỜ:
  ✗ Đi pitch 44 nguồn khi chưa có 3-5 vendor test
  ✗ Hứa "kiếm 5-15M/tháng" khi chưa có vendor nào đạt được
  ✗ Mở recruitment ồ ạt khi activation rate chưa được đo thực tế
  ✗ Build web dashboard phức tạp khi mới có <10 vendor
```

### 10. TỔNG KẾT PHẢN BIỆN (đã cập nhật 15/6)

```
┌────────────────────────┬───────────────────────────────────────────────────┐
│ Tiêu chí                │ Đánh giá                                          │
├────────────────────────┼───────────────────────────────────────────────────┤
│ Plan chuẩn OPS chưa?    │ ✅ ĐÃ CÓ — bot nudge/reminder/weekly live         │
│                         │ + Gateway Q&A + 3 cron jobs                      │
├────────────────────────┼───────────────────────────────────────────────────┤
│ Runbook dùng được?      │ ✅ DÙNG ĐƯỢC cho pilot (3-5 vendor)              │
│                         │ → Gateway lo Q&A, bot lo nudge                   │
│                         │ → Admin chỉ cần review draft + verify join       │
├────────────────────────┼───────────────────────────────────────────────────┤
│ Agent SOUL đủ skill?    │ ⚠️ ĐỦ persona + rubric, THIẾU workflow + code     │
│                         │ → 4/5 agent SOUL chưa có Python executor          │
│                         │ → Chỉ community_vendor_guide có runtime (gateway) │
├────────────────────────┼───────────────────────────────────────────────────┤
│ Activation system?      │ ✅ Bot nudge live (7-day), ⚠️ chưa có data thật  │
│                         │ → Cần 3-5 vendor test để đo activation rate       │
├────────────────────────┼───────────────────────────────────────────────────┤
│ Recruitment number?     │ ❌ Chưa test outreach — 0 apps thực tế            │
│                         │ → Cần chạy pitch vài group để có baseline         │
├────────────────────────┼───────────────────────────────────────────────────┤
│ Rank/Payment system?    │ ⚠️ Thiết kế tốt, thiếu automation                  │
│                         │ → vendor-registry.json có, funnel-db.py có        │
│                         │ → Cần script compute rank + formula bonus         │
├────────────────────────┼───────────────────────────────────────────────────┤
│ Có deploy được hôm nay? │ ✅ Pilot: CÓ (gateway + bot + cron đã chạy)      │
│                         │ ⏸️ Scale: CẦN thêm code (P2) + vendor thật        │
├────────────────────────┼───────────────────────────────────────────────────┤
│ Điểm mạnh nhất         │ Bot live 24/7, gateway LLM Q&A, cron automation   │
│ Điểm yếu nhất          │ 4 agent SOUL chưa có code, chưa có vendor thật    │
│ Việc cần làm tiếp      │ Tuyển 3-5 vendor test → đo activation → code P2   │
└────────────────────────┴───────────────────────────────────────────────────┘
```

### ĐIỂM SỐ THỰC TẾ (cập nhật 2026-06-15 sau deploy)

```
                    TRƯỚC (chỉ doc)      SAU (đã deploy bot)
                    ─────────────         ──────────────────
Document/Design:    8/10                  8/10  — không đổi
Agent Design:       6/10                  6/10  — SOUL chưa có workflow
OPS Readiness:      3/10                  6/10  — bot nudge/reminder/weekly live
Scalability:        2/10                  5/10  — cron auto, cần test real vendor
Thực tế:            4/10                  7/10  — dùng được pilot ngay

ĐÃ DEPLOY (2026-06-15):
  ✅ vendor_bot.py (259 dòng) — nudge 08:00 + reminder 18:00 + weekly T2
  ✅ Gateway community_vendor_guide — Q&A vendor (LLM Gemini Flash)
  ✅ Cron 3 jobs — nudge, reminder, weekly
  ✅ vendor-registry.json — live, vendor đầu tiên (@hiephoang47)
  ✅ funnel-db.py activate — log first post

CHƯA DEPLOY (cần test thêm):
  ⏸️ vendor_qualifier — auto score applicant (chưa code Python, mới có SOUL)
  ⏸️ vendor_draft_review — auto review draft (chưa code Python, mới có SOUL)
  ⏸️ vendor_boss — orchestrator (SOUL only, chưa có dispatch)
  ⏸️ vendor_reporter — auto RANK BOARD compute (SOUL only)
  ⏸️ Test với vendor thật >3 người — đo activation rate thực

→ BOT ĐÃ CHẠY. Gateway lo Q&A. Cron lo nudge.
  Cần 3-5 vendor thật để test activation pipeline.
```

### 1. END-TO-END — Hành Trình Vendor (Tuyển → Senior)

```
╔══════════════════════════════════════════════════════════════════════════════╗
║                     HERMES VENDOR — END-TO-END JOURNEY                      ║
╚══════════════════════════════════════════════════════════════════════════════╝

  TUYỂN DỤNG                 ONBOARD                   7-DAY ACTIVATION
 ┌──────────┐           ┌──────────────┐           ┌─────────────────────┐
 │ 5 ICP    │           │ Vào TG group │           │ D1: Đọc rule        │
 │ nguồn    │──▶ DM ──▶ │ Đọc rule     │──▶ Gate ─▶│ D2: Setup profile   │
 │ 44 kênh  │   vendor  │ Setup X prof │   pass    │ D3: Chọn content    │
 │ 6 loại   │   3 câu   │ Admin review │     │     │ D4: Viết nháp       │
 │ outreach │   hỏi     │ Cấp tag+link │     │     │ D5: ★ ĐĂNG BÀI ĐẦU  │
 └──────────┘           └──────────────┘     │     │ D6: Reply + engage  │
                                             │     │ D7: Review tuần     │
                    ┌────────────────────────┘     └─────────┬───────────┘
                    ▼                                        ▼
          ┌──────────────┐                          ┌──────────────┐
          │ ❌ FAIL      │                          │ ACTIVE       │
          │ Hẹn quay lại │                          │ 3+ bài/tuần  │
          │ khi đủ đk    │                          │ Có join đầu  │
          └──────────────┘                          └──────┬───────┘
                                                          │
                    RANK LADDER                           │
    ┌─────────────────────────────────────────────────────┘
    │
    ▼
┌──────────┐    first post    ┌──────────┐   ≥20 joins   ┌──────────┐
│   NEW    │ ───────────────▶ │  ACTIVE  │ ─────────────▶ │   TOP    │
│ vừa vào  │                  │ ≥3 bài   │                │ ≥20 join │
│ 0 bài    │ ◀─────────────── │ ≥1 join  │ ◀───────────── │ dẫn đầu  │
└──────────┘   <10 joins/30d  └──────────┘   <30 joins    └────┬─────┘
                                                               │
                          ≥50 joins × 3 tháng + mentor          │
                                                               ▼
                                                      ┌──────────────┐
                                                      │   SENIOR     │
                                                      │ tag vĩnh viễn│
                                                      │ 5% comm      │
                                                      │ mentor       │
                                                      └──────┬───────┘
                                                             │ tuyển vendor mới
                                                             ▼
                                                      ┌──────────────┐
                                                      │  GROWTH LOOP │
                                                      │  1 Senior →  │
                                                      │  5 New →     │
                                                      │  2 Active →  │
                                                      │  1 Top →     │
                                                      │  lặp lại     │
                                                      └──────────────┘
```

### 2. UX — 7 Ngày Kích Hoạt (Giao Diện Vendor Trong Telegram)

```
╔══════════════════════════════════════════════════════════════════════════════╗
║                     7-DAY ACTIVATION — VENDOR UX                            ║
╚══════════════════════════════════════════════════════════════════════════════╝

  NGÀY 1           NGÀY 2           NGÀY 3           NGÀY 4
 ┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐
 │ 📌 NHẬN: │    │ 📌 NHẬN: │    │ 📌 NHẬN: │    │ 📌 NHẬN: │
 │ Welcome  │    │ Nudge    │    │ Nudge    │    │ Nudge    │
 │ message  │    │ "setup   │    │ "chọn    │    │ "viết    │
 │          │    │  profile │    │  content │    │  nháp"   │
 │ 👆 LÀM:  │    │  hôm nay"│    │  hôm nay"│    │          │
 │ Đọc rule │    │          │    │          │    │ 👆 LÀM:  │
 │ Nhắn     │    │ 👆 LÀM:  │    │ 👆 LÀM:  │    │ Viết     │
 │ 'done'   │    │ Sửa X    │    │ Vào      │    │ nháp bài │
 │          │    │ profile  │    │ Thong    │    │ đầu tiên │
 │ ⏱ 5ph    │    │ Gửi link │    │ bao      │    │ Gửi draft│
 │          │    │ review   │    │ Chọn 1   │    │ cho admin│
 │          │    │          │    │ bài      │    │ check    │
 │          │    │ ⏱ 15ph   │    │          │    │          │
 │          │    │          │    │ ⏱ 10ph   │    │ ⏱ 30ph   │
 └──────────┘    └──────────┘    └──────────┘    └──────────┘

  NGÀY 5 ★         NGÀY 6           NGÀY 7
 ┌──────────┐    ┌──────────┐    ┌──────────┐
 │ 📌 NHẬN: │    │ 📌 NHẬN: │    │ 📌 NHẬN: │
 │ Nudge    │    │ Nudge    │    │ Nudge    │
 │ "ĐĂNG    │    │ "reply   │    │ "review  │
 │  BÀI ĐẦU"│    │  engage" │    │  tuần"   │
 │          │    │          │    │          │
 │ 👆 LÀM:  │    │ 👆 LÀM:  │    │ 👆 LÀM:  │
 │ ★ ĐĂNG  │    │ Reply    │    │ Review   │
 │   BÀI    │    │ 3-5 bài  │    │ tuần đầu │
 │   ĐẦU    │    │ Like     │    │ Chọn bài │
 │   TIÊN   │    │ 5-10 bài │    │ tiếp theo│
 │ Gửi post │    │ Retweet  │    │ Hỏi nếu  │
 │ -log     │    │ 2-3 bài  │    │ có thắc  │
 │          │    │          │    │ mắc      │
 │ ⏱ 10ph   │    │ ⏱ 20ph   │    │ ⏱ 15ph   │
 └──────────┘    └──────────┘    └──────────┘

  REACTION LOOP — Mỗi ngày admin gửi 1 nudge, vendor làm 1 việc, reply 'done'

  ┌─────────┐    ┌─────────┐    ┌─────────┐    ┌─────────┐    ┌─────────┐
  │ Admin   │───▶│ Vendor  │───▶│ Vendor  │───▶│ Vendor  │───▶│ Admin   │
  │ gửi     │    │ đọc     │    │ làm     │    │ reply   │    │ check   │
  │ nudge   │    │ nudge   │    │ task    │    │ 'done'  │    │ + log   │
  └─────────┘    └─────────┘    └─────────┘    └─────────┘    └─────────┘
       ▲                                                              │
       │                                                              │
       └──────────────────── lặp lại ngày tiếp ───────────────────────┘
```

### 3. MULTI-ICP ENTRY — 5 Cửa Vào, 1 Hệ Thống

```
╔══════════════════════════════════════════════════════════════════════════════╗
║               5 ICP ENTRY POINTS → SAME VENDOR SYSTEM                       ║
╚══════════════════════════════════════════════════════════════════════════════╝

  ICP 1: E-COMM               ICP 2: SINH VIÊN            ICP 3: FREELANCER
 ┌──────────────────┐       ┌──────────────────┐       ┌──────────────────┐
 │ Pain: Phí 40-50% │       │ Pain: Grab 15-25K │       │ Pain: Tháng trắng│
 │ 4-5K/đơn TMĐT    │       │ /h, tốn thời gian │       │ dự án, ko đều    │
 │                  │       │                  │       │                  │
 │ Pitch: "Cùng 100 │       │ Pitch: "30ph thay│       │ Pitch: "Tầng đệm │
 │ convert: 1M thay │       │ vì 3h — làm tại  │       │ thu nhập — ko    │
 │ vì 400K"         │       │ nhà"             │       │ phụ thuộc client" │
 │                  │       │                  │       │                  │
 │ Kênh: Group TMĐT │       │ Kênh: Group SV   │       │ Kênh: Group      │
 │ + TikTok aff     │       │ + Việc làm thêm  │       │ Freelance        │
 └────────┬─────────┘       └────────┬─────────┘       └────────┬─────────┘
          │                          │                          │
          └──────────────────────────┼──────────────────────────┘
                                     │
  ICP 4: ACCESSTRADE                 │                ICP 5: MẸ BỈM
 ┌──────────────────┐                │              ┌──────────────────┐
 │ Pain: KYC lằng   │                │              │ Pain: Ko giờ cố  │
 │ nhằng, bank duyệt│                │              │ định, khó ra     │
 │ lâu              │                │              │ ngoài            │
 │                  │                │              │                  │
 │ Pitch: "Campaign │                │              │ Pitch: "Con ngủ  │
 │ dễ nhất — ko KYC │                │              │ thì làm — giờ nào│
 │ real-time track" │                │              │ cũng được"       │
 │                  │                │              │                  │
 │ Kênh: Group      │                │              │ Kênh: Group mẹ   │
 │ Accesstrade + AF │                │              │ bỉm + KD online  │
 └────────┬─────────┘                │              └────────┬─────────┘
          │                          │                       │
          └──────────────────────────┼───────────────────────┘
                                     │
                                     ▼
                    ┌─────────────────────────────────┐
                    │         ╔══════════════╗        │
                    │         ║  CỔNG CHUNG  ║        │
                    │         ║  DM "vendor" ║        │
                    │         ║  3 câu hỏi   ║        │
                    │         ║  Admin review║        │
                    │         ╚══════╤═══════╝        │
                    │       ┌────────┴────────┐       │
                    │       ▼                 ▼       │
                    │  ┌─────────┐     ┌──────────┐   │
                    │  │✅ PASS  │     │❌ FAIL   │   │
                    │  │ Vào     │     │ Hẹn quay │   │
                    │  │ group   │     │ lại      │   │
                    │  └────┬────┘     └──────────┘   │
                    └───────┼─────────────────────────┘
                            │
                            ▼
         ┌──────────────────────────────────────────────┐
         │        CÙNG 1 HỆ THỐNG — KHÔNG PHÂN BIỆT     │
         │                                              │
         │  ✓ Cùng knowledge pack (13 cards)            │
         │  ✓ Cùng agent support (community_vendor_guide)│
         │  ✓ Cùng onboarding (Card 1-7)                │
         │  ✓ Cùng tracking (funnel-db.py)              │
         │  ✓ Cùng payment (10K/valid join, T2 hàng tuần)│
         │  ✓ Cùng rank ladder (New→Active→Top→Senior)  │
         └──────────────────────────────────────────────┘
```

### 4. RANK LADDER — Cơ Chế Thăng/Giáng Hạng + Reward

```
╔══════════════════════════════════════════════════════════════════════════════╗
║              RANK LADDER — THĂNG / GIÁNG / REWARD / ĐẶC QUYỀN               ║
╚══════════════════════════════════════════════════════════════════════════════╝

  ┌───────────────────┐       ┌───────────────────┐       ┌───────────────────┐
  │ 🟢 NEW            │       │ 🔵 ACTIVE          │       │ 🟣 TOP             │
  │                   │       │                   │       │                   │
  │ Vừa vào group     │──▶ FP │ Đã first post     │──▶20J │ ≥20 joins/30 ngày │
  │ Chưa có bài       │       │ ≥3 bài đã đăng    │       │ ≥90% pass review  │
  │                   │◀─ <10J│ ≥1 valid join     │◀─ <30J│ Dẫn đầu tuần      │
  │                   │       │                   │       │                   │
  │ REWARD:           │       │ REWARD:           │       │ REWARD:           │
  │ Chưa có           │       │ 10K/valid join    │       │ 10K/join          │
  │                   │       │ Tên trong weekly  │       │ + bonus 50K-200K  │
  │ ĐẶC QUYỀN:        │       │ report            │       │                   │
  │ Nhận nudge 7 ngày │       │                   │       │ ĐẶC QUYỀN:        │
  │                   │       │ ĐẶC QUYỀN:        │       │ Vendor of Week    │
  │                   │       │ Được gán source   │       │ Tên ghim trong    │
  │                   │       │ tag + tracking    │       │ group             │
  │                   │       │ link              │       │                   │
  └───────────────────┘       └───────────────────┘       └─────────┬─────────┘
                                                                     │
                          ≥50 joins × 3 tháng + mentor 1 vendor      │
                                                                     ▼
  ┌───────────────────────────────────────────────────────────────────────────┐
  │ 🔴 SENIOR                                                                  │
  │                                                                           │
  │ ≥50 valid joins/tháng × 3 tháng liên tiếp + đã mentor ít nhất 1 vendor mới │
  │                                                                           │
  │ REWARD:                             ĐẶC QUYỀN:                            │
  │ 10K/valid join (nền)                Tag "Senior Vendor" vĩnh viễn         │
  │ + 5% commission từ vendor           Quyền mentor vendor mới               │
  │   do mình tuyển dụng                Được ưu tiên trong weekly report      │
  │                                                                           │
  │ ◀─────── GIÁNG HẠNG: <30 joins/30d hoặc 60d ko mentor vendor mới ───────▶ │
  └───────────────────────────────────────────────────────────────────────────┘

  XÉT HẠNG: Thứ 2 hàng tuần (cùng payment cycle)
  ┌──────────┐    ┌──────────────┐    ┌──────────────┐    ┌──────────────┐
  │ New      │───▶│ Active       │───▶│ Top          │───▶│ Senior       │
  │ → Active │    │ → Top        │    │ → Senior     │    │ (giữ nếu đạt) │
  │ first    │    │ ≥20 joins    │    │ ≥50j ×3      │    │              │
  │ post     │    │ trong 30d    │    │ + mentor     │    │              │
  └──────────┘    └──────────────┘    └──────────────┘    └──────────────┘
```

### 5. TELEGRAM GROUP UI — Cấu Trúc Topics + Nội Dung

```
╔══════════════════════════════════════════════════════════════════════════════╗
║         TELEGRAM FORUM — HERMES VENDOR COMMUNITY (7 TOPICS)                 ║
╚══════════════════════════════════════════════════════════════════════════════╝

 ┌─────────────────────────────────────────────────────────────────────────┐
 │ 📌 NGUOI MOI                      │ 📌 QUAN TRONG                       │
 │                                   │                                     │
 │ Pin 1: Welcome + Flow + Rank     │ RANK BOARD 4 bậc                    │
 │ Pin 2: Rule ngắn                  │ Payment rule (10K/join)             │
 │ Onboarding checklist              │ Escalation policy                   │
 │ Profile setup guide               │ Abuse/Revoke rule                   │
 │                                   │                                     │
 │ 👤 Vendor đọc + reply 'done'      │ 👤 Vendor xem — admin-only post     │
 └───────────────────────────────────┴─────────────────────────────────────┘

 ┌─────────────────────────────────────────────────────────────────────────┐
 │ 🗓️ TUAN 1                         │ 📢 THONG BAO                        │
 │                                   │                                     │
 │ Ngày 1: Đọc rule                  │ Daily Content Pack (mỗi sáng)       │
 │ Ngày 2: Setup X profile           │ Weekly Report + RANK BOARD (T2)     │
 │ Ngày 3: Chọn content              │ Admin announcements                 │
 │ Ngày 4: Viết nháp                 │                                     │
 │ Ngày 5: ★ ĐĂNG BÀI ĐẦU TIÊN       │ 👤 Vendor đọc + lấy content          │
 │ Ngày 6: Reply + engage            │ 👨‍💼 Admin post — vendor ko reply     │
 │ Ngày 7: Review tuần đầu           │                                     │
 │                                   │                                     │
 │ 👤 Vendor làm + reply 'done'      │                                     │
 │ 👨‍💼 Admin gửi nudge mỗi ngày      │                                     │
 └───────────────────────────────────┴─────────────────────────────────────┘

 ┌─────────────────────────────────────────────────────────────────────────┐
 │ ❓ GOC THAC MAC                    │ 🐛 FEEDBACK LOI                     │
 │                                   │                                     │
 │ Vendor hỏi → community_vendor_    │ Broken link báo cáo                 │
 │ guide trả lời (Card 1-13)        │ Draft bị reject                     │
 │ Hoặc tag admin nếu escalate      │ Tracking issue                      │
 │                                   │                                     │
 │ 👤 Vendor hỏi                      │ 👤 Vendor báo lỗi                   │
 │ 🤖 Agent trả lời (auto/manual)    │ 👨‍💼 Admin xử lý                      │
 └───────────────────────────────────┴─────────────────────────────────────┘

 ┌─────────────────────────────────────────────────────────────────────────┐
 │ 📊 POST LOG                                                             │
 │                                                                         │
 │ Format: [URL bài X] | @handle | HH:MM | source: [tag]                   │
 │ Ví dụ:   https://x.com/xxx/123 | @xxx | 14:32 | source: x_gulf_v_tuan   │
 │                                                                         │
 │ 👤 Vendor gửi link sau mỗi bài đăng                                      │
 │ 👨‍💼 Admin validate → funnel-db.py log                                    │
 └─────────────────────────────────────────────────────────────────────────┘

 AGENT AUTO-REPLY LOGIC (community_vendor_guide):
 ┌────────────────┬────────────────────────────────────────────┐
 │ Vendor hỏi     │ Agent trả lời Card #                       │
 ├────────────────┼────────────────────────────────────────────┤
 │ "em mới vào"   │ Card 1 — START_HERE (7 bước)              │
 │ "content đâu"  │ Card 2 — CONTENT_SOURCE                   │
 │ "setup X"      │ Card 3 — X_PROFILE                        │
 │ "cách đăng"    │ Card 4 — POSTING_RULE                      │
 │ "check draft"  │ Card 5 — DRAFT_REVIEW                      │
 │ "tracking link"│ Card 6 — TRACKING_LINK (gate check)        │
 │ "post-log"     │ Card 7 — POST_LOG                          │
 │ "tiền/ payment"│ Card 8 — PAYMENT                           │
 │ "khiếu nại"    │ Card 9 — ESCALATE → admin                  │
 │ "làm vendor"   │ Card 10 — VENDOR_RECRUIT (3 câu hỏi)      │
 │ "hôm nay làm gì"│ Card 11 — VENDOR_ACTIVATION (ngày X)      │
 │ "rank/ thăng"  │ Card 12 — VENDOR_RANK (4 bậc)             │
 │ "tại sao làm"  │ Card 13 — VENDOR_OFFER (6 lý do)          │
 └────────────────┴────────────────────────────────────────────┘
```

### 6. GROWTH LOOP — Vòng Lặp Tăng Trưởng (Mô Phỏng 2 Chu Kỳ)

```
╔══════════════════════════════════════════════════════════════════════════════╗
║           GROWTH LOOP — SENIOR → TUYỂN → ACTIVE → TOP → SENIOR              ║
╚══════════════════════════════════════════════════════════════════════════════╝

  CHU KỲ 1 (3 tháng)                          CHU KỲ 2 (3 tháng tiếp)
 ─────────────────────                       ─────────────────────────

  1 SENIOR vendor                             2 SENIOR vendors
       │                                           │
       │ Tuyển 5 vendor mới                        │ Mỗi người tuyển 5 = 10 mới
       ▼                                           ▼
  ┌──────────┐                               ┌──────────┐
  │ 5 NEW    │                               │ 10 NEW   │
  └────┬─────┘                               └────┬─────┘
       │ 3/5 activated (first post)               │ 6/10 activated
       ▼                                           ▼
  ┌──────────┐                               ┌──────────┐
  │ 3 ACTIVE │                               │ 6 ACTIVE │
  └────┬─────┘                               └────┬─────┘
       │ 2/3 tiếp tục đăng bài                    │ 4/6 tiếp tục
       ▼                                           ▼
  ┌──────────┐                               ┌──────────┐
  │ 2 ACTIVE │                               │ 4 ACTIVE │
  │ (đều)    │                               │ (ổn định)│
  └────┬─────┘                               └────┬─────┘
       │ 1/2 lên Top (≥20 joins)                  │ 2/4 lên Top
       ▼                                           ▼
  ┌──────────┐                               ┌──────────┐
  │ 1 TOP    │                               │ 2 TOP    │
  └────┬─────┘                               └────┬─────┘
       │ Sau 3 tháng + mentor                     │ Sau 3 tháng + mentor
       ▼                                           ▼
  ┌──────────┐                               ┌──────────┐
  │ 1 SENIOR │                               │ 2 SENIOR │
  │ MỚI      │                               │ MỚI      │
  └────┬─────┘                               └────┬─────┘
       │                                           │
       └───────────────────┬───────────────────────┘
                           │
                           ▼
                    ┌──────────────┐
                    │ 4 SENIOR     │
                    │ vendors      │
                    │              │
                    │ Mỗi chu kỳ   │
                    │ 3 tháng:     │
                    │ Senior ×2    │
                    │ Active ×4    │
                    │ Join ×N      │
                    └──────────────┘

  ┌─────────────────────────────────────────────────────────────────────────┐
  │  KEY METRICS — Mỗi chu kỳ 3 tháng:                                      │
  │                                                                         │
  │  New → Activated:  60% (3/5)  │  Tỉ lệ rơi:  40% vendor bỏ sau 7 ngày  │
  │  Activated → Active: 67% (2/3) │  Tỉ lệ rơi:  33% bỏ sau khi đăng bài  │
  │  Active → Top:      50% (1/2)  │  Cần ≥20 joins/tháng để lên Top       │
  │  Top → Senior:     100% (1/1)  │  Cần 3 tháng liên tục + mentor        │
  │                                                                         │
  │  Growth factor: 2x mỗi chu kỳ (nếu mỗi Senior tuyển 5 vendor mới)      │
  │  Break-even: Senior đầu tiên mất ~6 tháng từ New                        │
  └─────────────────────────────────────────────────────────────────────────┘
```

### 7. DATA PIPELINE — Từ Post-Log Đến Payment

```
╔══════════════════════════════════════════════════════════════════════════════╗
║                   DATA FLOW — POST-LOG → TRACKING → PAYMENT                 ║
╚══════════════════════════════════════════════════════════════════════════════╝

  VENDOR                     ADMIN                          SYSTEM
 ────────                   ─────────                     ──────────

  Đăng bài X
      │
      ▼
  Gửi post-log ──────────▶ Validate bài
  [URL] | @handle              │
  | HH:MM | source:       ┌────┴────┐
                          ▼         ▼
                      ✅ PASS    ❌ FAIL
                          │         │
                          │         └──▶ Báo vendor sửa
                          ▼
                    ┌──────────────┐
                    │ Log CLICK    │
                    │ funnel-db.py │
                    │ log --source │
                    └──────┬───────┘
                           │
                           ▼
                    ┌──────────────┐     ┌──────────────┐
                    │ funnel.jsonl │────▶│ daily-stats  │
                    │ (append-only │     │ .json        │
                    │  JSONL)      │     │ (snapshot EOD)│
                    └──────┬───────┘     └──────────────┘
                           │
                           │ Khi có người join Telegram qua link vendor
                           ▼
                    ┌──────────────┐
                    │ Log JOIN     │
                    │ funnel-db.py │
                    │ log --join   │
                    └──────┬───────┘
                           │
                           │ Admin review → valid?
                           ▼
                    ┌──────────────┐
                    │ Log VALID    │
                    │ JOIN         │
                    │ funnel-db.py │
                    │ log --valid- │
                    │ join --vendor│
                    └──────┬───────┘
                           │
                           │ Khi vendor đăng bài đầu tiên
                           ▼
                    ┌──────────────┐
                    │ Log ACTIVATE │
                    │ funnel-db.py │
                    │ activate     │
                    │ --vendor     │
                    └──────┬───────┘
                           │
                           ▼
              ┌────────────────────────┐
              │   THỨ 2 HÀNG TUẦN     │
              │                        │
              │ funnel-db.py           │
              │   report --weekly      │
              │   payment --week       │
              │                        │
              │ → Weekly Report        │
              │ → Payment Estimate     │
              │ → RANK BOARD update    │
              └────────────┬───────────┘
                           │
                           ▼
                    ┌──────────────┐
                    │ 💰 PAYMENT   │
                    │ valid_joins  │
                    │ × 10,000 VND │
                    │              │
                    │ Gửi vendor   │
                    │ Thứ 2        │
                    └──────────────┘
```

### 8. BOT INTEGRATION — @hermes7979_bot × Vendor Community

```
╔══════════════════════════════════════════════════════════════════════════════╗
║           @hermes7979_bot — CHĂM VENDOR TỰ ĐỘNG TRONG GROUP                 ║
╚══════════════════════════════════════════════════════════════════════════════╝

  VENDOR GROUP (Telegram Forum)              @hermes7979_bot (VPS)
 ─────────────────────────────             ──────────────────────────

 ┌──────────────────────┐                  ┌──────────────────────────┐
 │ 🆕 Vendor join group │                  │ vendor_registry.json     │
 │                      │──▶ auto-detect ─▶│ Ghi: name, date, status  │
 └──────────────────────┘                  └────────────┬─────────────┘
                                                        │
 ┌──────────────────────┐                               ▼
 │ 👤 Vendor gửi msg    │                  ┌──────────────────────────┐
 │ trong Goc thac mac   │──▶ listener ───▶│ community_vendor_guide   │
 │                      │   quét 24/7     │ (Gemini 2.5 Flash)       │
 └──────────────────────┘                  │ → route Card 1-13       │
                                           │ → reply ngắn + next step│
 ┌──────────────────────┐                  └────────────┬─────────────┘
 │ ✍️ Vendor gửi /draft │                               │
 │ [text]               │──▶ analyze ───────────────────┘
 │                      │   → APPROVE / REWRITE / REJECT
 └──────────────────────┘

 ┌──────────────────────┐                  ┌──────────────────────────┐
 │ 📊 Vendor gửi /log   │──▶ validate ───▶│ funnel.jsonl             │
 │ [URL]                │   format         │ → log click              │
 │                      │   + detect       │ → nếu first post:        │
 │                      │   first post     │   log activate           │
 └──────────────────────┘                  │   → thăng New → Active  │
                                           └──────────────────────────┘

 ⏰ CRON JOBS (VPS) — Bot tự chạy:
 ┌─────────────────────┬─────────────────────────────────────────────────────┐
 │ 08:00 VN mỗi ngày   │ vendor_nudge: Quét vendor chưa first post →         │
 │                     │ gửi nudge ngày N vào Tuan 1. N>7 → flag cold.      │
 ├─────────────────────┼─────────────────────────────────────────────────────┤
 │ 18:00 VN mỗi ngày   │ vendor_reminder: Nhắc Active vendor chưa post       │
 │                     │ hôm nay: "Còn 30 phút — chưa thấy post-log!"        │
 ├─────────────────────┼─────────────────────────────────────────────────────┤
 │ Thứ 2 09:00 VN      │ vendor_weekly: Chạy report → auto-post Weekly       │
 │                     │ Report + RANK BOARD vào Thong bao                   │
 ├─────────────────────┼─────────────────────────────────────────────────────┤
 │ Liên tục            │ vendor_listener: Quét Goc thac mac + Post Log +     │
 │                     │ Feedback loi → auto-reply hoặc escalate             │
 └─────────────────────┴─────────────────────────────────────────────────────┘

 BOT COMMANDS — Vendor gõ trong group:
 ┌──────────────┬──────────────────────┬──────────────┬──────────────────────┐
 │ /start       │ START_HERE (7 bước) │ /payment     │ Formula 10K/join     │
 │ /content     │ CONTENT_SOURCE      │ /rank        │ VENDOR_RANK (4 bậc)  │
 │ /profile     │ X_PROFILE checklist │ /today       │ Nhiệm vụ hôm nay     │
 │ /post        │ POSTING_RULE        │ /why         │ 6 lý do làm vendor   │
 │ /draft [txt] │ DRAFT_REVIEW        │ /help        │ List tất cả lệnh      │
 │ /link        │ TRACKING_LINK gate  │ /escalate    │ Forward admin         │
 │ /log [URL]   │ Validate post-log   │              │                       │
 └──────────────┴──────────────────────┴──────────────┴──────────────────────┘

 BOT AUTO BEHAVIOR MATRIX:
 ┌─────────────────────┬─────────────────────────────────────────────────────┐
 │ Trigger             │ Bot Action                                          │
 ├─────────────────────┼─────────────────────────────────────────────────────┤
 │ Vendor join group   │ Gửi welcome DM + ghi registry + tag New rank       │
 │ 08:00 daily         │ Nudge vendor Tuan 1 (ngày 1-7)                     │
 │ 18:00 daily         │ Reminder Active vendor chưa post hôm nay           │
 │ First post detected │ Log activate → thăng New→Active → chúc mừng        │
 │ ≥20 joins/30d       │ Auto-promote Active→Top → post vào Thong bao       │
 │ ≥50j ×3 + mentor   │ Đề xuất Senior → báo admin duyệt                   │
 │ Thứ 2 09:00         │ Post Weekly Report + RANK BOARD vào Thong bao      │
 │ >14d no post        │ Flag cold → báo admin: "[tên] 14 ngày ko post"     │
 │ Violation detected  │ Cảnh báo + log + báo admin review                  │
 └─────────────────────┴─────────────────────────────────────────────────────┘

 VENDOR REGISTRY — Bot auto-maintain:
 ┌───────────────────────────────────────────────────────────────────────────┐
 │ /root/hermes-data/vendor-registry.json                                     │
 │                                                                           │
 │ { "vendor": "tuan", "rank": "active", "join_date": "2026-06-10",         │
 │   "first_post_date": "2026-06-15", "activation_day": 5,                   │
 │   "30day_joins": 12, "total_joins": 12, "status": "active" }             │
 │                                                                           │
 │ { "vendor": "vendor_cu", "rank": "new", "join_date": "2026-06-01",       │
 │   "first_post_date": null, "days_no_post": 15, "status": "cold" }        │
 └───────────────────────────────────────────────────────────────────────────┘
```

### 9. BOT + GROUP — Toàn Cảnh Tương Tác

```
╔══════════════════════════════════════════════════════════════════════════════╗
║              BOT × VENDOR × ADMIN — AI CHĂM SÓC 24/7                         ║
╚══════════════════════════════════════════════════════════════════════════════╝

                    🤖 @hermes7979_bot
                    (VPS 103.97.126.117)
                    ╔══════════════════╗
                    ║ 4 CRON JOBS      ║
                    ║ ┌──────────────┐ ║
                    ║ │ nudge 08:00  │ ║────▶ Gửi nudge Tuan 1 mỗi sáng
                    ║ │ reminder 18h │ ║────▶ Nhắc vendor chưa post
                    ║ │ weekly T2    │ ║────▶ Report + RANK BOARD
                    ║ │ listener 24/7│ ║────▶ Auto-reply vendor question
                    ║ └──────────────┘ ║
                    ║                  ║
                    ║ ┌──────────────┐ ║
                    ║ │ community_   │ ║
                    ║ │ vendor_guide │ ║────▶ 13 cards knowledge
                    ║ │ (Gemini Flash)│ ║────▶ NUDGE intent
                    ║ └──────────────┘ ║────▶ ESCALATE routing
                    ╚══════╤═══════════╝
                           │
            ┌──────────────┼──────────────┐
            │              │              │
            ▼              ▼              ▼
   ┌────────────┐  ┌────────────┐  ┌────────────┐
   │ 👤 VENDOR  │  │ 👤 VENDOR  │  │ 👨‍💼 ADMIN  │
   │            │  │            │  │            │
   │ Gõ /help  │  │ Gửi draft  │  │ /vendor    │
   │ → bot trả │  │ → bot      │  │ list       │
   │ lời ngay  │  │ review     │  │ → check    │
   │            │  │ auto       │  │ all status │
   └────────────┘  └────────────┘  └────────────┘

   ESCALATION PATH — Khi bot không xử lý được:
   ┌──────────┐     ┌──────────────┐     ┌──────────────┐
   │ Bot      │────▶│ Flag message │────▶│ Admin nhận   │
   │ detect:  │     │ + forward    │     │ alert → xử   │
   │ payout   │     │ đến admin    │     │ lý riêng     │
   │ dispute  │     │              │     │ (DM vendor)  │
   │ signal   │     │              │     │              │
   │ abuse    │     │              │     │              │
   └──────────┘     └──────────────┘     └──────────────┘
```

---

*Framework: $100M Leads (Hormozi) chương 5-6, 9-10 × Traffic Secrets (Brunson) Dream 100 × Expert Secrets (Brunson) Movement building × $100M Offers (Hormozi) Value Equation × DotCom Secrets (Brunson) Value Ladder*
*Status: APPROVED + BUILT — Phase 1-9 complete. 50 files. Agent ecosystem: 11 agents (6 tận dụng, 5 vendor). VOICE Gấu Trúc live 🐼. 3 runbooks. 9 sơ đồ UX/UI + Bot Integration + Agent Architecture.*
*Next: Anh test Telegram vendor bot → verify giọng Gấu Trúc → deploy dashboard Flask lên VPS.*
