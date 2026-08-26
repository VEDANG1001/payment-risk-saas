# Import BaseModel for creating Pydantic schemas.
from pydantic import BaseModel

# Import date because payment_date contains a date value.
from datetime import date


# Schema used when creating a new payment.
class PaymentCreate(BaseModel):

    # ID of the invoice this payment belongs to.
    invoice_id: int

    # Amount paid by the customer.
    amount: float

    # Date when the payment was made.
    payment_date: date


# Schema used when updating an existing payment.
class PaymentUpdate(BaseModel):

    # Invoice ID is optional during an update.
    invoice_id: int | None = None

    # Payment amount is optional during an update.
    amount: float | None = None

    # Payment date is optional during an update.
    payment_date: date | None = None


# Schema used when sending payment data back through the API.
class PaymentResponse(BaseModel):

    # Unique payment ID from the database.
    id: int

    # ID of the related invoice.
    invoice_id: int

    # Payment amount.
    amount: float

    # Date when the payment was made.
    payment_date: date