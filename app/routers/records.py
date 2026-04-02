import datetime
from typing import Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.middleware.auth import get_active_user, require_roles
from app.models.user import User, RoleEnum
from app.models.financial_record import TypeEnum
from app.schemas.financial_record import (
    RecordCreate, RecordUpdate, RecordResponse, PaginatedRecords
)
from app.services import record_service

router = APIRouter(prefix="/records", tags=["Financial Records"])


@router.get("/", response_model=PaginatedRecords)
def list_records(
    type: Optional[TypeEnum] = Query(None, description="Filter by type: income or expense"),
    category: Optional[str] = Query(None, description="Filter by category (partial match)"),
    date_from: Optional[datetime.date] = Query(None, description="Filter records from this date (YYYY-MM-DD)"),
    date_to: Optional[datetime.date] = Query(None, description="Filter records up to this date (YYYY-MM-DD)"),
    page: int = Query(1, ge=1, description="Page number"),
    limit: int = Query(10, ge=1, le=100, description="Records per page (max 100)"),
    current_user: User = Depends(get_active_user),
    db: Session = Depends(get_db),
):
    """
    List financial records with optional filters and pagination.
    Available to all authenticated users (VIEWER, ANALYST, ADMIN).
    """
    return record_service.get_records(
        db=db,
        record_type=type,
        category=category,
        date_from=date_from,
        date_to=date_to,
        page=page,
        limit=limit,
    )


@router.get("/{record_id}", response_model=RecordResponse)
def get_record(
    record_id: int,
    current_user: User = Depends(get_active_user),
    db: Session = Depends(get_db),
):
    """Get a single financial record by ID. Available to all authenticated users."""
    return record_service.get_record_by_id(record_id, db)


@router.post(
    "/",
    response_model=RecordResponse,
    status_code=201,
)
def create_record(
    payload: RecordCreate,
    current_user: User = Depends(require_roles(RoleEnum.ADMIN, RoleEnum.ANALYST)),
    db: Session = Depends(get_db),
):
    """
    Create a new financial record.
    Allowed roles: ADMIN, ANALYST.
    """
    return record_service.create_record(payload, current_user.id, db)


@router.put(
    "/{record_id}",
    response_model=RecordResponse,
    dependencies=[Depends(require_roles(RoleEnum.ADMIN))],
)
def update_record(
    record_id: int,
    payload: RecordUpdate,
    db: Session = Depends(get_db),
):
    """
    Update an existing financial record. Admin only.
    All fields are optional — send only what you want to change.
    """
    return record_service.update_record(record_id, payload, db)


@router.delete(
    "/{record_id}",
    dependencies=[Depends(require_roles(RoleEnum.ADMIN))],
)
def delete_record(
    record_id: int,
    db: Session = Depends(get_db),
):
    """
    Soft-delete a financial record. Admin only.
    The record is not permanently removed — it is marked with a deleted_at timestamp.
    """
    return record_service.soft_delete_record(record_id, db)
