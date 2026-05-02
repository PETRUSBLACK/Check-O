# SmartMall Project Context

Last updated: 2026-05-02 (Phase 1 closed, verification refreshed)

## Project Goal
Build a scalable smart commerce ecosystem combining:
- Multi-vendor marketplace
- Payments
- Delivery/logistics
- Realtime updates
- AI assistant layer
- ML recommendation/forecasting layer

## Architecture Direction
- Backend: Django + DRF + Channels (domain-driven app separation)
- Business logic: service modules, not views
- Mobile: React Native with feature-based structure
- Integrations: adapter-based payment/logistics/notification providers
- AI: calls backend tools/services (no duplicated domain logic)
- ML: training + serving API layer

## Current Repository State
- Backend foundation is scaffolded in `backend/`
- Docker orchestration exists in `docker-compose.yml`
- Root folders exist for `ai/`, `ml/`, `mobile/`, `integrations/`, `realtime/`, `docs/`

## Implemented Backend Apps
- `apps.users` (custom email-based user + role)
- `apps.businesses`
- `apps.products`
- `apps.orders`
- `apps.payments`
- `apps.delivery`
- `apps.notifications`
- `apps.subscriptions`
- `apps.ads`
- `apps.analytics`

## Core Shared Layer
- `core.models` (timestamp/uuid base models)
- `core.permissions`
- `core.middleware` (request ID)
- `core.exceptions` (DRF exception handler hook)

## API Router
Configured in `backend/config/api_urls.py`:
- `/api/users/`
- `/api/businesses/`
- `/api/products/`
- `/api/orders/`
- `/api/payments/`
- `/api/shipments/`
- `/api/notifications/`
- `/api/subscriptions/`
- `/api/promotions/`
- `/api/analytics-events/`

## Important Implemented Service Flows
- Order creation and stock deduction in `apps.orders.services.order_service`
- Payment initiation/confirmation in `apps.payments.services.gateway`
- Shipment status updates + websocket push in `apps.delivery.services.shipment_service`

## Verification Status
Previously completed in this workspace:
- Installed backend dependencies
- Generated initial migrations
- Applied migrations
- `python manage.py check` passed without issues
- All migrations currently applied (`python manage.py showmigrations`)
- Swagger/OpenAPI + ReDoc enabled and configured
- Health endpoint added (`/api/health/`)
- Re-ran backend verification successfully:
  - `python manage.py check`
  - `python manage.py spectacular --file schema.yml --validate`
  - `python manage.py showmigrations`
- OpenAPI schema file generated at `backend/schema.yml`

Note: Some later terminal checks were interrupted by the IDE/session, but the successful verification run had already completed earlier.

## Phase Status
- Phase 1 (Foundation & Architecture): complete
- Phase 2 (Identity & Access): started

## Known Gaps / Next Priorities (Phase 2+)
1. Tighten order/payment/shipment state machines and permission matrix
2. Add provider adapters (Flutterwave/Paystack/Stripe; GIG/Kwik/DHL)
3. Add tests (unit + API + integration)
4. Start React Native app scaffold and wire first customer flow
5. Add CI and lint/format/test automation

## Recent Updates
- Added auth endpoints:
  - `/api/auth/register/`
  - `/api/auth/token/`
  - `/api/auth/token/refresh/`
  - `/api/auth/me/`
- Added API docs:
  - Swagger UI: `/api/docs/`
  - ReDoc: `/api/redoc/`
  - OpenAPI schema: `/api/schema/`
- Added modern Django admin theming with `jazzmin`.
- Added `README.md` quick-start and service URL references.
- Hardened viewsets for schema generation compatibility (`swagger_fake_view` handling + explicit `queryset` on key viewsets).

## Resume Prompt (for future sessions)
When resuming work, read this file first, then:
1. Confirm backend still passes `python manage.py check`
2. Implement next priority in "Known Gaps / Next Priorities"
3. Keep business logic in service layer and maintain modular app boundaries
