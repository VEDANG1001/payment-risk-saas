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