# Bike Auction Platform

A full-stack web application for listing motorcycles, managing auctions, and placing bids online.

## Live Demo

- **Frontend:** https://bike-auction-platform-one.vercel.app/
- **Backend API:** https://bike-auction-platform-9a8p.onrender.com/api/auctions/
- **GitHub Repository:** https://github.com/Jayapraksh1234/bike-auction-platform

## Tech Stack

- **Frontend:** React, Vite
- **Backend:** Python, Django, Django REST Framework
- **Database:** PostgreSQL
- **Authentication:** JWT
- **Deployment:** Vercel, Render, Supabase
- **Additional Services:** Redis, Django Channels

## Features

- View available motorcycle auctions.
- View motorcycle and auction details.
- Place bids through the REST API.
- View bid history and current auction prices.
- Validate bids on the backend.
- Manage motorcycles and auctions through Django Admin.
- Authenticate API requests using JWT.

## Project Structure

```text
bike-auction-platform/
├── backend/
│   ├── auctions/
│   ├── config/
│   ├── manage.py
│   └── requirements.txt
└── frontend/
    ├── src/
    ├── package.json
    └── vite.config.js
```

## Run Locally

### 1. Backend

Open a terminal:

```bash
cd backend
python -m venv .venv
```

Activate the virtual environment on Windows:

```powershell
.venv\Scripts\Activate.ps1
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Configure the required environment variables using `backend/.env.example`. Set your own secret key and database credentials.

Apply migrations and start Django:

```bash
python manage.py migrate
python manage.py runserver
```

The backend runs at `http://127.0.0.1:8000/`.

### 2. Frontend

Open another terminal:

```bash
cd frontend
npm install
```

Create a frontend `.env` file using the provided example and set:

```env
VITE_API_URL=http://127.0.0.1:8000/api
```

Start the development server:

```bash
npm run dev
```

Open the local URL printed by Vite, usually `http://localhost:5173/`.

## API

The backend exposes REST endpoints for auction data and bidding.

- `GET /api/auctions/` — list auctions.
- `GET /api/auctions/{id}/` — retrieve auction details.
- `/api/auctions/{id}/bid/` — bid endpoint; supports authenticated `POST` requests.

Authentication and bid validation are handled by the backend.

## Deployment

- Frontend hosted on Vercel.
- Django API hosted on Render.
- PostgreSQL database hosted on Supabase.

Configure production environment variables through the hosting dashboards. Do not commit passwords, secret keys, or database credentials to GitHub.

## Testing

Run backend tests:

```bash
cd backend
python manage.py test
```

Build the frontend:

```bash
cd frontend
npm run build
```

## Security Notes

- Keep `DEBUG=False` in production.
- Use a strong secret key stored in environment variables.
- Configure allowed hosts and CORS origins for your deployed domains.
- Never commit `.env` files or production credentials.

## License

Add a license if you intend to distribute this project under specific reuse terms.