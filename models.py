from sqlalchemy import Column, Integer, String, DateTime, Numeric
from datetime import datetime, timezone
from database import Base

class Expense(Base):
    __tablename__ = "expenses"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, index=True, nullable=False)
    restaurant_id = Column(String, index=True, nullable=False)
    restaurant_name = Column(String, nullable=False)
    amount = Column(Numeric(10, 2), nullable=False)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), index=True)