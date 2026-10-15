# Assumptions and Trade-offs

## 1. Assumptions

1. Users must authenticate before performing protected actions such as placing bids.
2. Each auction has a starting price, current price, minimum bid increment, and defined start and end times.
3. The backend is the source of truth for bid validation and auction updates.
4. A bid must satisfy the auction's bidding rules before it can be accepted.
5. The application uses PostgreSQL for persistent storage.
6. The frontend and backend are deployed separately and communicate through REST APIs.

## 2. Engineering Decisions and Trade-offs

### Frontend and Backend Separation

**Decision:** Use React for the frontend and Django REST Framework for backend APIs.

**Benefit:** The frontend and backend can be developed, tested, and deployed independently.

**Trade-off:** Separate deployments require additional configuration for API URLs, CORS, and environment variables.

### PostgreSQL Database

**Decision:** Use PostgreSQL for application data.

**Benefit:** Relational data integrity and transaction support are useful for managing auctions and bids.

**Trade-off:** Database hosting and connection management add operational complexity.

### JWT Authentication

**Decision:** Use token-based authentication for protected API requests.

**Benefit:** The API can authenticate requests without relying on a traditional server-side session for every user interaction.

**Trade-off:** Token storage, expiration, refresh behavior, and secure transmission must be handled carefully.

### Server-side Bid Validation

**Decision:** Validate bid amounts in the backend rather than relying only on frontend checks.

**Benefit:** Users cannot bypass the core bidding rules simply by modifying the browser interface.

**Trade-off:** Every bid requires a backend request, and the frontend must handle validation errors.

### Concurrent Bid Handling

**Decision:** Process bids inside a database transaction using Django's `transaction.atomic()` and lock the relevant auction row using `select_for_update()`.

**Implementation:** The backend retrieves the auction row with a row lock, checks the latest accepted bid, validates the submitted amount against the minimum permitted bid, and creates the bid within the transaction.

**Benefit:** On PostgreSQL, this approach serializes competing bid attempts for the same auction and helps prevent stale bids from being accepted based on outdated auction state.

**Trade-off:** Row locking can increase contention when multiple users bid on the same auction. Its behavior depends on database support and transaction configuration, so concurrency should be tested against the production database as well as locally.

### Cloud Deployment

**Decision:** Use Vercel for the frontend, Render for the backend, and Supabase for PostgreSQL.

**Benefit:** Managed hosting reduces the amount of infrastructure that must be maintained manually.

**Trade-off:** Free-tier limitations, cold starts, database connection limits, and separate service configurations can affect reliability.

## 3. Limitations

Document the limitations that apply to the current implementation, such as:

- Hosting limits or occasional backend cold starts.
- Any remaining production database connection issues.
- Features that have not yet been implemented or tested.
- The extent of automated test coverage.

## 4. Potential Improvements

- Add broader automated integration and end-to-end tests.
- Perform load testing for concurrent bidding.
- Improve logging, monitoring, and error reporting.
- Review database connection pooling and production resource limits.
- Improve auction lifecycle management and user-facing error messages.

## 5. Conclusion

The implementation prioritizes a clear separation of responsibilities, backend enforcement of bidding rules, relational data storage, and straightforward cloud deployment. Future improvements should focus on production reliability, comprehensive testing, and robust concurrent bid processing.