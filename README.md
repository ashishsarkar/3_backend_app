# 3-backend-app — Booking Backend

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

| Directory           | Purpose |
|--------------------|--------|
| `tests/unit/`      | Unit tests (mocked Redis, health, confirmations, booking helpers, redis_client) |
| `tests/integration/` | Integration tests (full API with TestClient; in-memory SQLite, mocked messaging) |
| `tests/conftest.py` | Pytest fixtures: `client` (TestClient), env and mocks for no external services |

Unit tests mock external I/O (Redis, Kafka, RabbitMQ, MongoDB ping). Integration tests hit the real FastAPI app with a seeded in-memory SQLite database and mocked messaging so no Postgres/Redis/Kafka/RabbitMQ are required for `pytest`.

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
│   ├── main.py           # FastAPI app, lifespan, CORS, routers
│   ├── config.py         # Env-based config
│   ├── database.py       # SQLAlchemy engine, get_db
│   ├── mongodb.py        # Motor client
│   ├── redis_client.py   # Cache + confirmations log
│   ├── kafka_client.py   # Booking event producer
│   ├── rabbitmq_client.py # Confirmation queue producer + consumer
│   ├── models.py         # SQLAlchemy models
│   ├── db/seed.py        # Seed data
│   └── routers/          # flights, hotels, booking, user, wallet, promo, chat, alerts, activity, preferences, confirmations, health
├── tests/
│   ├── conftest.py       # Test client, mocks
│   ├── unit/             # Unit tests
│   └── integration/      # Integration tests
├── requirements.txt
├── requirements-dev.txt  # pytest, httpx, pytest-cov, etc.
├── pytest.ini
├── Dockerfile
└── .env.example
```

- **CURSOR.md** — Full context (API, routers, DBs, messaging).
- **DATABASE_DESIGN.md** — Relational database design, ER diagram, and modeling notes.
