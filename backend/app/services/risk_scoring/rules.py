# Calculate risk score based on late payment ratio
def late_payment_risk(late_payments: int, total_invoices: int) -> float:

    if total_invoices == 0:
        return 0.0

    ratio = (late_payments / total_invoices) * 100

    if ratio == 0:
        return 0.0
    elif ratio <= 20:
        return 20.0
    elif ratio <= 40:
        return 40.0
    elif ratio <= 60:
        return 60.0
    elif ratio <= 80:
        return 80.0
    else:
        return 100.0


# Calculate risk score based on average days late
def average_days_late_risk(average_days_late: float) -> float:

    if average_days_late <= 0:
        return 0.0
    elif average_days_late <= 3:
        return 20.0
    elif average_days_late <= 7:
        return 40.0
    elif average_days_late <= 15:
        return 70.0
    else:
        return 100.0


# Calculate risk score based on maximum days late
def maximum_days_late_risk(maximum_days_late: int) -> float:

    if maximum_days_late <= 0:
        return 0.0
    elif maximum_days_late <= 7:
        return 20.0
    elif maximum_days_late <= 15:
        return 50.0
    elif maximum_days_late <= 30:
        return 80.0
    else:
        return 100.0


# Calculate risk score based on outstanding amount
def outstanding_ratio_risk(
    total_outstanding: float,
    total_invoiced: float
) -> float:

    if total_invoiced <= 0:
        return 0.0

    ratio = (total_outstanding / total_invoiced) * 100

    if ratio == 0:
        return 0.0
    elif ratio <= 10:
        return 20.0
    elif ratio <= 25:
        return 50.0
    elif ratio <= 50:
        return 75.0
    else:
        return 100.0


# Calculate risk score based on payment completion
def payment_completion_risk(
    payment_completion_rate: float
) -> float:

    if payment_completion_rate >= 100:
        return 0.0
    elif payment_completion_rate >= 80:
        return 20.0
    elif payment_completion_rate >= 60:
        return 50.0
    elif payment_completion_rate >= 40:
        return 75.0
    else:
        return 100.0