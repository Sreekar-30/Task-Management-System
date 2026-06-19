# Scalable Expense Tracking API Platform

Production-ready FastAPI backend for expense tracking with JWT auth, role-based access control, MySQL, SQLAlchemy, analytics, budgets, Docker, and tests.

## Features

- User registration and login with bcrypt password hashing
- JWT access tokens and protected routes
- Admin/User role-based authorization
- Expense CRUD with filtering, search, pagination, and sorting
- Category CRUD with duplicate prevention
- Payment method support
- Budget tracking with alerts, remaining budget, and utilization
- Dashboard analytics: totals, monthly summaries, category spending, top categories, trends, weekly and yearly reports
- Centralized exception handling and structured logging
- Async FastAPI endpoints with SQLAlchemy session dependency
- MySQL connection pooling
- Docker and Docker Compose
- Pytest unit and integration test setup

## Project Structure

```text
app/
  api/routes/          REST endpoints
  core/                settings, security, logging, exceptions
  db/                  database session and base model
  models/              SQLAlchemy ORM models
  repositories/        database access layer
  schemas/             Pydantic request/response schemas
  services/            business logic
  main.py              FastAPI application factory
tests/                 pytest tests
docker-compose.yml     local MySQL + API stack
Dockerfile             API image
mysql_schema.sql       MySQL schema reference
```

## Quick Start

1. Copy environment defaults:

```bash
cp .env.example .env
```

2. Start with Docker:

```bash
docker compose up --build
```

3. Open Swagger UI:

[http://localhost:8000/docs](http://localhost:8000/docs)

## Local Development

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

On Windows PowerShell:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn app.main:app --reload
```

## Environment Variables

See `.env.example`.

Important production settings:

- Set a strong `SECRET_KEY`.
- Restrict `BACKEND_CORS_ORIGINS`.
- Use managed MySQL credentials through secrets.
- Disable auto-create tables and use migrations in larger production deployments.

## Authentication Flow

Register:

```bash
curl -X POST http://localhost:8000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email":"user@example.com","full_name":"Demo User","password":"StrongPass123!"}'
```

Login:

```bash
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=user@example.com&password=StrongPass123!"
```

Sample response:

```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIs...",
  "token_type": "bearer"
}
```

Use protected APIs:

```bash
curl http://localhost:8000/api/v1/expenses \
  -H "Authorization: Bearer <ACCESS_TOKEN>"
```

## Sample Requests

Create category:

```bash
curl -X POST http://localhost:8000/api/v1/categories \
  -H "Authorization: Bearer <ACCESS_TOKEN>" \
  -H "Content-Type: application/json" \
  -d '{"name":"Groceries","description":"Food and household supplies"}'
```

Create expense:

```bash
curl -X POST http://localhost:8000/api/v1/expenses \
  -H "Authorization: Bearer <ACCESS_TOKEN>" \
  -H "Content-Type: application/json" \
  -d '{
    "title":"Weekly groceries",
    "amount":82.45,
    "expense_date":"2026-06-19",
    "category_id":1,
    "payment_method_id":1,
    "description":"Vegetables, milk, pantry refill"
  }'
```

Filter expenses:

```bash
curl "http://localhost:8000/api/v1/expenses?category_id=1&min_amount=20&sort_by=amount&sort_order=desc&page=1&page_size=20" \
  -H "Authorization: Bearer <ACCESS_TOKEN>"
```

Budget status:

```bash
curl "http://localhost:8000/api/v1/budgets/status/2026/6" \
  -H "Authorization: Bearer <ACCESS_TOKEN>"
```

Analytics:

```bash
curl http://localhost:8000/api/v1/dashboard/category-wise \
  -H "Authorization: Bearer <ACCESS_TOKEN>"
```

## Tests

```bash
pytest
```

Tests use SQLite by default through `TEST_DATABASE_URL`, while the production app is configured for MySQL.

## Notes For Interviews

This codebase demonstrates separation of concerns through routes, services, repositories, schemas, and models. SQLAlchemy models include indexes, constraints, foreign keys, and relationships. Business rules live in service classes, while route functions remain thin and focused on HTTP concerns.
