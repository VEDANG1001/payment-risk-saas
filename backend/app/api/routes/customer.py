from fastapi import APIRouter, HTTPException
from sqlalchemy.exc import IntegrityError

from backend.app.db.session import SessionLocal
from backend.app.models.customer import Customer

# Import Pydantic schemas for request validation and response formatting.
from backend.app.schemas.customer import (
    CustomerCreate,
    CustomerUpdate,
    CustomerResponse,
)

router = APIRouter()

# Get all customers.
# The response_model validates the returned customer list.
@router.get("/", response_model=list[CustomerResponse])
def get_all_customers():

    db = SessionLocal()

    try:
        customers = db.query(Customer).all()

        return customers

    finally:
        db.close()

# Get one customer by customer ID.
# The response_model validates and formats the response.
@router.get("/{customer_id}", response_model=CustomerResponse)
def get_customer(customer_id: int):

    db = SessionLocal()

    try:
        customer = (
            db.query(Customer)
            .filter(Customer.id == customer_id)
            .first()
        )

        if not customer:
            raise HTTPException(
                status_code=404,
                detail="Customer not found"
            )

        return customer

    finally:
        db.close()

# Create a new customer.
@router.post("/", response_model=CustomerResponse, status_code=201)
def create_customer(customer_data: CustomerCreate):

    # Create a database session.
    db = SessionLocal()

    try:
        # Create a new customer object.
        new_customer = Customer(
            tenant_id=customer_data.tenant_id,
            name=customer_data.name,
            email=customer_data.email,
        )

        # Add the customer to the database session.
        db.add(new_customer)

        # Save the customer in the database.
        db.commit()

        # Refresh the object to get generated values like ID.
        db.refresh(new_customer)

        # Return the newly created customer.
        return new_customer

    finally:
        # Always close the database session.
        db.close()

# Update an existing customer using its ID.
@router.put("/{customer_id}", response_model=CustomerResponse)
def update_customer(
    customer_id: int,
    customer_data: CustomerUpdate
):

    # Create a database session.
    db = SessionLocal()

    try:
        # Find the customer.
        customer = (
            db.query(Customer)
            .filter(Customer.id == customer_id)
            .first()
        )

        # Return an error if the customer does not exist.
        if not customer:
            raise HTTPException(
                status_code=404,
                detail="Customer not found"
            )

        # Update name only if a new value was provided.
        if customer_data.name is not None:
            customer.name = customer_data.name

        # Update email only if a new value was provided.
        if customer_data.email is not None:
            customer.email = customer_data.email

        # Save the changes.
        db.commit()

        # Refresh the customer with the latest database values.
        db.refresh(customer)

        # Return the updated customer.
        return customer

    finally:
        # Always close the database session.
        db.close()

# Delete a customer using its ID.
@router.delete("/{customer_id}")
def delete_customer(customer_id: int):

    # Create a database session.
    db = SessionLocal()

    try:
        # Find the customer using its ID.
        customer = (
            db.query(Customer)
            .filter(Customer.id == customer_id)
            .first()
        )

        # Return an error if the customer does not exist.
        if not customer:
            raise HTTPException(
                status_code=404,
                detail="Customer not found"
            )

        # Delete the customer.
        db.delete(customer)

        # Save the deletion.
        db.commit()

        # Return a success message.
        return {
            "message": "Customer deleted successfully"
        }

    except IntegrityError:
        # Cancel the failed database transaction.
        db.rollback()

        # Prevent deletion when invoices are connected
        # to this customer.
        raise HTTPException(
            status_code=400,
            detail="Cannot delete customer because invoices are associated with it"
        )

    finally:
        # Always close the database session.
        db.close()