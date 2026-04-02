from datetime import date, datetime
from typing import Optional, List
from pydantic import BaseModel, field_validator
from app.models.financial_record import TypeEnum


# ── Request schemas ──────────────────────────────────────────────────────────

class RecordCreate(BaseModel):
    amount: float
    type: TypeEnum
    category: str
    date: date
    notes: Optional[str] = None

    @field_validator("amount")
    @classmethod
    def amount_must_be_positive(cls, v: float) -> float:
        if v <= 0:
            raise ValueError("Amount must be greater than 0")
        return v

    @field_validator("category")
    @classmethod
    def category_not_empty(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("Category cannot be empty")
        return v.strip()


class RecordUpdate(BaseModel):
    amount: Optional[float] = None
    type: Optional[TypeEnum] = None
    category: Optional[str] = None
    date: Optional[date] = None
    notes: Optional[str] = None

    @field_validator("amount")
    @classmethod
    def amount_must_be_positive(cls, v: Optional[float]) -> Optional[float]:
        if v is not None and v <= 0:
            raise ValueError("Amount must be greater than 0")
        return v


# ── Response schemas ─────────────────────────────────────────────────────────

class RecordResponse(BaseModel):
    id: int
    amount: float
    type: TypeEnum
    category: str
    date: date
    notes: Optional[str]
    created_by: int
    created_at: datetime

    model_config = {"from_attributes": True}


class PaginatedRecords(BaseModel):
    total: int
    page: int
    limit: int
    results: List[RecordResponse]
