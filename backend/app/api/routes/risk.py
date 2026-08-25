from fastapi import APIRouter

from backend.app.services.customer_behavior import (
    get_customer_payment_behavior,
    calculate_customer_metrics,
)

from backend.app.services.risk_scoring import calculate_risk_score


router = APIRouter()


@router.get("/customer/{customer_id}")
def get_customer_risk(customer_id: int):

    data = get_customer_payment_behavior(customer_id)

    metrics = calculate_customer_metrics(data["invoices"])

    risk_result = calculate_risk_score(metrics)

    return {
        "customer_id": customer_id,
        "metrics": metrics,
        "risk_result": risk_result,
    }