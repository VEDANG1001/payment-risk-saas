from .rules import (
    late_payment_risk,
    average_days_late_risk,
    maximum_days_late_risk,
    outstanding_ratio_risk,
    payment_completion_risk,
    unpaid_invoice_risk,      # NEW
    partial_payment_risk,     # NEW
)
# Generate reasons for the customer's risk
def generate_risk_reasons(metrics: dict) -> list[str]:

    # Store risk reasons
    reasons = []

    # Check late payment frequency
    if metrics["late_payments"] > 0:
        reasons.append(
            f"{metrics['late_payments']} late payment(s) detected"
        )

    # Check average payment delay
    if metrics["average_days_late"] > 0:
        reasons.append(
            f"Average payment delay: "
            f"{metrics['average_days_late']:.1f} days"
        )

    # Check maximum payment delay
    if metrics["maximum_days_late"] > 0:
        reasons.append(
            f"Maximum payment delay: "
            f"{metrics['maximum_days_late']} days"
        )

    # Check outstanding amount
    if metrics["total_outstanding"] > 0:
        reasons.append(
            f"Outstanding amount: "
            f"{metrics['total_outstanding']:.2f}"
        )

    # Check unpaid invoices
    if metrics["unpaid_invoices"] > 0:
        reasons.append(
            f"Unpaid invoices: "
            f"{metrics['unpaid_invoices']}"
        )

    # Check partial payments
    if metrics["partially_paid_invoices"] > 0:
        reasons.append(
            f"Partially paid invoices: "
            f"{metrics['partially_paid_invoices']}"
        )

    # Check payment completion
    if metrics["payment_completion_rate"] < 100:
        reasons.append(
            f"Payment completion rate: "
            f"{metrics['payment_completion_rate']:.1f}%"
        )

    # Return all reasons
    return reasons


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
    # Calculate unpaid invoice risk
    unpaid_risk = unpaid_invoice_risk(
        metrics["unpaid_invoice_ratio"]
    )
    # Calculate partial payment risk
    partial_risk = partial_payment_risk(
        metrics["partial_payment_ratio"]
    )

    # Apply weights
    score = (
        late_risk * 0.20
        + average_late_risk * 0.15
        + maximum_late_risk * 0.10
        + outstanding_risk * 0.20
        + completion_risk * 0.10
        + unpaid_risk * 0.15
        + partial_risk * 0.10
    )

    score = round(score, 2)
    # Generate explanations for the risk
    risk_reasons = generate_risk_reasons(metrics)


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
        "risk_reasons": risk_reasons,
        "components": {
            "late_payment_risk": late_risk,
            "average_days_late_risk": average_late_risk,
            "maximum_days_late_risk": maximum_late_risk,
            "outstanding_ratio_risk": outstanding_risk,
            "payment_completion_risk": completion_risk,
            "unpaid_invoice_risk": unpaid_risk,
            "partial_payment_risk": partial_risk,
        },
    }