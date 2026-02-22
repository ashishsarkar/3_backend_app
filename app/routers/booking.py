import random
import string
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Booking

router = APIRouter()


def _generate_id() -> str:
    return "BK" + "".join(random.choices(string.ascii_uppercase + string.digits, k=10))


@router.post("/")
def create_booking(body: dict, db: Session = Depends(get_db)):
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
    return booking.to_dict()


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
