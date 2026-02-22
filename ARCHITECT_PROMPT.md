# Architect Prompt — Backend Development

**Use this prompt in Cursor when developing the backend.** Copy or @ mention this file.

---

## Role

Act as a **Solution Architect**. Design and implement the backend (3_backend_app) according to the PRD in **v4-OSS/architecture-final-v4.html**, so it connects with the frontend (2_web-app) and the full application can run end-to-end.

---

## Objective

1. **Align with v4-OSS architecture** — Flight domain (Layer 03), Hotel domain (Layer 04), Cross-domain (Layer 05), Customer (Layer 06).
2. **Implement all API contracts** defined in `API_CONTRACTS.md` — frontend expects these exact paths and response shapes.
3. **Connect frontend to backend** — Frontend sets `NEXT_PUBLIC_API_BASE_URL=http://localhost:4000`; all `/api/*` calls go to backend.
4. **Enable full flow** — Search flights/hotels → Select → Checkout → Booking confirmation → My Bookings. All must work with the backend.

---

## Data Strategy (Phase 1)

**Use one of these for now — design for easy swap later:**

| Option | Description | Swap Path |
|--------|-------------|-----------|
| **Mock in-memory** | JSON fixtures in memory; same shape as frontend `mocks/fixtures/` | Replace service internals with DB calls |
| **SQLite + Prisma** | Local `booking.db`; Prisma ORM | Change `DATABASE_URL` to PostgreSQL later |
| **BetterSQLite3** | Lightweight, no ORM | Migrate to Prisma/PostgreSQL when ready |

**Recommendation:** Start with **mock in-memory** or **SQLite** to validate flow quickly. Ensure:
- Data layer is abstracted (repository or service interface)
- Schema mirrors what PostgreSQL will need
- No vendor-specific SQL; use Prisma or raw queries that map to Postgres

---

## Fixture Data (Match Frontend)

**Flights** (from `2_web-app/mocks/fixtures/flights.json`):
```json
{ "id", "origin", "originCity", "destination", "destinationCity", "departureTime", "arrivalTime", "price", "airline", "duration" }
```

**Hotels** (from `2_web-app/mocks/fixtures/hotels.json`):
```json
{ "id", "name", "location", "address", "lat", "lng", "price", "rating", "image", "amenities", "rooms": [{ "id", "name", "price", "maxGuests" }] }
```

Use this structure for seed data or mock responses.

---

## API Implementation Checklist

| Endpoint | Method | Response Shape | Data Source |
|----------|--------|----------------|-------------|
| `/api/flights/search` | GET | `{ flights: Flight[] }` | Filter by origin, destination |
| `/api/flights/:id` | GET | `Flight` | By id |
| `/api/hotels/search` | GET | `{ hotels: Hotel[] }` | Filter by location, checkIn, checkOut |
| `/api/hotels/:id` | GET | `Hotel` | By id |
| `/api/booking` | POST | `{ id, status, ... }` | Persist; return created |
| `/api/booking/:id` | GET | `{ id, status, flight?, hotel?, ... }` | By id |
| `/api/booking/:id` | PATCH | Updated booking | `{ status: 'cancelled' }` |
| `/api/user/profile` | GET | `{ name, email, loyaltyTier? }` | Mock user or DB |
| `/api/user/bookings` | GET | `{ bookings: Booking[] }` | By user (mock userId) |
| `/api/wallet` | GET | `{ balance: number }` | Mock or DB |
| `/api/wallet` | POST | `{ balance }` | `{ action: 'use'|'topup', amount }` |
| `/api/promo/validate` | POST | `{ valid, savings?, message? }` | SAVE10, FLAT500, WELCOME rules |
| `/api/chat` | POST | `{ reply: string }` | Mock replies for now |
| `/health/live` | GET | `{ status: 'ok' }` | Always ok |
| `/health/ready` | GET | `{ status: 'ok' }` | DB/cache check if used |

---

## Tech Stack

- **Runtime:** Node.js 20
- **Framework:** NestJS
- **Language:** TypeScript
- **Port:** 4000
- **Path prefix:** `/api` (e.g. `/api/flights/search`)
- **CORS:** Allow `http://localhost:3000` (frontend)

---

## Architecture (v4-OSS Mapping)

| v4-OSS | Backend Module |
|--------|----------------|
| Flight Search Service | `modules/flight` |
| Hotel Search Service | `modules/hotel` |
| Flight/Hotel Booking, Dynamic Packaging | `modules/booking` |
| User Service | `modules/user` |
| Wallet / Credits | `modules/wallet` |
| Coupon & Promo Engine | `modules/promo` |
| AI Chatbot | `modules/chat` |

---

## Acceptance Criteria

1. Backend runs on `http://localhost:4000`
2. Frontend with `NEXT_PUBLIC_API_BASE_URL=http://localhost:4000` can search flights/hotels, book, view confirmation, see My Bookings
3. All API contracts in `API_CONTRACTS.md` are implemented
4. Data layer is abstracted — easy to swap mock/SQLite for PostgreSQL
5. Health endpoints work

---

## Files to Reference

- `@3_backend_app/API_CONTRACTS.md` — Exact request/response shapes
- `@3_backend_app/REQUIREMENTS_AND_GAP_ANALYSIS.md` — Full scope and phased plan
- `@v4-OSS/architecture-final-v4.html` — PRD / architecture
- `@2_web-app/mocks/fixtures/flights.json` — Flight fixture shape
- `@2_web-app/mocks/fixtures/hotels.json` — Hotel fixture shape
- `@2_web-app/src/lib/api/*.js` — Frontend API client (paths and usage)

---

## Suggested First Message in Cursor

> Read @3_backend_app/ARCHITECT_PROMPT.md. Act as the architect and implement the backend (NestJS) per the v4-OSS PRD. Use mock data or SQLite for now; design so we can swap to PostgreSQL later. Ensure all API contracts in API_CONTRACTS.md are implemented and the frontend (2_web-app) can run end-to-end with NEXT_PUBLIC_API_BASE_URL=http://localhost:4000.
