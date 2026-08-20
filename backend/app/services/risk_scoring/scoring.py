from .rules import (
    late_payment_risk,
    average_days_late_risk,
    maximum_days_late_risk,
    outstanding_ratio_risk,
    payment_completion_risk,
)


def calculate_risk_score(metrics: dict) -> dict:

    late_risk = late_payment_risk(
        metrics["late_payments"],
        metrics["total_invoices"],
    )

    average_late_risk = average_days_late_risk(
        metrics["average_days_late"]
    )

    maximum_late_risk = maximum_days_late_risk(
        metrics["maximum_days_late"]
    )

    outstanding_risk = outstanding_ratio_risk(
        metrics["total_outstanding"],
        metrics["total_invoiced"],
    )

    completion_risk = payment_completion_risk(
        metrics["payment_completion_rate"]
    )

    # Apply weights
    score = (
        late_risk * 0.25
        + average_late_risk * 0.20
        + maximum_late_risk * 0.15
        + outstanding_risk * 0.25
        + completion_risk * 0.15
    )

    score = round(score, 2)

    # Determine risk level
    if score < 30:
        risk_level = "LOW"
    elif score < 60:
        risk_level = "MEDIUM"
    else:
        risk_level = "HIGH"

    return {
        "risk_score": score,
        "risk_level": risk_level,
        "components": {
            "late_payment_risk": late_risk,
            "average_days_late_risk": average_late_risk,
            "maximum_days_late_risk": maximum_late_risk,
            "outstanding_ratio_risk": outstanding_risk,
            "payment_completion_risk": completion_risk,
        },
    }