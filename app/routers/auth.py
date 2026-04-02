from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.user import UserCreate, UserResponse, TokenResponse, LoginRequest
from app.services.auth_service import register_user, login_user

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/register", response_model=UserResponse, status_code=201)
def register(payload: UserCreate, db: Session = Depends(get_db)):
    """
    Register a new user.
    - Default role is VIEWER if not specified.
    - Email must be unique.
    - Password must be at least 6 characters.
    """
    return register_user(payload, db)


@router.post("/login", response_model=TokenResponse)
def login(payload: LoginRequest, db: Session = Depends(get_db)):
    """
    Login and receive a JWT bearer token.
    Use this token in the Authorization header: `Bearer <token>`
    """
    return login_user(payload, db)


@router.post("/login/form", response_model=TokenResponse, include_in_schema=False)
def login_form(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    """OAuth2 compatible form login (used by Swagger UI Authorize button)."""
    payload = LoginRequest(email=form_data.username, password=form_data.password)
    return login_user(payload, db)
