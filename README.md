# Trading Journal API (Django + DRF)

This Django REST API provides CRUD endpoints to manage trades, assets, and tags for a quant-style trading journal.

## Quickstart

```bash
# 1) Copy env
cp .env.example .env

# 2) Start services
docker compose up -d --build

# 3) Run migrations
docker compose exec web python manage.py migrate --noinput

# 4) (Optional) Create admin user
docker compose exec web python manage.py createsuperuser

# 5) (Optional) Import legacy data from a JSON file
docker compose exec web python manage.py import_legacy /data/legacy.json
```

Open:
- API root: http://127.0.0.1:8000/api/v1/
- Admin:    http://127.0.0.1:8000/admin/

## Endpoints (CRUD only)
- `GET/POST /api/v1/tags/` ; `GET/PATCH/DELETE /api/v1/tags/{id}/`
- `GET/POST /api/v1/trades/` ; `GET/PATCH/DELETE /api/v1/trades/{id}/`

> Filters are not included yet per your request. (When ready, we'll add query params like `?symbol=BTCUSDT&from=2025-10-01&to=2025-10-13&side=BUY` to narrow results.)

## Notes
- Uses default `auth.User`. A `Profile` model stores timezone/bio.
- `Trade.tags` is a many‑to‑many relationship. (If you want “one tag per trade”, enforce it later in serializer logic.)
- Time is stored as UTC (`trade_time` is `DateTimeField`).

Generated: 2025-10-13T20:55:23.095796Z
