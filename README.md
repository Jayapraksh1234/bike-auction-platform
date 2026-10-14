# Bike Auction Platform

A full-stack starter implementation for a used-motorcycle auction platform using Django REST Framework, PostgreSQL, React, and optional Django Channels/Redis for real-time updates.

## Features
- JWT registration/login
- Motorcycle listings and auction detail endpoints
- Auction lifecycle status (`scheduled`, `live`, `ended`)
- Server-side bid validation and transaction/row locking
- Bid history
- Django admin
- React UI for listings, login, auction detail, and bidding
- Basic backend tests
- Environment-based configuration

## Requirements
- Python 3.11+
- Node.js 20+
- PostgreSQL 15+
- Optional: Redis 7+ for WebSocket events

## 1. Backend setup
```bash
cd backend
python -m venv .venv
# Windows:
.venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate
pip install -r requirements.txt
copy .env.example .env
# macOS/Linux: cp .env.example .env
```
Create a PostgreSQL database and user, then update `backend/.env`.
```bash
python manage.py makemigrations auctions
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```
API: `http://127.0.0.1:8000/api/`
Admin: `http://127.0.0.1:8000/admin/`

## 2. Frontend setup
```bash
cd frontend
npm install
cp .env.example .env
npm run dev
```
Open the URL printed by Vite, normally `http://localhost:5173`.

## API endpoints
- `POST /api/auth/register/`
- `POST /api/auth/token/`
- `POST /api/auth/token/refresh/`
- `GET /api/auctions/`
- `GET /api/auctions/{id}/`
- `GET /api/auctions/{id}/bids/`
- `POST /api/auctions/{id}/bid/` (authenticated)
- `GET /api/health/`

Auction listing and detail responses include calculated status. Bids are only accepted while the auction is live, before the end time, and when the amount meets the current minimum.

## Auction rules and assumptions
1. An auction has a scheduled start and end time; status is derived from the clock, so no scheduler is required for basic correctness.
2. The first bid must be at least the starting price. Later bids must be at least current highest bid + minimum increment.
3. A user cannot bid on their own listing.
4. Bid amounts use PostgreSQL `DecimalField` and JSON decimal strings to avoid floating-point currency errors.
5. This starter does not implement payments, escrow, shipping, identity verification, email verification, or seller payouts.
6. A Django staff user can manage motorcycles and auctions through Django admin.
7. JWT tokens are stored in browser memory in this starter. A production deployment should consider secure HttpOnly cookies, CSRF protections, rate limits, email verification, and stronger account recovery.

## Real-time updates
REST bidding works without Redis. The `channels` and `channels-redis` dependencies and ASGI setup are included as an integration point, but the current UI refreshes auction data by polling. This avoids claiming WebSocket broadcasting is complete before a channel consumer and event publisher have been implemented.

## Testing
Run:
```bash
cd backend
python manage.py test
```
Tests are included for auction status and bid validation. They have not been executed as part of file generation. Run them in your environment and record the actual result.

## Production checklist
- Set `DEBUG=False`, strong `SECRET_KEY`, allowed hosts and CORS origins.
- Use managed PostgreSQL with backups and TLS.
- Configure Redis and implement authenticated Channels consumers/event publishing before enabling WebSocket UI.
- Add API throttling, audit logs, structured logs, error monitoring, health checks, and metrics.
- Run migrations as a release step; serve React via a static host/CDN and Django via an ASGI/WSGI platform.
- Add CI, dependency scanning, image upload validation, pagination, email verification, and security review.
- Deploy, verify the public URL, and create test credentials before submitting. No deployment is performed by this project generator.
