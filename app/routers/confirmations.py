"""Confirmations log — entries written by RabbitMQ consumer (from booking flow)."""

from fastapi import APIRouter
from app.redis_client import confirmations_log_recent

router = APIRouter()


@router.get("/log")
def get_confirmations_log(limit: int = 10):
    """Return recent confirmation log entries (booking_id, status, type, total, created_at).
    Populated when RabbitMQ consumer processes messages from booking.confirmation queue."""
    if limit > 50:
        limit = 50
    return {"confirmations": confirmations_log_recent(limit=limit)}
