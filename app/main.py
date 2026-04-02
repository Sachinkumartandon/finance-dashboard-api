from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

from app.database import Base, engine
from app.routers import auth, users, records, dashboard

# Auto-create all tables on startup (use Alembic for production migrations)
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Finance Dashboard API",
    description="""
## Finance Dashboard Backend

A role-based financial records management system.

### Roles
| Role | Permissions |
|------|------------|
| **VIEWER** | View records, view dashboard summary |
| **ANALYST** | All VIEWER permissions + create records + view trends |
| **ADMIN** | Full access — manage users and all records |

### Quick Start
1. Register a user via `POST /auth/register`
2. Login via `POST /auth/login` to get your token
3. Click **Authorize** above and paste your token
4. Start making requests!
    """,
    version="1.0.0",
    contact={"name": "Finance Dashboard"},
    license_info={"name": "MIT"},
)

# ── CORS ──────────────────────────────────────────────────────────────────────
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # Restrict to your frontend domain in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Routers ───────────────────────────────────────────────────────────────────
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(records.router)
app.include_router(dashboard.router)


# ── Global error handlers ─────────────────────────────────────────────────────
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={"detail": "An unexpected error occurred. Please try again later."},
    )


# ── Health check ──────────────────────────────────────────────────────────────
@app.get("/", tags=["Health"])
def root():
    return {"status": "ok", "message": "Finance Dashboard API is running"}


@app.get("/health", tags=["Health"])
def health():
    return {"status": "healthy"}
