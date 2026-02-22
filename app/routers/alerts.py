"""Price Alerts router — store and manage user-defined price thresholds in MongoDB."""

from datetime import datetime
from bson import ObjectId
from fastapi import APIRouter, HTTPException
from app.mongodb import alerts_collection
from app.schemas.mongo import PriceAlertCreate

router = APIRouter()


def _alert_to_dict(doc: dict) -> dict:
    doc["id"] = str(doc.pop("_id"))
    return doc


@router.post("/")
async def create_alert(body: PriceAlertCreate, user_id: str = "default"):
    """Create a new price alert."""
    col = alerts_collection()
    doc = {
        **body.model_dump(),
        "user_id": user_id,
        "active": True,
        "created_at": datetime.utcnow(),
        "triggered_at": None,
    }
    result = await col.insert_one(doc)
    doc["id"] = str(result.inserted_id)
    doc.pop("_id", None)
    return doc


@router.get("/")
async def list_alerts(user_id: str = "default"):
    """List all active price alerts for a user."""
    col = alerts_collection()
    cursor = col.find({"user_id": user_id, "active": True})
    alerts = [_alert_to_dict(d) async for d in cursor]
    return {"alerts": alerts}


@router.get("/{alert_id}")
async def get_alert(alert_id: str):
    col = alerts_collection()
    try:
        doc = await col.find_one({"_id": ObjectId(alert_id)})
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid alert ID")
    if not doc:
        raise HTTPException(status_code=404, detail="Alert not found")
    return _alert_to_dict(doc)


@router.delete("/{alert_id}")
async def delete_alert(alert_id: str):
    """Deactivate (soft-delete) a price alert."""
    col = alerts_collection()
    try:
        result = await col.update_one(
            {"_id": ObjectId(alert_id)},
            {"$set": {"active": False}},
        )
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid alert ID")
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Alert not found")
    return {"deleted": True}


@router.post("/{alert_id}/trigger")
async def trigger_alert(alert_id: str):
    """Mark an alert as triggered (called by a background job in production)."""
    col = alerts_collection()
    try:
        result = await col.update_one(
            {"_id": ObjectId(alert_id)},
            {"$set": {"triggered_at": datetime.utcnow(), "active": False}},
        )
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid alert ID")
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Alert not found")
    return {"triggered": True}
