# SOUL Files — MCM Vendor Agent Character Config

## SOUL là gì?

SOUL = system prompt layer định nghĩa **tính cách, giọng điệu, và hard rules** cho từng AI agent.

SOUL KHÔNG phải code. SOUL là "linh hồn" được inject vào LLM prompt trước khi agent làm việc.

```
[SOUL file] → inject vào system prompt → LLM có tính cách cụ thể → output nhất quán
```

## Cách dùng

Khi dùng Claude Code hoặc gọi API, paste nội dung SOUL file vào system prompt:

```python
# Ví dụ inject agent1_SOUL.md
with open("souls/agent1_SOUL.md") as f:
    soul = f.read()

messages = [
    {"role": "system", "content": soul},
    {"role": "user", "content": "Score affiliate mới: ..."}
]
```

Hoặc trong Hermes skill yaml:
```yaml
system_prompt: |
  {{ include 'souls/agent1_SOUL.md' }}
```

## Mapping: SOUL → MCM Agent

| File | Agent | Adapted từ | Mô tả |
|------|-------|-----------|-------|
| `agent1_SOUL.md` | Agent 1 — Capture | vendor_qualifier_SOUL.md | Score Hot/Warm/Cold, fast_track/nurture |
| `agent2_SOUL.md` | Agent 2 — Onboard | vendor_boss_SOUL.md | D1-D7 orchestration, coaching daily |
| `agent3_SOUL.md` | Agent 3 — Daily Loop | x_personal_brand_SOUL.md | Content Telegram, checklist, coaching |
| `agent4_SOUL.md` | Agent 4 — CRM Sync | lead_curator_SOUL.md | EspoCRM events, commission, tracking |
| `agent5_SOUL.md` | Agent 5 — Monitor | vendor_reporter_SOUL.md | Report, rank board, PM dashboard |

## Quy tắc khi edit SOUL

- KHÔNG xóa hard boundaries — đây là safety rails
- KHÔNG thay giọng điệu Gấu Trúc 🐼 nếu chưa có lý do
- Mỗi thay đổi → ghi version + ngày ở đầu file
- Test với 3 prompt thật trước khi deploy lên VPS

## Ghi chú adapt từ hermes

- Xóa: path VPS (`/root/hermes-data/...`), blackboard scripts, funnel-db.py
- Giữ: scoring rubric, tone, hard rules, KPI targets
- Thêm: MCM Google Sheet schema, MCM Telegram bot context
