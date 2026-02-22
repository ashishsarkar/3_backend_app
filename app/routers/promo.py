from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Promo

router = APIRouter()


@router.post("/validate")
def validate_promo(body: dict, db: Session = Depends(get_db)):
    code = (body.get("code") or "").strip().upper()
    amount = float(body.get("amount") or 0)

    promo = db.query(Promo).filter(Promo.code == code).first()
    if not promo:
        return {"valid": False, "message": "Invalid promo code"}

    savings = promo.calc_savings(amount)
    if promo.discount_type == "percent":
        msg = f"{int(promo.discount_value)}% off applied! Saved ₹{savings:,.0f}"
    else:
        msg = f"Flat ₹{int(promo.discount_value)} off applied!"

    return {"valid": True, "savings": savings, "message": msg, "code": code}
