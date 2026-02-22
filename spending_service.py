import zmq
import json
from sqlalchemy import func
from database import SessionLocal, engine, Base
from models import Expense

Base.metadata.create_all(bind=engine)

# ZeroMQ
context = zmq.Context()

# listening
listen = context.socket(zmq.SUB)
listen.connect("tcp://localhost:5555")
listen.setsockopt_string(zmq.SUBSCRIBE, "expense_created")

# response
response = context.socket(zmq.REP)
response.bind("tcp://*:5556")

# adding expenses
def create_expense(data):
    db = SessionLocal()
    try:
        expense = Expense(
            user_id=data["user_id"],
            restaurant_id=data["restaurant_id"],
            restaurant_name=data["restaurant_name"],
            amount=data["amount"]
        )
        db.add(expense)
        db.commit()
        print(f"Stored expense: {data}")
    finally:
        db.close()

# summary
def summary(data):
    db = SessionLocal()
    try:
        total = db.query(func.sum(Expense.amount))\
                  .filter(Expense.user_id == data["user_id"])\
                  .scalar()
        return {"user_id": data["user_id"], "total_spent": float(total or 0)}
    finally:
        db.close()

# Poller to handle both sockets
poller = zmq.Poller()
poller.register(listen, zmq.POLLIN)
poller.register(response, zmq.POLLIN)

print("Spending service started...")

while True:
    socks = dict(poller.poll())

    # Handle expense events (SUB)
    if listen in socks:
        message = listen.recv_string()
        topic, payload = message.split(" ", 1)
        data = json.loads(payload)
        create_expense(data)

    # Handle summary requests (REP)
    if response in socks:
        message = response.recv_json()
        resp_data = summary(message)
        response.send_json(resp_data) 