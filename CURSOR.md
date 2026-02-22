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
- **Routers:** flight, hotel, booking, user, wallet, promo, chat, health
- **Data:** In-memory stores (Phase 1); design-ready for PostgreSQL swap

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
| /api/chat | POST | Chatbot |
| /health/live | GET | Liveness probe |
| /health/ready | GET | Readiness probe |

Full contracts: `API_CONTRACTS.md`. Scope & gaps: `REQUIREMENTS_AND_GAP_ANALYSIS.md`.

---

## Run Locally

```bash
cd 3_backend_app
pip install -r requirements.txt
uvicorn app.main:app --reload --port 4000
```

Or with Docker:

```bash
docker build -t 3-backend-app .
docker run -p 4000:4000 3-backend-app
```
