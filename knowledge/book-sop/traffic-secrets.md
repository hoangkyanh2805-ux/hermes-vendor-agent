# OPS PLAN: Traffic Secrets (Brunson) → Hermes tầng TRAFFIC

> Nguồn lý thuyết: sách Traffic Secrets — Russell Brunson
> Slug: traffic-secrets | Tầng phễu: TRAFFIC (đưa người lạ → chạm Hermes → đẩy sang LEAD/B7)
> Dùng cho: VSCode Claude (build), Codex (đối chiếu), Cowork (chạy ops)
> Loại file: OPS PLAN thực thi — không phải tóm tắt sách
> Phụ thuộc: nối thẳng vào `100m-leads.md` (traffic ra → lead vào). Agent đã hợp nhất 2026-06-14.
> Cập nhật: 2026-06-14

---

## 0. Cách dùng
Làm theo PHASE. Mỗi TASK: **Input → Action → Output → File/Agent → Done khi**. Chạy Phase 0.5 trước để thay giả định ⚠️ bằng path thật.

## 0.5. Checkpoint đọc repo TRƯỚC khi làm (bắt buộc)
```
[ ] Xác nhận agent đã merge: content_creator(104) x_farm_manager(78) combat_agent(68) signal_funnel(43)
[ ] ls scripts/ → t1-reply-cta.py, t2-amplifier-pack.py, t3-seeder-pack.py, wire-tele-to-x-auto.py
[ ] Xác nhận 4 X account T1 đang sống (handle nào?) + Module 1 (GenLogin) trạng thái
[ ] CLAUDE.md mục 3-Tier X Farm: 1B/2/3 đang live VPS? MODULE_API_URL có chưa?
[ ] Có sẵn file dream-100 chưa? (knowledge/dream-100-x.csv)
→ Điền path/handle thật vào "Bảng ánh xạ" cuối file, xoá ⚠️.
```
Không pass → DỪNG, báo thiếu gì.

---

## 1. Mục tiêu đo được
> TRAFFIC thành công = đúng người (prop-firm scalper) THẤY content + BẤM reply CTA về Tele. Traffic là đầu vào của B7 (lead).

| Chỉ số | Baseline (đo sau) | Target M0 (5 ngày) |
|--------|-------------------|--------------------|
| Impressions/ngày (4 acc T1) | ? | tăng dần |
| Reply/engage trên Dream 100/ngày | ? | ≥ 20 |
| Profile visit → follow | ? | ≥ 10 follow mới/ngày |
| Click reply-CTA → vào Tele | ? | ≥ 10/ngày (= input B7) |
| Account bị limit/ban | 0 | giữ 0 (anti-ban) |

---

## 2. Tiền đề & phụ thuộc
- 4 X account T1 sống + GenLogin/Module 1 chạy.
- content_creator + x_farm_manager + combat_agent đã merge (✅ 2026-06-14).
- 1 đích duy nhất để đổ traffic: reply CTA → @AZZAM_Trading_Expert (Tele).
- Source attribution: @azzamgoldpro + bot proof.

---

## PHASE 1 — Dream 100 (nền tảng nhắm đúng người)
**T1.1 — Lập danh sách 100 "nơi" ICP tụ tập**
- Input: ICP (`icp-prop-firm-scalper.md`).
- Action: liệt kê account/cộng đồng X mà prop-firm scalper đã ở sẵn: prop-firm chính chủ (FTMO/TFT/Topstep), creator gold/forex lớn, hashtag, cộng đồng scalping.
- Output: `knowledge/dream-100-x.csv` — cột: `handle | loại | follower | T1-reply? | T2-amplify?`
- Done khi: ≥ 50 dòng chất (không cần đủ 100 ngay), đúng ICP (không lẫn trader retail dài hạn).

**T1.2 — Phân tầng Working-In / Working-Out**
- Action: đánh dấu nguồn nào reply organic (Working-Out, ưu tiên) vs nguồn nào trả phí/shoutout (Working-In, để sau).
- Done khi: mỗi dòng Dream 100 có nhãn chiến thuật.

---

