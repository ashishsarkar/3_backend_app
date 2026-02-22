from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Flight

router = APIRouter()


@router.get("/search")
def search(origin: str | None = None, destination: str | None = None, db: Session = Depends(get_db)):
    query = db.query(Flight)
    if origin:
        query = query.filter(Flight.origin.ilike(origin))
    if destination:
        query = query.filter(Flight.destination.ilike(destination))
    return {"flights": [f.to_dict() for f in query.all()]}


@router.get("/{flight_id}")
def get_flight(flight_id: str, db: Session = Depends(get_db)):
    flight = db.query(Flight).filter(Flight.id == flight_id).first()
    if not flight:
        raise HTTPException(status_code=404, detail=f"Flight {flight_id} not found")
    return flight.to_dict()
