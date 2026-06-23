# Modules — MCM Vendor Standalone Code

**Status: CHƯA TÍCH HỢP — Standalone reference only**

Các module Python này copy từ `hermes/scripts/vendor-layer/`. Chưa được import vào agent1-5.  
Đây là reference để integrate về sau khi cần nâng cấp.

---

## Files

### `rank_engine.py`
**Adapted từ:** `hermes/scripts/vendor-layer/rank_engine.py`  
**Mô tả:** Pure state machine tính toán rank affiliate  
**Logic:**
- `new` → `active`: có first_post_date
- `active` → `top`: 30d joins ≥ 20
- `top` → `senior`: 30d joins ≥ 50 × 3 tháng + đã mentor ≥1
- `any` → `cold`: last_activity > 14d
- Demote: `top` → `active` nếu 30d joins < 10

**Dependencies:** stdlib only (json, datetime) — không cần install thêm

**Integrate vào:** Agent 4 (sau event Opportunity.create) hoặc Agent 5 (weekly rank computation)

---

### `account_health.py`
**Adapted từ:** `hermes/scripts/vendor-layer/account-health.py`  
**Mô tả:** Health + risk scoring cho affiliate accounts  
**Logic:**
- Tier-aware risk scoring (T1/T2/T3)
- Flag accounts theo suspension risk
- Cluster health summary

**Dependencies:**
```
json, datetime, pathlib  ← stdlib, không cần install
```

**Chú ý:** File gốc dùng hardcoded paths `/root/hermes-data/...`  
→ Khi integrate vào MCM: thay bằng Google Sheet hoặc local JSON

**Integrate vào:** Agent 5 (monthly health audit affiliates) hoặc Agent 4 (churn detection)

---

## Cách integrate (khi sẵn sàng)

### rank_engine vào Agent 4:
```python
# Trong agent4.py, sau event Opportunity.create:
from modules.rank_engine import compute_rank
new_rank = compute_rank(affiliate_data)
sheets_update_rank(affiliate_id, new_rank)
```

### account_health vào Agent 5:
```python
# Trong agent5.py, weekly report:
from modules.account_health import get_health_summary
health = get_health_summary(affiliates_list)
# Include trong daily report
```

---

## TODO (future)

- [ ] Adapt rank_engine để đọc từ Google Sheet thay vì vendor-registry.json
- [ ] Adapt account_health để dùng Sheet data thay vì /root/hermes-data/
- [ ] Test với dữ liệu Sheet thật trước khi integrate vào agents
- [ ] Import vào agent4.py sau khi test OK

**Không integrate trước khi test đầy đủ — agents đang live.**
