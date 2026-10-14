# Deployment guide (not yet deployed)

This repository has not been deployed and has no public demo credentials yet.

## Suggested deployment topology
- React: static hosting (for example, a CDN-backed static host).
- Django: an ASGI-capable application host.
- PostgreSQL: managed PostgreSQL with automated backups.
- Redis: managed Redis for Channels when WebSockets are implemented.
- HTTPS: enabled for frontend and API.

## Release checklist
1. Provision PostgreSQL and Redis.
2. Set `SECRET_KEY`, `DEBUG=False`, `ALLOWED_HOSTS`, database variables, `CORS_ALLOWED_ORIGINS`, and `REDIS_URL`.
3. Install backend dependencies and run `python manage.py migrate`.
4. Create a staff user using `python manage.py createsuperuser`.
5. Build frontend with `npm run build`; set `VITE_API_URL` to the public API base URL.
6. Configure static hosting and API routing.
7. Verify `/api/health/`, token acquisition, auction listing, and bid rejection/acceptance.
8. Run backend tests against PostgreSQL.
9. Add monitoring, backup restore testing, and deployment rollback instructions.
10. Create a dedicated demo user with a temporary password and include it only after the deployment is verified.
