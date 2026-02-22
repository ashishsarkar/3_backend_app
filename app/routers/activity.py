"""Activity log router — append-only event stream stored in MongoDB."""

from fastapi import APIRouter
from app.mongodb import activity_collection
from app.schemas.mongo import ActivityLogCreate

router = APIRouter()


@router.post("/")
async def log_event(body: ActivityLogCreate, user_id: str = "default"):
    """Record a user activity event."""
    from datetime import datetime
    col = activity_collection()
    doc = {
        "user_id": user_id,
        "event": body.event,
        "payload": body.payload,
        "timestamp": datetime.utcnow(),
    }
    result = await col.insert_one(doc)
    doc["id"] = str(result.inserted_id)
    doc.pop("_id", None)
    return doc


@router.get("/")
async def get_activity(user_id: str = "default", limit: int = 50):
    """Retrieve recent activity events for a user."""
    col = activity_collection()
    cursor = col.find(
        {"user_id": user_id},
        {"_id": 0},
    ).sort("timestamp", -1).limit(limit)
    events = await cursor.to_list(length=limit)
    return {"events": events}
