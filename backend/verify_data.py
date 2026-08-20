# Import SQLAlchemy query tools
from sqlalchemy import text

# Import our database session
from backend.app.db.session import SessionLocal


# Create a database session
db = SessionLocal()

try:

    # Query the complete payment chain
    result = db.execute(text("""
        SELECT
            t.name AS tenant_name,
            u.name AS user_name,
            c.name AS customer_name,
            i.amount AS invoice_amount,
            i.due_date,
            p.amount AS payment_amount,
            p.payment_date
        FROM tenants t
        JOIN users u
            ON u.tenant_id = t.id
        JOIN customers c
            ON c.tenant_id = t.id
        JOIN invoices i
            ON i.customer_id = c.id
        JOIN payments p
            ON p.invoice_id = i.id
        ORDER BY t.id
    """))

    # Get all returned rows
    rows = result.fetchall()

    # Display the results
    print("\n🔥 COMPLETE V1 DATA FLOW\n")

    for row in rows:
        print("Tenant:", row.tenant_name)
        print("User:", row.user_name)
        print("Customer:", row.customer_name)
        print("Invoice Amount:", row.invoice_amount)
        print("Due Date:", row.due_date)
        print("Payment Amount:", row.payment_amount)
        print("Payment Date:", row.payment_date)
        print("-" * 40)


except Exception as e:

    # Show any database error
    print("❌ Verification failed!")
    print(e)


finally:

    # Close the database session
    db.close()