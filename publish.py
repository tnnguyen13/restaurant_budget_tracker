import zmq
import json
import time
import random

context = zmq.Context()
socket = context.socket(zmq.PUB)
socket.bind("tcp://*:5555")

time.sleep(1)  # Wait for subscribers

different_restaurants = {
    1: "ABC Sushi",
    2: "American's Burger",
    3: "Nick the Greek",
    4: "Burger King",
    5: "Shawn's Hot Dogs"
}

random_restaurant = random.randint(1,5)

event = {
    "user_id": 1,
    "restaurant_id": str(random_restaurant),
    "restaurant_name": different_restaurants[random_restaurant],
    "amount": random.randint(1,200)
}

socket.send_string("expense_created " + json.dumps(event))
print("Sent expense_created event")