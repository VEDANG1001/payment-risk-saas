# Import date for the payment date
# Import ForeignKey to connect Payment with Invoice
from datetime import date

from sqlalchemy import Date, ForeignKey, Numeric
from sqlalchemy.orm import Mapped, mapped_column

# Import our common SQLAlchemy Base
from backend.app.db.base import Base


# Create the Payment database model
class Payment(Base):

    # Tell SQLAlchemy the database table name
    __tablename__ = "payments"

    # Unique ID for every payment
    id: Mapped[int] = mapped_column(
        primary_key=True,      # Primary key
        autoincrement=True     # Database generates the ID
    )

    # ID of the invoice this payment belongs to
    invoice_id: Mapped[int] = mapped_column(
        ForeignKey("invoices.id"),  # Connects to invoices.id
        nullable=False               # Every payment needs an invoice
    )

    # Date when the payment was made
    payment_date: Mapped[date] = mapped_column(
        Date,
        nullable=False
    )

    # Amount paid
    amount: Mapped[float] = mapped_column(
        Numeric(12, 2),        # Money with 2 decimal places
        nullable=False
    )