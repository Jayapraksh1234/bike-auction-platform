# Architecture and Design Notes

## Components
- React/Vite: user-facing experience, forms, auction listings, bid history.
- Django REST Framework: API boundary, authentication, authorization, input validation.
- PostgreSQL: source of truth for auctions and bids.
- Django admin: staff operations for listings and auction records.
- Redis/Channels dependencies: intended transport for WebSocket updates; event publishing and consumers are not implemented yet.

## Data model
- User: Django's configured user model.
- Motorcycle: seller, descriptive fields, image URL.
- Auction: one-to-one with Motorcycle, start/end timestamps, starting price, minimum increment.
- Bid: auction, bidder, decimal amount, server timestamp.

## Bid transaction
1. Validate request body with a decimal serializer.
2. Start a database transaction.
3. Lock the auction row using `select_for_update()`.
4. Validate time window and seller/bidder separation.
5. Read highest bid and compute the minimum next amount.
6. Insert the bid; commit transaction.
7. Log a structured event.

The lock works as intended on PostgreSQL. SQLite is not a suitable database for validating this concurrency behavior.

## Security
- JWT authentication for bid endpoints.
- Django password hashing and password validators.
- Read-only auction endpoints.
- Serializer-controlled bid fields; clients cannot choose bidder or timestamp.
- API throttling and CORS configuration.
- Production requires secure secrets, HTTPS, email verification, secure token storage, rate limiting review, audit retention, and dependency/security scanning.

## Observability
- Console application logs with bid identifiers.
- Health endpoint.
- Production follow-up: JSON logs, metrics, tracing, error reporting, DB pool monitoring, and alerts for failed bids/latency.

## Known limitations / trade-offs
- No payment or escrow flow.
- No seller self-service listing creation endpoint.
- No real-time WebSocket consumer/event broadcast yet; the frontend polls.
- No image upload pipeline; image URL is a field.
- No scheduler required for basic status because status derives from timestamps; automated closure notifications would require a worker.
- Pagination and richer filtering should be added before large-scale deployment.
