"""User Preferences router — per-user settings stored in MongoDB."""

from datetime import datetime
from fastapi import APIRouter
from app.mongodb import preferences_collection
from app.schemas.mongo import UserPreferencesUpdate

router = APIRouter()


@router.get("/")
async def get_preferences(user_id: str = "default"):
    col = preferences_collection()
    doc = await col.find_one({"user_id": user_id}, {"_id": 0})
    if not doc:
        doc = {"user_id": user_id, "currency": "INR", "theme": "light", "email_alerts": True}
    return doc


@router.patch("/")
async def update_preferences(body: UserPreferencesUpdate, user_id: str = "default"):
    col = preferences_collection()
    updates = {k: v for k, v in body.model_dump().items() if v is not None}
    updates["updated_at"] = datetime.utcnow()
    await col.update_one(
        {"user_id": user_id},
        {"$set": updates},
        upsert=True,
    )
    doc = await col.find_one({"user_id": user_id}, {"_id": 0})
    return doc
