# OPS PLAN: $100M Leads (Hormozi) → Hermes B7 "Lead từ X engage"

> Nguồn lý thuyết: sách $100M Leads — Alex Hormozi
> Slug: 100m-leads | Tầng phễu: LEAD | Ưu tiên: #1 (đúng gap B7)
> Dùng cho: VSCode Claude (build), Codex (đối chiếu), Cowork (chạy ops)
> Loại file: OPS PLAN thực thi — không phải tóm tắt sách
> Cập nhật: 2026-06-14

---

## 0. Cách dùng file này
Claude Code/Codex đọc từ trên xuống, làm theo PHASE. Mỗi TASK có: **Input → Action → Output → File đụng tới → Done khi**. Không nhảy phase. Trước khi code, làm **Phase 0.5 (đọc repo)** để thay mọi giả định ⚠️ bằng sự thật.

## 0.5. Checkpoint đọc repo TRƯỚC khi làm (bắt buộc)
> Tác giả SOP không đọc được repo thật → các đường dẫn dưới là GIẢ ĐỊNH (⚠️). Claude Code phải verify:

```
[ ] Đọc CLAUDE.md → xác nhận B7 còn ⬜ và pipeline Tele→X hiện trạng
[ ] ls scripts/  → tìm file capture lead thật (lead-funnel-cli.py?) + schema leads.csv
[ ] cat lead-funnel-cli.py → xác nhận cột CSV + cách ghi
[ ] ls marketing-ops-youtube-x-telegram/lead-magnets/ → xác nhận FTMO checklist tồn tại
[ ] Xác nhận lệnh Tele: score @handle, list lurker hoạt động (CLAUDE.md mục Pipeline)
[ ] Ghi lại path THẬT vào mục "Bảng ánh xạ" cuối file, xoá cờ ⚠️
```
Không pass checkpoint này thì DỪNG, báo người dùng thiếu gì.

---

## 1. Mục tiêu đo được (Definition of Success)
| Chỉ số | Baseline (điền sau khi đo) | Target M0 (5 ngày) |
|--------|---------------------------|--------------------|
| Lead mới vào Tele/ngày | ? | ≥ 10/ngày |
| Tỉ lệ reply CTA → vào Tele | ? | ≥ 15% |
| Lead được score (@handle ghi CRM) | ? | ≥ 70% lead vào |
| Lead "qualified" (≥4/6 signal) | ? | ≥ 30% lead score |
| Chi phí/lead | ? (Tele-ads) | giảm vs ads |

Thứ tự Hormozi: **More → Better → Cheaper → Reliably**. M0 chỉ tối ưu "More" + đo. KHÔNG tối ưu chi phí sớm.

---

