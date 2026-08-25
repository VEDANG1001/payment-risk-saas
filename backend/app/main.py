from fastapi import FastAPI

from backend.app.api.main import api_router


app = FastAPI(
    title="Payment Risk SaaS API",
    version="1.0.0"
)


@app.get("/")
def root():
    return {
        "message": "Payment Risk SaaS API is running"
    }


app.include_router(
    api_router,
    prefix="/api/v1"
)