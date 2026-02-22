"""FastAPI app — v4-OSS aligned backend with PostgreSQL (relational) + MongoDB (document)."""

from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import Base, engine, SessionLocal
from app.models import Flight, Hotel, Room, Booking, Wallet, Promo  # noqa: F401 — needed for metadata
from app.db.seed import seed
from app.mongodb import close_mongo
from app.routers import booking, chat, flights, health, hotels, promo, user, wallet
from app.routers import alerts, activity, preferences


@asynccontextmanager
async def lifespan(app: FastAPI):
    # ── Startup ──────────────────────────────────────────────────────────────
    # PostgreSQL: create tables + seed
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        seed(db)
    finally:
        db.close()

    # MongoDB: nothing extra needed — Motor connects lazily
    yield

    # ── Shutdown ──────────────────────────────────────────────────────────────
    await close_mongo()


app = FastAPI(title="3_backend_app", version="1.0.0", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# PostgreSQL-backed routes
app.include_router(flights.router, prefix="/api/flights", tags=["flights"])
app.include_router(hotels.router, prefix="/api/hotels", tags=["hotels"])
app.include_router(booking.router, prefix="/api/booking", tags=["booking"])
app.include_router(user.router, prefix="/api/user", tags=["user"])
app.include_router(wallet.router, prefix="/api/wallet", tags=["wallet"])
app.include_router(promo.router, prefix="/api/promo", tags=["promo"])

# MongoDB-backed routes
app.include_router(chat.router, prefix="/api/chat", tags=["chat"])
app.include_router(alerts.router, prefix="/api/alerts", tags=["alerts"])
app.include_router(activity.router, prefix="/api/activity", tags=["activity"])
app.include_router(preferences.router, prefix="/api/preferences", tags=["preferences"])

app.include_router(health.router, prefix="/health", tags=["health"])


@app.get("/")
def root():
    return {
        "service": "3_backend_app",
        "docs": "/docs",
        "databases": {
            "postgresql": "flights, hotels, rooms, bookings, wallet, promos",
            "mongodb": "chat_messages, price_alerts, activity_logs, user_preferences",
        },
    }
