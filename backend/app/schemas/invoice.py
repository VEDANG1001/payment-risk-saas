# Import BaseModel for creating Pydantic schemas.
from pydantic import BaseModel

# Import date type for invoice and due dates.
from datetime import date


# Schema used when creating a new invoice.
class InvoiceCreate(BaseModel):

    # ID of the customer this invoice belongs to.
    customer_id: int

    # Total invoice amount.
    amount: float

    # Date when the invoice was created.
    invoice_date: date

    # Date by which the customer should pay.
    due_date: date


# Schema used when updating an existing invoice.
class InvoiceUpdate(BaseModel):

    # All fields are optional because we may update only one field.
    customer_id: int | None = None

    # Updated invoice amount.
    amount: float | None = None

    # Updated invoice date.
    invoice_date: date | None = None

    # Updated payment due date.
    due_date: date | None = None


# Schema used when sending invoice data back through the API.
class InvoiceResponse(BaseModel):

    # Unique invoice ID from the database.
    id: int

    # ID of the customer who owns this invoice.
    customer_id: int

    # Invoice amount.
    amount: float

    # Invoice creation date.
    invoice_date: date

    # Invoice payment due date.
    due_date: date

    class Config:
        from_attributes = True