# Import String for text columns
# Import ForeignKey to connect User with Tenant
from sqlalchemy import String, ForeignKey

# Import tools for defining database columns
from sqlalchemy.orm import Mapped, mapped_column

# Import our common database Base
from backend.app.db.base import Base


# Create the User database model
class User(Base):

    # Tell SQLAlchemy the table name
    __tablename__ = "users"

    # Unique ID for every user
    id: Mapped[int] = mapped_column(
        primary_key=True,      # Makes id the primary key
        autoincrement=True    # Database automatically creates the ID
    )

    # ID of the company/tenant this user belongs to
    tenant_id: Mapped[int] = mapped_column(
        ForeignKey("tenants.id"),  # Connects to tenants.id
        nullable=False              # User must belong to a tenant
    )

    # User's name
    name: Mapped[str] = mapped_column(
        String(255),           # Maximum 255 characters
        nullable=False         # Name is required
    )

    # User's email
    email: Mapped[str] = mapped_column(
        String(255),           # Maximum 255 characters
        nullable=False,         # Email is required
        unique=True             # Email must be unique
    )