# PetVerse 🐾

One app for everything a pet owner needs: pet health records, booking groomers and vets, and later teleconsults, a store, adoption and community.

## Structure

```
petverse/
├── backend/          Django + Django REST Framework API
│   ├── config/       settings, root urls
│   └── apps/
│       ├── accounts/   phone-OTP login, users & roles (owner / provider / admin)
│       ├── pets/       pet profiles, vaccinations
│       └── providers/  service providers (verified by admin) and their services
├── frontend/         Next.js (React) + Tailwind web app
└── docker-compose.yml  Postgres + Redis for local dev (optional)
```

## Run it locally

**Backend** (http://localhost:8000)
```bash
cd backend
python3 -m venv .venv && .venv/bin/pip install -r requirements.txt
cp .env.example .env
.venv/bin/python manage.py migrate
.venv/bin/python manage.py seed_demo         # optional: sample verified providers
.venv/bin/python manage.py createsuperuser   # admin login at /admin
.venv/bin/python manage.py runserver
```
Uses SQLite by default. To use Postgres: `docker compose up -d`, then set `DATABASE_URL` in `backend/.env`.

In dev, OTP codes are **printed in the backend terminal** (no SMS is sent).

**Frontend** (http://localhost:3000)
```bash
cd frontend
npm install
npm run dev
```

**Tests**
```bash
cd backend && .venv/bin/python manage.py test apps
```

## API (so far)

| Method | Endpoint | What it does |
|---|---|---|
| POST | `/api/auth/otp/request/` | `{phone}` – sends a 6-digit code |
| POST | `/api/auth/otp/verify/` | `{phone, code}` – returns JWT `access` + `refresh` |
| POST | `/api/auth/token/refresh/` | `{refresh}` – new access token |
| GET/PATCH | `/api/auth/me/` | current user profile |
| CRUD | `/api/pets/` | your pets |
| CRUD | `/api/pets/<id>/vaccinations/` | a pet's vaccinations |
| GET | `/api/providers/?city=&category=&home=true` | browse verified providers (public) |
| GET/POST/PATCH | `/api/provider/profile/` | register / edit your provider profile |
| CRUD | `/api/provider/services/` | a provider's services and prices |

## Roadmap

- [x] **Phase 0 – Foundation:** OTP login, pet profiles, provider onboarding + admin verification
- [ ] **Phase 1 – Services marketplace:** availability slots, bookings, Razorpay payments, reviews, commission tracking
- [ ] **Phase 2 – Vet teleconsult:** video/chat, freemium plans, prescriptions on the pet record
- [ ] **Phase 3 – Store:** catalogue, cart, orders, food subscriptions
- [ ] **Phase 4 – Community & adoption:** lost & found alerts, NGO adoption listings, forums
- [ ] **Phase 5 – AI & more:** diet plans, health insights, walkers, boarding, transport, insurance
