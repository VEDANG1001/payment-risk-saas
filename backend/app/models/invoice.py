# Import date for invoice and due dates
# Import Numeric for storing money accurately
# Import ForeignKey to connect Invoice with Customer
from datetime import date

from sqlalchemy import Date, ForeignKey, Numeric
from sqlalchemy.orm import Mapped, mapped_column

# Import our common SQLAlchemy Base
from backend.app.db.base import Base


# Create the Invoice database model
class Invoice(Base):

    # Tell SQLAlchemy the database table name
    __tablename__ = "invoices"

    # Unique ID for every invoice
    id: Mapped[int] = mapped_column(
        primary_key=True,      # Primary key
        autoincrement=True    # Database generates the ID
    )

    # ID of the customer who owns this invoice
    customer_id: Mapped[int] = mapped_column(
        ForeignKey("customers.id"),  # Connects to customers.id
        nullable=False                # Every invoice needs a customer
    )

    # Date when the invoice was created
    invoice_date: Mapped[date] = mapped_column(
        Date,
        nullable=False
    )

    # Date when payment is expected
    due_date: Mapped[date] = mapped_column(
        Date,
        nullable=False
    )

    # Total amount of the invoice
    amount: Mapped[float] = mapped_column(
        Numeric(12, 2),       # Up to 12 digits, 2 decimal places
        nullable=False
    )