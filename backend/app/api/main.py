from fastapi import APIRouter

from backend.app.api.routes.risk import router as risk_router
from backend.app.api.routes.behavior import router as behavior_router
from backend.app.api.routes.customer import router as customer_router
from backend.app.api.routes.invoice import router as invoice_router
from backend.app.api.routes.payment import router as payment_router


api_router = APIRouter()

api_router.include_router(
    risk_router,
    prefix="/risk",
    tags=["Risk Scoring"]
)

api_router.include_router(
    behavior_router,
    prefix="/behavior",
    tags=["Customer Behavior"]
)

api_router.include_router(
    customer_router,
    prefix="/customers",
    tags=["Customers"]
)

api_router.include_router(
    invoice_router,
    prefix="/invoices",
    tags=["Invoices"]
)
api_router.include_router(
    payment_router,
    prefix="/payments",
    tags=["Payments"]
)