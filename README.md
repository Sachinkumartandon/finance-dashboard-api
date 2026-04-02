# Finance Dashboard API

A backend system for managing financial records with role-based access control, built with **FastAPI**, **PostgreSQL**, and **SQLAlchemy**.

---

## 🚀 Tech Stack

| Layer | Technology |
|---|---|
| Framework | FastAPI |
| Database | PostgreSQL |
| ORM | SQLAlchemy |
| Migrations | Alembic |
| Authentication | JWT (JSON Web Tokens) |
| Validation | Pydantic v2 |
| Password Hashing | bcrypt via passlib |
| Testing | Pytest + HTTPX |

---

## 📁 Project Structure

```
finance-dashboard/
├── app/
│   ├── main.py                    # App entry point
│   ├── database.py                # DB connection and session
│   ├── core/
│   │   ├── config.py              # Environment settings
│   │   └── security.py            # JWT and password utilities
│   ├── models/
│   │   ├── user.py                # User model + RoleEnum
│   │   └── financial_record.py    # FinancialRecord model
│   ├── schemas/
│   │   ├── user.py                # User request/response schemas
│   │   ├── financial_record.py    # Record request/response schemas
│   │   └── dashboard.py           # Dashboard response schemas
│   ├── routers/
│   │   ├── auth.py                # Auth endpoints
│   │   ├── users.py               # User management endpoints
│   │   ├── records.py             # Financial record endpoints
│   │   └── dashboard.py           # Dashboard/analytics endpoints
│   ├── services/
│   │   ├── auth_service.py        # Auth business logic
│   │   ├── user_service.py        # User business logic
│   │   ├── record_service.py      # Record business logic
│   │   └── dashboard_service.py   # Analytics business logic
│   └── middleware/
│       └── auth.py                # JWT guard + role checker
├── alembic/                       # Database migrations
├── tests/
│   ├── conftest.py                # Test fixtures
│   ├── test_auth.py               # Auth tests
│   ├── test_records.py            # Records tests
│   ├── test_dashboard.py          # Dashboard tests
│   └── test_users.py              # User management tests
├── seed.py                        # Sample data script
├── requirements.txt
├── .env.example
└── README.md
```

---

## ⚙️ Setup & Installation

### 1. Clone the repository

```bash
git clone https://github.com/Sachinkumartandon/finance-dashboard-api.git
cd finance-dashboard-api
```

### 2. Create virtual environment

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

```bash
cp .env.example .env
```

Edit `.env` with your values:

```env
DATABASE_URL=postgresql://postgres:yourpassword@localhost:5432/finance_db
SECRET_KEY=your-super-secret-key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
```

### 5. Create PostgreSQL database

```bash
psql -U postgres
CREATE DATABASE finance_db;
\q
```

### 6. Run migrations

```bash
alembic upgrade head
```

### 7. Seed sample data

```bash
python seed.py
```

### 8. Start the server

```bash
uvicorn app.main:app --reload
```

---

## 📖 API Documentation

Once the server is running, visit:

- **Swagger UI:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc

---

## 🔐 Authentication

All protected endpoints require a JWT Bearer token in the Authorization header:

```
Authorization: Bearer <your_token>
```

Get a token by calling `POST /auth/login`.

---

## 👥 Roles & Permissions

| Action | VIEWER | ANALYST | ADMIN |
|---|---|---|---|
| View own profile | ✅ | ✅ | ✅ |
| View records | ✅ | ✅ | ✅ |
| View dashboard summary | ✅ | ✅ | ✅ |
| View recent activity | ✅ | ✅ | ✅ |
| View category breakdown | ✅ | ✅ | ✅ |
| Create records | ❌ | ✅ | ✅ |
| View monthly trends | ❌ | ✅ | ✅ |
| Update records | ❌ | ❌ | ✅ |
| Delete records (soft) | ❌ | ❌ | ✅ |
| Manage users | ❌ | ❌ | ✅ |

---

## 🧪 Test Accounts (after seeding)

| Email | Password | Role |
|---|---|---|
| admin@example.com | admin123 | ADMIN |
| analyst@example.com | analyst123 | ANALYST |
| viewer@example.com | viewer123 | VIEWER |

---

## 📡 API Endpoints

### Authentication
| Method | Endpoint | Description |
|---|---|---|
| POST | `/auth/register` | Register a new user |
| POST | `/auth/login` | Login and get JWT token |

### Users (Admin only)
| Method | Endpoint | Description |
|---|---|---|
| GET | `/users/me` | Get own profile |
| GET | `/users/` | List all users |
| GET | `/users/{id}` | Get user by ID |
| PATCH | `/users/{id}` | Update user role/status |
| DELETE | `/users/{id}` | Delete a user |

### Financial Records
| Method | Endpoint | Role | Description |
|---|---|---|---|
| GET | `/records/` | All | List records with filters |
| GET | `/records/{id}` | All | Get single record |
| POST | `/records/` | ADMIN, ANALYST | Create record |
| PUT | `/records/{id}` | ADMIN | Update record |
| DELETE | `/records/{id}` | ADMIN | Soft delete record |

**Available filters for GET /records/:**
- `type` — income or expense
- `category` — partial match
- `date_from` — start date (YYYY-MM-DD)
- `date_to` — end date (YYYY-MM-DD)
- `page` — page number (default: 1)
- `limit` — results per page (default: 10, max: 100)

### Dashboard
| Method | Endpoint | Role | Description |
|---|---|---|---|
| GET | `/dashboard/summary` | All | Total income, expenses, net balance |
| GET | `/dashboard/by-category` | All | Totals grouped by category |
| GET | `/dashboard/trends` | ANALYST, ADMIN | Monthly trends |
| GET | `/dashboard/recent` | All | Recent activity |

---

## 📊 Example Responses

### GET /dashboard/summary
```json
{
  "total_income": 50776.91,
  "total_expenses": 82024.98,
  "net_balance": -31248.07,
  "total_records": 60
}
```

### GET /dashboard/by-category
```json
{
  "income": [
    { "category": "Salary", "total": 25000.00, "count": 5 },
    { "category": "Freelance", "total": 8000.00, "count": 3 }
  ],
  "expenses": [
    { "category": "Rent", "total": 15000.00, "count": 5 },
    { "category": "Groceries", "total": 4200.00, "count": 12 }
  ]
}
```

### GET /dashboard/trends
```json
[
  {
    "year": 2024,
    "month": 6,
    "month_name": "June",
    "total_income": 5000.00,
    "total_expenses": 3200.00,
    "net": 1800.00
  }
]
```

---

## ✅ Running Tests

Tests use an in-memory SQLite database — no PostgreSQL needed.

```bash
pytest -v
```

**Results: 35 tests, all passing ✅**

---

## 🏗️ Design Decisions

### Soft Delete
Records are never permanently removed. A `deleted_at` timestamp is set instead, preserving historical data integrity.

### JWT Authentication
Stateless JWT tokens with configurable expiry. Clean and scalable with no session storage needed.

### Flat Role Model
Roles are implemented as a simple enum (VIEWER, ANALYST, ADMIN) for clarity and simplicity, which is appropriate for this use case.

### Separation of Concerns
Each layer has a clear responsibility — routers handle HTTP, services handle business logic, models handle data, and schemas handle validation.

### Pagination
All list endpoints support pagination (default 10 per page, max 100) to handle large datasets efficiently.

### Error Handling
All errors return consistent JSON responses with appropriate HTTP status codes (200, 201, 400, 401, 403, 404, 409, 422).
