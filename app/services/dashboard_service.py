import calendar
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.models.financial_record import FinancialRecord, TypeEnum


def _active_records(db: Session):
    """Base query returning only non-deleted records."""
    return db.query(FinancialRecord).filter(FinancialRecord.deleted_at.is_(None))


def get_summary(db: Session) -> dict:
    base = _active_records(db)

    total_income = (
        base.filter(FinancialRecord.type == TypeEnum.INCOME)
        .with_entities(func.coalesce(func.sum(FinancialRecord.amount), 0.0))
        .scalar()
    )
    total_expenses = (
        base.filter(FinancialRecord.type == TypeEnum.EXPENSE)
        .with_entities(func.coalesce(func.sum(FinancialRecord.amount), 0.0))
        .scalar()
    )
    total_records = base.count()

    return {
        "total_income": round(float(total_income), 2),
        "total_expenses": round(float(total_expenses), 2),
        "net_balance": round(float(total_income) - float(total_expenses), 2),
        "total_records": total_records,
    }


def get_by_category(db: Session) -> dict:
    base = _active_records(db)

    def category_totals(record_type: TypeEnum):
        rows = (
            base.filter(FinancialRecord.type == record_type)
            .with_entities(
                FinancialRecord.category,
                func.sum(FinancialRecord.amount).label("total"),
                func.count(FinancialRecord.id).label("count"),
            )
            .group_by(FinancialRecord.category)
            .order_by(func.sum(FinancialRecord.amount).desc())
            .all()
        )
        return [
            {"category": row.category, "total": round(float(row.total), 2), "count": row.count}
            for row in rows
        ]

    return {
        "income": category_totals(TypeEnum.INCOME),
        "expenses": category_totals(TypeEnum.EXPENSE),
    }


def get_monthly_trends(db: Session, months: int = 6) -> list:
    """
    Returns income vs expense totals grouped by month,
    for the last N months (default: 6).
    """
    from sqlalchemy import extract
    import datetime

    base = _active_records(db)

    rows = (
        base.with_entities(
            extract("year", FinancialRecord.date).label("year"),
            extract("month", FinancialRecord.date).label("month"),
            FinancialRecord.type,
            func.sum(FinancialRecord.amount).label("total"),
        )
        .group_by("year", "month", FinancialRecord.type)
        .order_by("year", "month")
        .all()
    )

    # Build a dict: {(year, month): {income: x, expense: y}}
    trend_map: dict = {}
    for row in rows:
        key = (int(row.year), int(row.month))
        if key not in trend_map:
            trend_map[key] = {"income": 0.0, "expense": 0.0}
        if row.type == TypeEnum.INCOME:
            trend_map[key]["income"] = round(float(row.total), 2)
        else:
            trend_map[key]["expense"] = round(float(row.total), 2)

    result = []
    for (year, month), values in sorted(trend_map.items()):
        result.append({
            "year": year,
            "month": month,
            "month_name": calendar.month_name[month],
            "total_income": values["income"],
            "total_expenses": values["expense"],
            "net": round(values["income"] - values["expense"], 2),
        })

    # Return only the last N months
    return result[-months:]


def get_recent_activity(db: Session, limit: int = 10) -> dict:
    records = (
        _active_records(db)
        .order_by(FinancialRecord.created_at.desc())
        .limit(limit)
        .all()
    )
    return {
        "records": [
            {
                "id": r.id,
                "amount": r.amount,
                "type": r.type.value,
                "category": r.category,
                "date": str(r.date),
                "notes": r.notes,
            }
            for r in records
        ]
    }
