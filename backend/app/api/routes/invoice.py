from fastapi import APIRouter, HTTPException

from backend.app.db.session import SessionLocal
from backend.app.models.invoice import Invoice


router = APIRouter()


@router.get("/")
def get_all_invoices():

    db = SessionLocal()

    try:
        invoices = db.query(Invoice).all()

        return invoices

    finally:
        db.close()


@router.get("/{invoice_id}")
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
