# MCM Vendor — Status & Plan
_Cập nhật: 2026-06-24_

---

## TRẠNG THÁI HỆ THỐNG (VPS 103.97.126.28)

| Agent | PID | Status | Ghi chú |
|-------|-----|--------|---------|
| Agent1 (Capture) | 144136 | ✅ Running | Restart 13:40, code mới nhất |
| Agent2 (Onboard) | — | ✅ Cron 8AM | Chạy qua crontab, không phải daemon |
| Agent3 (Daily Loop) | 100711 | ✅ Running | Server mode + 3 crons (7AM/2PM/9PM) |
| Agent4 (CRM Sync) | 79717 | ✅ Running | EspoCRM webhook listener |
| Agent5 (Monitor) | — | ✅ Cron 8PM | Daily report + weekly summary |
| Hermes Gateway | 89439 | ✅ Running | Orchestrator chính |

---

## NHỮNG GÌ ĐÃ BUILD (SESSION NÀY)

### Bug fixes từ test thực tế (Antonio @antnio7979)

**Bug 1 — `score_lead()` trả channel="none" khi affiliate chọn TikTok**
- Root cause: kr/* quota 402 → exception → default `channel="none"`
- Fix: Thêm `_parse_score_direct(q1, q2)` — rule-based parser không cần LLM
- Commit: `07050bf`

**Bug 2 — D1 message không gửi khi LLM quota hết**
- Root cause: cả 2 model fail → `generate_content()` trả None → `run_immediate()` return sớm
- Fix: Thêm `D1_FALLBACK` hardcoded string, dùng khi LLM unavailable
- Commit: `54bf4be`

**Bug 3 — Affiliate hỏi sau qualify → nhận "new visitor" form link**
- Root cause: `clear_lead_state()` set stage="done" nhưng poll loop không có `elif stage == "done"`
- Fix: Thêm handler cho stage="done" → gửi guidance message
- Commit: `07050bf`

**Bug 4 — Affiliate state bị mất → nhận form link mãi**
- Root cause: state bị clear thủ công, poll loop không restore từ Sheet
- Fix: Thêm `_affiliate_cache` + `_is_existing_affiliate()` — check Sheet khi `/start` hoặc unknown text → restore stage="done"
- Commit: `510c49b`

---

### Agent3 — LLM Fallback Pattern

3-layer resilience cho cả hệ thống:
```
Layer 1: kr/claude-sonnet-4.5  (primary)
Layer 2: gemini/gemini-2.0-flash (secondary)
Layer 3: hardcoded template     (guarantee delivery)
```

- `llm()`: loop qua `FALLBACK_MODELS` thay vì single model
- `_checklist_fallback()`: 3 tasks X-focused dựa theo days_post + refer_drop
- `_coaching_fallback()`: message dựa theo inactive vs refer_drop
- Channel default sửa từ `"telegram"` → `"x"` (X-first)
- Commits: `1399a05`, `3a66275`

---

### Claude Code Skills (Developer Tools)

3 skills từ [addyosmani/agent-skills](https://github.com/addyosmani/agent-skills) đã install:

| Command | File | Dùng khi |
|---------|------|---------|
| `/spec` | `.claude/skills/spec-driven-development/SKILL.md` | Trước khi build feature mới |
| `/review` | `.claude/skills/code-review-and-quality/SKILL.md` | Sau khi viết code, trước khi deploy |
| `/doubt` | `.claude/skills/doubt-driven-development/SKILL.md` | Stress-test quyết định với Advisory Board |

Advisory Board: Gary Vee · Hormozi · Chris Voss · Dan Kennedy · MrBeast · Brunson · Ali Abdaal

**Note:** Commands load khi restart session Claude Code. Trong session hiện tại dùng trực tiếp qua SKILL.md.

Commit: `919b90e`

---

## VẤN ĐỀ CÒN LẠI (CHƯA FIX)

### P1 — Duplicate rows trong Sheet (QUAN TRỌNG)
- **Vấn đề:** Mỗi lần webhook trigger = 1 row mới. Antonio có 3 rows: AFF-8833 (channel=none), AFF-4030 (Hot/telegram), AFF-0047 (channel=none)
- **Hậu quả:** Agent2 cron đọc sai row → D1-D7 không track đúng → commission sai
- **Fix cần làm:** Trong `agent1.py` hàm `sheets_append()` → check username đã tồn tại chưa → nếu có thì update row cũ thay vì tạo mới

### P2 — Sheet data rác cần clean
- Xóa row AFF-8833 và AFF-0047 (duplicate của Antonio)
- Giữ AFF-4030 (đúng nhất: Hot/fast_track/telegram)
- Cập nhật onboard_day và status cho đúng

### P3 — LLM timeout 60s khi quota hết
- **Vấn đề:** 2 models × 30s timeout = 60s wait trước khi fallback
- **Fix:** Phân biệt HTTP 402/429 (quota) vs timeout/network → skip ngay sang model tiếp theo không chờ timeout

### P4 — GitHub webhook cho Agent5 chưa setup
- SOP checklist item `6.1` còn `[ ]`
- Agent5 đang chỉ có cron, không có GitHub webhook trigger

---

## TRẠNG THÁI 9ROUTER / LLM

- `kr/claude-sonnet-4.5`: **402 Payment Required** — quota hết
- `gemini/gemini-2.0-flash`: **429 Too Many Requests** — rate limited
- **Hệ thống hiện đang chạy 100% bằng hardcoded fallback**
- Cần: nạp thêm 9Router credit HOẶC thêm OpenRouter key vào `.env`

---

## COMMIT HISTORY (SESSION NÀY)

```
510c49b fix: agent1 restore affiliate state on /start or unknown text
3a66275 fix: agent3 clean up dead code from review
1399a05 fix: agent3 LLM fallback chain + hardcoded checklist/coaching fallback
919b90e feat: install 3 claude-code skills from agent-skills repo
54bf4be fix: agent2 D1 hardcoded fallback when LLM quota exhausted
7169e70 fix: agent2 gemini fallback when kr/* hits 402 quota
07050bf fix: agent1 score fallback + post-qualify handler
```

---

## NEXT ACTIONS

1. **[Hiep]** Nạp 9Router credit hoặc add OpenRouter key → LLM hoạt động trở lại
2. **[Hiep]** Clean Sheet: xóa 2 rows rác của Antonio, update AFF-4030 đúng data
3. **[Build khi ready]** P1: Duplicate prevention trong agent1
4. **[Build khi ready]** P3: LLM timeout short-circuit
5. **[Build khi ready]** P4: GitHub webhook cho Agent5
