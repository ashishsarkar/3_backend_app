# 3-backend-app — Booking Backend

<!-- CI Status -->
[![Unit tests](https://github.com/ashishsarkar/3-backend-app/actions/workflows/unit-tests.yml/badge.svg)](https://github.com/ashishsarkar/3-backend-app/actions/workflows/unit-tests.yml)
[![Integration tests](https://github.com/ashishsarkar/3-backend-app/actions/workflows/integration-tests.yml/badge.svg)](https://github.com/ashishsarkar/3-backend-app/actions/workflows/integration-tests.yml)

<!-- Code Quality & Coverage -->
[![codecov](https://codecov.io/gh/ashishsarkar/3-backend-app/branch/main/graph/badge.svg)](https://codecov.io/gh/ashishsarkar/3-backend-app)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

<!-- Version & License -->
[![GitHub release](https://img.shields.io/github/v/release/ashishsarkar/3-backend-app?include_prereleases)](https://github.com/ashishsarkar/3-backend-app/releases)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

<!-- Stack -->
[![Python](https://img.shields.io/badge/python-3.10%2B-blue?logo=python&logoColor=white)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100%2B-009688?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![Docker](https://img.shields.io/badge/docker-ready-2496ED?logo=docker&logoColor=white)](https://hub.docker.com/)

<!-- Community -->
[![GitHub issues](https://img.shields.io/github/issues/ashishsarkar/3-backend-app)](https://github.com/ashishsarkar/3-backend-app/issues)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](https://github.com/ashishsarkar/3-backend-app/pulls)

FastAPI REST API for the flight & hotel booking platform. Uses PostgreSQL, MongoDB, Redis, Kafka, and RabbitMQ.

## Dependencies

### Runtime (required to run the app)

- **Python** 3.10+
- **PostgreSQL** — relational data (flights, hotels, bookings, wallet, promos)
- **MongoDB** — document data (chat, price alerts, activity, preferences)
- **Redis** — search cache (flights/hotels), confirmations log
- **Kafka** — booking events (topic: `booking.events`)
- **RabbitMQ** — confirmation queue (`booking.confirmation` → Redis log)

### Python packages

```bash
pip install -r requirements.txt
```

See `requirements.txt` for versions (FastAPI, SQLAlchemy, Motor, Redis, aiokafka, aio-pika, etc.).

### Optional: development and testing

```bash
pip install -r requirements.txt -r requirements-dev.txt
```

Adds: `pytest`, `pytest-asyncio`, `httpx`, `pytest-cov`.

---

## CI / GitHub Actions

The badges at the top show the latest run status for each workflow ([repo](https://github.com/ashishsarkar/3-backend-app)).

Workflows live under **`.github/workflows/`** (repo root when this app is the whole repo):

- **`unit-tests.yml`** — runs on push/PR to `main`, `develop`, `feature/webapp-backend` when `tests/` changes.
- **`integration-tests.yml`** — same triggers; runs integration tests.

- **`paths:`** — workflow runs only when changed files match these globs (e.g. `app/**`, `tests/**`). Avoids running backend CI when only docs or other apps change.
- **`working-directory:`** — not used here; steps run from the repo root (this backend app).

If this app lives inside a **monorepo** (e.g. root has `2-web-app`, `3-backend-app`), use a workflow at the **repository root** `.github/workflows/` that runs these tests with `working-directory: 3-backend-app` and `paths: 3-backend-app/**`.

---

## How to run the app

### 1. Local development (all services on host)

1. Start PostgreSQL, MongoDB, Redis, Kafka, and RabbitMQ (e.g. via Docker or local installs).
2. Copy env and start the API:

```bash
cd 3-backend-app
cp .env.example .env
# Edit .env if your DB/Redis/Kafka/RabbitMQ URLs differ
pip install -r requirements.txt
uvicorn app.main:app --reload --port 4000
```

- API: http://localhost:4000  
- Swagger: http://localhost:4000/docs  

### 2. Full stack with Docker Compose (recommended)

From the repo root (or the folder that contains `project-automation-docker-file`):

```bash
cd project-automation-docker-file
docker compose up --build
```

This starts Postgres, MongoDB, Redis, Kafka, RabbitMQ, the backend, and the frontend. Backend is on port 4000.

### 3. Backend only in Docker

```bash
cd 3-backend-app
docker build -t 3-backend-app .
docker run -p 4000:4000 \
  -e DATABASE_URL=postgresql://booking_user:booking_pass@host.docker.internal:5432/booking \
  -e MONGODB_URL=mongodb://host.docker.internal:27017 \
  -e REDIS_URL=redis://host.docker.internal:6379/0 \
  -e KAFKA_BOOTSTRAP_SERVERS=host.docker.internal:9092 \
  -e RABBITMQ_URL=amqp://guest:guest@host.docker.internal:5672/ \
  3-backend-app
```

---

## How to run tests

Tests use **pytest**. Redis, Kafka, and RabbitMQ are **mocked**; the app uses an in-memory **SQLite** DB when `DATABASE_URL` is not set (set by the test suite).

### Install test dependencies

```bash
pip install -r requirements.txt -r requirements-dev.txt
```

### Run all tests

```bash
cd 3-backend-app
pytest
```

### Run only unit tests

```bash
pytest tests/unit
```

### Run only integration tests

```bash
pytest tests/integration
```

### Run with coverage

```bash
pytest --cov=app --cov-report=term-missing
```

### Run a specific file or test

```bash
pytest tests/unit/test_health.py
pytest tests/unit/test_health.py::test_health_live
pytest tests/integration/test_api_booking.py
```

---

## Test layout

| Directory | Purpose |
|-----------|---------|
| `tests/conftest.py` | `client` fixture (TestClient), SQLite in-memory DB, all external services mocked |
| `tests/unit/` | Unit tests — no DB or network required |
| `tests/integration/` | Integration tests — full API via TestClient with seeded SQLite |

### Unit tests

| File | Covers |
|------|--------|
| `test_health.py` | `/health/live`, `/health/ready` |
| `test_confirmations.py` | Confirmations log (mocked Redis) |
| `test_redis_client.py` | `cache_get`, `cache_set`, TTL, confirmations helpers |
| `test_booking_router.py` | ID generation format, GET 404 |
| `test_promo.py` | `Promo.calc_savings` (percent, fixed, cap), promo endpoints |
| `test_wallet.py` | GET balance, top-up, use credits, insufficient balance |
| `test_seed.py` | Data integrity: counts, required fields, unique IDs, 2026 dates |

### Integration tests

| File | Covers |
|------|--------|
| `test_api_flights.py` | Search with filters, GET by ID, 404 |
| `test_api_flights_extended.py` | City-name match, COK→CCU route, CCU departures, field shapes |
| `test_api_booking.py` | Create, GET, cancel (full CRUD) |
| `test_api_confirmations.py` | GET /log (mocked Redis) |
| `test_api_hotels.py` | Search by location, partial match, GET by ID, rooms, 404 |
| `test_api_promo.py` | Valid/invalid codes, percent/fixed, case-insensitivity, cap |
| `test_api_wallet.py` | GET balance, top-up, use, insufficient balance, chained ops |
| `test_api_locations.py` | ES-mocked search, response shape, required params, size validation |

Unit tests mock all external I/O (Redis, Kafka, RabbitMQ, Elasticsearch, MongoDB ping). Integration tests hit the real FastAPI app with a seeded in-memory SQLite database and mocked messaging — no external services needed.

---

## Environment variables

See `.env.example`. Main ones:

- `DATABASE_URL` — PostgreSQL URL  
- `MONGODB_URL`, `MONGODB_DB` — MongoDB  
- `REDIS_URL`, `CACHE_TTL_SECONDS` — Redis cache and confirmations log  
- `KAFKA_BOOTSTRAP_SERVERS`, `KAFKA_BOOKING_TOPIC` — Kafka  
- `RABBITMQ_URL`, `RABBITMQ_QUEUE_CONFIRMATIONS` — RabbitMQ  
- `PORT` — default 4000  

---

## Project structure (summary)

```
3-backend-app/
├── app/
│   ├── main.py                  # FastAPI app, lifespan, CORS, all routers
│   ├── config.py                # Env-based config (DB, Redis, Kafka, RabbitMQ, ES)
│   ├── database.py              # SQLAlchemy engine, get_db
│   ├── mongodb.py               # Motor client
│   ├── redis_client.py          # Cache + confirmations log
│   ├── kafka_client.py          # Booking event producer
│   ├── rabbitmq_client.py       # Confirmation queue + consumer
│   ├── elasticsearch_client.py  # ES client, 133-location seed, search_locations
│   ├── models.py                # SQLAlchemy models
│   ├── db/seed.py               # 54 flights, hotels, wallet, promos (auto-resyncs)
│   └── routers/                 # flights, hotels, booking, user, wallet, promo,
│                                # chat, alerts, activity, preferences, confirmations,
│                                # locations, health
├── tests/
│   ├── conftest.py              # TestClient, SQLite in-memory, all mocks
│   ├── unit/                    # test_health, test_redis_client, test_confirmations,
│   │                            # test_booking_router, test_promo, test_wallet, test_seed
│   └── integration/             # test_api_flights, test_api_flights_extended,
│                                # test_api_booking, test_api_confirmations,
│                                # test_api_hotels, test_api_promo, test_api_wallet,
│                                # test_api_locations
├── requirements.txt
├── requirements-dev.txt         # pytest, httpx, pytest-cov, etc.
├── pytest.ini
├── Dockerfile
└── .env.example
```

- **CURSOR.md** — Full context (API, routers, DBs, messaging, Elasticsearch).
- **DATABASE_DESIGN.md** — Relational database design, ER diagram, and modeling notes.

---

## CI Infrastructure

The frontend project (`2-web-app`) has a full CI pipeline. The backend shares the same CI infrastructure services for vulnerability management and artifact storage:

| Service | URL | Credentials | Purpose |
|---------|-----|-------------|---------|
| DefectDojo | http://localhost:8080 | admin / admin | Vulnerability aggregation |
| Dependency-Track | http://localhost:8082 | admin / admin | SCA & SBOM tracking |
| MinIO | http://localhost:9001 | minioadmin / minioadmin | CI report storage |
| Container Registry | http://localhost:5050 | No auth | Image storage |

```bash
cd 5-ci-infra && docker compose up -d
```

See `5-ci-infra/README.md` for full setup, credentials, and troubleshooting.
