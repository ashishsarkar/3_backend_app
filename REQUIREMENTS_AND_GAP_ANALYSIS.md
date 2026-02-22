# Backend — Requirements & Gap Analysis

Aligns with **v4-OSS/architecture-final-v4.html** and **2_web-app** (frontend).

---

## 1. Directory Structure (3_backend_app)

```
3_backend_app/
├── src/
│   ├── main.ts                      # NestJS bootstrap, port 4000
│   ├── app.module.ts                # Root module
│   ├── common/                      # Shared layer
│   │   ├── filters/                 # Exception filters
│   │   ├── guards/                  # Auth guards
│   │   ├── interceptors/            # Logging, transform
│   │   ├── decorators/
│   │   └── dto/
│   ├── config/                      # Config & env
│   │   ├── app.config.ts
│   │   └── database.config.ts
│   ├── modules/
│   │   ├── flight/                  # Flight domain (per v4-OSS Layer 03)
│   │   │   ├── flight.module.ts
│   │   │   ├── flight.controller.ts
│   │   │   ├── flight.service.ts
│   │   │   └── dto/
│   │   ├── hotel/                   # Hotel domain (per v4-OSS Layer 04)
│   │   │   ├── hotel.module.ts
│   │   │   ├── hotel.controller.ts
│   │   │   └── hotel.service.ts
│   │   ├── booking/                 # Cross-domain booking (Layer 05)
│   │   │   ├── booking.module.ts
│   │   │   ├── booking.controller.ts
│   │   │   └── booking.service.ts
│   │   ├── user/                    # User service (Layer 05/06)
│   │   ├── wallet/                  # Wallet / Credits (Layer 06)
│   │   ├── promo/                   # Coupon & Promo (Layer 06)
│   │   ├── chat/                    # AI Chatbot (Layer 01)
│   │   └── health/                  # /health/live, /health/ready
│   └── database/                    # Prisma / TypeORM
│       ├── migrations/
│       └── seeds/
├── test/
│   ├── e2e/
│   └── unit/
├── package.json
├── tsconfig.json
├── nest-cli.json
├── .env.example
├── Dockerfile
└── REQUIREMENTS_AND_GAP_ANALYSIS.md
```

---

## 2. API Contracts (Frontend Expectation)

The **2_web-app** expects these endpoints. Base URL: `NEXT_PUBLIC_API_BASE_URL` (e.g. `http://localhost:4000`).

| Endpoint | Method | Purpose | Request / Response |
|----------|--------|---------|--------------------|
| `/api/flights/search` | GET | Search flights | `?origin=DEL&destination=BOM` → `{ flights: [...] }` |
| `/api/flights/:id` | GET | Flight detail | → `{ id, origin, destination, ... }` |
| `/api/hotels/search` | GET | Search hotels | `?location=...&checkIn=...&checkOut=...` → `{ hotels: [...] }` |
| `/api/hotels/:id` | GET | Hotel detail | → `{ id, name, rooms, ... }` |
| `/api/booking` | POST | Create booking | `{ type, item, flight, hotel, total, ... }` → `{ id, status, ... }` |
| `/api/booking/:id` | GET | Get booking | → `{ id, status, flight, hotel, ... }` |
| `/api/booking/:id` | PATCH | Cancel | `{ status: 'cancelled' }` |
| `/api/user/profile` | GET | User profile | → `{ name, email, loyaltyTier, ... }` |
| `/api/user/bookings` | GET | My bookings | → `{ bookings: [...] }` |
| `/api/wallet` | GET | Wallet balance | → `{ balance: number }` |
| `/api/wallet` | POST | Use / Top-up | `{ action: 'use'|'topup', amount }` |
| `/api/promo/validate` | POST | Validate promo | `{ code, amount }` → `{ valid, savings, message }` |
| `/api/chat` | POST | Chatbot | `{ message }` → `{ reply }` |

---

## 3. Architecture Alignment (v4-OSS)

