from fastapi import APIRouter, HTTPException

from backend.app.db.session import SessionLocal
from backend.app.models.payment import Payment


router = APIRouter()


@router.get("/")
def get_all_payments():

    db = SessionLocal()

    try:
        payments = db.query(Payment).all()

        return payments

    finally:
        db.close()


@router.get("/{payment_id}")
def get_payment(payment_id: int):

    db = SessionLocal()

    try:
        payment = (
            db.query(Payment)
            .filter(Payment.id == payment_id)
            .first()
        )

        if not payment:
            raise HTTPException(
                status_code=404,
                detail="Payment not found"
            )

        return payment

    finally:
        db.close()
        