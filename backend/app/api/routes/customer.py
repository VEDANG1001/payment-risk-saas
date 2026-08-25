from fastapi import APIRouter, HTTPException

from backend.app.db.session import SessionLocal
from backend.app.models.customer import Customer


router = APIRouter()


@router.get("/")
def get_all_customers():

    db = SessionLocal()

    try:
        customers = db.query(Customer).all()

        return customers

    finally:
        db.close()


@router.get("/{customer_id}")
def get_customer(customer_id: int):

    db = SessionLocal()

    try:
        customer = (
            db.query(Customer)
            .filter(Customer.id == customer_id)
            .first()
        )

        if not customer:
            raise HTTPException(
                status_code=404,
                detail="Customer not found"
            )

        return customer

    finally:
        db.close()