| v4-OSS Layer | Component | Backend Mapping |
|--------------|-----------|-----------------|
| 02 Gateway | API Gateway | Express/Nest gateway; add Kong later |
| 02 Routing | BFF — Web | NestJS controllers aggregate domain calls |
| 03 Flight | Flight Search Service | `modules/flight` |
| 03 Flight | Flight Booking Service | `modules/booking` (orchestrates) |
| 04 Hotel | Hotel Search Service | `modules/hotel` |
| 04 Hotel | Hotel Booking Service | `modules/booking` |
| 05 Cross | Dynamic Packaging Engine | `modules/booking` (bundle support) |
| 05 Cross | Itinerary Service | PDF generation (or delegate to frontend) |
| 05 Core | User Service | `modules/user` |
| 05 Core | Notification Service | Phase 2 (Email/SMS) |
| 06 Customer | Wallet / Credits Service | `modules/wallet` |
| 06 Customer | Coupon & Promo Engine | `modules/promo` |
| 07 Finance | Payment Orchestrator | Phase 2 (Razorpay/Stripe) |
| 08 Data | PostgreSQL | Primary DB |
| 08 Data | Redis | Cache, sessions, rate limit |
| 09 Messaging | Kafka / BullMQ | Phase 2 (async jobs) |

---

## 4. Gap Analysis

### 4.1 Current Frontend (2_web-app) — Mock APIs

| API | Current Implementation | Backend Needed |
|-----|------------------------|----------------|
| Flights | JSON fixture filter | Real search (DB/Elasticsearch or mock DB) |
| Hotels | JSON fixture filter | Real search (DB or mock) |
| Booking | In-memory Map | PostgreSQL, state machine |
| User | Mock store | PostgreSQL, auth integration |
| Wallet | In-memory Map | PostgreSQL, double-entry ledger |
| Promo | Hardcoded (SAVE10, FLAT500, WELCOME) | DB-driven promo engine |
| Chat | Mock LLM response | LLM integration (OpenAI/LangChain) |

### 4.2 Gaps to Address

| Gap | Priority | Effort | Notes |
|-----|----------|--------|-------|
| Replace in-memory stores with DB | P0 | High | PostgreSQL + Prisma/TypeORM |
| Booking state machine | P0 | Medium | PNR, hold, confirmed, cancelled |
| Wallet double-entry | P0 | Medium | Credits, refunds, top-up |
| Promo validation from DB | P1 | Low | Rules, usage limits |
| Auth (JWT) | P1 | Medium | Keycloak or custom JWT |
| Chat LLM integration | P2 | Medium | OpenAI / tool calling |
| Redis cache | P2 | Low | Search, rate limit |
| Kafka / event bus | P3 | High | Phase 2 |
| GDS / Hotel supplier APIs | P3 | High | Amadeus, Booking.com, etc. |
| PDF itinerary on backend | P3 | Low | Optional; frontend already does it |

---

## 5. Phased Implementation Plan

### Phase 1 — Core API (MVP)

**Goal:** Replace frontend mocks with a real backend. Frontend points to `NEXT_PUBLIC_API_BASE_URL`.

1. **Scaffold NestJS** — Project, modules, config
2. **PostgreSQL + Prisma** — Schema for flights, hotels, bookings, users, wallet, promos
3. **Flight module** — Search (DB query), get by id
4. **Hotel module** — Search, get by id
5. **Booking module** — Create, get, cancel; persist to DB
6. **User module** — Profile, bookings (mock auth first)
7. **Wallet module** — Balance, top-up, use at checkout
8. **Promo module** — Validate from DB rules
9. **Health** — `/health/live`, `/health/ready`
10. **CORS** — Allow frontend origin
11. **API path prefix** — `/api` to match frontend

### Phase 2 — Auth & Resilience

- JWT auth (Keycloak or custom)
- Redis cache for search
- Rate limiting
- Notification service (email on booking)

### Phase 3 — Advanced

- Kafka / BullMQ for async jobs
- GDS / hotel supplier integration
- Fraud detection, reconciliation

---

## 6. Environment & Integration

### Frontend Integration

Set in **2_web-app**:

```
NEXT_PUBLIC_API_BASE_URL=http://localhost:4000
```

Frontend `src/lib/api/*.js` uses this base; paths remain `/api/flights/search`, etc.

### Backend Env (.env.example)

```
PORT=4000
DATABASE_URL=postgresql://user:pass@localhost:5432/booking
REDIS_URL=redis://localhost:6379
JWT_SECRET=...
OPENAI_API_KEY=...  # for chat
```

---

## 7. Summary

| Item | Status |
|------|--------|
| Directory structure (3_backend_app) | ✅ Proposed |
| API contracts | ✅ Defined from frontend |
| Architecture alignment | ✅ Mapped to v4-OSS |
| Gap analysis | ✅ Documented |
| Phased plan | ✅ Phase 1–3 |
| Next step | Implement Phase 1 (NestJS scaffold, DB, modules) |
