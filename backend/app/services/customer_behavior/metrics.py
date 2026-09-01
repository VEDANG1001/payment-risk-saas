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
    calculate_unpaid_days_late,
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
              days_late = calculate_unpaid_days_late(
                  invoice.due_date
              )
            
              # Check whether the unpaid invoice is overdue
              if days_late > 0:
                  status = "OVERDUE"
              else:
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

    # Fully paid invoices
    paid_invoices = sum(
        1 for invoice in invoices
        if invoice["outstanding_amount"] == 0
        and invoice["total_paid"] > 0
    )

    # Unpaid invoices
    unpaid_invoices = sum(
        1 for invoice in invoices
        if invoice["total_paid"] == 0
    )

          # Overdue unpaid invoices
    overdue_invoices = sum(
        1 for invoice in invoices
        if invoice["payment_status"] == "OVERDUE"
    )
     
    # Partially paid invoices
    partially_paid_invoices = sum(
        1 for invoice in invoices
        if invoice["total_paid"] > 0
        and invoice["outstanding_amount"] > 0
    )

    # Count on-time payments
    on_time_payments = sum(
        1 for invoice in invoices
        if invoice["payment_status"] == "ON_TIME"
    )

    # Count late payments
     # Count both paid-late and currently overdue invoices
    late_payments = sum(
        1 for invoice in invoices
        if invoice["payment_status"] in ("LATE", "OVERDUE")
    )

    # Total invoice amount
    total_invoiced = sum(
        invoice["invoice_amount"]
        for invoice in invoices
    )

    # Total paid amount
    total_paid = sum(
        invoice["total_paid"]
        for invoice in invoices
    )

    # Total outstanding amount
    total_outstanding = sum(
        invoice["outstanding_amount"]
        for invoice in invoices
    )

    # Days late from invoices that received payment
   # Include both paid-late and currently overdue invoices
    late_days = [
        invoice["days_late"]
        for invoice in invoices
        if invoice["payment_status"] in ("LATE", "OVERDUE")
    ]
    # Average days late
    average_days_late = (
        sum(late_days) / len(late_days)
        if late_days
        else 0
    )

    # Maximum days late
    maximum_days_late = (
        max(late_days)
        if late_days
        else 0
    )

    # Unpaid invoice ratio
    unpaid_invoice_ratio = (
        (unpaid_invoices / total_invoices) * 100
        if total_invoices
        else 0
    )

    # Partial payment ratio
    partial_payment_ratio = (
        (partially_paid_invoices / total_invoices) * 100
        if total_invoices
        else 0
    )

    # Payment completion rate
    payment_completion_rate = (
        (paid_invoices / total_invoices) * 100
        if total_invoices
        else 0
    )

    # Return complete customer metrics
    return {
        "total_invoices": total_invoices,
        "paid_invoices": paid_invoices,
        "unpaid_invoices": unpaid_invoices,
        "partially_paid_invoices": partially_paid_invoices,
        "on_time_payments": on_time_payments,
        "late_payments": late_payments,
        "total_invoiced": total_invoiced,
        "total_paid": total_paid,
        "total_outstanding": total_outstanding,
        "average_days_late": average_days_late,
        "maximum_days_late": maximum_days_late,
        "unpaid_invoice_ratio": unpaid_invoice_ratio,
        "partial_payment_ratio": partial_payment_ratio,
        "payment_completion_rate": payment_completion_rate,
        "overdue_invoices": overdue_invoices,
    }
   