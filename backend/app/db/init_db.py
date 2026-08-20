# Import the database engine
from backend.app.db.session import engine

# Import Base so SQLAlchemy knows about our models
from backend.app.db.base import Base

# Import Tenant so SQLAlchemy registers the tenants table
from backend.app.models.tenant import Tenant
from backend.app.models.user import User
from backend.app.models.customer import Customer
from backend.app.models.invoice import Invoice
from backend.app.models.payment import Payment



# Create all tables defined in Base metadata
Base.metadata.create_all(bind=engine)

print("Database tables created successfully!")