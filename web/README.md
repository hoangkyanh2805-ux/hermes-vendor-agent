# MCM Web — Landing & Dashboard

## Trạng thái hiện tại
- `landing.html` — copy từ hermes/docs/vendor-landing-final.html (20/06/2026)
- `dashboard.html` — copy từ hermes/docs/vendor-dashboard-final.html (20/06/2026)
- `api_server.py` — Python HTTP server port 3003, inject live data từ Google Sheet

## Đang chạy
- `mcm-web.service` → `http://103.97.126.28:3003/`
- `/` hoặc `/dashboard` → dashboard với số liệu thật
- `/landing` → landing page tĩnh
- `/api/stats` → JSON từ Sheet (cache 5 phút)

## TODO — chưa làm (không ưu tiên)

### Dashboard = per-user view, không phải admin
Dashboard hiện tại serve số liệu tổng (admin view).
Về bản chất đây là **dashboard của từng affiliate** — mỗi người đăng nhập thấy data của mình.

Cần build thêm:
- [ ] Auth layer — login bằng Telegram username hoặc token
- [ ] Per-user data filtering — api_server.py lọc Sheet theo `telegram_username`
- [ ] Session management — cookie hoặc JWT đơn giản
- [ ] Route `/dashboard/<username>` → data riêng của affiliate đó
- [ ] Admin view riêng (aggregate toàn bộ affiliates)

### Khác
- [ ] Nginx reverse proxy + domain (thay vì port 3003 thô)
- [ ] Adapt landing page content cho MCM branding (tên, CTA, Telegram link)
- [ ] Firewall: quyết định port 3003 public hay chỉ internal

## Nguồn file gốc
```
hermes/docs/vendor-landing-final.html  (718 KB)
hermes/docs/vendor-dashboard-final.html (732 KB)
```
Bản mới nhất tính đến 20/06/2026. Nếu có update mới hơn bên hermes thì copy lại.
