# CURSOR.md — Backend (3-backend-app)

> **For the next context window:** Pin or mention `@3-backend-app/CURSOR.md` at the start of a new chat so the AI has full backend context without re-scanning.

**Suggested first message:**  
`Read @3-backend-app/CURSOR.md. I need help with [your task].`

---

## Overview

| Field | Value |
|-------|-------|
| **Name** | booking-backend |
| **Directory** | `3-backend-app` (hyphens, not underscores) |
| **Type** | FastAPI REST API |
| **Language** | Python |
| **Port** | 4000 |
| **Docs** | http://localhost:4000/docs (Swagger UI) |

---

## Architecture

- **Pattern:** BFF (Backend for Frontend) — one API serving `2-web-app`
- **Dual database:**
  - **PostgreSQL** (SQLAlchemy ORM): relational, transactional data
  - **MongoDB** (Motor, async): flexible document data

---

## Routers

| Router | Prefix | Database | Purpose |
|--------|--------|----------|---------|
| flights | `/api/flights` | PostgreSQL | Search, detail |
| hotels | `/api/hotels` | PostgreSQL | Search, detail, rooms |
| booking | `/api/booking` | PostgreSQL | Create, get, cancel |
| user | `/api/user` | PostgreSQL | Profile, bookings |
| wallet | `/api/wallet` | PostgreSQL | Balance, top-up, use credits |
| promo | `/api/promo` | PostgreSQL | Validate promo code |
| chat | `/api/chat` | MongoDB | Chatbot replies + history (GET/DELETE) |
| alerts | `/api/alerts` | MongoDB | Price alerts CRUD |
| activity | `/api/activity` | MongoDB | Event logging, retrieval |
| preferences | `/api/preferences` | MongoDB | User preferences |
| health | `/health` | — | Liveness + readiness (checks both DBs) |

---

## API Contracts

Frontend base: `NEXT_PUBLIC_API_BASE_URL` → `http://localhost:4000`

| Path | Method | Purpose |
|------|--------|---------|
| `/api/flights/search` | GET | Search flights (`?origin=&destination=`) |
| `/api/flights/:id` | GET | Flight detail |
| `/api/hotels/search` | GET | Search hotels (`?location=&checkIn=&checkOut=`) |
| `/api/hotels/:id` | GET | Hotel detail + rooms |
| `/api/booking` | POST | Create booking |
| `/api/booking/:id` | GET, PATCH | Get / cancel booking |
| `/api/user/profile` | GET | User profile |
| `/api/user/bookings` | GET | User's bookings |
| `/api/wallet` | GET, POST | Balance; top-up/use (`{ action, amount }`) |
| `/api/promo/validate` | POST | Validate promo (`{ code, amount }`) |
| `/api/chat` | POST | Chatbot — `{ message, session_id }` |
| `/api/chat/history/:session_id` | GET | Load chat history |
| `/api/chat/history/:session_id` | DELETE | Clear chat history |
| `/api/alerts` | GET, POST | List / create price alerts |
| `/api/alerts/:id` | DELETE | Remove alert (soft delete) |
| `/api/activity` | POST, GET | Log / list activity events |
| `/api/preferences` | GET, PATCH | User preferences (upsert) |
| `/health/live` | GET | Liveness probe |
| `/health/ready` | GET | Readiness — checks PostgreSQL + MongoDB |

Full details: `API_CONTRACTS.md` | Scope & gaps: `REQUIREMENTS_AND_GAP_ANALYSIS.md`

---

## MongoDB Collections

| Collection | Fields | Purpose |
|------------|--------|---------|
| `chat_messages` | session_id, role, text, timestamp | Full chat history per browser session |
| `price_alerts` | user_id, type, origin, destination, location, max_price, active | User price thresholds |
| `activity_logs` | user_id, event, payload, timestamp | Search, view, booking events |
| `user_preferences` | user_id, currency, theme, email_alerts | Per-user settings |

---

## PostgreSQL Models (SQLAlchemy)

