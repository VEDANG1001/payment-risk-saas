# Import String for text columns
# Import ForeignKey to connect Customer with Tenant
from sqlalchemy import String, ForeignKey

# Import tools for defining database fields
from sqlalchemy.orm import Mapped, mapped_column

# Import our common SQLAlchemy Base
from backend.app.db.base import Base


# Create the Customer database model
class Customer(Base):

    # Tell SQLAlchemy the database table name
    __tablename__ = "customers"

    # Unique ID for each customer
    id: Mapped[int] = mapped_column(
        primary_key=True,      # Makes id the primary key
        autoincrement=True     # Database automatically creates the ID
    )

    # ID of the firm that owns this customer
    tenant_id: Mapped[int] = mapped_column(
        ForeignKey("tenants.id"),  # Connects to tenants.id
        nullable=False              # Every customer must belong to a tenant
    )

    # Customer's name
    name: Mapped[str] = mapped_column(
        String(255),           # Maximum 255 characters
        nullable=False         # Name is required
    )

    # Customer's email
    email: Mapped[str] = mapped_column(
        String(255),           # Maximum 255 characters
        nullable=True          # Email can be optional
    )