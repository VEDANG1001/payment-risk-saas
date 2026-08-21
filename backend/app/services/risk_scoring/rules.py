# ==========================================
# RISK SCORING RULES
# ==========================================


# ------------------------------------------
# 1. Late Payment Risk
# ------------------------------------------
def late_payment_risk(
    late_payments: int,
    total_invoices: int
) -> float:

    # Avoid division by zero
    if total_invoices == 0:
        return 0.0

    # Calculate late payment percentage
    ratio = (late_payments / total_invoices) * 100

    # No late payments
    if ratio == 0:
        return 0.0

    # Up to 20% late
    elif ratio <= 20:
        return 20.0

    # Up to 40% late
    elif ratio <= 40:
        return 40.0

    # Up to 60% late
    elif ratio <= 60:
        return 60.0

    # Up to 80% late
    elif ratio <= 80:
        return 80.0

    # More than 80% late
    else:
        return 100.0


# ------------------------------------------
# 2. Average Days Late Risk
# ------------------------------------------
def average_days_late_risk(
    average_days_late: float
) -> float:

    # No delay
    if average_days_late <= 0:
        return 0.0

    # 1–3 days late
    elif average_days_late <= 3:
        return 20.0

    # 4–7 days late
    elif average_days_late <= 7:
        return 40.0

    # 8–15 days late
    elif average_days_late <= 15:
        return 70.0

    # More than 15 days late
    else:
        return 100.0


# ------------------------------------------
# 3. Maximum Days Late Risk
# ------------------------------------------
def maximum_days_late_risk(
    maximum_days_late: int
) -> float:

    # No late payment
    if maximum_days_late <= 0:
        return 0.0

    # Up to 7 days late
    elif maximum_days_late <= 7:
        return 20.0

    # 8–15 days late
    elif maximum_days_late <= 15:
        return 50.0

    # 16–30 days late
    elif maximum_days_late <= 30:
        return 80.0

    # More than 30 days late
    else:
        return 100.0


# ------------------------------------------
# 4. Outstanding Amount Risk
# ------------------------------------------
def outstanding_ratio_risk(
    total_outstanding: float,
    total_invoiced: float
) -> float:

    # Avoid division by zero
    if total_invoiced <= 0:
        return 0.0

    # Calculate outstanding percentage
    ratio = (total_outstanding / total_invoiced) * 100

    # Nothing outstanding
    if ratio == 0:
        return 0.0

    # Up to 10% outstanding
    elif ratio <= 10:
        return 20.0

    # Up to 25% outstanding
    elif ratio <= 25:
        return 50.0

    # Up to 50% outstanding
    elif ratio <= 50:
        return 75.0

    # More than 50% outstanding
    else:
        return 100.0


# ------------------------------------------
# 5. Payment Completion Risk
# ------------------------------------------
def payment_completion_risk(
    payment_completion_rate: float
) -> float:

    # 100% completed
    if payment_completion_rate >= 100:
        return 0.0

    # 80–99% completed
    elif payment_completion_rate >= 80:
        return 20.0

    # 60–79% completed
    elif payment_completion_rate >= 60:
        return 50.0

    # 40–59% completed
    elif payment_completion_rate >= 40:
        return 75.0

    # Below 40%
    else:
        return 100.0


# ------------------------------------------
# 6. Unpaid Invoice Risk
# ------------------------------------------
def unpaid_invoice_risk(
    unpaid_invoice_ratio: float
) -> float:

    # No unpaid invoices
    if unpaid_invoice_ratio == 0:
        return 0.0

    # Up to 10% unpaid
    elif unpaid_invoice_ratio <= 10:
        return 20.0

    # Up to 25% unpaid
    elif unpaid_invoice_ratio <= 25:
        return 50.0

    # Up to 50% unpaid
    elif unpaid_invoice_ratio <= 50:
        return 75.0

    # More than 50% unpaid
    else:
        return 100.0


# ------------------------------------------
# 7. Partial Payment Risk
# ------------------------------------------
def partial_payment_risk(
    partial_payment_ratio: float
) -> float:

    # No partial payments
    if partial_payment_ratio == 0:
        return 0.0

    # Up to 10% partial
    elif partial_payment_ratio <= 10:
        return 20.0

    # Up to 25% partial
    elif partial_payment_ratio <= 25:
        return 50.0

    # Up to 50% partial
    elif partial_payment_ratio <= 50:
        return 75.0

    # More than 50% partial
    else:
        return 100.0

# Convert risk score into severity
def get_risk_severity(risk_score: float) -> str:

    # Low risk
    if risk_score < 30:
        return "LOW"

    # Medium risk
    elif risk_score < 60:
        return "MEDIUM"

    # High risk
    else:
        return "HIGH"
    