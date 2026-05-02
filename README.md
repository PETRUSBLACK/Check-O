# SmartMall

SmartMall is a modular smart commerce platform with marketplace, logistics, payments, realtime updates, AI, and ML layers.

## Current Scope

The backend foundation is implemented with:
- Django + DRF
- JWT auth + role-based user model
- Modular domain apps
- Swagger/ReDoc API docs
- Jazzmin-enhanced Django admin
- Docker compose setup (Postgres + Redis + backend)

## Quick Start (Local)

1. Copy environment defaults:
   - create `.env` from `.env.example` (or use compose defaults)
2. Start services:
   - `docker compose up --build`
3. API base:
   - `http://localhost:8000/api/`

## Useful URLs

- Admin: `http://localhost:8000/admin/`
- Swagger UI: `http://localhost:8000/api/docs/`
- ReDoc: `http://localhost:8000/api/redoc/`
- OpenAPI schema: `http://localhost:8000/api/schema/`
- Health: `http://localhost:8000/api/health/`

## Local Python Run (without Docker)

From `backend/`:

1. `python -m pip install -r requirements.txt`
2. `python manage.py migrate`
3. `python manage.py runserver`

## Notes

- Business logic is expected in app `services` modules.
- Views should stay thin and call service-layer functions.
- Keep `docs/PROJECT_CONTEXT.md` updated at the end of each milestone.
