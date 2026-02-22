# Backend Application — Book Flights

Backend API for the Flight & Hotel booking platform, aligned with the v4-OSS architecture.

## Directory Structure

```
3_backend_app/
├── src/
│   ├── main.ts                 # NestJS bootstrap
│   ├── app.module.ts           # Root module
│   ├── common/                 # Shared utilities, filters, interceptors
│   ├── config/                 # Config, env validation
│   ├── modules/
│   │   ├── flight/             # Flight Search, Booking (per architecture)
│   │   ├── hotel/              # Hotel Search, Booking
│   │   ├── booking/            # Cross-domain booking orchestration
│   │   ├── user/               # User, Profile
│   │   ├── wallet/             # Wallet / Credits
│   │   ├── promo/              # Coupon & Promo Engine
│   │   ├── chat/               # AI Chatbot (LLM integration)
│   │   └── health/             # Health checks
│   └── database/               # DB config, migrations
├── test/                       # E2E, unit tests
├── package.json
├── tsconfig.json
├── .env.example
└── REQUIREMENTS_AND_GAP_ANALYSIS.md
```

## Tech Stack (per v4-OSS)

- **Runtime:** Node.js 20
- **Framework:** NestJS
- **DB:** PostgreSQL (primary), Redis (cache/sessions)
- **API Style:** REST (BFF pattern for web)
- **Auth:** JWT (Keycloak/OAuth2 in future)

## Getting Started

See `REQUIREMENTS_AND_GAP_ANALYSIS.md` for full scope and phased plan.
