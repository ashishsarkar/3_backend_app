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
- **Databases:**
  - **PostgreSQL** (SQLAlchemy ORM): relational data (flights, hotels, bookings, wallet, promos)
  - **MongoDB** (Motor, async): document data (chat, alerts, activity, preferences)
  - **Redis**: search cache (flights/hotels), confirmations log (list)
- **Messaging:**
  - **Kafka**: booking events (topic `booking.events` — BookingCreated)
  - **RabbitMQ**: queue `booking.confirmation` → in-process consumer → append to Redis confirmations log

---

## Routers

| Router | Prefix | Backing | Purpose |
|--------|--------|---------|---------|
| flights | `/api/flights` | PostgreSQL + Redis cache | Search (partial + city name match), detail |
| hotels | `/api/hotels` | PostgreSQL + Redis cache | Search (partial location match), detail, rooms |
| booking | `/api/booking` | PostgreSQL + Kafka + RabbitMQ | Create, get, cancel |
| user | `/api/user` | PostgreSQL | Profile, bookings |
| wallet | `/api/wallet` | PostgreSQL | Balance, top-up, use credits |
| promo | `/api/promo` | PostgreSQL | Validate promo code (percent/fixed, case-insensitive) |
| chat | `/api/chat` | MongoDB | Chatbot replies + history (GET/DELETE) |
| alerts | `/api/alerts` | MongoDB | Price alerts CRUD |
| activity | `/api/activity` | MongoDB | Event logging, retrieval |
| preferences | `/api/preferences` | MongoDB | User preferences |
| confirmations | `/api/confirmations` | Redis | GET /log — recent confirmations (from RabbitMQ consumer) |
| locations | `/api/locations` | Elasticsearch | Autocomplete — cities, airports, states, countries |
| health | `/health` | — | Liveness + readiness (PostgreSQL + MongoDB) |

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
| `/api/confirmations/log` | GET | Recent confirmations log (`?limit=10`, max 50) |
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
│   ├── config.py            # Env: DATABASE_URL, MONGODB_*, REDIS_*, KAFKA_*, RABBITMQ_*, ELASTICSEARCH_*
│   ├── database.py          # SQLAlchemy engine, SessionLocal, get_db, check_db_connection
│   ├── mongodb.py           # Motor client, ping_mongo, close_mongo
│   ├── redis_client.py      # cache_get/cache_set, confirmations_log_append/recent, close_redis
│   ├── kafka_client.py      # get_kafka_producer, publish_booking_event, close_kafka
│   ├── rabbitmq_client.py   # publish_confirmation_task, start_rabbitmq_consumer, close_rabbitmq
│   ├── elasticsearch_client.py  # ES client, index+mapping setup, seed 133 locations, search_locations
│   ├── models.py            # SQLAlchemy ORM models
│   ├── schemas/
│   │   ├── __init__.py
│   │   └── mongo.py         # Pydantic schemas for MongoDB collections
│   ├── db/
│   │   ├── __init__.py
│   │   └── seed.py          # Seed PostgreSQL (54 flights, hotels, wallet, promos); auto-resyncs on count change
│   └── routers/
│       ├── __init__.py
│       ├── flights.py       # Partial match: ilike(code) OR ilike(%city%)
│       ├── hotels.py        # Partial match on location/name
│       ├── booking.py       # Publishes to Kafka + RabbitMQ on create
│       ├── user.py
│       ├── wallet.py
│       ├── promo.py
│       ├── chat.py
│       ├── alerts.py
│       ├── activity.py
│       ├── preferences.py
│       ├── confirmations.py # GET /log from Redis
│       ├── locations.py     # GET /search — Elasticsearch autocomplete
│       └── health.py        # /health/live, /health/ready
├── tests/
│   ├── conftest.py          # client fixture, SQLite in-memory, mocks for Redis/Kafka/RabbitMQ/ES
│   ├── unit/                # test_health, test_confirmations, test_redis_client, test_booking_router,
│   │                        # test_promo, test_wallet, test_seed
│   └── integration/         # test_api_flights, test_api_flights_extended, test_api_booking,
│                            # test_api_confirmations, test_api_hotels, test_api_promo,
│                            # test_api_wallet, test_api_locations
├── requirements.txt
├── requirements-dev.txt     # pytest, pytest-asyncio, httpx, pytest-cov
├── pytest.ini
├── Dockerfile
├── .env.example
├── DATABASE_DESIGN.md
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

