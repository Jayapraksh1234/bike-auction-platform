# Deployment Guide

## 1. Deployment Overview

The Bike Auction Platform is deployed using the following services:

- **Frontend:** Vercel
- **Backend:** Render
- **Database:** Supabase PostgreSQL
- **Source code:** GitHub

### Live URLs

- Frontend: https://bike-auction-platform-one.vercel.app/
- Backend API: https://bike-auction-platform-9a8p.onrender.com/api/auctions/
- Django Admin: https://bike-auction-platform-9a8p.onrender.com/admin/
- GitHub: https://github.com/Jayapraksh1234/bike-auction-platform

## 2. Frontend Deployment — Vercel

1. Import the GitHub repository into Vercel.
2. Set the project root directory to `frontend`.
3. Configure the build command as `npm run build`.
4. Configure the output directory as `dist`.
5. Set the environment variable:

   `VITE_API_URL=https://bike-auction-platform-9a8p.onrender.com/api`

6. Deploy the application.
7. Verify that the frontend loads and can communicate with the backend API.

## 3. Backend Deployment — Render

1. Connect the GitHub repository to Render.
2. Set the root directory to `backend`.
3. Install dependencies from `requirements.txt`.
4. Configure the ASGI start command:

   `python -m uvicorn config.asgi:application --host 0.0.0.0 --port $PORT`

5. Configure the required environment variables in the Render dashboard.
6. Apply database migrations as part of a successful deployment.
7. Verify the deployment logs and confirm that the service is running.

## 4. Database Configuration — Supabase

1. Create or select a PostgreSQL database in Supabase.
2. Configure the backend database connection using the host, port, username, password, and database name provided by Supabase.
3. Enable the required SSL configuration.
4. Run Django migrations against the configured database.
5. Verify that auction data can be retrieved through the API.

Use the connection mode recommended for the application and its hosting environment. Keep database credentials out of source control.

## 5. Environment Variables and Security

Configure environment variables in the relevant hosting dashboards.

Backend configuration may include:

- `SECRET_KEY`
- `DEBUG`
- `ALLOWED_HOSTS`
- Database connection variables
- `DB_SSLMODE`
- `CORS_ALLOWED_ORIGINS`
- `REDIS_URL`, if required by the deployed application
- Demo administrator variables, if the deployment uses the custom account-creation command

Frontend configuration:

- `VITE_API_URL`

Use strong secrets, restrict allowed hosts and CORS origins, and never commit production credentials or `.env` files to GitHub.

## 6. Deployment Verification

After deployment, verify the following:

1. The frontend URL loads successfully.
2. The backend auction endpoint returns an appropriate response.
3. Login works with a dedicated demo account.
4. Auction details and prices display correctly.
5. Valid bids are accepted according to the application's rules.
6. Invalid or unauthorized bids are rejected.
7. Database connectivity remains stable.
8. Backend logs do not show unresolved errors.

## 7. Operational Considerations

Managed hosting reduces infrastructure maintenance, but service limits, cold starts, database connection limits, and configuration errors can affect availability.

Review deployment logs after releases. Ensure database connectivity and migrations are healthy before considering a deployment ready for evaluation.

## 8. Demo Access

Provide the evaluator with a dedicated demo account through the assignment's designated secure channel. Do not publish passwords, administrator credentials, or production secrets in this repository.