## PHASE 2 — Content engine (Hook–Story–Offer)
**T2.1 — Sinh post từ tín hiệu**
- Input: tín hiệu @azzamgoldpro / market context.
- Action: gọi **content_creator** → mỗi post = Hook (chặn scroll) + Story (proof: bot $3K→$23.6K, top1 FTMO) + value. CTA KHÔNG ở body.
- Output: 4 post (4 persona) cho 4 acc T1, ≤280 ký tự, label theo handle.
- Done khi: 4 post qua gate X-safety (xem Mục 7).

**T2.2 — Hook–Retain–Reward**
- Action: mỗi post phải giữ người đọc hết (retain = value thật) rồi mới reward (CTA ở reply).
- Done khi: post có cấu trúc 3 lớp, không phải "spam signal".

---

## PHASE 3 — Phân phối qua X farm (traffic SỞ HỮU)
**T3.1** — Đăng 4 post qua **x_farm_manager** + GenLogin, đúng 3 session (ASIA/LONDON/NY), anti-duplicate.
**T3.2** — `t1-reply-cta.py`: reply CTA dưới chính post của mình → dẫn về Tele.
**T3.3** — `t2-amplifier-pack.py`: acc phụ amplify post chính (chờ MODULE2_API_URL nếu thiếu).
- Done khi: 4 post live đủ 3 session, có reply CTA, không trùng nội dung.

---

## PHASE 4 — Traffic MƯỢN (reply dưới Dream 100)
**T4.1** — Dùng **combat_agent** reply giá trị dưới post của Dream 100 (Working-Out list).
- Reply mang giá trị thật (insight/quan điểm), KHÔNG spam link, KHÔNG copy-paste hàng loạt → tránh ban.
- Soft DM CTA chỉ khi có tương tác qua lại.
- Done khi: ≥20 reply chất/ngày, 0 account bị limit.

---

## PHASE 5 — Chuyển hoá traffic (Mượn → Sở hữu → Kiểm soát)
**T5.1** — Người tương tác từ Dream 100 → kéo về follow 4 acc (sở hữu).
**T5.2** — Follower → reply CTA → vào Tele (kiểm soát) = **bàn giao sang B7/100m-leads**.
- Done khi: có luồng đếm được từ reply → follow → vào Tele.

---

## PHASE 6 — Đo & lặp (cuối ngày)
**T6.1** — **signal_funnel**: ghi 5 KPI Mục 1 vào journal.
**T6.2** — Tìm nút thắt lớn nhất (ít impression? reply không ra follow? follow không vào Tele?) → 1 thử nghiệm ngày sau.
- Done khi: có số + 1 quyết định.

---

## 6. Data artifacts
```
dream-100-x.csv   → handle | loại | follower | T1-reply? | T2-amplify?
cta-templates.md  → reply CTA đã qua gate (dùng chung 100m-leads)
daily-journal     → 5 KPI traffic/ngày (signal_funnel)
```

## 7. Guardrails X-safety (KHÔNG vi phạm — CLAUDE.md rule #2)
- Post full signal (Entry/SL/TP) + source attribution + "Not financial advice" + risk %/trade.
- KHÔNG link trong body (CTA ở reply).
- KHÔNG bịa win-rate. KHÔNG post result của lệnh đang mở (chỉ sau khi đóng).
- Anti-duplicate + anti-ban: 4 persona khác nhau, reply không hàng loạt 1 nội dung.

## 8. Định nghĩa HOÀN THÀNH
Traffic coi như chạy khi: 4 acc đăng đều 3 session + reply Dream 100 ≥20/ngày + có luồng đếm được reply→follow→Tele ≥10/ngày + 0 account ban, trong 5 ngày M0.

## 9. Bảng ánh xạ repo (Claude Code điền sau Phase 0.5)
| Khái niệm | Giả định ⚠️ | Path/handle THẬT |
|-----------|------------|------------------|
| Content gen | agent content_creator | |
| Đăng farm | agent x_farm_manager + GenLogin | |
| Reply CTA | scripts/t1-reply-cta.py | |
| Amplify | scripts/t2-amplifier-pack.py | |
| Reply Dream100 | agent combat_agent | |
| 4 acc T1 | @azzam_gold / @goldrisk_vip / @smc_xauusd / @goldmacro_ | |
| Đích traffic | Tele @AZZAM_Trading_Expert | |

## 10. Bàn giao
TRAFFIC ra → đút thẳng vào `100m-leads.md` Phase 2 (capture). Hai plan nối nhau: traffic Phase 5 = lead Phase "traffic vào".