# Redis (cache + confirmations log)
REDIS_URL=redis://localhost:6379/0
CACHE_TTL_SECONDS=300

# Kafka (booking.events)
KAFKA_BOOTSTRAP_SERVERS=localhost:9092
KAFKA_BOOKING_TOPIC=booking.events

# RabbitMQ (booking.confirmation → Redis log)
RABBITMQ_URL=amqp://guest:guest@localhost:5672/
RABBITMQ_QUEUE_CONFIRMATIONS=booking.confirmation

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
3. `start_rabbitmq_consumer()` — background task consumes `booking.confirmation` and appends to Redis
4. MongoDB connects lazily on first request

On shutdown: `close_rabbitmq()`, `close_kafka()`, `close_redis()`, `close_mongo()`.

---

## Testing

- **Framework:** pytest
- **Config:** `pytest.ini` — `asyncio_mode = auto`, `testpaths = tests`
- **No external services needed:** SQLite in-memory DB; Redis/Kafka/RabbitMQ/Elasticsearch mocked in `conftest.py`

### Unit tests (`tests/unit/`)

| File | What it covers |
|------|----------------|
| `test_health.py` | `/health/live`, `/health/ready` — liveness + readiness probes |
| `test_confirmations.py` | Confirmations log via mocked Redis |
| `test_redis_client.py` | `cache_get`, `cache_set`, TTL, confirmations helpers |
| `test_booking_router.py` | `_generate_id` format, GET 404 |
| `test_promo.py` | `Promo.calc_savings` logic (percent/fixed/capped), promo router endpoints |
| `test_wallet.py` | GET balance, top-up, use credits, insufficient balance |
| `test_seed.py` | Seed data integrity — counts, required fields, unique IDs, 2026 dates |

### Integration tests (`tests/integration/`)

| File | What it covers |
|------|----------------|
| `test_api_flights.py` | Search (origin/dest filters), GET by ID, 404, root endpoint |
| `test_api_flights_extended.py` | City-name search, COK→CCU route, CCU departures, field shapes |
| `test_api_booking.py` | Create, GET, PATCH/cancel (full CRUD cycle) |
| `test_api_confirmations.py` | GET /log from Redis (mocked) |
| `test_api_hotels.py` | Search (location filter, partial match), GET by ID, rooms shape, 404 |
| `test_api_promo.py` | Valid/invalid codes, percent/fixed discount, case-insensitivity, cap logic |
| `test_api_wallet.py` | GET balance, top-up, use, insufficient balance, multi-operation chain |
| `test_api_locations.py` | ES-mocked search, response shape, required params, size validation |

**Run all tests:**
```bash
pip install -r requirements.txt -r requirements-dev.txt
pytest
```

**Run unit only:** `pytest tests/unit`  
**Run integration only:** `pytest tests/integration`  
**With coverage:** `pytest --cov=app --cov-report=term-missing`

See **README.md** for full test and run instructions.

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
redis>=5.0.0
aiokafka>=0.10.0
aio-pika>=9.4.0
```

**Dev/test:** `requirements-dev.txt` — pytest, pytest-asyncio, httpx, pytest-cov

---

## Related

- **Workspace root** — `CURSOR.md` (workspace layout, quick start, env vars)
- **`2-web-app/`** — Frontend; see `2-web-app/CURSOR.md`
- **`project-automation-docker-file/docker-compose.yml`** — Full stack (Postgres, MongoDB, backend, frontend)
- **`.github/workflows/ci.yml`** — GitHub Actions CI (frontend: Node; backend job may need Python)
- **`API_CONTRACTS.md`** — Detailed request/response shapes
- **`DATABASE_DESIGN.md`** — Relational database design, ER, tables, and modeling notes
- **`ARCHITECT_PROMPT.md`** — Backend design / PRD reference
- **`REQUIREMENTS_AND_GAP_ANALYSIS.md`** — Scope and gaps
