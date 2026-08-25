
# Import SQLAlchemy tools
from sqlalchemy import text

from backend.app.db.session import SessionLocal

from backend.app.models.tenant import Tenant
from backend.app.models.user import User
from backend.app.models.customer import Customer
from backend.app.models.invoice import Invoice
from backend.app.models.payment import Payment

# Import date for invoice/payment dates
from datetime import date


# Create a database session
db = SessionLocal()

try:

    # -------------------------
    # 1. Create a Tenant
    # -------------------------

    tenant = Tenant(
        name="Demo Company"
    )

    db.add(tenant)
    db.flush()

    print("Tenant created:", tenant.id)


    # -------------------------
    # 2. Create a User
    # -------------------------

    user = User(
        tenant_id=tenant.id,
        name="Demo Admin",
        email="admin2@demo.com"
    )

    db.add(user)
    db.flush()

    print("User created:", user.id)


    # -------------------------
    # 3. Create a Customer
    # -------------------------

    customer = Customer(
        tenant_id=tenant.id,
        name="ABC Traders",
        email="customer@abc.com"
    )

    db.add(customer)
    db.flush()

    print("Customer created:", customer.id)


    # -------------------------
    # 4. Create an Invoice
    # -------------------------

    invoice = Invoice(
        customer_id=customer.id,
        invoice_date=date(2026, 8, 1),
        due_date=date(2026, 8, 30),
        amount=50000.00
    )

    db.add(invoice)
    db.flush()

    print("Invoice created:", invoice.id)


    # -------------------------
    # 5. Create a Payment
    # -------------------------

    payment = Payment(
        invoice_id=invoice.id,
        payment_date=date(2026, 9, 5),
        amount=50000.00
    )

    db.add(payment)


    # Save everything to PostgreSQL
    db.commit()

    print("\n🔥 COMPLETE V1 TEST DATA CREATED!")
    print("Tenant:", tenant.id)
    print("User:", user.id)
    print("Customer:", customer.id)
    print("Invoice:", invoice.id)
    print("Payment:", payment.id)


except Exception as e:

    # Cancel changes if anything goes wrong
    db.rollback()

    print("\n❌ TEST FAILED")
    print(e)


finally:

    # Always close the database connection
    db.close()