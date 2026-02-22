"""MongoDB async client using Motor.

Collections:
  - chat_messages   : Full chat history per session
  - price_alerts    : User-defined price alert conditions
  - activity_logs   : Search, view, booking events
  - user_preferences: Per-user settings (theme, currency, etc.)
"""

import os
from motor.motor_asyncio import AsyncIOMotorClient

MONGODB_URL = os.environ.get("MONGODB_URL", "mongodb://localhost:27017")
MONGODB_DB = os.environ.get("MONGODB_DB", "booking")

_client: AsyncIOMotorClient | None = None


def get_mongo_client() -> AsyncIOMotorClient:
    global _client
    if _client is None:
        _client = AsyncIOMotorClient(MONGODB_URL)
    return _client


def get_mongo_db():
    return get_mongo_client()[MONGODB_DB]


# Typed collection accessors
def chat_collection():
    return get_mongo_db()["chat_messages"]


def alerts_collection():
    return get_mongo_db()["price_alerts"]


def activity_collection():
    return get_mongo_db()["activity_logs"]


def preferences_collection():
    return get_mongo_db()["user_preferences"]


async def close_mongo():
    global _client
    if _client:
        _client.close()
        _client = None


async def ping_mongo() -> bool:
    try:
        await get_mongo_client().admin.command("ping")
        return True
    except Exception:
        return False
