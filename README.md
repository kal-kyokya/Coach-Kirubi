# Coach Kirubi / Keruvim Performance Web App

Production-minded monorepo for selling athletic training programs online.

## Stack
- **Frontend:** React + Vite
- **Backend:** Django + Django REST Framework
- **Payments:** M-Pesa (Daraja), with mock mode for local development

## Repository Structure
- `backend/` Django API, dommain, admin management, payment integration
- `frontend/` React storefront for browsing and purchasing programs
- `IMPLEMENTATION_PLAN.md` incremental delivery plan and architecture direction

## Features in this version
### Customer-facing
- Home page with editable hero content
- Program catalog listing published programs
- Program detail page with checkout form
- Checkout initiation via M-Pesa STK push (Daraja wrapper)
- Post-checkout status page to check payment/access state

## Admin-facing
- Manage programs in Django admin (publish/unpublish, pricing, metadata)
- Manage orders and payment events in Django admin
- Manage homepage content in Django admin

### Payment reliability
- Server-side callback endpoint for payment verification
- Idempotent callback handling for already-paid orders
- Payment event logging for initiate/callback observability

## Quick Start
## 1) Backend
```bash
python -m venv .keruvim_venv
source .keruvim_venv/bin/activate
pip install django
django-admin --version
django-admin startproject backend
cd backend
python manage.py startapp <app_name>
pip install -r requirements.txt
cp .env.sample .env
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

API runs on `http:localhost:8000`.

## 2) Frontend
```bash
cd frontend
npm install
cp .env.sample .env
npm run dev
```

Frontend runs on `http://localhost:5173`.

## Environment Variables
### Backend (`backend/.env`)
- `DJANGO_SECRET_KEY`
- `DJANGO_DEBUG`
- `DJANGO_ALLOWED_HOSTS`
- `CORS_ALLOWED_ORIGINS`
- `MPESA_MOCK_MODE` (`true` for local)
- `MPESA_ENVIRONMENT` (`sandbox` or `production`)
- `MPESA_CONSUMER_KEY`
- `MPESA_CONSUMER_SECRET`
- `MPESA_SHORTCODE`
- `MPESA_PASSKEY`
- `MPESA_CALLBACK_URL`
- `MPESA_TIMEOUT_SECONDS`

### Frontend (`frontend/.env`)
- `VITE_API_BASE_URL` (defaults to `http://localhost:8000/api`)

## Notes for production hardening
- Put Django behind a proper WSGI/ASGI server + reverse proxy.
- Move DB to Postgres and enable secure backups.
- Restrict CORS and allowed hosts to exact domains.
- Ensure callback URL is publicly reachable over HTTPS.
- Add authentication layer for customer content portal if needed.
- Add async task queu for retries/webhooks/email notifications.

## Testing
Run backend tests:
```bash
cd backend
python manage.py test
```

## Roadmap-ready extension points
Current architecture is intentionally straightforward and supports future additions:
- coupons
- subscriptions
- email automation
- analytics
- testimonials
- blog/content marketing pages
- video-based delivery and gated member area
