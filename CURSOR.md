# CURSOR.md — Backend (3_backend_app)

> **Project context for backend.** Read this when working in 3_backend_app.

---

## Overview

| Field | Value |
|-------|-------|
| **Name** | booking-backend |
| **Directory** | `3_backend_app` |
| **Type** | FastAPI REST API |
| **Language** | Python |
| **Port** | 4000 |

---

## Architecture (v4-OSS aligned)

- **BFF — Web** pattern via FastAPI routers
- **Dual database:**
  - **PostgreSQL** (SQLAlchemy): flights, hotels, rooms, bookings, wallet, promos
  - **MongoDB** (Motor): chat_messages, price_alerts, activity_logs, user_preferences

---

## Routers

| Router | Prefix | DB | Purpose |
|--------|--------|----|---------|
| flights | /api/flights | PostgreSQL | Search, detail |
| hotels | /api/hotels | PostgreSQL | Search, detail, rooms |
| booking | /api/booking | PostgreSQL | Create, get, cancel |
| user | /api/user | PostgreSQL | Profile, bookings |
| wallet | /api/wallet | PostgreSQL | Balance, top-up, use |
| promo | /api/promo | PostgreSQL | Validate promo |
| chat | /api/chat | MongoDB | Chatbot, history (GET/DELETE) |
| alerts | /api/alerts | MongoDB | Price alerts CRUD |
| activity | /api/activity | MongoDB | Event logging, retrieval |
| preferences | /api/preferences | MongoDB | User preferences |
| health | /health | — | Live, ready (checks both DBs) |

---

## API Contracts

Frontend (2_web-app) expects these paths. Base: `NEXT_PUBLIC_API_BASE_URL` → `http://localhost:4000`.

| Path | Method | Purpose |
|------|--------|---------|
| /api/flights/search | GET | Search flights |
| /api/flights/:id | GET | Flight detail |
| /api/hotels/search | GET | Search hotels |
| /api/hotels/:id | GET | Hotel detail |
| /api/booking | POST | Create booking |
| /api/booking/:id | GET, PATCH | Get / cancel booking |
| /api/user/profile | GET | User profile |
| /api/user/bookings | GET | My bookings |
| /api/wallet | GET, POST | Balance, top-up, use |
| /api/promo/validate | POST | Validate promo |
| /api/chat | POST | Chatbot (body: `{ message, session_id }`) |
| /api/chat/history/:session_id | GET | Chat history |
| /api/chat/history/:session_id | DELETE | Clear chat history |
| /api/alerts | GET, POST | List / create price alerts |
| /api/alerts/:id | DELETE | Remove alert |
| /api/activity | POST, GET | Log / list activity events |
| /api/preferences | GET, PATCH | User preferences |
| /health/live | GET | Liveness probe |
| /health/ready | GET | Readiness (PostgreSQL + MongoDB) |

Full contracts: `API_CONTRACTS.md`. Scope & gaps: `REQUIREMENTS_AND_GAP_ANALYSIS.md`.

---

## MongoDB Collections

| Collection | Purpose |
|------------|---------|
| chat_messages | Full chat history per session (session_id, role, text, timestamp) |
| price_alerts | User price thresholds (type, origin/destination or location, max_price) |
| activity_logs | Search, view, booking events (event, payload, timestamp) |
| user_preferences | Currency, theme, email_alerts |

---

## Environment

| Variable | Purpose |
|----------|---------|
| DATABASE_URL | PostgreSQL connection string |
| MONGODB_URL | MongoDB connection string (default: `mongodb://localhost:27017`) |
| MONGODB_DB | MongoDB database name (default: `booking`) |
| PORT | API port (default: 4000) |

---

## Run Locally

```bash
cd 3_backend_app
pip install -r requirements.txt
# Create .env with DATABASE_URL and MONGODB_URL
uvicorn app.main:app --reload --port 4000
```

**Docker Compose (full stack):**
```bash
# From workspace root
docker compose up --build
```

**Docker (backend only):**
```bash
cd 3_backend_app
docker build -t 3-backend-app .
docker run -p 4000:4000 \
  -e DATABASE_URL=postgresql://booking_user:booking_pass@host.docker.internal:5432/booking \
  -e MONGODB_URL=mongodb://host.docker.internal:27017 \
  3-backend-app
```

---

## Project Structure

```
3_backend_app/
├── app/
│   ├── main.py           # FastAPI app, lifespan, CORS, routers
│   ├── database.py       # SQLAlchemy engine, session, get_db
│   ├── mongodb.py        # Motor client, collection accessors, ping_mongo
│   ├── models.py         # SQLAlchemy models (Flight, Hotel, Room, Booking, Wallet, Promo)
│   ├── schemas/
│   │   └── mongo.py      # Pydantic schemas for MongoDB collections
│   ├── db/
│   │   └── seed.py       # PostgreSQL seed (flights, hotels, rooms, wallet, promos)
│   └── routers/          # flights, hotels, booking, user, wallet, promo, chat, alerts, activity, preferences, health
├── requirements.txt
├── Dockerfile
├── .env.example
├── API_CONTRACTS.md
└── CURSOR.md
```
