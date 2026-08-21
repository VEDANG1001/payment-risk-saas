from .customer_risk_profile import build_risk_profile
from .rules import (
    late_payment_risk,
    average_days_late_risk,
    maximum_days_late_risk,
    outstanding_ratio_risk,
    payment_completion_risk,
    unpaid_invoice_risk,      # NEW
    partial_payment_risk,   # NEW
    get_risk_severity,      # NEW
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


# Get summary of risk factors
def summarize_risk_factors(components: dict) -> dict:

    # Store factors by severity
    summary = {
        "HIGH": [],
        "MEDIUM": [],
        "LOW": [],
    }

    # Check every risk factor
    for name, data in components.items():

        # Get its severity
        severity = data["severity"]

        # Add factor to its severity group
        summary[severity].append(name)

    # Return grouped factors
    return summary


# Generate positive factors
def generate_positive_factors(metrics: dict) -> list[str]:

    # Store positive factors
    positive_factors = []

    # Check outstanding amount
    if metrics["total_outstanding"] == 0:
        positive_factors.append(
            "No outstanding amount"
        )

    # Check unpaid invoices
    if metrics["unpaid_invoices"] == 0:
        positive_factors.append(
            "No unpaid invoices"
        )

    # Check partial payments
    if metrics["partially_paid_invoices"] == 0:
        positive_factors.append(
            "No partial payments"
        )

    # Check payment completion
    if metrics["payment_completion_rate"] == 100:
        positive_factors.append(
            "100% payment completion"
        )

    # Check on-time payments
    if metrics["late_payments"] == 0:
        positive_factors.append(
            "All payments were on time"
        )

    # Return positive factors
    return positive_factors



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
    # i am replacing the payment completion risk with this new logic to calculate the risk score based on the new metrics
    # Calculate payment completion risk
    # No invoices = no payment history to evaluate
    if metrics["total_invoices"] == 0:
        completion_risk = 0.0
    else:
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

    # Get severity for each risk factor
    late_severity = get_risk_severity(late_risk)
    average_late_severity = get_risk_severity(average_late_risk)
    maximum_late_severity = get_risk_severity(maximum_late_risk)
    outstanding_severity = get_risk_severity(outstanding_risk)
    completion_severity = get_risk_severity(completion_risk)
    unpaid_severity = get_risk_severity(unpaid_risk)
    partial_severity = get_risk_severity(partial_risk)

    

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

    # Generate positive factors
    positive_factors = generate_positive_factors(metrics)


    # Determine risk level
    if score < 30:
        risk_level = "LOW"
    elif score < 60:
        risk_level = "MEDIUM"
    else:
        risk_level = "HIGH"

       # Store all risk components
    components = {
        "late_payment": {
            "score": late_risk,
            "severity": late_severity,
        },
        "average_days_late": {
            "score": average_late_risk,
            "severity": average_late_severity,
        },
        "maximum_days_late": {
            "score": maximum_late_risk,
            "severity": maximum_late_severity,
        },
        "outstanding_ratio": {
            "score": outstanding_risk,
            "severity": outstanding_severity,
        },
        "payment_completion": {
            "score": completion_risk,
            "severity": completion_severity,
        },
        "unpaid_invoices": {
            "score": unpaid_risk,
            "severity": unpaid_severity,
        },
        "partial_payments": {
            "score": partial_risk,
            "severity": partial_severity,
        },
    }

    # Group risk factors by severity
    risk_factor_summary = summarize_risk_factors(components)

    # Build complete customer risk profile
    return build_risk_profile(
        score=score,
        level=risk_level,
        reasons=risk_reasons,
        positive_factors=positive_factors,
        components=components,
        summary=risk_factor_summary,
    )
