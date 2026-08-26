from fastapi import APIRouter, HTTPException

from backend.app.db.session import SessionLocal
from backend.app.models.payment import Payment


from backend.app.schemas.payment import (
    PaymentCreate,
    PaymentUpdate,
    PaymentResponse,
)

router = APIRouter()


# Get all payments.
@router.get("/", response_model=list[PaymentResponse])
def get_all_payments():

    db = SessionLocal()

    try:
        payments = db.query(Payment).all()

        return payments

    finally:
        db.close()

# Get one payment by payment ID.
@router.get("/{payment_id}", response_model=PaymentResponse)
def get_payment(payment_id: int):

    db = SessionLocal()

    try:
        payment = (
            db.query(Payment)
            .filter(Payment.id == payment_id)
            .first()
        )

        if not payment:
            raise HTTPException(
                status_code=404,
                detail="Payment not found"
            )

        return payment

    finally:
        db.close()

# Create a new payment.
# The request data is validated using PaymentCreate.
@router.post("/", response_model=PaymentResponse, status_code=201)
def create_payment(payment_data: PaymentCreate):

    # Create a new database session.
    db = SessionLocal()

    try:
        # Create a new Payment object using validated request data.
        new_payment = Payment(
            invoice_id=payment_data.invoice_id,
            amount=payment_data.amount,
            payment_date=payment_data.payment_date,
        )

        # Add the new payment to the database session.
        db.add(new_payment)

        # Save the new payment in the database.
        db.commit()

        # Refresh the object to get generated database values like ID.
        db.refresh(new_payment)

        # Return the newly created payment.
        return new_payment

    finally:
        # Always close the database session.
        db.close()

# Update an existing payment using its ID.
@router.put("/{payment_id}", response_model=PaymentResponse)
def update_payment(
    payment_id: int,
    payment_data: PaymentUpdate
):

    # Create a database session.
    db = SessionLocal()

    try:
        # Find the payment using its ID.
        payment = (
            db.query(Payment)
            .filter(Payment.id == payment_id)
            .first()
        )

        # Return an error if the payment does not exist.
        if not payment:
            raise HTTPException(
                status_code=404,
                detail="Payment not found"
            )

        # Update invoice_id only if a new value was provided.
        if payment_data.invoice_id is not None:
            payment.invoice_id = payment_data.invoice_id

        # Update amount only if a new value was provided.
        if payment_data.amount is not None:
            payment.amount = payment_data.amount

        # Update payment_date only if a new value was provided.
        if payment_data.payment_date is not None:
            payment.payment_date = payment_data.payment_date

        # Save the updated values.
        db.commit()

        # Refresh the object with the latest database values.
        db.refresh(payment)

        # Return the updated payment.
        return payment

    finally:
        # Always close the database session.
        db.close()

# Delete a payment using its ID.
@router.delete("/{payment_id}")
def delete_payment(payment_id: int):

    # Create a database session.
    db = SessionLocal()

    try:
        # Find the payment using its ID.
        payment = (
            db.query(Payment)
            .filter(Payment.id == payment_id)
            .first()
        )

        # Return an error if the payment does not exist.
        if not payment:
            raise HTTPException(
                status_code=404,
                detail="Payment not found"
            )

        # Delete the payment from the database.
        db.delete(payment)

        # Save the deletion.
        db.commit()

        # Return a success message.
        return {
            "message": "Payment deleted successfully"
        }

    finally:
        # Always close the database session.
        db.close()