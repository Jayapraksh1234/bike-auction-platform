# Assumptions and Trade-offs

1. Auction status is derived from timestamps, avoiding a scheduler for the core state.
2. Starting price is the minimum first bid; subsequent bids must exceed the highest bid by at least the configured increment.
3. Sellers cannot bid on their own motorcycles.
4. PostgreSQL row-level locking serializes bid writes per auction.
5. Currency values are decimal, not floating-point.
6. Only staff users can manage records through Django admin in this first version.
7. The initial frontend uses polling for updates; WebSocket infrastructure is a planned extension, not claimed as complete.
8. Payments, escrow, KYC, notifications, disputes, seller payouts, and image upload are outside the first implementation scope.
9. The public demo and credentials are deployment deliverables that must be created after deployment; none are supplied by this source bundle.