## 2. Tiền đề & phụ thuộc
- Traffic vào: cần `traffic-secrets.md` đã chạy (X farm reply có người đọc).
- Lead magnet sẵn: FTMO checklist PDF.
- Capture: `lead-funnel-cli.py` + `score @handle` + lead_qualifier 6-signal.
- Guardrail: chỉ `lead-funnel-cli.py` ghi `leads.csv` (rule CLAUDE.md #3), không LLM ghi.

---

## PHASE 1 — Lead Magnet pass "gate" (1 buổi)

**T1.1 — Audit lead magnet hiện tại**
- Input: `lead-magnets/ftmo-xauusd-scalping-checklist.md`
- Action: chấm theo gate Hormozi → giải **1 vấn đề HẸP + CẤP BÁCH** cho prop-firm scalper? (vd "không cháy tài khoản FTMO challenge"). Quá rộng = fail.
- Output: 1 đoạn verdict PASS/FAIL + lý do.
- Done khi: có verdict; nếu FAIL → T1.2.

**T1.2 — (nếu cần) Thu hẹp lead magnet**
- Action: rewrite tiêu đề + scope về 1 outcome đo được. Mẫu: "Checklist 7 bước qua FTMO Challenge $100k không vi phạm daily drawdown".
- Output: file checklist v2.
- Done khi: tiêu đề chứa outcome + con số + đối tượng cụ thể.

---

## PHASE 2 — Wiring capture flow (lõi của B7)

Mục tiêu: chuỗi **X reply → Tele → giao PDF → xin @handle → score → leads.csv** chạy end-to-end, không rơi bước.

**T2.1 — Vẽ flow thật từ code**
- Input: scripts X farm (`t1-reply-cta.py`), bot Tele (@hermes7979_bot handlers), `lead-funnel-cli.py`.
- Action: trace từng bước, đánh dấu bước nào tự động / bước nào thủ công / bước nào THIẾU.
- Output: sơ đồ flow + bảng "bước | trạng thái | file".
- Done khi: mỗi bước trong flow ở trên có 1 dòng trạng thái.

**T2.2 — Bịt lỗ rò (gap fix)**
- Action: với mỗi bước THIẾU/thủ công, đề xuất fix nhỏ nhất (script/handler). Vd: bot tự gửi PDF + prompt xin @handle khi user gõ keyword.
- Output: danh sách task fix + ước lượng, KHÔNG tự sửa file lớn nếu chưa được duyệt.
- Done khi: gap có owner + cách fix; người dùng duyệt trước khi code.

**T2.3 — CTA chuẩn (X safety)**
- Action: soạn 3 mẫu reply CTA: không link trong body, link/keyword ở reply, kèm "Not financial advice".
- Output: 3 mẫu trong `content-os/` hoặc nơi tương đương.
- Done khi: cả 3 qua gate X safety (CLAUDE.md rule #2).

---

## PHASE 3 — Bật Core Four (4 nguồn lead)
> Làm theo thứ tự dễ→khó, mỗi nguồn 1 task, đo riêng.

**T3.1 Post free content** (X farm) — đã có; đảm bảo mỗi post có Hook→Retain→Reward(CTA).
**T3.2 Warm outreach** — telegram-nurture skill (#10): chuỗi DM cho người đã vào Tele.
**T3.3 Cold outreach** — combat_agent: reply + soft DM, KHÔNG spam (anti-ban).
**T3.4 Paid** — Tele-ads: giữ tối thiểu, đo cost/lead để so với organic.
- Done mỗi task khi: nguồn đó tạo ra ≥1 lead có thật ghi được vào CRM.

---

## PHASE 4 — Score & qualify
**T4.1** — Mọi @handle vào → chạy `score @handle` (lead_qualifier 6-signal rubric).
**T4.2** — Lead ≥4/6 → đẩy nurture/sales; <4 → follow-up engine (skill #11).
- Done khi: leads.csv có cột score + trạng thái, không lead nào "mồ côi".

---

## PHASE 5 — Đo & lặp (chạy cuối mỗi ngày M0)
**T5.1** — Cuối ngày: đếm 5 chỉ số ở Mục 1 từ leads.csv → ghi `signal_funnel` journal.
**T5.2** — Tìm 1 nút thắt lớn nhất (post ít reply? reply ít vào Tele? vào Tele ít để handle?) → 1 thử nghiệm cho ngày sau.
- Done khi: có số + 1 quyết định cho ngày kế.

---

## 6. Data artifacts cần có
```
leads.csv         → cột: handle | nguồn | ngày | score | trạng thái  (chỉ lead-funnel-cli.py ghi)
dream-100-x.csv   → dùng chung với traffic-secrets.md
cta-templates.md  → 3 mẫu reply CTA đã qua gate
daily-journal     → 5 KPI/ngày (signal_funnel)
```

## 7. Guardrails (KHÔNG vi phạm)
- Chỉ `lead-funnel-cli.py` ghi CRM — không LLM (CLAUDE.md #3).
- Không bịa win-rate; mọi CTA kèm "Not financial advice" + risk %.
- Không link trong body post X (link ở reply).
- Cold DM: có giá trị trước, không spam → tránh khoá account.

## 8. Định nghĩa HOÀN THÀNH (toàn plan)
B7 coi như done khi: flow capture chạy E2E không thủ công ở khâu lõi + đạt target Mục 1 trong 5 ngày M0 + leads.csv sạch (mọi lead có score).

## 9. Bảng ánh xạ repo (Claude Code điền sau Phase 0.5)
| Khái niệm | Path/lệnh GIẢ ĐỊNH ⚠️ | Path THẬT (điền) |
|-----------|----------------------|------------------|
| Capture CRM | scripts/lead-funnel-cli.py | |
| Lead magnet | lead-magnets/ftmo-...md | |
| Score | lệnh Tele `score @handle` | |
| X reply CTA | scripts/t1-reply-cta.py | |
| Nurture | skill #10 telegram-nurture | |
