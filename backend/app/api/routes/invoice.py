from fastapi import APIRouter, HTTPException
from sqlalchemy.exc import IntegrityError


from backend.app.db.session import SessionLocal
from backend.app.models.invoice import Invoice
from backend.app.schemas.invoice import (
    InvoiceCreate,
    InvoiceUpdate,
    InvoiceResponse,
)

router = APIRouter()


@router.get("/", response_model=list[InvoiceResponse])
def get_all_invoices():

    db = SessionLocal()

    try:
        invoices = db.query(Invoice).all()

        return invoices

    finally:
        db.close()


@router.get("/{invoice_id}", response_model=InvoiceResponse)
def get_invoice(invoice_id: int):

    db = SessionLocal()

    try:
        invoice = (
            db.query(Invoice)
            .filter(Invoice.id == invoice_id)
            .first()
        )

        if not invoice:
            raise HTTPException(
                status_code=404,
                detail="Invoice not found"
            )

        return invoice

    finally:
        db.close()

# Create a new invoice.
# The request data is validated using InvoiceCreate.
@router.post("/", response_model=InvoiceResponse, status_code=201)
def create_invoice(invoice_data: InvoiceCreate):

    # Create a new database session.
    db = SessionLocal()

    try:
        # Create a new Invoice object using validated request data.
        new_invoice = Invoice(
            customer_id=invoice_data.customer_id,
            amount=invoice_data.amount,
            invoice_date=invoice_data.invoice_date,
            due_date=invoice_data.due_date,
        )

        # Add the new invoice to the database session.
        db.add(new_invoice)

        # Save the new invoice in the database.
        db.commit()

        # Refresh the object to get generated database values like ID.
        db.refresh(new_invoice)

        # Return the newly created invoice.
        return new_invoice

    finally:
        # Always close the database session.
        db.close()

# Update an existing invoice.
# The request data is validated using InvoiceUpdate.
@router.put("/{invoice_id}", response_model=InvoiceResponse)
def update_invoice(
    invoice_id: int,
    invoice_data: InvoiceUpdate
):

    # Create a new database session.
    db = SessionLocal()

    try:
        # Find the invoice by its ID.
        invoice = (
            db.query(Invoice)
            .filter(Invoice.id == invoice_id)
            .first()
        )

        # Return an error if the invoice does not exist.
        if not invoice:
            raise HTTPException(
                status_code=404,
                detail="Invoice not found"
            )

        # Get only the fields that were actually provided.
        update_data = invoice_data.model_dump(
            exclude_unset=True
        )

        # Update each provided field.
        for field, value in update_data.items():
            setattr(invoice, field, value)

        # Save the changes in the database.
        db.commit()

        # Refresh the invoice with the updated database data.
        db.refresh(invoice)

        # Return the updated invoice.
        return invoice

    finally:
        # Always close the database session.
        db.close()

@router.delete("/{invoice_id}")
def delete_invoice(invoice_id: int):

    db = SessionLocal()

    try:
        invoice = (
            db.query(Invoice)
            .filter(Invoice.id == invoice_id)
            .first()
        )

        if not invoice:
            raise HTTPException(
                status_code=404,
                detail="Invoice not found"
            )

        db.delete(invoice)
        db.commit()

        return {
            "message": "Invoice deleted successfully"
        }

    except IntegrityError:
        db.rollback()

        raise HTTPException(
            status_code=400,
            detail="Cannot delete invoice because payments are associated with it"
        )

    finally:
        db.close()