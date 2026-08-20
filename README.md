# Payment Risk SaaS

A multi-tenant SaaS application that analyzes customer payment behavior and assigns risk scores.

## V1 Goal

CSV Upload
→ Customer Data
→ Payment Features
→ Risk Score
→ Risk Tier
→ Customer Dashboard

## Tech Stack

- Backend: Python + FastAPI
- Database: PostgreSQL
- ORM: SQLAlchemy
- Migrations: Alembic
- Frontend: Next.js + TypeScript + Tailwind CSS

## V1 Scope

The first version will:

1. Allow a company to create an account.
2. Keep each company's data isolated.
3. Accept customer invoice/payment data through CSV.
4. Calculate payment behavior features.
5. Calculate a customer risk score.
6. Assign a risk tier.
7. Show the risk score and reasons through an API and dashboard.





venv creation 
The name is:.venv

It is located here:
D:\payment-risk-saas\.venv

So:
payment-risk-saas/
└── .venv/        ← VIRTUAL ENVIRONMENT

How to activate it in PowerShell
From your current project folder:
D:\payment-risk-saas

run:
.\.venv\Scripts\Activate.ps1



fastapi          → Backend API framework
uvicorn          → Runs the FastAPI application
sqlalchemy       → Python ORM for PostgreSQL
alembic          → Database migrations
psycopg2-binary  → PostgreSQL driver
python-dotenv    → Reads .env configuration
pydantic         → Data validation
pandas           → CSV/data processing

Package           Version
----------------- -----------
alembic           1.19.1
annotated-doc     0.0.5
annotated-types   0.8.0
anyio             4.14.2
click             8.4.2
colorama          0.4.6
fastapi           0.141.1
greenlet          3.5.5
h11               0.16.0
idna              3.19
Mako              1.4.1
MarkupSafe        3.0.3
numpy             2.5.2
pandas            3.0.5
pip               26.1.2
psycopg2-binary   2.9.12
pydantic          2.13.4
pydantic_core     2.46.4
python-dateutil   2.9.0.post0
python-dotenv     1.2.3
six               1.17.0
SQLAlchemy        2.0.52
starlette         1.6.0
typing_extensions 4.16.0
typing-inspection 0.4.4
tzdata            2026.3
uvicorn           0.52.4