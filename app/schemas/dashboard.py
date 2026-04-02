from typing import List
from pydantic import BaseModel


class SummaryResponse(BaseModel):
    total_income: float
    total_expenses: float
    net_balance: float
    total_records: int


class CategoryTotal(BaseModel):
    category: str
    total: float
    count: int


class CategoryBreakdown(BaseModel):
    income: List[CategoryTotal]
    expenses: List[CategoryTotal]


class MonthlyTrend(BaseModel):
    year: int
    month: int
    month_name: str
    total_income: float
    total_expenses: float
    net: float


class RecentRecord(BaseModel):
    id: int
    amount: float
    type: str
    category: str
    date: str
    notes: str | None


class RecentActivity(BaseModel):
    records: List[RecentRecord]
