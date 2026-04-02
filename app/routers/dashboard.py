from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.middleware.auth import get_active_user, require_roles
from app.models.user import User, RoleEnum
from app.schemas.dashboard import (
    SummaryResponse, CategoryBreakdown, RecentActivity
)
from app.services import dashboard_service

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])


@router.get("/summary", response_model=SummaryResponse)
def summary(
    current_user: User = Depends(get_active_user),
    db: Session = Depends(get_db),
):
    """
    Get overall financial summary:
    total income, total expenses, net balance, and record count.
    Available to all authenticated users.
    """
    return dashboard_service.get_summary(db)


@router.get("/by-category", response_model=CategoryBreakdown)
def by_category(
    current_user: User = Depends(get_active_user),
    db: Session = Depends(get_db),
):
    """
    Get income and expense totals grouped by category.
    Available to all authenticated users.
    """
    return dashboard_service.get_by_category(db)


@router.get("/trends")
def trends(
    months: int = Query(6, ge=1, le=24, description="Number of past months to include"),
    current_user: User = Depends(require_roles(RoleEnum.ANALYST, RoleEnum.ADMIN)),
    db: Session = Depends(get_db),
):
    """
    Get monthly income vs expense trends.
    Allowed roles: ANALYST, ADMIN.
    Returns up to 24 months of data (default: last 6 months).
    """
    return dashboard_service.get_monthly_trends(db, months=months)


@router.get("/recent", response_model=RecentActivity)
def recent_activity(
    limit: int = Query(10, ge=1, le=50, description="Number of recent records to return"),
    current_user: User = Depends(get_active_user),
    db: Session = Depends(get_db),
):
    """
    Get the most recently added financial records.
    Available to all authenticated users.
    """
    return dashboard_service.get_recent_activity(db, limit=limit)
