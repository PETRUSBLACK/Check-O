# SmartMall Project Context

Last updated: 2026-05-06 (vendor verification onboarding)

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
- `/api/health/`
- `/api/auth/register/` — optional `vendor_business` payload for vendors (creates draft business profile)
- `/api/auth/token/`, `/api/auth/token/refresh/`, `/api/auth/me/`
- `/api/users/`
- `/api/businesses/` — see vendor verification actions below
- `/api/products/` — vendors blocked from creating products until business is **approved** (platform admins can override)
- `/api/orders/`, `/api/payments/`, `/api/shipments/`
- `/api/notifications/`, `/api/subscriptions/`, `/api/promotions/`, `/api/analytics-events/`
- Docs: `/api/schema/`, `/api/docs/`, `/api/redoc/`

## Vendor verification (onboarding)
- New businesses default to **`draft`** until the vendor completes profile fields and submits for review.
- **Required before submit:** `legal_name`, `registration_number`, `address` (plus display `name` / `slug`).
- **Flow:** `draft` → **POST** `submit-for-review` → `pending` → admin **approve** / **reject** → `approved` / `rejected` (rejected vendors can edit and resubmit).
- **Endpoints:**
  - `POST /api/businesses/{id}/submit-for-review/`
  - `POST /api/businesses/{id}/approve/` (staff or `role=admin`)
  - `POST /api/businesses/{id}/reject/` body `{ "reason": "..." }` (staff or `role=admin`)
- **Products:** creation requires `business.status == approved` for vendors; staff/platform admin may bypass for support.

## Important Implemented Service Flows
- Order creation and stock deduction in `apps.orders.services.order_service`
- Payment initiation/confirmation in `apps.payments.services.gateway`
- Shipment status updates + websocket push in `apps.delivery.services.shipment_service`
- Business registration / submit / approve / reject in `apps.businesses.services.registration`

## Verification Status
- Migrations: `businesses.0003_vendor_verification_fields` applied
- Last run: `python manage.py check` — no issues
- Swagger/OpenAPI + ReDoc enabled; health at `/api/health/`

## Phase Status
- Phase 1 (Foundation & Architecture): complete
- Phase 2 (Identity & Access): in progress — vendor onboarding verification implemented

## Known Gaps / Next Priorities
1. Optional email/phone OTP verification for customers and vendors (separate from business approval)
2. Payment/logistics provider adapters (Flutterwave/Paystack/Stripe; GIG/Kwik/DHL)
3. Automated tests (API + state transitions + onboarding)
4. React Native app scaffold + first flows
5. CI (lint, test, migrate check)

## Resume Prompt (for future sessions)
When resuming work, read this file first, then:
1. Run `python manage.py check` in `backend/`
2. Pick the next item under Known Gaps / Next Priorities
3. Keep business logic in services and thin views
