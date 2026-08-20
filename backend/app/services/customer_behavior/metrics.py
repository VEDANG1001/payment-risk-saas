# SQLAlchemy query support
from sqlalchemy import select

# Database session
from backend.app.db.session import SessionLocal

# Database models
from backend.app.models.invoice import Invoice
from backend.app.models.payment import Payment

# Payment behavior calculations
from backend.app.services.payment_behavior.calculations import (
    calculate_days_late,
    calculate_outstanding_amount,
    get_payment_status,
)

# Get payment behavior for one customer
def get_customer_payment_behavior(customer_id: int) -> dict:

    # Create database session
    db = SessionLocal()

    try:
        # Get all invoices for this customer
        invoices = db.scalars(
            select(Invoice).where(
                Invoice.customer_id == customer_id
            )
        ).all()

        # Store invoice behavior results
        results = []

        # Process every invoice
        for invoice in invoices:

            # Get payments for this invoice
            payments = db.scalars(
                select(Payment).where(
                    Payment.invoice_id == invoice.id
                )
            ).all()

            # Calculate total paid
            total_paid = sum(
                float(payment.amount)
                for payment in payments
            )

            # Calculate outstanding amount
            outstanding = calculate_outstanding_amount(
                float(invoice.amount),
                total_paid
            )

            # Check whether payment exists
            if payments:

                # Get latest payment date
                latest_payment_date = max(
                    payment.payment_date
                    for payment in payments
                )

                # Calculate late days
                days_late = calculate_days_late(
                    invoice.due_date,
                    latest_payment_date
                )

                # Calculate payment status
                status = get_payment_status(
                    latest_payment_date,
                    invoice.due_date
                )

            else:

                # No payment has been made
                days_late = 0
                status = "UNPAID"

            # Store invoice behavior
            results.append({
                "invoice_id": invoice.id,
                "invoice_amount": float(invoice.amount),
                "total_paid": total_paid,
                "outstanding_amount": outstanding,
                "days_late": days_late,
                "payment_status": status,
            })

        # Return customer behavior
        return {
            "customer_id": customer_id,
            "invoices": results,
        }

    finally:
        # Always close database session
        db.close()

def calculate_customer_metrics(invoices: list[dict]) -> dict:
    # Count total invoices
    total_invoices = len(invoices)

    # Count paid invoices
    paid_invoices = sum(
        1 for invoice in invoices
        if invoice["payment_status"] != "UNPAID"
    )

    # Count on-time paymentsss
    on_time_payments = sum(
        1 for invoice in invoices
        if invoice["payment_status"] == "ON_TIME"
    )

    # Count late payments
    late_payments = sum(
        1 for invoice in invoices
        if invoice["payment_status"] == "LATE"
    )

    # Calculate total invoice amount
    total_invoiced = sum(
        invoice["invoice_amount"]
        for invoice in invoices
    )

    # Calculate total paid amount
    total_paid = sum(
        invoice["total_paid"]
        for invoice in invoices
    )

    # Calculate total outstanding amount
    total_outstanding = sum(
        invoice["outstanding_amount"]
        for invoice in invoices
    )

    # Get days late values only from paid invoices
    late_days = [
        invoice["days_late"]
        for invoice in invoices
        if invoice["payment_status"] != "UNPAID"
    ]

    # Calculate average days late
    average_days_late = (
        sum(late_days) / len(late_days)
        if late_days
        else 0
    )

    # Calculate maximum days late
    maximum_days_late = max(late_days) if late_days else 0

    # Calculate payment completion percentage
    payment_completion_rate = (
        (paid_invoices / total_invoices) * 100
        if total_invoices
        else 0
    )

    # Return complete customer metrics
    return {
        "total_invoices": total_invoices,
        "paid_invoices": paid_invoices,
        "on_time_payments": on_time_payments,
        "late_payments": late_payments,
        "total_invoiced": total_invoiced,
        "total_paid": total_paid,
        "total_outstanding": total_outstanding,
        "average_days_late": average_days_late,
        "maximum_days_late": maximum_days_late,
        "payment_completion_rate": payment_completion_rate,
    }