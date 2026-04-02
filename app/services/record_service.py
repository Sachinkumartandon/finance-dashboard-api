import datetime
from typing import Optional
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import and_

from app.models.financial_record import FinancialRecord, TypeEnum
from app.schemas.financial_record import RecordCreate, RecordUpdate


def create_record(payload: RecordCreate, user_id: int, db: Session) -> FinancialRecord:
    record = FinancialRecord(
        amount=payload.amount,
        type=payload.type,
        category=payload.category,
        date=payload.date,
        notes=payload.notes,
        created_by=user_id,
    )
    db.add(record)
    db.commit()
    db.refresh(record)
    return record


def get_records(
    db: Session,
    record_type: Optional[TypeEnum] = None,
    category: Optional[str] = None,
    date_from: Optional[datetime.date] = None,
    date_to: Optional[datetime.date] = None,
    page: int = 1,
    limit: int = 10,
) -> dict:
    query = db.query(FinancialRecord).filter(FinancialRecord.deleted_at.is_(None))

    # Apply filters
    if record_type:
        query = query.filter(FinancialRecord.type == record_type)
    if category:
        query = query.filter(FinancialRecord.category.ilike(f"%{category}%"))
    if date_from:
        query = query.filter(FinancialRecord.date >= date_from)
    if date_to:
        query = query.filter(FinancialRecord.date <= date_to)

    total = query.count()
    records = (
        query.order_by(FinancialRecord.date.desc())
        .offset((page - 1) * limit)
        .limit(limit)
        .all()
    )

    return {
        "total": total,
        "page": page,
        "limit": limit,
        "results": records,
    }


def get_record_by_id(record_id: int, db: Session) -> FinancialRecord:
    record = (
        db.query(FinancialRecord)
        .filter(
            FinancialRecord.id == record_id,
            FinancialRecord.deleted_at.is_(None),
        )
        .first()
    )
    if not record:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Record with id {record_id} not found",
        )
    return record


def update_record(
    record_id: int, payload: RecordUpdate, db: Session
) -> FinancialRecord:
    record = get_record_by_id(record_id, db)

    if payload.amount is not None:
        record.amount = payload.amount
    if payload.type is not None:
        record.type = payload.type
    if payload.category is not None:
        record.category = payload.category.strip()
    if payload.date is not None:
        record.date = payload.date
    if payload.notes is not None:
        record.notes = payload.notes

    db.commit()
    db.refresh(record)
    return record


def soft_delete_record(record_id: int, db: Session) -> dict:
    record = get_record_by_id(record_id, db)
    record.deleted_at = datetime.datetime.utcnow()
    db.commit()
    return {"detail": f"Record {record_id} deleted successfully"}
