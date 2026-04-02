import enum
import datetime
from sqlalchemy import (
    Column, Integer, String, Float, Enum, Date,
    DateTime, ForeignKey, Text
)
from sqlalchemy.orm import relationship
from app.database import Base


class TypeEnum(str, enum.Enum):
    INCOME = "income"
    EXPENSE = "expense"


class FinancialRecord(Base):
    __tablename__ = "financial_records"

    id = Column(Integer, primary_key=True, index=True)
    amount = Column(Float, nullable=False)
    type = Column(Enum(TypeEnum), nullable=False)
    category = Column(String(100), nullable=False, index=True)
    date = Column(Date, nullable=False, index=True)
    notes = Column(Text, nullable=True)
    created_by = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(
        DateTime,
        default=datetime.datetime.utcnow,
        onupdate=datetime.datetime.utcnow,
    )
    # Soft delete: NULL means active, timestamp means deleted
    deleted_at = Column(DateTime, nullable=True, default=None)

    creator = relationship("User", back_populates="records")
