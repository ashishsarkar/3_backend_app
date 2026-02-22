from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Wallet

router = APIRouter()
USER_ID = "default"


@router.get("/")
def get_balance(db: Session = Depends(get_db)):
    wallet = db.query(Wallet).filter(Wallet.user_id == USER_ID).first()
    return {"balance": wallet.balance if wallet else 0}


@router.post("/")
def update_wallet(body: dict, db: Session = Depends(get_db)):
    action = body.get("action", "topup")
    amount = float(body.get("amount") or 0)

    wallet = db.query(Wallet).filter(Wallet.user_id == USER_ID).first()
    if not wallet:
        wallet = Wallet(user_id=USER_ID, balance=0)
        db.add(wallet)

    if action == "topup":
        wallet.balance += amount
    else:
        if amount > wallet.balance:
            raise HTTPException(status_code=400, detail="Insufficient wallet balance")
        wallet.balance = max(0, wallet.balance - amount)

    db.commit()
    db.refresh(wallet)
    return {"balance": wallet.balance}
