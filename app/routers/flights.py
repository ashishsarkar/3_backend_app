from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import or_
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Flight
from app.redis_client import cache_get, cache_set

router = APIRouter()

CACHE_KEY_PREFIX = "flights:search"


@router.get("/search")
def search(origin: str | None = None, destination: str | None = None, db: Session = Depends(get_db)):
    cache_key = f"{CACHE_KEY_PREFIX}:{origin or ''}:{destination or ''}"
    cached = cache_get(cache_key)
    if cached is not None:
        return cached

    query = db.query(Flight)

    if origin:
        term = f"%{origin.strip()}%"
        # Match by IATA code (exact, case-insensitive) OR city name (partial)
        query = query.filter(
            or_(
                Flight.origin.ilike(origin.strip()),
                Flight.origin_city.ilike(term),
            )
        )
    if destination:
        term = f"%{destination.strip()}%"
        query = query.filter(
            or_(
                Flight.destination.ilike(destination.strip()),
                Flight.destination_city.ilike(term),
            )
        )

    result = {"flights": [f.to_dict() for f in query.all()]}
    cache_set(cache_key, result)
    return result


@router.get("/{flight_id}")
def get_flight(flight_id: str, db: Session = Depends(get_db)):
    flight = db.query(Flight).filter(Flight.id == flight_id).first()
    if not flight:
        raise HTTPException(status_code=404, detail=f"Flight {flight_id} not found")
    return flight.to_dict()
