# Funnel Tracking v2 — 100-Account Architecture

> Cho: Team Tuấn + Founder | Cập nhật: 2026-06-08
> Mục tiêu: Theo dõi X → Telegram conversion trên 5 geo cluster

---

## Kiến Trúc

```
100 X Accounts → 5 Geo Clusters → 10 T1 Links + 5 T2 Pool Links → @azzamgoldpro
                                         │
                                    Payment: 10,000 VND / valid join
```

| Cluster | Accounts | T1 Links | T2 Pool |
|---------|----------|----------|---------|
| **Gulf** | 20 | 3 (signal, risk, smc) | x_gulf_t2_pool |
| **Europe** | 25 | 4 (signal, risk, smc, prop_firm) | x_europe_t2_pool |
| **Africa** | 20 | 2 (signal, prop_firm) | x_africa_t2_pool |
| **South Asia** | 15 | 1 (signal) | x_pakistan_t2_pool |
| **Americas** | 20 | 0 (T2 only) | x_americas_t2_pool |
| **Legacy** | 4 | 4 (founder, risk, smc, macro) | — |

---

## Setup — 15 Links

### 10 T1 Links (mỗi link = 1 account cụ thể, tracking chính xác)

| # | Source Tag | Cluster | Persona |
|---|-----------|---------|---------|
| 1 | x_gulf_t1_01 | Gulf | signal_proof |
| 2 | x_gulf_t1_02 | Gulf | risk |
| 3 | x_gulf_t1_03 | Gulf | smc |
| 4 | x_europe_t1_01 | Europe | signal_proof |
| 5 | x_europe_t1_02 | Europe | risk |
| 6 | x_europe_t1_03 | Europe | smc |
| 7 | x_europe_t1_04 | Europe | prop_firm |
| 8 | x_africa_t1_01 | Africa | signal_proof |
| 9 | x_africa_t1_02 | Africa | prop_firm |
| 10 | x_pakistan_t1_01 | S.Asia | signal_proof |

### 5 T2 Pool Links (mỗi cluster 1 link chung cho các account còn lại)

| # | Source Tag | Cluster |
|---|-----------|---------|
| 11 | x_gulf_t2_pool | Gulf |
| 12 | x_europe_t2_pool | Europe |
| 13 | x_africa_t2_pool | Africa |
| 14 | x_pakistan_t2_pool | South Asia |
| 15 | x_americas_t2_pool | Americas |

---

## Cluster Dashboard — Hàng Tuần

| Tuần | Gulf | Europe | Africa | S.Asia | Americas | Legacy | TỔNG |
|------|------|--------|--------|--------|----------|--------|------|
| W1 | | | | | | | |
| W2 | | | | | | | |

---

## Payment Report — Thứ 2 Hàng Tuần

| Cluster | Joins | Rate | Payment |
|---------|-------|------|---------|
| Gulf | | 10K | VND |
| Europe | | 10K | VND |
| Africa | | 10K | VND |
| South Asia | | 10K | VND |
| Americas | | 10K | VND |
| Legacy | | 10K | VND |
| **TOTAL** | | | **VND** |

---

## Lệnh VPS

```bash
# Cluster summary + payment
python3 /root/hermes-bin/vendor-layer/funnel-db.py clusters

# Payment report
python3 /root/hermes-bin/vendor-layer/funnel-db.py payment --week
python3 /root/hermes-bin/vendor-layer/funnel-db.py payment --month

# Log join
python3 /root/hermes-bin/vendor-layer/funnel-db.py log --source x_gulf_t1_01 --join

# Log verified payable join
python3 /root/hermes-bin/vendor-layer/funnel-db.py log --source x_gulf_t1_01 --valid-join --vendor tuan --telegram-user @lead1
```

## Valid Join Rule

`join` = raw join event, useful for fast operational tracking.

`valid_join` = verified payable join. Weekly payment uses `valid_join` when
available. If a period has no `valid_join` data yet, the tracker falls back to
raw `join` and labels the payment basis as unverified legacy data.

Never confirm payout inside the vendor group unless the weekly tracker report
has been checked by founder/admin.
