# Import date for date calculations
from datetime import date


# Calculate how many days late a payment was
def calculate_days_late(
    due_date: date,
    payment_date: date
) -> int:

    # Payment made on or before due date
    if payment_date <= due_date:
        return 0

    # Calculate late days
    return (payment_date - due_date).days


# Calculate unpaid invoice amount
def calculate_outstanding_amount(
    invoice_amount: float,
    total_paid: float
) -> float:

    # Calculate remaining amount
    outstanding = invoice_amount - total_paid

    # Never allow negative outstanding amount
    return max(outstanding, 0.0)


# Determine payment status
def get_payment_status(
    payment_date: date,
    due_date: date
) -> str:

    # Payment made on or before due date
    if payment_date <= due_date:
        return "ON_TIME"

    # Payment made after due date
    return "LATE"

# Calculate how many days an unpaid invoice is overdue
def calculate_unpaid_days_late(
    due_date: date
) -> int:

    # Get today's date
    today = date.today()

    # If the invoice is not overdue yet
    if today <= due_date:
        return 0

    # Calculate how many days the invoice is overdue
    return (today - due_date).days