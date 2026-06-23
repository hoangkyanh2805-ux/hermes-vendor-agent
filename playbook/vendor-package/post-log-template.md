# POST LOG - TEMPLATE

Hermes XAUUSD Vendor Affiliate Network  
Danh cho: vendor gui link bai X vao Telegram sau khi dang

## Format Vendor Gui

Gui mot dong:

```text
[URL bai X] | @handle | [HH:MM] | source: [tag cua ban]
```

Vi du:

```text
https://x.com/yourhandle/status/123 | @yourhandle | 14:32 | source: x_gulf_v_tuan
```

Topic: `Post Log` neu da tao. Neu chua co, gui trong `General` hoac topic admin chi dinh.

## Admin Validate

Truoc khi log click:

```text
[ ] URL mo duoc.
[ ] Source tag khop vendor.
[ ] Co source attribution neu dung signal/source cu the.
[ ] Co "Not financial advice" neu la signal post.
[ ] Telegram CTA khong nam trong main post body.
[ ] Khong copy nguyen cau tu source.
[ ] Khong fake win-rate, PnL, member count, profit guarantee.
```

## Admin Log Vao Funnel DB

Click event, khi vendor da dang bai hop le:

```bash
python3 /root/hermes-bin/vendor-layer/funnel-db.py log --source x_gulf_v_tuan
```

Raw join event, khi co nguoi join qua link do:

```bash
python3 /root/hermes-bin/vendor-layer/funnel-db.py log --source x_gulf_v_tuan --join --telegram-user @leadhandle
```

Valid join event, chi sau khi admin review:

```bash
python3 /root/hermes-bin/vendor-layer/funnel-db.py log --source x_gulf_v_tuan --valid-join --vendor tuan --telegram-user @leadhandle
```

Khong auto-confirm `valid_join`.

## Valid Join Criteria

Admin chi confirm `valid_join` khi:

```text
[ ] Join qua link cua vendor/source.
[ ] Account Telegram khong ro spam/bot.
[ ] Khong duplicate/self-referral.
[ ] Con trong group sau review window, mac dinh 24h.
```

Reject: bot account, fake traffic, duplicate join, self-referral, no-avatar/no-username spam, leave ngay.

## Weekly Report

Thu Hai:

```bash
python3 /root/hermes-bin/vendor-layer/funnel-db.py report --weekly
python3 /root/hermes-bin/vendor-layer/funnel-db.py payment --week
```

Payment estimate:

```text
valid joins x 10,000 VND
```

Admin/founder confirm truoc khi payout. Agent/admin khong confirm tranh chap
payout trong public group.

## Source Tag Registry

| Vendor | Tag | Cluster | Link name | Status |
|---|---|---|---|---|
| [ten] | x_gulf_v_[ten] | gulf | v_[ten]_gulf | active |

Tag format:

```text
x_[cluster]_v_[vendor_ascii]
```

Clusters:

```text
gulf | europe | africa | south_asia | americas | legacy
```

