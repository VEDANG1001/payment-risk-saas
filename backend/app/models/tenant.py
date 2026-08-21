# Import String so we can define text columns
from sqlalchemy import String

# Import SQLAlchemy tools for typed model fields
from sqlalchemy.orm import Mapped, mapped_column

# Import our common Base class
from backend.app.db.base import Base


# Create the Tenant database model
class Tenant(Base):

    # Tell SQLAlchemy the database table name
    __tablename__ = "tenants"

    # Create the primary key column
    id: Mapped[int] = mapped_column(
        primary_key=True,      # Each tenant gets a unique ID
        autoincrement=True    # Database automatically generates the ID
    )

    # Create the company/firm name column
    name: Mapped[str] = mapped_column(
        String(255),          # Maximum 255 characters
        nullable=False        # Company name is required
    )