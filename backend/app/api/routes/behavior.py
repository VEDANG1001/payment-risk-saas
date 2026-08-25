from fastapi import APIRouter, HTTPException

from backend.app.services.customer_behavior import (
    get_customer_payment_behavior,
    calculate_customer_metrics,
)


router = APIRouter()


@router.get("/customer/{customer_id}")
def get_customer_behavior(customer_id: int):

    try:
        data = get_customer_payment_behavior(customer_id)

        metrics = calculate_customer_metrics(
            data["invoices"]
        )

        return {
            "customer_id": customer_id,
            "metrics": metrics,
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )