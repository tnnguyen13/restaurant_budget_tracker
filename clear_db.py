# program used to clear the database

from database import SessionLocal, Base, engine
from models import Expense

Base.metadata.create_all(bind=engine)  # Ensure tables exist

db = SessionLocal()
try:
    db.query(Expense).delete()
    db.commit()
finally:
    db.close()

print("Database cleared!")