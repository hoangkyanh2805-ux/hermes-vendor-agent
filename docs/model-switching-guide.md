# Hermes Model Switching Guide

## Kiến trúc Model

```
Telegram → Hermes Gateway → 9Router (port 20128) → Kiro API → LLM
```

**9Router** là local proxy chạy trên VPS port 20128. Hermes gateway route tất cả LLM calls qua đây.

Config trong `~/.hermes/.env`:
```
OPENAI_BASE_URL=http://127.0.0.1:20128/v1
OPENROUTER_BASE_URL=http://127.0.0.1:20128/v1
```

Config model trong `~/.hermes/config.yaml`:
```yaml
model:
  default: kr/claude-sonnet-4.5
  provider: openrouter
  base_url: http://127.0.0.1:20128/v1
```

---

## Models có sẵn trong 9Router

Chạy lệnh để xem danh sách đầy đủ:
```bash
curl -s http://127.0.0.1:20128/v1/models | python3 -c "import sys,json; [print(m['id']) for m in json.load(sys.stdin).get('data',[])]"
```

### Nhóm kiro (kr/) — dùng chung 1 quota pool
| Model | Ghi chú |
|-------|---------|
| `kr/claude-sonnet-4.5` | Default, mạnh nhất |
| `kr/claude-sonnet-4` | Fallback |
| `kr/claude-haiku-4.5` | Nhanh, rẻ |
| `kr/claude-sonnet-4.5-agentic` | Tối ưu tool use |
| `kr/deepseek-3.2` | Thay thế khi claude hết |
| `kr/auto` | 9Router tự chọn |

> ⚠️ Tất cả `kr/*` models dùng chung **1 monthly quota**. Khi 1 cái hết → tất cả hết.

### Nhóm Gemini — quota riêng
| Model | Ghi chú |
|-------|---------|
| `gemini/gemini-3.1-pro-preview` | Mạnh nhất |
| `gemini/gemini-3.1-flash-lite-preview` | Nhanh, nhẹ |
| `gemini/gemini-3-flash-preview` | Ổn định |
| `gemini/gemma-4-31b-it` | Open source |

---

## Cách đổi model

### Qua Telegram (nhanh nhất)
```
/model kr/claude-haiku-4.5
```

### Qua SSH (permanent)
```bash
ssh -p 2018 root@103.97.126.28
sed -i 's|  default: .*|  default: MODEL_ID_MỚI|' ~/.hermes/config.yaml
systemctl --user restart hermes-gateway
```

Rồi trong Telegram gửi `/new` để session mới pick up model mới.

---

## Xử lý khi gặp lỗi provider

### Bước 1 — Xem log lỗi thật sự
```bash
ssh -p 2018 root@103.97.126.28
tail -20 ~/.hermes/logs/errors.log
```

### Bước 2 — Đọc loại lỗi

| Lỗi trong log | Nguyên nhân | Fix |
|---------------|-------------|-----|
| `HTTP 402: MONTHLY_REQUEST_COUNT` | Hết quota tháng | Đổi sang model khác / đợi reset |
| `HTTP 403` | Không có quyền dùng model | Đổi model |
| `HTTP 401: Missing Authentication header` | Sai provider config | Kiểm tra `.env` và `config.yaml` |
| `No active credentials for provider` | Key không hợp lệ với endpoint | Không bypass 9Router |

### Bước 3 — Fix theo tình huống

**Khi `kr/*` hết quota (MONTHLY_REQUEST_COUNT):**
```bash
# Thử Gemini Flash thay thế
sed -i 's|  default: .*|  default: gemini/gemini-3.1-flash-lite-preview|' ~/.hermes/config.yaml
systemctl --user restart hermes-gateway
```

**Khi cần reset về default:**
```bash
sed -i 's|  default: .*|  default: kr/claude-sonnet-4.5|' ~/.hermes/config.yaml
systemctl --user restart hermes-gateway
```

---

## QUAN TRỌNG — Không bypass 9Router

Hermes config dùng **Kiro API key** (`sk-390da7...`), KHÔNG phải OpenRouter key thật.
Key này chỉ hoạt động qua 9Router proxy.

Nếu comment out `OPENROUTER_BASE_URL` hoặc `OPENAI_BASE_URL` → Hermes gọi thẳng OpenRouter → 401 Auth error.

**Không bao giờ xóa 2 dòng này khỏi `~/.hermes/.env`:**
```
OPENAI_BASE_URL=http://127.0.0.1:20128/v1
OPENROUTER_BASE_URL=http://127.0.0.1:20128/v1
```

---

## Quota reset

- Kiro monthly quota reset: **đầu tháng** (ngày 1 hàng tháng)
- Sau reset: đổi lại `kr/claude-sonnet-4.5` là model mạnh nhất
