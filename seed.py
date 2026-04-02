import sys
import datetime
import random

sys.path.append(".")

from app.database import SessionLocal, engine, Base
from app.models.user import User, RoleEnum
from app.models.financial_record import FinancialRecord, TypeEnum
from app.core.security import hash_password

# ── Create all tables if they don't exist ─────────────────────────────────────
print("Creating tables...")
Base.metadata.create_all(bind=engine)

db = SessionLocal()

# ── Clear existing data ───────────────────────────────────────────────────────
print("Clearing existing data...")
db.query(FinancialRecord).delete()
db.query(User).delete()
db.commit()

# ── Create users ──────────────────────────────────────────────────────────────
print("Creating users...")
users = [
    User(name="Admin User",    email="admin@example.com",   password_hash=hash_password("admin123"),   role=RoleEnum.ADMIN),
    User(name="Alice Analyst", email="analyst@example.com", password_hash=hash_password("analyst123"), role=RoleEnum.ANALYST),
    User(name="Victor Viewer", email="viewer@example.com",  password_hash=hash_password("viewer123"),  role=RoleEnum.VIEWER),
]
db.add_all(users)
db.commit()
for u in users:
    db.refresh(u)

admin = users[0]

# ── Create financial records ──────────────────────────────────────────────────
print("Creating financial records...")
categories_income  = ["Salary", "Freelance", "Investment", "Bonus", "Rental Income"]
categories_expense = ["Rent", "Groceries", "Utilities", "Transport", "Entertainment", "Healthcare", "Insurance"]

records = []
today = datetime.date.today()

for i in range(60):
    day_offset = random.randint(0, 180)
    record_date = today - datetime.timedelta(days=day_offset)
    is_income = random.random() < 0.4

    records.append(FinancialRecord(
        amount=round(random.uniform(50, 5000), 2),
        type=TypeEnum.INCOME if is_income else TypeEnum.EXPENSE,
        category=random.choice(categories_income if is_income else categories_expense),
        date=record_date,
        notes=f"Auto-generated record #{i + 1}",
        created_by=admin.id,
    ))

db.add_all(records)
db.commit()

print("\n✅ Seed complete!")
print("─" * 40)
print("Test accounts:")
print("  admin@example.com   / admin123   (ADMIN)")
print("  analyst@example.com / analyst123 (ANALYST)")
print("  viewer@example.com  / viewer123  (VIEWER)")
print(f"\n  {len(records)} financial records created.")
db.close()