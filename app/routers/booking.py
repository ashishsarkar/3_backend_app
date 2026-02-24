import random
import string
from datetime import datetime
from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Booking
from app.kafka_client import publish_booking_event
from app.rabbitmq_client import publish_confirmation_task

router = APIRouter()


def _generate_id() -> str:
    return "BK" + "".join(random.choices(string.ascii_uppercase + string.digits, k=10))


async def _publish_booking_created(booking_dict: dict) -> None:
    """Publish to Kafka (event) and RabbitMQ (confirmation task)."""
    try:
        await publish_booking_event("BookingCreated", {
            "booking_id": booking_dict["id"],
            "status": booking_dict["status"],
            "type": booking_dict["type"],
            "total": booking_dict.get("total"),
            "created_at": booking_dict.get("createdAt"),
        })
    except Exception:
        pass
    try:
        await publish_confirmation_task({
            "booking_id": booking_dict["id"],
            "status": booking_dict["status"],
            "type": booking_dict["type"],
            "total": booking_dict.get("total"),
            "created_at": booking_dict.get("createdAt"),
        })
    except Exception:
        pass


@router.post("/")
def create_booking(body: dict, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    booking = Booking(
        id=_generate_id(),
        status="confirmed",
        type=body.get("type", "flight"),
        flight_json=body.get("flight"),
        hotel_json=body.get("hotel"),
        total=body.get("total"),
        promo_json=body.get("promo"),
        insurance=body.get("insurance", False),
        use_wallet=body.get("useWallet", False),
        wallet_deduction=body.get("walletDeduction", 0),
        card_number=body.get("cardNumber"),
        expiry=body.get("expiry"),
        created_at=datetime.utcnow(),
    )
    db.add(booking)
    db.commit()
    db.refresh(booking)
    result = booking.to_dict()
    background_tasks.add_task(_publish_booking_created, result)
    return result


@router.get("/{booking_id}")
def get_booking(booking_id: str, db: Session = Depends(get_db)):
    booking = db.query(Booking).filter(Booking.id == booking_id).first()
    if not booking:
        raise HTTPException(status_code=404, detail=f"Booking {booking_id} not found")
    return booking.to_dict()


@router.patch("/{booking_id}")
def update_booking(booking_id: str, body: dict, db: Session = Depends(get_db)):
    booking = db.query(Booking).filter(Booking.id == booking_id).first()
    if not booking:
        raise HTTPException(status_code=404, detail=f"Booking {booking_id} not found")
    if body.get("status") == "cancelled":
        booking.status = "cancelled"
        booking.refund_status = "initiated"
        booking.refund_initiated_at = datetime.utcnow()
    db.commit()
    db.refresh(booking)
    return booking.to_dict()
