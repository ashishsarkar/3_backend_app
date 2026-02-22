from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Booking

router = APIRouter()


@router.get("/profile")
def get_profile():
    return {"name": "Demo User", "email": "demo@example.com", "loyaltyTier": "Silver"}


@router.get("/bookings")
def get_bookings(db: Session = Depends(get_db)):
    bookings = (
        db.query(Booking)
        .order_by(Booking.created_at.desc())
        .all()
    )
    return {"bookings": [b.to_dict() for b in bookings]}
