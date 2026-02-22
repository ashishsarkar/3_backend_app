from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Hotel

router = APIRouter()


@router.get("/search")
def search(location: str | None = None, db: Session = Depends(get_db)):
    query = db.query(Hotel)
    if location:
        query = query.filter(
            Hotel.location.ilike(f"%{location}%") | Hotel.name.ilike(f"%{location}%")
        )
    return {"hotels": [h.to_dict() for h in query.all()]}


@router.get("/{hotel_id}")
def get_hotel(hotel_id: str, db: Session = Depends(get_db)):
    hotel = db.query(Hotel).filter(Hotel.id == hotel_id).first()
    if not hotel:
        raise HTTPException(status_code=404, detail=f"Hotel {hotel_id} not found")
    return hotel.to_dict()
