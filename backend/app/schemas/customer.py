# Import BaseModel from Pydantic.
# We use BaseModel to create API request and response schemas.
from pydantic import BaseModel, EmailStr


# Schema used when creating a new customer.
class CustomerCreate(BaseModel):
    # Tenant ID is required to associate the customer with a specific tenant.
    tenant_id: int     

    # Customer name is required.
    name: str

    # Customer email is required.
    # EmailStr automatically validates the email format.
    email: EmailStr


# Schema used when updating an existing customer.
class CustomerUpdate(BaseModel):

    # Name is optional because we may only want to update the email.
    name: str | None = None

    # Email is optional because we may only want to update the name.
    email: EmailStr | None = None


# Schema used when sending customer data back through the API.
class CustomerResponse(BaseModel):

    # Unique customer ID from the database.
    id: int

    # Customer name.
    name: str

    # Customer email.
    email: EmailStr