| Model | Table | Key fields |
|-------|-------|------------|
| Flight | `flights` | origin, destination, price, airline, departure/arrival |
| Hotel | `hotels` | name, location, price, rating; → rooms |
| Room | `rooms` | hotel_id (FK), type, price, capacity |
| Booking | `bookings` | booking_ref, type, flight_id/hotel_id, user_id, status, amount |
| Wallet | `wallet` | user_id, balance |
| Promo | `promos` | code, type, value, min_amount |

---

## Project Structure

```
3-backend-app/
├── app/
│   ├── main.py              # FastAPI app — lifespan, CORS, all routers
│   ├── database.py          # SQLAlchemy engine, SessionLocal, get_db, check_db_connection
│   ├── mongodb.py           # Motor client, collection accessors, ping_mongo, close_mongo
│   ├── models.py            # SQLAlchemy ORM models
│   ├── schemas/
│   │   ├── __init__.py
│   │   └── mongo.py         # Pydantic schemas for all MongoDB collections
│   ├── db/
│   │   ├── __init__.py
│   │   └── seed.py          # Seed PostgreSQL on startup (flights, hotels, wallet, promos)
│   └── routers/
│       ├── __init__.py
│       ├── flights.py
│       ├── hotels.py
│       ├── booking.py
│       ├── user.py
│       ├── wallet.py
│       ├── promo.py
│       ├── chat.py          # POST chat, GET/DELETE history
│       ├── alerts.py
│       ├── activity.py
│       ├── preferences.py
│       └── health.py        # /health/live, /health/ready
├── requirements.txt
├── Dockerfile
├── recreate-docker-build-backend.sh
├── .env.example             # DATABASE_URL, MONGODB_URL, MONGODB_DB, PORT
├── .gitignore
├── .dockerignore
├── .cursorignore
├── API_CONTRACTS.md
├── ARCHITECT_PROMPT.md
├── REQUIREMENTS_AND_GAP_ANALYSIS.md
└── CURSOR.md                # This file
```

---

## Environment Variables

Copy `.env.example` → `.env`:

```
# PostgreSQL
DATABASE_URL=postgresql://booking_user:booking_pass@localhost:5432/booking

# MongoDB
MONGODB_URL=mongodb://localhost:27017
MONGODB_DB=booking

PORT=4000
```

---

## How to Run

**Local dev:**
```bash
cd 3-backend-app
pip install -r requirements.txt
# Create .env from .env.example
uvicorn app.main:app --reload --port 4000
# → http://localhost:4000
# → Swagger: http://localhost:4000/docs
```

**Full stack (Docker Compose):**
```bash
cd ../project-automation-docker-file
docker compose up --build
```

**Backend Docker only:**
```bash
cd 3-backend-app
docker build -t 3-backend-app .
docker run -p 4000:4000 \
  -e DATABASE_URL=postgresql://booking_user:booking_pass@host.docker.internal:5432/booking \
  -e MONGODB_URL=mongodb://host.docker.internal:27017 \
  3-backend-app
```

---

## Startup Behaviour

On startup (`app/main.py` lifespan):
1. `Base.metadata.create_all(bind=engine)` — creates all PostgreSQL tables
2. `seed(db)` — populates flights, hotels, rooms, wallet, promos if tables are empty
3. MongoDB connects lazily on first request

---

## Dependencies (`requirements.txt`)

```
fastapi>=0.109.0
uvicorn[standard]>=0.27.0
sqlalchemy>=2.0.0
psycopg2-binary>=2.9.0
alembic>=1.13.0
motor>=3.3.0
pymongo>=4.6.0
```

---

## Related

- **Workspace root** — `CURSOR.md` (workspace layout, quick start, env vars)
- **`2-web-app/`** — Frontend; see `2-web-app/CURSOR.md`
- **`project-automation-docker-file/docker-compose.yml`** — Full stack (Postgres, MongoDB, backend, frontend)
- **`.github/workflows/ci.yml`** — GitHub Actions CI (frontend: Node; backend job may need Python)
- **`API_CONTRACTS.md`** — Detailed request/response shapes
- **`ARCHITECT_PROMPT.md`** — Backend design / PRD reference
- **`REQUIREMENTS_AND_GAP_ANALYSIS.md`** — Scope and gaps
