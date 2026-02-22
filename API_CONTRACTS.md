# API Contracts — Backend ↔ Frontend

Reference for backend implementation. Frontend (2_web-app) expects these exact paths and shapes.

## Base URL

`NEXT_PUBLIC_API_BASE_URL` — e.g. `http://localhost:4000`

All paths below are relative to base (e.g. `/api/flights/search`).

---

## Flights

| Method | Path | Query/Body | Response |
|--------|------|------------|----------|
| GET | `/api/flights/search` | `origin`, `destination` | `{ flights: Flight[] }` |
| GET | `/api/flights/:id` | — | `Flight` |

**Flight shape:** `{ id, origin, destination, originCity, destinationCity, departureTime, arrivalTime, airline, price, seat?, duration? }`

---

## Hotels

| Method | Path | Query/Body | Response |
|--------|------|------------|----------|
| GET | `/api/hotels/search` | `location`, `checkIn`, `checkOut`, etc. | `{ hotels: Hotel[] }` |
| GET | `/api/hotels/:id` | — | `Hotel` |

**Hotel shape:** `{ id, name, location, rooms: [{ id, name, price }], price? }`

---

## Booking

| Method | Path | Query/Body | Response |
|--------|------|------------|----------|
| POST | `/api/booking` | `{ type, item?, flight?, hotel?, total, promo?, insurance?, ... }` | `{ id, status, ... }` |
| GET | `/api/booking/:id` | — | `{ id, status, flight?, hotel?, createdAt, ... }` |
| PATCH | `/api/booking/:id` | `{ status: 'cancelled' }` | Updated booking |

---

## User

| Method | Path | Response |
|--------|------|----------|
| GET | `/api/user/profile` | `{ name, email, loyaltyTier?, ... }` |
| GET | `/api/user/bookings` | `{ bookings: Booking[] }` |

---

## Wallet

| Method | Path | Query/Body | Response |
|--------|------|------------|----------|
| GET | `/api/wallet` | — | `{ balance: number }` |
| POST | `/api/wallet` | `{ action: 'use' \| 'topup', amount }` | `{ balance: number }` or similar |

---

## Promo

| Method | Path | Body | Response |
|--------|------|------|----------|
| POST | `/api/promo/validate` | `{ code, amount }` | `{ valid: boolean, savings?: number, message?: string }` |

---

## Chat

| Method | Path | Body | Response |
|--------|------|------|----------|
| POST | `/api/chat` | `{ message: string }` | `{ reply: string }` |
