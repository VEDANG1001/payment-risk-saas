from fastapi import APIRouter, HTTPException
from sqlalchemy import select

from backend.app.db.session import SessionLocal
from backend.app.models.customer import Customer

from backend.app.services.customer_behavior import (
    get_customer_payment_behavior,
    calculate_customer_metrics,
)

from backend.app.services.risk_scoring import calculate_risk_score


router = APIRouter()


@router.get("/customer/{customer_id}")
def get_customer_risk(customer_id: int):

    # Check whether customer exists
    db = SessionLocal()

    try:
        customer = db.scalar(
            select(Customer).where(
                Customer.id == customer_id
            )
        )

        if customer is None:
            raise HTTPException(
                status_code=404,
                detail="Customer not found"
            )

    finally:
        db.close()

    # Get customer payment behavior
    data = get_customer_payment_behavior(customer_id)

    # Calculate customer metrics
    metrics = calculate_customer_metrics(data["invoices"])

    # Calculate risk score
    risk_result = calculate_risk_score(metrics)

    return {
        "customer_id": customer_id,
        "metrics": metrics,
        "risk_result": risk_result,
    }