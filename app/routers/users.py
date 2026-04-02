from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.middleware.auth import get_active_user, require_roles
from app.models.user import User, RoleEnum
from app.schemas.user import UserResponse, UserUpdate
from app.services import user_service

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/me", response_model=UserResponse)
def get_my_profile(current_user: User = Depends(get_active_user)):
    """Get your own profile. Available to all authenticated users."""
    return current_user


@router.get(
    "/",
    response_model=List[UserResponse],
    dependencies=[Depends(require_roles(RoleEnum.ADMIN))],
)
def list_users(db: Session = Depends(get_db)):
    """List all users. Admin only."""
    return user_service.get_all_users(db)


@router.get(
    "/{user_id}",
    response_model=UserResponse,
    dependencies=[Depends(require_roles(RoleEnum.ADMIN))],
)
def get_user(user_id: int, db: Session = Depends(get_db)):
    """Get a specific user by ID. Admin only."""
    return user_service.get_user_by_id(user_id, db)


@router.patch(
    "/{user_id}",
    response_model=UserResponse,
    dependencies=[Depends(require_roles(RoleEnum.ADMIN))],
)
def update_user(user_id: int, payload: UserUpdate, db: Session = Depends(get_db)):
    """
    Update a user's name, role, or active status. Admin only.
    - Use `is_active: false` to deactivate a user.
    - Use `role` to promote/demote a user.
    """
    return user_service.update_user(user_id, payload, db)


@router.delete(
    "/{user_id}",
    dependencies=[Depends(require_roles(RoleEnum.ADMIN))],
)
def delete_user(
    user_id: int,
    current_user: User = Depends(require_roles(RoleEnum.ADMIN)),
    db: Session = Depends(get_db),
):
    """Permanently delete a user. Admin only. Cannot delete your own account."""
    return user_service.delete_user(user_id, current_user.id, db)
